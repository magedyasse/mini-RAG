
from abc import ABC, abstractmethod
from openai.types.chat import ChatCompletionMessageParam

class LLMInterFace(ABC):


    @abstractmethod
    def set_generation_model(self, model_id: str):
        pass


    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass


    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list[str], max_output_tokens: int | None = None, temperature: float | None = None):
        pass

    @abstractmethod 
    def embed_text(self, text: str, document_type: str | None = None) -> list[float] | None:
        pass

    @abstractmethod
    def construct_prompt(self, prompt :str  , role: str)  :
        pass




