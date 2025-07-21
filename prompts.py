
def template_question_with_context(context: list[str], text: str)->str:
    prompt = "Using the following pieces of context: \n\n"
    for item in context:
        prompt += f"{item}\n"

    prompt += "Please answer the query: \n\n"
    prompt += text
    return prompt

def template_generate_rag_queries(text: str)->list[str]:
    rag_prompt_header = """Convert the following query into a JSON list of strings 
    to be submitted to a vector database for retrieval-augmented generation (RAG):\n\n"""
    prompt = rag_prompt_header + text
    return rag_prompt_header