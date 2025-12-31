from .BaseController import BaseController
from fastapi import FastAPI , APIRouter , Depends , UploadFile
from models import ResponseSignal
from .ProjectController import ProjectController
import re
import os


class DataController(BaseController):
   
    def __init__(self):
          super().__init__()
          self.size_scale = 1024 * 1024  # Convert MB to Bytes

    def validate_uplaoded_file(self , file:UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False , ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        file_size = file.size or 0
        if file_size > self.app_settings.FILE_MAX_SIZE_MB * self.size_scale:
            return False , ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True , ResponseSignal.FILE_VALIDATION_SUCCESS.value

    def generate_unique_filepath(self , original_filename:str , project_id:str):

        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        clean_filename = self.get_clean_file_name(
            filename=original_filename
            )

        new_filename_path = os.path.join(
            project_path ,
            f"{random_key}_{clean_filename}"
        )
        


        while os.path.exists(new_filename_path):
            random_key = self.generate_random_string()
            new_filename_path = os.path.join(
                project_path ,
                f"{random_key}_{clean_filename}"
            )

        return new_filename_path , random_key + "_" + clean_filename


    def get_clean_file_name(self , filename:str):

        # Remove special characters and spaces
        clean_filename = re.sub(r'[^a-zA-Z0-9_.-]' , '_' , filename)

        clean_filename = re.sub(r'__+' , '_' , clean_filename)  # Replace multiple underscores with a single underscore

        # replace spaces with underscores
        clean_filename = clean_filename.replace(' ' , '_')

        return clean_filename 