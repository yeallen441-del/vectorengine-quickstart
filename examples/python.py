import requests

response = requests.post(
    "https://www.vectronode.com/v1/chat/completions",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": "Hello from Vector Engine API"
            }
        ],
    },
)

print(response.json())
