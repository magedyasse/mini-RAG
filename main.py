from fastapi import FastAPI
from routes import base ,data
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from helper.config import get_settings
from typing import Any


app = FastAPI()

# Type hints for custom app attributes
app.mongodb_client: Any = None  # type: ignore
app.database: Any = None  # type: ignore

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URI)  # type: ignore
    app.database = app.mongodb_client[settings.MONGODB_DATABASE]  # type: ignore


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()  # type: ignore    



app.include_router(base.base_router)
app.include_router(data.data_router)



