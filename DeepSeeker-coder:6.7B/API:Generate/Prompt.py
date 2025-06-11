import requests

prompt = """ Hi, what's up? """

response = requests.post("http://localhost:11434/api/generate", json={
    "model": "deepseek-coder:6.7b",    # inserire modello scelto
    "prompt": prompt,
    "stream": False
})

print(response.json()["response"])
