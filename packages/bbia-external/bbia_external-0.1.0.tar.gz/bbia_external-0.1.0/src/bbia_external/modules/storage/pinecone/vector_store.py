from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from ....core.conf import settings


class PineconeStoreDB:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    db = Pinecone(settings.PINECONE_API_KEY)
    index = db.Index("bbia-internal")

    @classmethod
    def get_vector_store(cls, tenant_id: str):
        vector = PineconeVectorStore(cls.index, cls.embeddings, namespace=f"tenant-{tenant_id}")

        return vector
