from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database import Base, engine
from src.utils import GetWeatherRequest
from src.user.models import User


class City(Base):
    __tablename__ = 'city'

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
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    time = Column(DateTime, nullable=False)

    def __repr__(self):
        return f'<Событие {self.id}>'


class EventRegistration(Base):
    __tablename__ = 'event_registration'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)

    user = relationship(User, backref='events')
    event = relationship(Event, backref='users')

    def __repr__(self):
        return f'<Регистрация {self.id}>'


Base.metadata.create_all(bind=engine)
