import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_answer(question: str, context: str):

    prompt = f"""
You are a document-grounded AI assistant.

Use ONLY the information contained in the context.
say:

"I cannot find this information in the document."

Context:
{context}

Question:
{question}

Answer based only on the context.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]