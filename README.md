# Running GraphQL with AWS Lambda

The following code downloads data from Reddit as:

https://www.reddit.com/r/MaliciousCompliance.json

And convers the response to a GraphQL API.

To run it execute: 

```bash
foo@bar$ pipenv --rm
foo@bar$ pipenv install --three
foo@bar$ export FLASK_APP=server.py
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
    ups
    downs
    author
    selftext
  }
}
```
