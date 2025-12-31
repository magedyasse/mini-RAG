from enum import Enum



class LLMEnums(str, Enum):



 OPENAI = "openai"
 COHERE = "cohere"



class OpenAIEnums(Enum):

      SYSTEM = "system"
      USER = "user"
      ASSISTANT = "assistant"
      



