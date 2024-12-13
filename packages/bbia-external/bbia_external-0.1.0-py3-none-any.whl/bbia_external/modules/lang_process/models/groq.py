from langchain_groq import ChatGroq

from ....core.conf import settings

groq_model = ChatGroq(model="llama-3.1-70b-versatile", api_key=settings.GROQ_API_KEY)
