from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/property",
    tags = ['Property'] # this is to show a group in property
)

@router.get("/property_pdf")
def get_pdf(no_street: str,
            street_name: str,
            street_type: str,
            suburb: str,
            postcode: int):

    property = utils.Property(
        no_street = no_street,
        street_name = street_name,
        street_type = street_type,
        suburb = suburb,
        postcode = postcode
    ) 
    # property = utils.Property(
    #     **property.dict()
    # )

    has_pfi = property.check_address_exist()
    if not has_pfi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the address is invalid")
    else:
        property_pdf_url = property.get_property_pdf_url()
        return RedirectResponse(property_pdf_url)

@router.get("/planning_pdf")
def get_pdf(no_street: str,
            street_name: str,
            street_type: str,
            suburb: str,
            postcode: int):

    property = utils.Property(
        no_street = no_street,
        street_name = street_name,
        street_type = street_type,
        suburb = suburb,
        postcode = postcode
    )

    has_pfi = property.check_address_exist()
    if not has_pfi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the address is invalid")
    else:
        planning_pdf_url = property.get_planning_pdf_url()

        return RedirectResponse(planning_pdf_url)