from .BaseDataModel import BaseDataModel
from .db_schemes import  DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDataModel):

    def __init__(self , db_client:object) :

        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_data_chunk(self , data_chunk : DataChunk) :

        result  = await self.collection.insert_one(data_chunk.dict(by_alias=True, exclude_unset=True))
        data_chunk.id = result.inserted_id
                
        return data_chunk


    async def get_chunk(self , chunk_id:str) :    

        result = await self.collection.find_one(
            {
                "_id": ObjectId(chunk_id) 
            }
        )  

        if result is None :
            return None

        return DataChunk(**result)


    async def insert_many_chunks(self, data_chunks: list,batch_size: int = 100):
        
        
        for i in range(0 , len(data_chunks) , batch_size):
            batch = data_chunks[i : i + batch_size]

            operations = [
                InsertOne(chunk.dict(by_alias=True, exclude_unset=True)) 
                for chunk in batch
            ]

            await self.collection.bulk_write(operations)

        # Fixed: return was inside the for loop, causing early exit after first batch
        return len(data_chunks) 

    async def delete_chunks_by_project_id(self , project_id : ObjectId) :

        result = await self.collection.delete_many(
            {
                "chunk_project_id" : project_id
            }
        )

        return result.deleted_count



            
