from qdrant_client import AsyncQdrantClient
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from main_agent.core.config import settings
from typing import Dict, List

class QdrantRAGTool:
    """
    A tool to retrieve documents from a Qdrant vector database using LlamaIndex.
    Returns raw retrieved documents without LLM processing.
    """
    def __init__(self):
        """
        Initializes the Qdrant client, vector store, and the LlamaIndex retriever.
        """
        aclient = AsyncQdrantClient(
            url=settings.QDRANT_URL, 
            api_key=settings.QDRANT_API_KEY
        )
        
        vector_store = QdrantVectorStore(
            aclient=aclient,
            collection_name=settings.QDRANT_COLLECTION_NAME,
        )
        
        # Load the index from the existing vector store
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model=GoogleGenAIEmbedding(model_name="text-embedding-004")
        )

        self.retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=5,
        )
            
    async def retrieve_documents(self, question: str) -> Dict[str, List[str]]:
        """
        Asynchronously retrieves relevant documents from the knowledge base.
        
        Args:
            question: The question to search for in the knowledge base.

        Returns:
            A dictionary containing the list of retrieved document contents.
        """
        nodes = await self.retriever.aretrieve(question)
        
        retrieved_texts = []
        for node in nodes:
            retrieved_texts.append(node.text)
            
        return {"retrieved_documents": retrieved_texts}

# Create a single instance of the RAG tool to be used by the agent
rag_tool_instance = QdrantRAGTool()

async def retrieve_from_collection(question: str) -> Dict[str, List[str]]:
    """
    Function to be used as a tool by the agent.
    
    Args:
        question: The question to search for in the knowledge base.
        
    Returns:
        A dictionary containing retrieved documents.
    """
    return await rag_tool_instance.retrieve_documents(question)  