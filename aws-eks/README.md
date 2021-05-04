Prerequisites

```bash
foo@bar$ docker pull bitnami/python
foo@bar$ brew tap weaveworks/tap
foo@bar$ brew install weaveworks/tap/eksctl
```

Build commands

```
foo@bar$ docker container stop reddit
foo@bar$ docker container rm reddit
foo@bar$ docker image rm reddit-graphql:1.0
foo@bar$ docker rmi $(docker images -a -q) # Remove all images
foo@bar$ docker build . --tag reddit-graphql:1.0
foo@bar$ docker exec -i -t -u root reddit /bin/bash # Dev
foo@bar$ docker run --publish 80:80 --name reddit -t -d reddit-graphql:1.0 # Prod
```

http://127.0.0.1/graphql

You can then run the following graphql query

```javascript
query{
  posts (subreddit:"maliciouscompliance"){
    id
    title
    url
    ups
    downs
    author
    selftext
  }
}
```

Configure the AWS cli

https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html

```bash
foo@bar$ aws configure # Default output format : text
```

Push to Docker Container Image to Amazon ECR

https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html

```bash
foo@bar$ export ACCOUNTID=$(aws sts get-caller-identity | cut -f 1)
foo@bar$ export REGION="eu-west-1"
foo@bar$ aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${ACCOUNTID}.dkr.ecr.${REGION}.amazonaws.com
foo@bar$ aws ecr create-repository --repository-name reddit-graphql --image-scanning-configuration scanOnPush=true --region ${REGION}
foo@bar$ docker tag reddit-graphql:1.0 ${ACCOUNTID}.dkr.ecr.${REGION}.amazonaws.com/reddit-graphql:1.0
foo@bar$ docker push ${ACCOUNTID}.dkr.ecr.${REGION}.amazonaws.com/reddit-graphql:1.0
```

The result should be visible on the Amazon ECR

https://eu-west-1.console.aws.amazon.com/ecr/repositories?region=eu-west-1

Create a Helm chart and package it up

```bash
foo@bar:~$ helm create demo
foo@bar:~$ vim ./demo/values.yaml
foo@bar:~$ helm package demo
```

Start Kubernetes locally

```bash
foo@bar:~$ minikube stop
foo@bar:~$ minikube delete --all
foo@bar:~$ rm -rf ~/.kube
foo@bar:~$ minikube start
```

Create AWS ECR Registry Credential in Kubernetes as a Secret (local deployment)

```bash
foo@bar:~$ kubectl delete secret --ignore-not-found eu-west-1-ecr-registry
foo@bar:~$ aws ecr get-authorization-token | cut -f2 | base64 -d | cut -d: -f2 | xargs kubectl create secret docker-registry eu-west-1-ecr-registry --docker-server=https://${ACCOUNTID}.dkr.ecr.${REGION}.amazonaws.com --docker-username=AWS --docker-email="doesnt@matter.com" --docker-password 
foo@bar:~$ kubectl get secret eu-west-1-ecr-registry --output=yaml
foo@bar:~$ docker login https://${ACCOUNTID}.dkr.ecr.${REGION}.amazonaws.com/v2/reddit-graphql/
```

Deploy chart

```bash
foo@bar:~$ helm install demo demo-0.1.0.tgz
foo@bar:~$ kubectl get pods
foo@bar:~$ kubectl describe pods
foo@bar:~$ kubectl get services reddit
foo@bar:~$ minikube tunnel --cleanup
```

You should now be able to access the service at

http://127.0.0.1/graphql

Uninstall helm deployment

```bash
foo@bar:~$ helm uninstall demo
```

=========================================

Create an AWS EKS cluster

https://eu-west-1.console.aws.amazon.com/eks

```
foo@bar:~$ eksctl create cluster --name hughs-cluster --region ${REGION} # note "--fargate" profile requires annotation
foo@bar:~$ kubectl config current-context
foo@bar:~$ kubectl get svc
foo@bar:~$ kubectl get pods
foo@bar:~$ kubectl get deploymeents
foo@bar:~$ kubectl get nodes
```

Open the IAM console

https://console.aws.amazon.com/iam

Open your user and add an inline policy to your user

```javascript
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "eks:ListClusters",
                "eks:DescribeAddonVersions",
                "eks:CreateCluster"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "eks:*",
            "Resource": "[CLUSTER ARN]"
        }
    ]
}
```

https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html

Next deploy the chart on Amazon Elastic Kubernetes Service (remote deployment)

```bash
foo@bar:~$ kubectl config current-context
foo@bar:~$ kubectl get svc
foo@bar:~$ helm install demo ./demo-0.1.0.tgz
foo@bar:~$ kubectl get svc
foo@bar:~$ kubectl get pods
foo@bar:~$ kubectl get deployments
```

Next open a port, open the cluster 

https://eu-west-1.console.aws.amazon.com/eks

Navigate to "Configuration" -> "Networking" -> "Cluster security group"

This should bring you to the security group in the VPC

https://eu-west-1.console.aws.amazon.com/vpc

Press "Actions" -> "Edit inbound rules" -> "Add rule" -> Type: HTTP, Source: Anywhere -> "Save Rules"

Next open the url:

```bash
foo@bar:~$ kubectl get svc
foo@bar:~$ export SERVICE_IP=$(kubectl get svc --namespace default reddit --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}")
foo@bar:~$ curl http://$SERVICE_IP:80
```

Cleanup

```bash
foo@bar:~$ eksctl delete cluster hughs-cluster
foo@bar:~$ aws ecr delete-repository --repository-name reddit-graphql --force
```
