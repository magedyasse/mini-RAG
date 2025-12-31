from pydantic import BaseModel 
from typing import Optional


class  ProcessRequest(BaseModel):


    # project_id: str

    file_id: str  = ""

    chunk_size: int = 100  

    overlap_size: int = 20

    do_reset : int = 0 

