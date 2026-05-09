import os

from openai import OpenAI


client = OpenAI(
    api_key=os.environ["VECTOR_ENGINE_API_KEY"],
    base_url="https://www.vectronode.com/v1",
)

response = client.chat.completions.create(
    model=os.getenv("VECTOR_ENGINE_MODEL", "gpt-4o-mini"),
    messages=[
        {
            "role": "user",
            "content": "Write one sentence about building with Vector Engine API.",
        }
    ],
)

print(response.choices[0].message.content)
