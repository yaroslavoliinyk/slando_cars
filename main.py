import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from contextlib import asynccontextmanager

from routers.cars import router as cars_router
from models import CarBase


DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)

origins = [
       "http://localhost",
       "http://localhost:8080",
       "http://localhost:3000",
       "http://localhost:8000",
]

app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)
app.include_router(cars_router, prefix="/cars", tags=["cars"])


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# @asynccontextmanager
# async def lifespan():
#     # On startup
#     app.mongodb_client = AsyncIOMotorClient(DB_URL)
#     app.mongodb = app.mongodb_client[DB_NAME]
#     print("Mongo instatiated")
#     yield
#     # On shutdown
#     app.mongodb_client.close()



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
