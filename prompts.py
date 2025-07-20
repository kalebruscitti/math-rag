
def template_question_with_context(context: list[str], text: str)->str:
    prompt = "Using the following pieces of context: \n\n"
    for item in context:
        prompt += f"{item}\n"

    prompt += "Please answer the query: \n\n"
    prompt += text
    return prompt