from llama_cpp import Llama

llm = Llama.from_pretrained(
	repo_id="Qwen/Qwen2.5-3B-Instruct-GGUF",
	filename="qwen2.5-3b-instruct-q5_k_m.gguf",
)

output = llm.create_chat_completion(
	messages = [
		{
			"role": "user",
			"content": "What is the capital of France?"
		}
	]
)
print(output['choices']['0'])
