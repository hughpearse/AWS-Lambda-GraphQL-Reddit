# Running GraphQL with AWS Lambda

The following code downloads data from Reddit as:

https://www.reddit.com/r/MaliciousCompliance.json

And converts the response to a GraphQL defintion. The original Reddit API is wrapped in a new API using Flask. This is done using 2 different approaches:

1. The code first approach
2. The schema first approach
3. The serverless cloud functions approach
