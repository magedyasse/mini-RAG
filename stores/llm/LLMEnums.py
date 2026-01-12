from enum import Enum



class LLMEnums(str, Enum):

 OPENAI = "OPENAI"
 COHERE = "COHERE"



class OpenAIEnums(Enum):

      SYSTEM = "system"
      USER = "user"
      ASSISTANT = "assistant"
      

class CohereEnums(Enum):
      SYSTEM = "SYSTEM"
      USER= "USER"
      ASSISTANT = "ASSISTANT"

      DOCUMENT = "search_document"
      QUERY = "search_query"


class DocumentTypeEnums(Enum):
      DOCUMENT = "document"
      QUERY = "query"
      TEXT = "text"
      PDF = "pdf"
      WORD = "word"
      MARKDOWN = "markdown"
      HTML = "html"
