import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from typing import Dict
class MongoDBModel:
    def __init__ (self
        , DB_name : str
        , collection_name : str
        , uri_name : str =""):
        self.Mongo_uri = os.getenv(uri_name) 
        self.client = MongoClient(self.Mongo_uri, server_api=ServerApi('1'))
        self.client.admin.command('ping')  
        self.collection=self.client[DB_name][collection_name] 
        self.vector_store=None
    
        
    def delete_all_documents(self) -> None: 
        self.collection.delete_many({}) 
        return print(self.collection.count_documents({})) 
    
    def count_number_of_documents(self) -> None: 
        return(self.collection.count_documents({})) 

    def get_all_documents(self) : 
        return list(self.collection.find({"embedding": {"$exists": True}})) 
    

    def set_vector_store(self
        , relevance_scores: str = "dotProduct"
        , index_name: str = "hnsw_index"
        , embedding_model: str = "text-embedding-3-small"
        , api_key_name: str = None
        , model_name: str = None
        , model_kwargs: Dict = {"device": "cpu"}
        , encode_kwargs: Dict = {"normalize_embeddings": True}
        ) -> MongoDBAtlasVectorSearch:
        if api_key_name :
            api_key=os.getenv(api_key_name)
        if embedding_model == "text-embedding-3-small":
            embedding=OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)
        elif embedding_model == "HuggingFaceEmbeddings":
            embedding=HuggingFaceEmbeddings(
                 model_name=model_name
                , model_kwargs=model_kwargs
                , encode_kwargs=encode_kwargs
            )


        # Create a MongoDB Atlas vector search instance
        vector_store = MongoDBAtlasVectorSearch(
            collection=self.collection  # Collection to store embeddings
            ,   embedding=embedding  # Embedding to use
            ,    relevance_score_fn=relevance_scores  # Similarity score function, can also be "euclidean" or "dotProduct"
            ,    index_name=index_name  # Name of the vector search index
            )
        # Set the vector store
        self.vector_store = vector_store
        return vector_store
