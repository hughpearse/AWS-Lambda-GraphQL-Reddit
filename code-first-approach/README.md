# Running GraphQL with AWS Lambda

The following code downloads data from Reddit as:

https://www.reddit.com/r/MaliciousCompliance.json

And converts the response to a GraphQL defintion. The original Reddit API is wrapped in a new API using Flask. This is done using flask-graphql

To run it execute: 

```bash
foo@bar$ pipenv --rm
foo@bar$ pipenv install --three
foo@bar$ pipenv shell
foo@bar$ export FLASK_APP=app.py
foo@bar$ pipenv run flask run
```
Then open

http://127.0.0.1:5000/graphql

You can then run the following graphql query
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

