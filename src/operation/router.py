import datetime as dt
from typing import List
from fastapi import HTTPException, APIRouter, Query, Depends
from src.database import Session
from src.database import get_db
from src.external_requests import GetWeatherRequest
from src.operation.models import City, Event, EventRegistration
from src.operation.schemas import CityResponse, CityValidator, EventValidator, EventResponse, RegisterToEventResponse, \
    RegisterToEventValidator, EventData
from src.user.models import User

router = APIRouter()


@router.get('/city/info/', response_model=List[CityResponse])
def get_cities(city: str = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(City)
    if city is not None:
        query = query.filter(City.name == city)

    else:
        query = query.all()

    return [
        {
            'id': city.id, 'name': city.name, 'weather': city.weather
        }
        for city in query
    ]


@router.post('/city/create/', response_model=List[CityResponse])
def create_city(city: CityValidator, db: Session = Depends(get_db)):
    if city.name is None:
        raise HTTPException(status_code=400, detail='Параметр city должен быть указан')

    check = GetWeatherRequest()
    if not check.check_existing(city.name):
        raise HTTPException(status_code=400, detail='Параметр city должен быть существующим городом')

    query = db.query(City).filter(City.name == city.name.capitalize()).first()

    if query is None:
        query = City(name=city.name.capitalize())
        db.add(query)
        db.commit()

    return [{'id': query.id, 'name': query.name, 'weather': query.weather}]


@router.get('/info/', response_model=List[EventData])
def get_events(datetime: dt.datetime = None, past: bool = True, db: Session = Depends(get_db)):
    query = db.query(Event)
    if datetime is not None:
        query = query.filter(Event.time == datetime)

    if not past:
        query = query.filter(Event.time >= dt.datetime.now())

    return [
        {
            'id': event.id,
            'name': db.query(City).filter(City.id == event.id).first().name,
            'time': event.time,
            'users': [
                {
                    'id': pr.user.id,
                    'name': pr.user.name,
                    'surname': pr.user.surname,
                    'age': pr.user.age,
                }
                for pr in event.users
            ]
        }
        for event in query
    ]


@router.post('/create/', response_model=List[EventResponse])
def create_event(request: EventValidator, db: Session = Depends(get_db)):
    city_id = request.city_id
    datetime = request.time

    if city_id is None:
        raise HTTPException(status_code=400, detail='Город должен быть указан')

    if datetime is None:
        raise HTTPException(status_code=400, detail='Время должно быть указано')

    query = Event(city_id=city_id, time=datetime)
    db.add(query)
    db.commit()

    return [
        {
            'id': query.id,
            'name': db.query(City).filter(City.id == city_id).first().name,
            'time': query.time,
        }
    ]


@router.post('/register/', response_model=List[RegisterToEventResponse])
def register_to_event(request: RegisterToEventValidator, db: Session = Depends(get_db)):
    user_id = request.user_id
    event_id = request.event_id

    user_query = db.query(User).filter(User.id == user_id).first()
    if user_query is None:
        raise HTTPException(status_code=400, detail="Пользователь не найден")

    event_query = db.query(Event).filter(Event.id == event_id).first()
    if event_query is None:
        raise HTTPException(status_code=400, detail="Пикник не найден")

    registration_query = EventRegistration(user_id=user_id, event_id=event_id)

    db.add(registration_query)
    db.commit()

    return [
        {
            'id': user_query.id,
            'name': user_query.name,
            'time': event_query.time,
        }
    ]
