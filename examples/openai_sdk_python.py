import os

from openai import OpenAI


client = OpenAI(
    api_key=os.environ["VECTORNODE_API_KEY"],
    base_url=os.getenv("VECTORNODE_BASE_URL", "https://www.vectronode.com/v1"),
)

response = client.chat.completions.create(
    model=os.environ["VECTORNODE_MODEL"],
    messages=[
        {
            "role": "user",
            "content": "Write one sentence about building with VectorNode.",
        }
    ],
)

print(response.choices[0].message.content)
