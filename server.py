from collections import namedtuple
from graphene import ObjectType, String, ID, Int, ObjectType, List
from flask import Flask
from flask_graphql import GraphQLView
from graphene import Schema
import requests
import json
import os

class Post(ObjectType):
    id = ID()
    title = String()
    url = String()
    url_overridden_by_dest = String()
    author = String ()
    ups = Int()
    downs = Int()
    selftext = String()

def api_call(subreddit=None):
    url = 'https://www.reddit.com/r/{subr}'.format(subr=subreddit if subreddit else "worldnews")
    r = requests.get(url + '.json', headers = {'User-agent': 'hughs bot 0.1'})
    posts_arr = [x['data'] for x in r.json()['data']['children']]
    payload = {
            "posts": posts_arr
    }
    return posts_arr

class Query(ObjectType):
    posts = List(Post, subreddit=String(required=False))

    def resolve_posts(self, info, subreddit=None):
        posts = api_call(subreddit)
        return posts

view_func = GraphQLView.as_view(
    'graphql', schema=Schema(query=Query), graphiql=True)

app = Flask(__name__)
app.add_url_rule('/graphql', view_func=view_func)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
