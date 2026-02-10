from .BaseDataModel import BaseDataModel
from .db_schemes import  DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
# from pymongo import InsertOne
from sqlalchemy import select , func , delete
from typing import Any, Optional

class ChunkModel(BaseDataModel):

    def __init__(self , db_client: Any) :

        super().__init__(db_client=db_client)
        self.collection = db_client

    @classmethod
    async def create_instance(cls , db_client: Any) :
        instance = cls(db_client=db_client)
        return instance    

    
  


    async def create_data_chunk(self , data_chunk : DataChunk) :

       
        async with self.db_client( ) as session:
            async with session.begin():
                session.add(data_chunk)
            await session.commit()
            await session.refresh(data_chunk)    
                
        return data_chunk


    

    async def get_chunk(self , chunk_id:int) :    
   
        async with self.db_client( ) as session:
            async with session.begin():
                query  = select(DataChunk).where(DataChunk.chunk_id == chunk_id)
                result= query.scalar_one_or_none() # type: ignore
                if result is None :
                    return None

        return DataChunk(**result)


    async def insert_many_chunks(self, data_chunks: list,batch_size: int = 100):
        
        async with self.db_client( ) as session:
            async with session.begin():
                session.add_all(data_chunks)    
            await session.commit()
        return len(data_chunks) 

    async def delete_chunks_by_project_id(self , project_id : ObjectId) :

        async with self.db_client( ) as session:
            async with session.begin():
                query = delete(DataChunk).where(DataChunk.chunk_project_id == project_id)
                result = await session.execute(query)
            await session.commit()

        return result.rowcount  # type: ignoree
    

    
    async def get_project_chunks(self , project_id : ObjectId , page_no : int = 1, page_size: int = 10 )  :

                
        async with self.db_client( ) as session:
            async with session.begin():
                query = select(DataChunk).where(DataChunk.chunk_project_id == project_id).offset((page_no -1) * page_size).limit(page_size)
                result = await session.execute(query)
                records = result.scalars().all()  # type: ignore
        
        return records
            
