from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base
from operation.utils import GetWeatherRequest

if TYPE_CHECKING:
    from user.models import User  # To associate with the User model


class City(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    @property
    def weather(self) -> str:
        r = GetWeatherRequest()
        weather = r.get_weather(self.name)
        if weather is not None:
            return weather

    def __repr__(self):
        return f'<Город "{self.name}">'


class Event(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    time = Column(DateTime, nullable=False)

    def __repr__(self):
        return f'<Событие {self.id}>'


class EventRegistration(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)

    user = relationship("User", backref='events')
    event = relationship("Event", backref='users')

    def __repr__(self):
        return f'<Регистрация {self.id}>'
