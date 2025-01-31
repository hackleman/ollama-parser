from pydantic import BaseModel # type: ignore
from models.USState import State
import json

# class Address(BaseModel):
#     city: str
#     state: State
class Address(BaseModel):
    city: str
    state: State

    def __init__(self, city, state):
        super().__init__(city=city, state=state)
    def to_dict(self):
        return {
            "city": self.city,
            "state": self.state,
        }

    def to_json(self):
        return json.dumps(self.to_dict())
    
# class Meeting(BaseModel):
#     name: str
#     address: Address
#     URL: str
#     PhoneNumber: list[str]

class Meeting(BaseModel):
    name: str
    address: Address
    URL: str
    PhoneNumber: list[str]
    latitude: float | None
    longitude: float | None


    def __init__(self, name, address, URL, PhoneNumber, latitude, longitude):
        super().__init__(
            name=name, 
            address=address, 
            URL=URL, 
            PhoneNumber=PhoneNumber,
            latitude=None,
            longitude=None
            )
    
    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address,
            "URL": self.URL,
            "PhoneNumber": self.PhoneNumber,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    def to_json(self):
        return json.dumps(self.to_dict())
    
    def setGeolocation(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Meetings(BaseModel):
    meetings: list[Meeting]