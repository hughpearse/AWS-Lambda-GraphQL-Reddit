from flask import Flask, request, jsonify
import requests
import json
import os
from ariadne import make_executable_schema, ObjectType, QueryType, gql, graphql_sync
from ariadne.asgi import GraphQL
from ariadne.constants import PLAYGROUND_HTML
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GraphQLReddit')

myschema = gql("""
type Query {
    posts(subreddit: String): [Post]
}
type Post {
    id: ID
    title: String
    url: String
    author: String
    ups: Int
    downs: Int
    content: String
    url_overridden_by_dest: String
    selftext: String
}
""")

query = QueryType()

@query.field("posts")
def get_posts(obj, info, subreddit=None):
    url = 'https://www.reddit.com/r/{subr}'.format(subr="worldnews" if not subreddit else subreddit)
    r = requests.get(url + '.json', headers = {'User-agent': 'hughs bot 0.1'})
    posts_arr = [x['data'] for x in r.json()['data']['children']]
    return posts_arr

type_defs = myschema
posts = ObjectType("Post")
schema = make_executable_schema(type_defs, query, posts)
app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

def handler(event, context):
    with app.app_context():
      response = table.put_item(Item={'graphqlquery': str(event)})
      success, result = graphql_sync(
          schema,
          event,
          context_value=request,
          debug=app.debug
      )
      status_code = 200 if success else 400
      return result

