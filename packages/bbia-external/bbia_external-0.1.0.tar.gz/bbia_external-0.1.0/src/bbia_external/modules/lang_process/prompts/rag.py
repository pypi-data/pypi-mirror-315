from langchain.prompts import PromptTemplate

rag_template = """
Você é um assistente para tarefas de perguntas e respostas. 
Use os seguintes trechos de contexto recuperados para responder à pergunta. 
Se você não souber a resposta, apenas diga que não sabe. 
Use no máximo três frases e mantenha a resposta concisa.

Pergunta: {question}

Contexto: {context}

Resposta:
"""

rag_prompt = PromptTemplate.from_template(rag_template)
