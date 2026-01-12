from fastapi import APIRouter, FastAPI ,status , Request
from fastapi.responses import JSONResponse
import logging
from routes.schemes.nlp import PushRequest ,SearchRequest
from models.ProjectModel import ProjectModel 
from models.ChunkModel import ChunkModel , DataChunk
from controllers.NLPController import NLPController
from models import  ResponseSignal

logging = logging.getLogger("uvicorn.error")


nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1" ,"nlp"]
    )

@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request ,project_id: str , push_request: PushRequest):


    

    project_model = await ProjectModel.create_instance(# type: ignore
        db_client=request.app.database  
    )
    
    project  =  await project_model.get_project_or_create_one(
        project_id=project_id 
        )
    
    chunk_model = await ChunkModel.create_instance( # type: ignore
        db_client=request.app.database
    )
    
    if not project :
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                
                "signal": ResponseSignal.PROJECT_NOT_FOUND_ERROR.value

            }
        )

    nlp_controller = NLPController(
        vectoerdb_client=request.app.vectoerdb_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client
    )


    has_records =  True
    page_no  =  1 
    inserted_items_count = 0
    idx = 0


    while has_records :
        page_chunks  = await chunk_model.get_project_chunks(project_id=project.id, page_no=page_no)  # type: ignore

        if len(page_chunks) :
            page_no += 1
        
        if not page_chunks or len(page_chunks) ==0 :
            has_records = False
            break

        chunks_ids = list(range(idx, idx + len(page_chunks)))
        idx += len(page_chunks)

        is_inserted = nlp_controller.index_into_vector_db(
                project=project, # type: ignore
                chunks=page_chunks,  # type: ignore
                do_reset= push_request.do_reset  # type: ignore
                , chunks_ids= chunks_ids
            ) 
        
        if not is_inserted :
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    
                    "signal": ResponseSignal.INSERT_INTO_VECTOR_DB_ERROR.value

                }
            )
        inserted_items_count += len(page_chunks)
        
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.INSERT_INTO_VECTOR_DB_SUCCESS.value
            ,"inserted_items_count": inserted_items_count   
        }
    )
    

    
    # chunks  = await chunk_model.get_project_chunks(project_id=project.project_id ) # type: ignore


@nlp_router.get("/index/info/{project_id}")   
async def get_project_index_info(request: Request , project_id: str) :

    project_model = await ProjectModel.create_instance(# type: ignore
        db_client=request.app.database  
    )
    
    project  =  await project_model.get_project_or_create_one(
        project_id=project_id 
        )
    
    nlp_controller = NLPController(
        vectoerdb_client=request.app.vectoerdb_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client
    )

    collection_info = nlp_controller.get_vector_db_collection_info(
        project=project  # type: ignore
    )

    return JSONResponse(
        content={
            "signal": ResponseSignal.VECTOR_DB_COLLECTION_RETRIEVE_SUCCESS.value,
            "collection_info": collection_info
        },
        status_code=status.HTTP_200_OK
    )


@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request , project_id: str, search_request: SearchRequest):
    project_model = await ProjectModel.create_instance(# type: ignore
        db_client=request.app.database  
    )
    
    project  =  await project_model.get_project_or_create_one(
        project_id=project_id 
        )
    
    nlp_controller = NLPController(
        vectoerdb_client=request.app.vectoerdb_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client
    )


    resluts = nlp_controller.search_vector_db_collection(
        project=project,  # type: ignore
        query_text=search_request.query_text,
        top_k=search_request.top_k
    )
    if resluts is None :
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                
                "signal": ResponseSignal.VECTOR_DB_ERROR.value

            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.VECTOR_DB_SUCCESS.value,
            "results": resluts
        }
    )

    
        
    
    


    


   
