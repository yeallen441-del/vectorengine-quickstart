# How to Connect an OpenAI SDK App to Vector Engine API

If your project already uses the OpenAI SDK, you can connect it to Vector Engine
API by changing two things: the API key and the base URL.

Vector Engine API gives builders one OpenAI-compatible API for GPT, Claude,
Gemini, Llama, and DeepSeek, which makes it useful for chatbots, RAG apps,
agents, demos, and side projects that need to test different model families
without rewriting integration code.

## Today’s Builder Promotion

New builders can unlock API credits:

- $5 after email verification
- +$10 after the first successful API call

Start here:
https://www.vectronode.com?aff=nPRB&utm_source=hashnode&utm_medium=article&utm_campaign=quickstart

## Why Use an API Relay?

An API relay is useful when you want:

- One API key for multiple model providers
- OpenAI-compatible request and response formats
- A faster way to test models in the same app
- Usage-based billing with card and USDT payment options
- A quick setup for chatbots, RAG apps, and agents

## Python Example

Install the SDK:

```bash
pip install openai
```

Set your key:

```bash
export VECTOR_ENGINE_API_KEY="YOUR_API_KEY"
```

Call the API:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["VECTOR_ENGINE_API_KEY"],
    base_url="https://www.vectronode.com/v1",
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Explain API relays in one sentence.",
        }
    ],
)

print(response.choices[0].message.content)
```

## Node.js Example

Install the SDK:

```bash
npm install openai
```

Set your key:

```bash
export VECTOR_ENGINE_API_KEY="YOUR_API_KEY"
```

Call the API:

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.VECTOR_ENGINE_API_KEY,
  baseURL: "https://www.vectronode.com/v1",
});

const response = await client.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [
    {
      role: "user",
      content: "Explain API relays in one sentence.",
    },
  ],
});

console.log(response.choices[0].message.content);
```

## curl Test

```bash
curl https://www.vectronode.com/v1/chat/completions \
  -H "Authorization: Bearer $VECTOR_ENGINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {
        "role": "user",
        "content": "Hello from Vector Engine API"
      }
    ]
  }'
```

## Postman Test

If you prefer testing without writing code, create a Postman request:

- Method: `POST`
- URL: `https://www.vectronode.com/v1/chat/completions`
- Header: `Authorization: Bearer YOUR_API_KEY`
- Header: `Content-Type: application/json`

Body:

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "user",
      "content": "Hello from Vector Engine API"
    }
  ]
}
```

## Final Notes

Vector Engine API is designed for builders who want to move quickly: one key,
OpenAI-compatible endpoints, and access to multiple model families from one
integration.

Start here:
https://www.vectronode.com?aff=nPRB&utm_source=hashnode&utm_medium=article&utm_campaign=quickstart
