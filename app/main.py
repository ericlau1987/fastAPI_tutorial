from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from Property import Property
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel): 
    # https://docs.pydantic.dev/usage/types/
    # the class to automatically check whether parameters 
    # are the same as the required
    title: str
    content: str
    published: bool = True
    rating: Optional['int'] = None


class PropertyAddress(BaseModel):
    no_street: int 
    street_name: str 
    street_type: str 
    suburb: str 
    postcode: int

# request Get method url: "/"
# the order of the function matters
# the api run from

my_posts = [
    {
        "title": "title of post 11",
        "content": " content of post 1",
        "id": 1},
    {
        "title": "favorite foods",
        "content": "I like pizza",
        "id": 2}
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/") # decorator
async def root():
    return {"message": "Hello world"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# @app.get("/key")
# def get_key(property: PropertyAddress):
#     no_street = property.no_street
#     street_name = property.street_name
#     street_type = property.street_type
#     suburb = property.suburb
#     postcode = property.postcode

#     res = urllib.request.urlopen(f'https://www.land.vic.gov.au/property-report/property-dashboard2/street_suggestions.json?extraQuery=amendment-id&profile=amendment-id&partial_query={no_street}%20{street_name.upper()}%20{street_type.upper()}%20{suburb.upper()}%20{postcode}').read()
#     key = json.loads(res.decode('utf-8'))[0]["key"]
#     pfi = urllib.request.urlopen(f'https://www.land.vic.gov.au/property-report/property-dashboard2/get_street_key.json?query={key}').read()
#     pfi = json.loads(pfi.decode('utf-8'))['pfi']
#     search_website = f'https://www.land.vic.gov.au/property-report?property={no_street}+{street_name}+{street_type}+{suburb}+{pfi}%2C{key}'
#     _ = urllib.request.urlopen(f'https://www.land.vic.gov.au/property-report?property={no_street}+{street_name}+{street_type}+{suburb}+{pfi}%2C{key}')
#     # detailed_property_report_url = f'https://production-detailed-report-pdf.s3-ap-southeast-2.amazonaws.com/{no_street}-{street_name}-{street_type}-{suburb}-(ID{pfi})-Detailed-Property-Report.pdf'
#     detailed_property_report_url = f'https://property-report-api.mapshare.vic.gov.au/?PFI={pfi}&Type=Property&source=propertyportal'
#     parcel_pfi_url = f'https://www.land.vic.gov.au/property-report/property-dashboard2/get_related_property.json?query={pfi}'
#     parcel_pfi = urllib.request.urlopen(parcel_pfi_url).read()
#     parcel_pfi = json.loads(parcel_pfi.decode('utf-8'))
#     data_reporter_url = f'https://www.land.vic.gov.au/property-report/property-dashboard2/get_datareporter.json?query={pfi}&inputSearchType=property'
#     data_reporter = urllib.request.urlopen(data_reporter_url).read()
#     data_reporter = json.loads(data_reporter.decode('utf-8'))
#     parcel_address_url = f'https://www.land.vic.gov.au/property-report/property-dashboard2/get_parcel_address.json?query={pfi}'
#     parcel_address = urllib.request.urlopen(parcel_address_url).read()
#     parcel_address = json.loads(parcel_address.decode('utf-8'))

#     data = {
#             "no_street": no_street,
#             "street_name": street_name,
#             "street_type": street_type,
#             "suburb": suburb,
#             "postcode": postcode,
#             "key": key,
#             "pfi": pfi,
#             "search_website": search_website,
#             "detailed_property_report_url": detailed_property_report_url,
#             "parcel_pfi": parcel_pfi,
#             "data_reporter": data_reporter,
#             "parcel_address": parcel_address

#     }
#     return data

@app.get("/property/property_pdf")
def get_pdf(property: PropertyAddress):

    property = Property(
        no_street = property.no_street,
        street_name = property.street_name,
        street_type = property.street_type,
        suburb = property.suburb,
        postcode = property.postcode
    )

    property_pdf_url = property.get_property_pdf_url()

    return RedirectResponse(property_pdf_url)

@app.get("/property/property_pdf")
def get_pdf(property: PropertyAddress):

    property = Property(
        no_street = property.no_street,
        street_name = property.street_name,
        street_type = property.street_type,
        suburb = property.suburb,
        postcode = property.postcode
    )

    planning_pdf_url = property.get_planning_pdf_url()

    return RedirectResponse(planning_pdf_url)

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']}; content: {payload['content']}"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response): # add int to convert str to integer
    
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}

    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    # deleting post
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} doesn't exist")
    my_posts.pop(index)
    # when deleting data, we dont want to return any data 
    # instead, we just send the status back
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    print(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} doesn't exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"message": "update the post"}