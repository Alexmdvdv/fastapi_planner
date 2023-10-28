from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class CityRequest(BaseModel):
    name: str = Field(description="Название города")


class CityResponse(BaseModel):
    id: int = Field(description="id города")
    name: str = Field(description="Название города")
    weather: str = Field(description="Погода в городе")


class PicnicRequest(BaseModel):
    city_id: int = Field(description="id города")
    time: datetime = Field(description="Время пикника")


class PicnicResponse(BaseModel):
    id: int = Field(description="id пикника")
    name: str = Field(description="Название города")
    time: datetime = Field(description="Время пикника")


class RegisterToPicnicRequest(BaseModel):
    user_id: int = Field(description="id пользователя")
    picnic_id: int = Field(description="id пикника для регистрации")


class RegisterToPicnicResponse(BaseModel):
    id: int = Field(description="id зарегистрированного пикника")
    name: str = Field(description="Имя пользователя")
    time: datetime = Field(description="Время пикника")


class PicnicUser(BaseModel):
    id: int
    name: str = Field(description="Имя")
    surname: str = Field(description="Фамилия")
    age: int = Field(description="Возраст")


class PicnicData(BaseModel):
    id: int = Field(description="id пикника")
    name: str = Field(description="Город")
    time: datetime = Field(description="Время пикника")
    users: List[PicnicUser] = Field(description="Пользователь")
