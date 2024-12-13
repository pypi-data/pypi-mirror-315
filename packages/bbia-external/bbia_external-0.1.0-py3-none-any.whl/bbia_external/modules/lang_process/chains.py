from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from ..storage.pinecone.vector_store import PineconeStoreDB
from .models.groq import groq_model
from .prompts.rag import rag_prompt

vector_store = PineconeStoreDB.get_vector_store("6712ddd64176bd1107b3098cf")

retriever = vector_store.as_retriever()

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | groq_model
    | StrOutputParser()
)
