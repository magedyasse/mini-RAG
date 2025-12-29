from fastapi import FastAPI , APIRouter , Depends , UploadFile ,status , Request
import os
import aiofiles
from helper.config import get_settings , Settings
from controllers import DataController , ProjectController , ProcessController
from models import ResponseSignal
from fastapi.responses import JSONResponse
import logging 
from .schemes.data import ProcessRequest 
from models.ProjectModel import ProjectModel
from models.db_schemes import DataChunk , Asset
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
from models.enums.AssetTypeEnum import AssetTypeEnum

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)


@data_router.post("/upload/{project_id}")
async def upload_data(request : Request , project_id: str, file: UploadFile ,
        app_settings : Settings = Depends(get_settings)):


        project_model = await ProjectModel.create_instance(
            db_client=request.app.database  # Fixed: was mongodb_client (MongoClient), should be database (Database object)
        )

        project = await project_model.get_project_or_create_one(
            project_id=project_id
        )

        # Validate file extension
        data_controller = DataController()
        is_valid , message = data_controller.validate_uplaoded_file(file=file)

        if not is_valid:
            return JSONResponse(
                status_code= status.HTTP_400_BAD_REQUEST,
                content={"message": message}    
            )

        # Get project path
        project_dir_path = ProjectController().get_project_path(project_id=project_id)
        file_path, file_id = data_controller.generate_unique_filepath(
            original_filename=file.filename ,
            project_id=project_id
        )

        try:
            async with aiofiles.open(file_path , 'wb') as f:
                while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):  # Read file in chunks
                    await f.write(chunk)
        except Exception as e:   

            logger.error(f"File upload failed: {e}")
            return JSONResponse(
                    status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={
                        "message": ResponseSignal.FILE_UPLOAD_FAILED.value
                    }    
                )   

        # store asset record in db
        asset_model = await AssetModel.create_instance(
            db_client=request.app.database
        )

        asset_resource = Asset(
           asset_project_id = project.id,
           asset_type = AssetTypeEnum.FILE.value,
           asset_name = file_id, 
           asset_size = os.path.getsize(file_path),
       )

        asset_record = await asset_model.create_asset(
            asset=asset_resource
        )

        return JSONResponse(
                status_code= status.HTTP_200_OK,
                content={
                    "message": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                    # "file_id": file_id,
                    "file_id": str(asset_record.id)
                }  
            )           



@data_router.post("/process/{project_id}")
async def process_data(project_id: str, process_request: ProcessRequest, request: Request):  # Fixed: renamed ProcessRequest param and added Request param
    # Your processing logic here
    file_id =  process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(
            db_client=request.app.database  # Now correctly uses FastAPI Request object
        )
    project = await project_model.get_project_or_create_one(
            project_id=project_id
        )




    process_controller = ProcessController(project_id=project_id)   

    file_content = process_controller.get_file_content(file_id=file_id)
    
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content={
                "message": ResponseSignal.PROCESSING_FAILED.value
            }    
        )

    # return file_chunks 

    file_chunks_records = [

        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id= project.id,  # Fixed: ProjectDBScheme has '_id', not 'id'
        )
        for i,chunk in  enumerate(file_chunks)
    ]

    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.database 
    )    
    
    if do_reset==1 :
        deleted_count = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id  # Fixed: ProjectDBScheme has '_id', not 'id'
        )
        # logger.info(f"Deleted {deleted_count} chunks for project_id: {project_id}")


    no_records = await chunk_model.insert_many_chunks(
        data_chunks=file_chunks_records,
       
    )

    return JSONResponse(
         content={
            "message": ResponseSignal.PROCESSING_SUCCESS.value,
            "records_inserted": no_records
         }
    )