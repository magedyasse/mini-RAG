from ..VectoerDBInterface import VectorDBInterface
from qdrant_client import QdrantClient
from qdrant_client.http import models
from ..VectoerDBEnums import DistanceMethodEnums
import logging
from typing import List, Optional, Union, Dict, Any


class QdrantDBProvider(VectorDBInterface):


    def __init__(self, db_path: str, distance_method: str):

        self.db_path = db_path
        self.client: Optional[QdrantClient] = None
        self.distance_method: Optional[models.Distance] = None

        # Case-insensitive comparison
        distance_method_lower = distance_method.lower()
        
        if distance_method_lower == DistanceMethodEnums.COSINE.value.lower():
            self.distance_method = models.Distance.COSINE
        elif distance_method_lower == DistanceMethodEnums.DOT.value.lower():
            self.distance_method = models.Distance.DOT
        elif distance_method_lower == DistanceMethodEnums.EUCLIDEAN.value.lower():
            self.distance_method = models.Distance.EUCLID
        elif distance_method_lower == DistanceMethodEnums.MANHATTAN.value.lower():
            self.distance_method = models.Distance.MANHATTAN
        else:
            # Default to COSINE if not recognized
            self.distance_method = models.Distance.COSINE
        
        self.logger = logging.getLogger(__name__)

    def connect(self):
         
         self.client = QdrantClient(path=self.db_path)


    def disconnect(self):
        self.client = None

    def is_collection_exists(self, collection_name: str) -> bool:
        if self.client is None:
            raise RuntimeError("Client not connected. Call connect() first.")
        return self.client.collection_exists(collection_name=collection_name) 
    
    def list_all_collections(self) -> Optional[List[str]]:
        if self.client is None:
            raise RuntimeError("Client not connected. Call connect() first.")
        return self.client.get_collections()
    

    def get_collection_info(self, collection_name: str) -> Optional[dict]:
        if self.client is None:
            raise RuntimeError("Client not connected. Call connect() first.")
        return self.client.get_collection(collection_name=collection_name)
    

    def delete_collection(self, collection_name: str) -> Optional[bool]:

        if self.client is None:
            raise RuntimeError("Client not connected. Call connect() first.")
        
        if not self.is_collection_exists(collection_name):
            self.logger.warning(f"Collection {collection_name} does not exist.")
            return None
        
        return self.client.delete_collection(collection_name)
    

    def create_collection(self,  collection_name: str,
                                 embedding_size: int,
                                 do_reset : bool = False) -> Optional[bool]:

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
                           metadata: Optional[dict] = None,
                           record_id : Optional[str] = None) -> Optional[str]:  # Fixed: Added return type to match interface
       

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
                            metadatas   : Optional[list] = None,
                            record_ids : Optional[list] = None,
                            batch_size : int = 50) -> Optional[List[str]]:  # Fixed: Added return type to match interface
        
        if self.client is None: 
            raise RuntimeError("Client not connected. Call connect() first.")

        if not self.is_collection_exists(collection_name):
              self.logger.error(f"Collection {collection_name} does not exist.")
              return None
        


        if metadatas is None:
            metadatas = [None] * len(texts)

        # Fixed: Generate string IDs instead of None values
        if record_ids is None:
            record_ids = [str(i) for i in range(len(texts))]

        all_inserted_ids: List[str] = []  # Track all inserted record IDs

        for i in range(0, len(texts) , batch_size):
             
          batch_end =  i + batch_size

          batch_texts = texts[i: batch_end]

          batch_vectors = vectoers[i: batch_end]

          batch_metadatas = metadatas[i: batch_end]

          batch_ids = record_ids[i: batch_end]  # Get batch of record IDs

          batch_record = [
              
                models.Record(
                  id=batch_ids[x],  # Fixed: Include record ID
                  vector=batch_vectors[x],
                  payload={
                      "text": batch_texts[x],
                      "metadata": batch_metadatas[x]
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
                                limit: int = 5,) -> Optional[List[dict]]:
        
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
    

         

            

         
          



        

