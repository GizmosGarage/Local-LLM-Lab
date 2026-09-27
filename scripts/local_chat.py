import requests

url = "http://127.0.0.1:8080/v1/chat/completions"

prompt = input("You: ")

data = {
    "model": "qwen3-4b",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "temperature": 0.2,
    "max_tokens": 300,
    "chat_template_kwargs": {
        "enable_thinking": False
    }
}

response = requests.post(url, json=data)

response.raise_for_status()

result = response.json()

answer = result["choices"][0]["message"]["content"]

print("\nQwen:", answer)