from qdrant_client import AsyncQdrantClient
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from typing import Dict, List
import logging
from main_agent.core.config import settings

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
            api_key=settings.QDRANT_API_KEY,
            timeout=15.0,
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
            similarity_top_k=2,
        )
            
    async def retrieve_documents(self, question: str) -> Dict[str, List[str]]:
        """
        Asynchronously retrieves relevant documents from the knowledge base.
        Includes basic error handling for network issues.

        Args:
            question: The question to search for in the knowledge base.

        Returns:
            A dictionary containing the list of retrieved document contents,
            or an error message if retrieval fails.
        """
        try:
            logging.info(f"Retrieving documents for question: {question[:50]}...")
            nodes = await self.retriever.aretrieve(question)
            retrieved_texts = [node.text for node in nodes]
            logging.info(f"Successfully retrieved {len(retrieved_texts)} documents.")
            return {"retrieved_documents": retrieved_texts}
        except Exception as e:
            # Catch potential exceptions (like timeouts) and return a structured error
            # that the agent can understand.
            error_message = f"Failed to retrieve documents from the knowledge base. Error: {str(e)}"
            logging.error(error_message)
            return {"retrieved_documents": [f"Error: {error_message}"]}


# Create a single instance of the RAG tool to be used by the agent
rag_tool_instance = QdrantRAGTool()

async def retrieve_from_collection(question: str) -> Dict[str, List[str]]:
    """
    Function to be used as a tool by the agent to retrieve relevant sections from
    the UAE School Inspection Framework documentation.

    Args:
        question: A specific query or finding to look up in the framework.

    Returns:
        A dictionary containing retrieved document snippets from the framework.
    """
    return await rag_tool_instance.retrieve_documents(question) 