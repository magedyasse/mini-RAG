from fastapi import FastAPI
from routes import base ,data ,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helper.config import get_settings
from typing import Any
from stores.llm.LLMProviderFactory import LLMProviderFactory 
from stores.vectordb.VectoerDBProvidersFactory import VectoerDBProvidersFactory   


app = FastAPI()

# Type hints for custom app attributes
app.mongodb_client: Any = None  # type: ignore
app.database: Any = None  # type: ignore

# @app.on_event("startup")
async def startup_span():

    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URI)  # type: ignore
    app.database = app.mongodb_client[settings.MONGODB_DATABASE]  # type: ignore
    

    llm_provider_factory = LLMProviderFactory(settings)
    vectoerdb_provider_factory = VectoerDBProvidersFactory(settings)


    app.generation_client = llm_provider_factory.create_provider(provider_type = settings.GENERATION_BACKEND)  # type: ignore
    app.generation_client.set_generation_model(model_id= settings.GENERATION_MODEL_ID) # type: ignore
    

    app.embedding_client = llm_provider_factory.create_provider(provider_type = settings.EMBEDDING_BACKEND)  # type: ignore
    app.embedding_client.set_embedding_model(model_id= settings.EMBEDDING_MODEL_ID # type: ignore
                                             , embedding_size= settings.EMBEDDING_MODEL_SIZE)  



    app.vectoerdb_client   = vectoerdb_provider_factory.create( # type: ignore
        provider=settings.VECTOR_DB_BACKEND,
    )  

    app.vectoerdb_client.connect()  # type: ignore



# @app.on_event("shutdown")
async def shutdown_span():
    app.mongodb_client.close()  # type: ignore    
    app.vectoerdb_client.disconnect()  # type: ignore



# app.router.lifespan.on_startup.append(startup_span)    # type: ignore
# app.router.lifespan.on_shutdown.append(shutdown_span)  # type: ignore

app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)



