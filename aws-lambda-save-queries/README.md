
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
Handler: service.handler
```

And create an associated REST gateway configuration

https://console.aws.amazon.com/apigateway/

```text
Actions -> Create Method -> POST
Actions -> Enable CORS
Actions -> Deploy API
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
