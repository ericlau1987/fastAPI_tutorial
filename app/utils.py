from passlib.context import CryptContext
import json
import urllib.request

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

class Property:
    def __init__(self, no_street: str, 
            street_name: str, 
            street_type: str, 
            suburb: str, 
            postcode: int):
        self.no_street = no_street
        self.street_name = street_name
        self.street_type = street_type
        self.suburb = suburb
        self.postcode = postcode
        self.pfi = self._get_pfi()

    def _read_json(self, url: str):
        response = urllib.request.urlopen(url).read()
        result = json.loads(response.decode('utf-8'))
        return result

    def check_address_exist(self):
        if self.pfi:
            return True 
        else:
            return False

    def _get_pfi(self):
        
        try:
            full_address = " ".join([self.no_street, self.street_name, self.street_type, self.suburb, str(self.postcode)])
            full_address = full_address.upper().replace(" ", "%20")
            get_key_url = f"https://www.land.vic.gov.au/property-report/property-dashboard2/street_suggestions.json?extraQuery=amendment-id&profile=amendment-id&partial_query={full_address}"
            key = self._read_json(get_key_url)[0]["key"]
            get_pfi_url = f'https://www.land.vic.gov.au/property-report/property-dashboard2/get_street_key.json?query={key}'
            pfi = self._read_json(get_pfi_url)["pfi"]
            return pfi
        except:
            raise(get_key_url)
            return None
    
    def get_property_pdf_url(self):
        property_pdf_url = f"https://property-report-api.mapshare.vic.gov.au/?PFI={self.pfi}&Type=Property&source=propertyportal"
        return property_pdf_url
    
    def get_planning_pdf_url(self):
        planning_pdf_url = f"https://planning-report-api.maps.vic.gov.au/?PFI={self.pfi}&Type=Property&source=propertyportal"
        
        return planning_pdf_url



