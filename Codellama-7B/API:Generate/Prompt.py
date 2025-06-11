import requests

prompt = """ Hi, what's up? """

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "codellama",
    "prompt": prompt,
    "stream": False
})

print(response.json()["response"])
