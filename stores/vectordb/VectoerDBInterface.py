from abc import ABC, abstractmethod
from typing import List



class VectorDBInterface(ABC):


    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> bool | None:
        pass

    @abstractmethod
    def list_all_collections(self) -> List[str] | None:
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict  | None:
        pass    

    @abstractmethod
    def create_collection(self, collection_name: str,
                                embedding_size : int  , 
                                do_reset : bool = False) -> bool | None:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) -> bool   | None:
        pass

    @abstractmethod
    def insert_one(self, collection_name: str,
                           text : str,
                           vectoer: List[float],
                           metadata: dict | None = None,
                           record_id : str | None = None) -> str | None:
        pass
        
    @abstractmethod
    def insert_many(self ,  collection_name : str,
                            texts      : list,
                            vectoers   : List,
                            metadata   : list | None = None,
                            record_ids : list | None = None,
                            batch_size : int = 50) -> List[str] | None:
        pass

    @abstractmethod
    def search_by_vector(self, collection_name: str,
                                vector: List,
                                limit: int = 5,) -> List[dict] | None:
                                            
        pass
 



    @abstractmethod
    def disconnect(self):
        pass