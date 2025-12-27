from pydantic import BaseModel , Field , validator
from typing import Optional
from bso.objectid import ObjectId

class ProjectDBScheme(BaseModel):

    _id : Optional[ObjectId]
    project_id : str =  Field(... , min_length=3 , max_length=20)


    @validator("project_id")
    def validate_project_id(cls , v):
        if not v.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return v


    class Config:
        # use this to allow ObjectId type
        arbitrary_types_allowed = True 
      