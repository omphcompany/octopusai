from langchain.chat_models import ChatVertexAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from typing import Any, Dict, List

def conversation_chain(vectorstore, query: str, chat_history: List[Dict[str, Any]] = []):
    """
    Generates a conversation chain based on a given query and chat history.

    Args:
        vectorstore (VectorStore): The vector store used for retrieval.
        query (str): The query to generate a conversation chain for.
        chat_history (List[Dict[str, Any]], optional): The chat history to include in the conversation chain. Defaults to [].

    Returns:
        Dict[str, Any]: The generated conversation chain.
    """
    chat = ChatVertexAI(
        verbose=True,
        temperature=0,
        max_output_tokens=1024
    )
    memory = ConversationBufferMemory(memory_key = "chat_history", return_message = True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = chat,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )
    return conversation_chain({"question": query, "chat_history": chat_history})