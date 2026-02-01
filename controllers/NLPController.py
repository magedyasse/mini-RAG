from .BaseController import BaseController
from models.ProjectModel import ProjectModel  
from models.ChunkModel import DataChunk
from typing import List
from stores.llm import LLMEnums
import json
# from stores.vectordb import VectorDBInterface


class NLPController(BaseController):

    def __init__(self , vectoerdb_client    , embedding_client  , generation_client ,template_parser) :
        super().__init__()


        self.vectoerdb_client = vectoerdb_client
        self.embedding_client = embedding_client
        self.generation_client = generation_client
        self.template_parser = template_parser

    def   create_collection_name(self , project_id:str) -> str:
        return f"project_{project_id}_collection"  
    

    def reset_vector_db_collection(self , project : ProjectModel) :
        collection_name = self.create_collection_name(project_id =project.project_id) # type: ignore
        
        return self.vectoerdb_client.delete_collection(collection_name=collection_name)

    def  get_vector_db_collection_info(self , project : ProjectModel) :
        collection_name = self.create_collection_name(project_id =project.project_id) # type: ignore
        collection_info = self.vectoerdb_client.get_collection_info(collection_name=collection_name)

        return json.loads(json.dumps(collection_info, default=lambda o: o.__dict__ ))
    

    def index_into_vector_db(self , project : ProjectModel  , chunks: List[DataChunk]  , chunks_ids: List[int] , do_reset : bool =False) :

        # step 1 : create collection if not exists
        collection_name = self.create_collection_name(project_id =project.project_id) # type: ignore

        # step 2 : mange item
        texts = [ chunk.chunk_text  for chunk in chunks ]
        metadatas = [ chunk.chunk_metadata  for chunk in chunks ]
        vectors = [
            self.embedding_client.embed_text(  text=text ,
                                              document_type = LLMEnums.DocumentTypeEnums.DOCUMENT)
            for text in texts
        ]

       #step 3 : create collection if not exists
        _ = self.vectoerdb_client.create_collection(
            collection_name=collection_name,
            embedding_size= self.embedding_client.embedding_size,
            do_reset = do_reset
        )
       

        # step 4 : insert items
        _ =  self.vectoerdb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            vectoers=vectors,
            metadatas=metadatas,
            record_ids= chunks_ids
        )

        return True

    def search_vector_db_collection(self , project : ProjectModel  , query_text: str , top_k : int =10) :



        # step 1  Get collection name
        collection_name = self.create_collection_name(project_id =project.project_id) # type: ignore

        # step 2  get text embedding 
        query_vector = self.embedding_client.embed_text(  text=query_text ,
                                              document_type = LLMEnums.DocumentTypeEnums.QUERY)


        if not query_vector   :  
            return False
        # step 3  search in vector db 
        results = self.vectoerdb_client.search_by_vector(
            collection_name=collection_name,
            vector=query_vector,
            limit=top_k
        )

        if results is None:
            return None
        
        return results
            
    def answer_rag_question(self , project : ProjectModel  , query_text: str , top_k : int =10) : 
        
        answer , full_prompt , chat_history = None , None , None
       
        # step 1 : retrieve related documents
        retrieved_docs = self.search_vector_db_collection(
            project=project,
            query_text=query_text,
            top_k=top_k
        )
        
        if not retrieved_docs or len(retrieved_docs)  == 0 :
            return answer , full_prompt , chat_history
        
        # step 2 : Construct LLM Prompt 
        
        system_prompt = self.template_parser.get("rag" ,"system_prompt")
        
            
        documents_prompts = "\n".join([   
            self.template_parser.get("rag" ,"document_prompt"  ,{
                    "doc_num" : idx + 1 ,
                    "chunk_text" : doc.text
            })               
            for idx, doc in enumerate(retrieved_docs)                
        ])
        
        
        footer_prompt = self.template_parser.get("rag" ,"footer_prompt" ,{
            "query" : query_text
        })
        
        chat_history = [
            
            self.generation_client.construct_prompt(
                prompt = system_prompt ,
                role = self.generation_client.enums.SYSTEM.value,
            )
        ]
        
        full_prompt = "\n\n".join([documents_prompts,footer_prompt])
        
        answer =  self.generation_client.generate_text(
            prompt = full_prompt ,
            chat_history = chat_history
        )
        
        return answer , full_prompt , chat_history
        
        
          
        
        
         