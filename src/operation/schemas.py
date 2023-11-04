from typing import List
from pydantic import BaseModel
from datetime import datetime


class CityValidator(BaseModel):
    name: str


class CityResponse(BaseModel):
    id: int
    name: str
    weather: str


class EventValidator(BaseModel):
    city_id: int
    time: datetime


class EventResponse(BaseModel):
    id: int
    name: str
    time: datetime


class RegisterToEventValidator(BaseModel):
    user_id: int
    event_id: int


class RegisterToEventResponse(BaseModel):
    id: int
    name: str
    time: datetime


class UserEvent(BaseModel):
    id: int
    name: str
    surname: str
    age: int


class EventData(BaseModel):
    id: int
    name: str
    time: datetime
    users: List[UserEvent]
