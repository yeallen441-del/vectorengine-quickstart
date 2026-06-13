import os

import requests

response = requests.post(
    "https://www.vectronode.com/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['VECTORNODE_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": os.environ["VECTORNODE_MODEL"],
        "messages": [
            {
                "role": "user",
                "content": "Hello from VectorNode"
            }
        ],
    },
)

print(response.json())
