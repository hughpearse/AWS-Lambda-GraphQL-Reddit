
```bash
foo@bar$ pipenv --rm
foo@bar$ pipenv install --three
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

build the archive

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
