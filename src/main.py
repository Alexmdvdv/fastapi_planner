from fastapi import FastAPI
from operation.router import router as router_operation
from user.router import router as router_user

app = FastAPI()

app.include_router(
    router_operation,
    prefix='/picnic',
    tags=['Operation']
)

app.include_router(
    router_user,
    prefix='/user',
    tags=['User']
)
