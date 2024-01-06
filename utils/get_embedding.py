from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import FAISS

def get_vector_store(text_chunks):
    """
    Generate a vector store from a list of text chunks.

    Args:
        text_chunks (list): A list of text chunks.

    Returns:
        vectorstore: A vector store generated from the text chunks.
    """
    embeddings = VertexAIEmbeddings()
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding = embeddings)
    return vectorstore


