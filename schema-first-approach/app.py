from ariadne import make_executable_schema, ObjectType, QueryType, gql, graphql_sync
from ariadne.asgi import GraphQL
import requests
import json

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
def resolve_posts(obj, info, subreddit=None):
    print("triggered")
    url = 'https://www.reddit.com/r/{subr}'.format(subr=subreddit if subreddit else "worldnews")
    r = requests.get(url + '.json', headers = {'User-agent': 'hughs bot 0.1'})
    posts_arr = [x['data'] for x in r.json()['data']['children']]
    return posts_arr

type_defs = myschema
posts = ObjectType("Post")
schema = make_executable_schema(type_defs, query, posts)
myasgi_app = GraphQL(schema, debug=True)

