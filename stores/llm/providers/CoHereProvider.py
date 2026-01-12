from  ..LLMInterFace import LLMInterFace
from  ..LLMEnums import CohereEnums , DocumentTypeEnums
from typing import List, Optional, Union
import cohere
from cohere.types import Message
import logging



class CohereProvider(LLMInterFace):

    def __init__(self, api_key: str , 
                        default_input_max_characters: int = 1000 ,
                        defalut_generation_max_outputtokens: int = 1000,
                        defalut_generation_temperature: float = 0.1,
                        ):
  
            self.api_key = api_key

            self.default_input_max_characters = default_input_max_characters
            self.defalut_generation_max_outputtokens = defalut_generation_max_outputtokens
            self.defalut_generation_temperature = defalut_generation_temperature
          
            self.generation_model_id = None

            self.embedding_model_id = None
            self.embedding_size = None

            self.client = cohere.Client(self.api_key)

            self.logger = logging.getLogger(__name__)


    def set_generation_model(self, model_id: str):
                self.generation_model_id = model_id


    def set_embedding_model(self, model_id: str , embedding_size: int):
                self.embedding_model_id = model_id
                self.embedding_size = embedding_size


    def process_text(self, text: str) -> str:
                return text[:self.default_input_max_characters].strip()      


    def generate_text(self, prompt: str, chat_history: Optional[List[Message]] = None, max_output_tokens: Optional[int] = None, temperature: Optional[float] = None):      # type: ignore

           
            if not self.client :
                self.logger.error("Cohere client is not initialized.")
                return  None
            

            if not self.generation_model_id :
                self.logger.error("Generation model is not set.")
                return  None
            
            temperature = temperature if temperature is not None else self.defalut_generation_temperature
            max_output_tokens = max_output_tokens if max_output_tokens is not None else self.defalut_generation_max_outputtokens
            
            response = self.client.chat(
                    model = self.generation_model_id,
                    chat_history = chat_history,
                    message= self.process_text(prompt),
                    temperature  = temperature,
                    max_tokens = max_output_tokens
            )

            if not response or not response.text:
                self.logger.error("No response from Cohere chat generation.")
                return None
            
            return response.text
    
    def embed_text(self, text: str, document_type: Optional[str] = None) -> Optional[List[float]]:
            

            if not self.client :
                    self.logger.error("Cohere client is not initialized.")
                    return  None
                

            if not self.embedding_model_id :
                    self.logger.error("Embedding model is not set.")
                    return  None
                
            input_text = CohereEnums.DOCUMENT.value if document_type == CohereEnums.DOCUMENT.value else CohereEnums.QUERY.value

            response = self.client.embed(
                    model = self.embedding_model_id,
                    texts = [self.process_text(text)],
                    input_type = input_text,
                    embedding_types= ['float']
            )


            if not response or not response.embeddings:
                    self.logger.error("No embeddings returned from Cohere.")
                    return None
            
            # When using embedding_types=['float'], embeddings is EmbedByTypeResponseEmbeddings
            # Access float embeddings via float_ attribute (underscore because 'float' is reserved)
            float_embeddings = getattr(response.embeddings, 'float_', None)
            
            if not float_embeddings:
                    self.logger.error("No float embeddings returned from Cohere.")
                    return None

            return float_embeddings[0]
           
    def construct_prompt(self, prompt: str, role: str) : # pyright: ignore[reportIncompatibleMethodOverride]
              return {
                    "role": role,  # type: ignore
                    "text": self.process_text(prompt)
               }         