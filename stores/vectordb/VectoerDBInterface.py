from abc import ABC, abstractmethod
from typing import List, Optional, Union, Dict, Any



class VectorDBInterface(ABC):


    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> Optional[bool]:
        pass

    @abstractmethod
    def list_all_collections(self) -> Optional[List[str]]:
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> Optional[dict]:
        pass    

    @abstractmethod
    def create_collection(self, collection_name: str,
                                embedding_size : int  , 
                                do_reset : bool = False) -> Optional[bool]:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> Optional[bool]:
        pass

    @abstractmethod
    def insert_one(self, collection_name: str,
                           text : str,
                           vectoer: List[float],
                           metadata: Optional[dict] = None,
                           record_id : Optional[str] = None) -> Optional[str]:
        pass
        
    @abstractmethod
    def insert_many(self ,  collection_name : str,
                            texts      : list,
                            vectoers   : List,
                            metadatas   : Optional[list] = None,
                            record_ids : Optional[list] = None,
                            batch_size : int = 50) -> Optional[List[str]]:
        pass

    @abstractmethod
    def search_by_vector(self, collection_name: str,
                                vector: List,
                                limit: int = 5,) -> Optional[List[dict]]:
                                            
        pass
 



    @abstractmethod
    def disconnect(self):
        pass