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

@router.get("/pfi")
def get_pdf(address: str):

    property = utils.Property(
        address = address
    ) 

    has_pfi = property.check_address_exist()
    if not has_pfi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the address is invalid")
    else:
        property_pdf_url = property.get_property_pdf_url()
        return {"pfi": property.pfi}
    

@router.get("/property_pdf")
def get_pdf(address: str):

    property = utils.Property(
        address = address
    ) 

    has_pfi = property.check_address_exist()
    if not has_pfi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the address is invalid")
    else:
        property_pdf_url = property.get_property_pdf_url()
        return RedirectResponse(property_pdf_url)

@router.get("/planning_pdf")
def get_pdf(address: str):

    property = utils.Property(
        address = address
    )

    has_pfi = property.check_address_exist()
    if not has_pfi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the address is invalid")
    else:
        planning_pdf_url = property.get_planning_pdf_url()

        return RedirectResponse(planning_pdf_url)
    
@router.get("/related_property_data")
def get_pdf(address: str):

    property = utils.Property(
        address = address
    )

    has_pfi = property.check_address_exist()
    if not has_pfi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the address is invalid")
    else:
        property_data_url = property.get_related_property_data_url()
        data = property.read_json(property_data_url)
        return {"data": data}
    
@router.get("/get_street_address")
def get_pdf(address: str):

    property = utils.Property(
        address = address
    )

    has_pfi = property.check_address_exist()
    if not has_pfi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the address is invalid")
    else:
        street_address_url = property.get_street_address_url()
        data = property.read_json(street_address_url)
        return {"data": data}
    
@router.get("/property_report_data")
def get_pdf(address: str):

    property = utils.Property(
        address = address
    )

    has_pfi = property.check_address_exist()
    if not has_pfi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the address is invalid")
    else:
        url = property.get_property_report_data_url()
        data = property.read_json(url)
        return data
    
@router.get("/parcel_address")
def get_pdf(address: str):

    property = utils.Property(
        address = address
    )

    has_pfi = property.check_address_exist()
    if not has_pfi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the address is invalid")
    else:
        url = property.get_parcel_address_url()
        data = property.read_json(url)
        return {"data": data}

@router.get("/property_results")
def get_pdf(address: str):

    property = utils.Property(
        address = address
    )

    has_pfi = property.check_address_exist()
    if not has_pfi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the address is invalid")
    else:
        result = []
        lga, overlay_zone_code_group_label, zone_code_group_label, \
        zone_desc, council_prop_num, spi, lot, plan, lot_plan \
            = [None]*9
        pfi = property.pfi
        parcel_pfi = property.get_parcel_pfi()
        property_report_data_url = property.get_property_report_data_url()
        property_report_data = property.read_json(property_report_data_url)
        multi_parcel_address_url = property.get_multi_parcel_address_url()
        multi_parcel_address_data = property.read_json(multi_parcel_address_url)
        
        for data in property_report_data:
            if data['paramName'] == 'overlays':
                if data['value']['features']:
                    overlay_zone_code_group_label = data['value']['features'][0]['attributes']["ZONE_CODE_GROUP_LABEL"]

            if data['paramName'] == 'zones':
                if data['value']['features']:
                    lga = data['value']['features'][0]['attributes']["LGA"]
                    zone_code_group_label = data['value']['features'][0]['attributes']["ZONE_CODE_GROUP_LABEL"]
                    zone_desc = data['value']['features'][0]['attributes']["ZONE_DESCRIPTION"]

            if data['paramName'] == 'searchFeature':
                if data['value']['features']:
                    council_prop_num = data['value']['features'][0]['attributes']["PROP_PROPNUM"]

        spi = multi_parcel_address_data[0]['spi']
        lot = multi_parcel_address_data[0]['lot']
        plan = multi_parcel_address_data[0]['plan']
        lot_plan = f'{lot} {plan}'

        result = [
                {
                    'paramName': 'PROPERTY DETAILS',
                    'fields': {
                        'lga': 'Local Government Area (Council)',
                        'council_prop_num': 'Council Property Number',
                        'lot_plan' : 'Lot / Plan',
                        'spi': 'Standard Parcel Identifier (SPI)'
                    },
                    'values': {
                        'lga': lga,
                        'council_prop_num': council_prop_num,
                        'lot_plan' : lot_plan,
                        'spi': spi
                    }
                },
                {
                    'paramName': 'ZONE AND OVERLAYS',
                    'fields': {
                        'zone': 'Zone',
                        'overlays': 'Overlays'
                    },
                    'values': {
                        'zone': [zone_code_group_label, zone_desc],
                        'overlays': overlay_zone_code_group_label
                    }
                }
            ]
        
        return {"data": result}
        
            
