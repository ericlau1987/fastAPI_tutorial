from fastapi import FastAPI
import json
import urllib

app = FastAPI()

# request Get method url: "/"
# the order of the function matters
# the api run from the top

@app.get("/") # decorator
async def root():
    return {"message": "Hello world"}

@app.get("/")
def get_posts():
    return {"data": "This is your posts"}