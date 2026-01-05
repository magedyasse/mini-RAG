from fastapi import FastAPI
from routes import base ,data
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from helper.config import get_settings
from typing import Any
from stores.LLMProviderFactory import LLMProviderFactory 

app = FastAPI()

# Type hints for custom app attributes
app.mongodb_client: Any = None  # type: ignore
app.database: Any = None  # type: ignore

# @app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URI)  # type: ignore
    app.database = app.mongodb_client[settings.MONGODB_DATABASE]  # type: ignore
    

    llm_provider_factory = LLMProviderFactory(settings)
    app.generic_llm_provider = llm_provider_factory.create_provider(provider_type = settings.GENERATION_BACKEND)  # type: ignore

    app.generic_llm_provider.set_generation_model(model_id= settings.GENRATION_MODEL_ID)  # type: ignore
    app.embedding_provider = llm_provider_factory.create_provider(provider_type = settings.EMBEDDING_BACKEND)  # type: ignore

    app.embedding_provider.set_embedding_model(model_id= settings.EMBEDDING_MODEL_ID , embedding_size= settings.EMBEDDING_MODEL_SIZE)  # type: ignore


# @app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()  # type: ignore    


app.router.lifespan.on_startup.append(startup_db_client)    # type: ignore
app.router.lifespan.on_shutdown.append(shutdown_db_client)  # type: ignore


app.include_router(base.base_router)
app.include_router(data.data_router)



