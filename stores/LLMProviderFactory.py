from .LLMEnums import LLMEnums
from .llm.providers import CohereProvider ,OpenAIProvider


class LLMProviderFactory:


    def __init__(self, config):

        self.config = config


    def create_provider(self, provider_type: str ):
        
        if provider_type == LLMEnums.OPENAI.value:

          return OpenAIProvider(
              api_key =    self.config.OPENAI_API_KEY     ,
              api_url= self.config.OPENAI_API_URL ,
              default_input_max_characters = self.config.INPUT_DAFAULT_MAX_CHARACTERS ,
              defalut_generation_max_outputtokens = self.config.GENERATION_DAFAULT_MAX_TOKENS ,
              defalut_generation_temperature = self.config.GENERATION_DAFAULT_TEMPERATURE ,   
            )         
                           
           

        if provider_type == LLMEnums.COHERE.value:
            return CohereProvider(
                api_key =    self.config.COHERE_API_KEY     ,
                default_input_max_characters = self.config.INPUT_DAFAULT_MAX_CHARACTERS ,
                defalut_generation_max_outputtokens = self.config.GENERATION_DAFAULT_MAX_TOKENS ,
                defalut_generation_temperature = self.config.GENERATION_DAFAULT_TEMPERATURE ,   
                )
        
        return None
            
        
        