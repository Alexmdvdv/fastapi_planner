from typing import List
from database import Session
from fastapi import Query, Depends
from fastapi import APIRouter

from dependencies import get_db
from user.models import User
from user.schemas import RegisterUserRequest, UserModel, UserResponse

router = APIRouter()


@router.get('/info/', response_model=List[UserResponse], description="Список пользователей")
def get_users(max_age: int = Query(default=None, description="Младше"),
              min_age: int = Query(default=None, description="Старше"), db: Session = Depends(get_db)):
    query = db.query(User)

    if max_age is not None:
        users = query.filter(User.age <= max_age)

    elif min_age is not None:
        users = query.filter(User.age >= min_age)

    else:
        users = query.all()
    return [{
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age,
    } for user in users]


@router.post('/register/', response_model=List[UserModel], description="Регистрация пользователя")
def register_user(user: RegisterUserRequest, db: Session = Depends(get_db)):
    user_object = User(**user.dict())
    session = db
    session.add(user_object)
    session.commit()

    return [{
        "id": user_object.id,
        "name": user_object.name,
        "surname": user_object.surname,
        "age": user_object.age
    }]
