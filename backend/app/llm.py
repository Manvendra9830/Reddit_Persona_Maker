import os
import ollama
from groq import Groq

class LLM:
    def __init__(self, model_name: str = "llama3-8b-8192"):
        self.model_name = model_name
        self.llm_provider = os.getenv("LLM_PROVIDER", "groq")  # Default to groq

    def get_response(self, prompt: str) -> str:
        if self.llm_provider == "ollama":
            return self._get_ollama_response(prompt)
        else:
            return self._get_groq_response(prompt)

    def _get_ollama_response(self, prompt: str) -> str:
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.7, "top_p": 0.9, "max_tokens": 4096},
            )
            return response["message"]["content"]
        except Exception as e:
            print(f"Error getting Ollama response: {e}")
            raise

    def _get_groq_response(self, prompt: str) -> str:
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Error getting Groq response: {e}")
            raise
