from ..VectoerDBInterface import VectorDBInterface
from qdrant_client import QdrantClient, models # type: ignore
from ..VectoerDBEnums import DistanceMethodEnums
import logging
from typing import List, Optional




class QdrantDBProvider(VectorDBInterface):


    def __init__(self, db_path: str, distance_method: str):

        self.db_path = db_path
        self.client: Optional[QdrantClient] = None
        self.distance_method: Optional[models.Distance] = None

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT 
        
        self.logger = logging.getLogger(__name__)

    def connect(self):
         
         self.client = QdrantClient(path=self.db_path)


    def disconnect(self):
        self.client = None

    def is_collection_exists(self, collection_name: str) -> bool:
        if self.client is None:
            raise RuntimeError("Client not connected. Call connect() first.")
        return self.client.collection_exists(collection_name=collection_name) 
    
    def list_all_collections(self) -> list[str] | None:
        if self.client is None:
            raise RuntimeError("Client not connected. Call connect() first.")
        return self.client.get_collections()
    

    def get_collection_info(self, collection_name: str) -> dict | None:
        if self.client is None:
            raise RuntimeError("Client not connected. Call connect() first.")
        return self.client.get_collection_info(collection_name)
    

    def delete_collection(self, collection_name: str) -> bool | None:

        if self.client is None:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        if not self.is_collection_exists(collection_name):
            self.logger.warning(f"Collection {collection_name} does not exist.")
            return None
        
        return self.client.delete_collection(collection_name)
    

    def create_collection(self,  collection_name: str,
                                 embedding_size: int,
                                 do_reset : bool = False) -> bool | None:

        if self.client is None:
            raise RuntimeError("Client not connected. Call connect() first.")

        if do_reset :
           _ = self.delete_collection(collection_name=collection_name)

        if not self.is_collection_exists(collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                        size=embedding_size,
                        distance=self.distance_method
                )
            )
            return True
        return False
    
    def insert_one(self, collection_name: str,
                           text : str,
                           vectoer: List[float],
                           metadata: dict | None = None,
                           record_id : str | None = None) -> str | None:  # Fixed: Added return type to match interface
       

        if self.client is None:
            raise RuntimeError("Client not connected. Call connect() first.")
        

        if not self.is_collection_exists(collection_name):
           self.logger.error(f"Collection {collection_name} does not exist.")
           return None
           
        # Fixed: Generate record ID if not provided
        if record_id is None:
            import uuid
            record_id = str(uuid.uuid4())
            
        try:
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=record_id,
                        vector=vectoer,
                        payload={
                            "text": text,
                            "metadata": metadata
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error inserting record: {e}")
            return None    
        
        return record_id  # Fixed: Return the record ID instead of True


    def insert_many(self ,  collection_name : str,
                            texts      : list,
                            vectoers   : List,
                            metadata   : list | None = None,
                            record_ids : list | None = None,
                            batch_size : int = 50) -> List[str] | None:  # Fixed: Added return type to match interface
        
        if self.client is None: 
            raise RuntimeError("Client not connected. Call connect() first.")

        if not self.is_collection_exists(collection_name):
              self.logger.error(f"Collection {collection_name} does not exist.")
              return None
        


        if metadata is None:
            metadata = [None] * len(texts)

        # Fixed: Generate string IDs instead of None values
        if record_ids is None:
            record_ids = [str(i) for i in range(len(texts))]

        all_inserted_ids: List[str] = []  # Track all inserted record IDs

        for i in range(0, len(texts) , batch_size):
             
          batch_end =  i + batch_size

          batch_texts = texts[i: batch_end]

          batch_vectors = vectoers[i: batch_end]

          batch_metadata = metadata[i: batch_end]

          batch_ids = record_ids[i: batch_end]  # Get batch of record IDs

          batch_record = [
              
                models.Record(
                  id=batch_ids[x],  # Fixed: Include record ID
                  vector=batch_vectors[x],
                  payload={
                      "text": batch_texts[x],
                      "metadata": batch_metadata[x]
                  },
                ) 

              for x in range (len(batch_texts)) 

          ] 

          try: 
             _ = self.client.upload_records(
                collection_name=collection_name,
                records=batch_record
            )
             all_inserted_ids.extend(batch_ids)  # Add successful batch IDs

          except Exception as e:
                self.logger.error(f"Error inserting batch starting at index {i}: {e}")
                return None
        

        return all_inserted_ids  # Fixed: Return list of IDs instead of True    
    
    def search_by_vector(self, collection_name: str,
                                vector: List,
                                limit: int = 5,) -> List[dict] | None:
        
        # Added proper error handling and null checks                                      
        if self.client is None:
            raise RuntimeError("Client not connected. Call connect() first.")
            
        if not self.is_collection_exists(collection_name):
            self.logger.error(f"Collection {collection_name} does not exist.")
            return None
            
        try:
            return self.client.search(
                collection_name=collection_name,
                query_vector=vector,
                limit=limit
            )
        except Exception as e:
            self.logger.error(f"Error searching in collection {collection_name}: {e}")
            return None
    

         

            

         
          



        

