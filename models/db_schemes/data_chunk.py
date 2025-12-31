from pydantic import BaseModel, Field , validator
from typing import Optional 
from bson.objectid import ObjectId

class DataChunk (BaseModel):

    id : Optional[ObjectId] = Field(None , alias="_id")

    chunk_text : str = Field(... , min_length=1)
    chunk_metadata : dict 
    chunk_order : int = Field(... , gt=0)
    chunk_project_id : ObjectId # Optional[ObjectId]
    chunk_asset_id : ObjectId  #  [ObjectId] = None


    class Config:
        # use this to allow ObjectId type
        arbitrary_types_allowed = True


    @classmethod
    def get_indexes(cls):

        return [
            {
                "key": [

                    ("chunk_project_id", 1),
                    
                ],
                "name": "chunk_project_id_1",
                "unique": False
            }
        ]    

        