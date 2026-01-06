from .providers.QdrantDBProvider import QdrantDBProvider
from .VectoerDBEnums import VectoerDBEnums
from controllers.BaseController import BaseController

class VectoerDBProvidersFactory:
  


    def __init__(self, config):
      self.config = config
      self.base_controller = BaseController()

    def create(self , provider:str) :
        if provider == VectoerDBEnums.QDRANT.value:
           db_path = self.base_controller.get_database_path(db_name=self.config.VECTOER_DB_PATH)

           return QdrantDBProvider(
                db_path=db_path,
                distance_method=self.config.VECTOER_DB_DISTANCE_METHOD
           )
        return None
       
        

