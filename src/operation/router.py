import datetime as dt
from typing import List
from fastapi import HTTPException, APIRouter, Query, Depends
from database import Session
from dependencies import get_db
from external_requests import GetWeatherRequest
from models import City, Picnic, PicnicRegistration, User
from operation.schemas import CityResponse, CityRequest, PicnicResponse, PicnicRequest, RegisterToPicnicResponse, \
    PicnicData, RegisterToPicnicRequest

router = APIRouter()


@router.get('/city/info/', response_model=List[CityResponse], description="Список городов")
def get_cities(q: str = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(City)
    if q is not None:
        query = query.filter(City.name == q)

    else:
        query = query.all()

    return [
        {
            'id': city.id, 'name': city.name, 'weather': city.weather
        }
        for city in query
    ]


@router.get('/info/', response_model=List[PicnicData], description="Список пикников")
def get_picnics(datetime: dt.datetime = None, past: bool = True, db: Session = Depends(get_db)):
    query = db.query(Picnic)
    if datetime is not None:
        query = query.filter(Picnic.time == datetime)

    if not past:
        query = query.filter(Picnic.time >= dt.datetime.now())

    return [
        {
            'id': picnic.id,
            'name': db.query(City).filter(City.id == picnic.id).first().name,
            'time': picnic.time,
            'users': [
                {
                    'id': pr.user.id,
                    'name': pr.user.name,
                    'surname': pr.user.surname,
                    'age': pr.user.age,
                }
                for pr in picnic.users
            ]
        }
        for picnic in query
    ]


@router.post('/city/create/', response_model=List[CityResponse], description="Создание города по его названию")
def create_city(city: CityRequest, db: Session = Depends(get_db)):
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


@router.post('/create/', response_model=List[PicnicResponse], description="Создание пикника")
def create_picnic(request: PicnicRequest, db: Session = Depends(get_db)):
    city_id = request.city_id
    datetime = request.time

    if city_id is None:
        raise HTTPException(status_code=400, detail='Город должен быть указан')

    if datetime is None:
        raise HTTPException(status_code=400, detail='Время должно быть указано')

    query = Picnic(city_id=city_id, time=datetime)
    db.add(query)
    db.commit()

    return [
        {
            'id': query.id,
            'name': db.query(City).filter(City.id == query.id).first().name,
            'time': query.time,
        }
    ]


@router.post('/register/', response_model=List[RegisterToPicnicResponse], description="Регистрация на пикник")
def register_to_picnic(request: RegisterToPicnicRequest, db: Session = Depends(get_db)):
    user_id = request.user_id
    picnic_id = request.picnic_id

    user_query = db.query(User).filter(User.id == user_id).first()
    if user_query is None:
        raise HTTPException(status_code=400, detail="Пользователь не найден")

    picnic_query = db.query(Picnic).filter(Picnic.id == picnic_id).first()
    if picnic_query is None:
        raise HTTPException(status_code=400, detail="Пикник не найден")

    registration_query = PicnicRegistration(user_id=user_id, picnic_id=picnic_id)

    db.add(registration_query)
    db.commit()

    return [
        {
            'id': user_query.id,
            'name': user_query.name,
            'time': picnic_query.time,
        }
    ]
