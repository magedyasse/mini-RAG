from fastapi import FastAPI , APIRouter , Depends , UploadFile ,status
import os
import aiofiles
from helper.config import get_settings , Settings
from controllers import DataController , ProjectController , ProcessController
from models import ResponseSignal
from fastapi.responses import JSONResponse
import logging 
from .schemes.data import ProcessRequest 


logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)


@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile ,
        app_settings : Settings = Depends(get_settings)):


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
        return JSONResponse(
                status_code= status.HTTP_200_OK,
                content={
                    "message": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                    "file_path": file_path,
                    "file_id": file_id

                }  
            )           



@data_router.post("/process/{project_id}")
async def process_data(project_id: str, request: ProcessRequest):
    # Your processing logic here
    file_id =  request.file_id

    chunk_size = request.chunk_size
    
    overlap_size = request.overlap_size

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

    return file_chunks 