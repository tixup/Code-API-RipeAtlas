import requests

# 1. Carica il contesto dal file txt (circa 3K Token)
with open("ripe_atlas_basics.txt", "r") as f:
    ripe_context = f.read()

# 2. Query in linguaggio naturale
user_query = "Hi, what's up? "

# 3. Costruisci il messaggio per la chat (stato mantenuto)
chat_payload = {
    "model": "deepseek-coder:6.7b",
    "messages": [
        {
            "role": "system",       # usato per passare documentazione
            "content": ripe_context
        },
        {
            "role": "user",         # usato per passare quey
            "content": user_query
        }
    ],
    "stream": False,
    "options": {                    # inserito per limitare 'hallucination'
        "max_tokens": 1000,
}

}

# 4. Invia la richiesta all'API REST di Ollama
response = requests.post("http://localhost:11434/api/chat", json=chat_payload)

# 5. Stampa il risultato
if response.status_code == 200:
    print("\nLLM Response:\n")
    print(response.json()["message"]["content"])
else:
    print(f"Errore: {response.status_code}\n{response.text}")
