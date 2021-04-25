# Running GraphQL with AWS Lambda

The following code downloads data from Reddit as:

https://www.reddit.com/r/MaliciousCompliance.json

And converts the response to a GraphQL defintion. The original Reddit API is wrapped in a new API using Flask. This is done using 2 different approaches:

1. The code first approach
2. The schema first approach

You can then upload to AWS. First compress to an archive

```bash
foo@bar$ zip -r files.zip ./app.py ./.venv/*
```

Then upload to AWS Lambda (cloud functions)

https://eu-west-1.console.aws.amazon.com/lambda/

with the settings:

```text
name: myRedditGraphQLWrapper
environment: python v3.7
```

And create an associated REST gateway configuration

https://console.aws.amazon.com/apigateway/
