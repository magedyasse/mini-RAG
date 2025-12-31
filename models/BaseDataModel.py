from helper.config import get_settings , Settings
from typing import Any



class BaseDataModel:

    def __init__(self , db_client: Any) :

        self.db_client = db_client 
        self.app_settings = get_settings()
        
