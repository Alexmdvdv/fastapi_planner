import logging
from fastapi import FastAPI
from operation.router import router as router_operation
from user.router import router as router_user

logging.basicConfig(filename='./logging.log', level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] - %(message)s')
app = FastAPI()

app.include_router(
    router_operation,
    prefix='/event',
    tags=['Operation']
)

app.include_router(
    router_user,
    prefix='/user',
    tags=['User']
)
