from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
import json
import urllib

app = FastAPI()

class Post(BaseModel): 
    # https://docs.pydantic.dev/usage/types/
    # the class to automatically check whether parameters 
    # are the same as the required
    title: str
    content: str


# request Get method url: "/"
# the order of the function matters
# the api run from

@app.get("/") # decorator
async def root():
    return {"message": "Hello world"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.get("/key")
def get_key(payload: dict = Body(...)):
    no_street = payload['no_street']
    street_name = payload['street_name']
    street_type = payload['street_type']
    suburb = payload['suburb']
    postcode = payload['postcode']
    url = f'https://www.land.vic.gov.au/property-report/property-dashboard2/street_suggestions.json?extraQuery=amendment-id&profile=amendment-id&partial_query={no_street}%20{street_name.upper()}%20{street_type.upper()}%20{suburb.upper()}%20{postcode}'
    # res = urllib.request.urlopen(url).read()
    # print(url)
    # data = json.loads(res.decode('utf-8'))
    return url

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']}; content: {payload['content']}"}

@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post.title) # if would extract from json and print out as value
    return {"new_post": "new posts"}

# title str, content str, category, Bool published