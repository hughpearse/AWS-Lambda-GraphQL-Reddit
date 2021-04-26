
```bash
foo@bar$ pipenv --rm
foo@bar$ pipenv install -d --three # Dev
foo@bar$ pipenv install --three # Production
foo@bar$ pipenv shell
```

You can test the lambda code:

```bash
foo@bar$ lambda init # dev purposes only
foo@bar$ lambda invoke
```

Or you can run the web server

```bash
foo@bar$ export FLASK_APP=service.py
foo@bar$ flask run
```

And access the UI at

http://127.0.0.1:5000/graphql

Next create a table called "GraphQLReddit" on DynamoDB in the samee region

https://console.aws.amazon.com/dynamodb

It should have a Primary key name "graphqlquery" with a type String. Take a note of the table "ARN" value.

```text
arn:aws:lambda:eu-west-1:123456789:function:myRedditGraphQLWrapper
```

Next you can build the archive

```bash
foo@bar$ lambda build
```

You can then upload the resulting zip archive (in dist/) to AWS Lambda (cloud functions)

https://eu-west-1.console.aws.amazon.com/lambda/

with the settings:

```text
name: myRedditGraphQLWrapper
environment: python v3.7
Runtime settings -> Handler: service.handler
```

Then in your Lambda function navigate to

```text
Configuration -> Execution role -> Role name -> myRedditGraphQLWrapper-role-xxxxxxx
```

And open the IAM page to "Add Inline Policy"

https://console.aws.amazon.com/iam

```javascript
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:Query",
                "dynamodb:UpdateItem"
            ],
            "Resource": "[YOUR DATABASE ARN]"
        }
    ]
}
```

Press "Review Policy" -> Name: myRedditGraphQLWrapperPolicy -> Create Polocy

Next create an associated REST gateway configuration

https://console.aws.amazon.com/apigateway/

```text
API name: myRedditGraphQLWrapper
Endpoint Type: Edge optimized
Actions -> Create Method -> POST
Actions -> Enable CORS
Actions -> Deploy API
Deployment Stage: New Stage
Stage name: Beta
```

Take a note of the gateway endpoint. 

Next create a table called "GraphQLReddit" on DynamoDB in the samee region

https://console.aws.amazon.com/dynamodb

It should have a Primary key name "graphqlquery" with a type String

You can then test your new API on a hosted Grapql Playground tool like

https://lucasconstantino.github.io/graphiql-online/

or

https://www.graphqlbin.com/v2/new

```javascript
query{
  posts (subreddit:"maliciouscompliance"){
    id
    title
    url
    url_overridden_by_dest
    ups
    downs
    author
    selftext
  }
}
```
