from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
import json
import urllib.request
from typing import Optional

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

@app.get("/") # decorator
async def root():
    return {"message": "Hello world"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

"""
@app.get("/key")
def get_key(property: PropertyAddress):
    no_street = property.no_street
    street_name = property.street_name
    street_type = property.street_type
    suburb = property.suburb
    postcode = property.postcode

    res = urllib.request.urlopen(f'https://www.land.vic.gov.au/property-report/property-dashboard2/street_suggestions.json?extraQuery=amendment-id&profile=amendment-id&partial_query={no_street}%20{street_name.upper()}%20{street_type.upper()}%20{suburb.upper()}%20{postcode}').read()
    key = json.loads(res.decode('utf-8'))[0]["key"]
    pfi = urllib.request.urlopen(f'https://www.land.vic.gov.au/property-report/property-dashboard2/get_street_key.json?query={key}').read()
    pfi = json.loads(pfi.decode('utf-8'))['pfi']
    detailed_property_report_url = f'https://production-detailed-report-pdf.s3-ap-southeast-2.amazonaws.com/{no_street}-{street_name}-{street_type}-{suburb}-(ID{pfi})-Detailed-Property-Report.pdf'
    parcel_pfi_url = f'https://www.land.vic.gov.au/property-report/property-dashboard2/get_related_property.json?query={pfi}'
    parcel_pfi = urllib.request.urlopen(parcel_pfi_url).read()
    parcel_pfi = json.loads(parcel_pfi.decode('utf-8'))
    data_reporter_url = f'https://www.land.vic.gov.au/property-report/property-dashboard2/get_datareporter.json?query={pfi}&inputSearchType=property'
    data_reporter = urllib.request.urlopen(data_reporter_url).read()
    data_reporter = json.loads(data_reporter.decode('utf-8'))
    parcel_address_url = f'https://www.land.vic.gov.au/property-report/property-dashboard2/get_parcel_address.json?query={pfi}'
    parcel_address = urllib.request.urlopen(parcel_address_url).read()
    parcel_address = json.loads(parcel_address.decode('utf-8'))

    data = {
            "no_street": no_street,
            "street_name": street_name,
            "street_type": street_type,
            "suburb": suburb,
            "postcode": postcode,
            "key": key,
            "pfi": pfi,
            "detailed_property_report_url": detailed_property_report_url,
            "parcel_pfi": parcel_pfi,
            "data_reporter": data_reporter,
            "parcel_address": parcel_address

    }
    return data
"""
    

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']}; content: {payload['content']}"}

@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post)
    print(new_post.dict()) # if would extract from json and print out as value
    return {"new_post": "new posts"}

# title str, content str, category, Bool published