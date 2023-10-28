from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int = Field(description="id пользователя")
    name: str = Field(description="Имя пользователя")
    surname: str = Field(description="Фамилия пользователя")
    age: int = Field(description="Возраст пользователя")


class RegisterUserRequest(BaseModel):
    name: str = Field(description="Имя пользователя")
    surname: str = Field(description="Фамилия пользователя")
    age: int = Field(description="Возраст пользователя")


class UserModel(BaseModel):
    id: int = Field(description="id пользователя")
    name: str = Field(description="Имя пользователя")
    surname: str = Field(description="Фамилия пользователя")
    age: int = Field(description="Возраст пользователя")

    class Config:
        orm_mode = True
