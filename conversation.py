from ollama import chat
from ollama import ChatResponse
from pydantic import BaseModel
from prompts import *
import vector_database as vdb

class Conversation():
    def __init__(self):
        self.history = ""
        
class RAGQueries(BaseModel):
    queries: list[str]
    
def generate_rag_queries(text: str)->list[str]:
    print("Generating RAG Queries...")
    response: ChatResponse = chat(model='gemma3:4b', messages=[
     {
       'role': 'user',
       'content': template_generate_rag_queries(text)
     }],
     format=RAGQueries.model_json_schema()
    )
    queries = RAGQueries.model_validate_json(response.message.content)
    return queries.queries

def retrieve_from_database(queries: list[str])->list[str]:
    results = vdb.collection.query(
        query_texts=queries,
        n_results=5,
    )
    return results['documents']

def answer_question(text: str)->None:
    queries = generate_rag_queries(text)
    results = retrieve_from_database(queries)
    prompt = template_question_with_context(results, text)
    stream = chat(model='gemma3:4b',
        messages=[{
            'role': 'user',
            'content': prompt
        }],
        stream=True
    )
    #for chunk in stream:
    #    print(chunk['message']['content'], end='', flush=True)
    return stream