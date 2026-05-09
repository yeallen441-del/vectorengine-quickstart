# Vector Engine API Quickstart

One OpenAI-compatible API for GPT, Claude, Gemini, Llama, and DeepSeek.

Vector Engine API helps AI builders test chatbots, RAG apps, agents, and side
projects with one API key. If your app already uses the OpenAI SDK, you can
usually switch by changing the `base_url` / `baseURL` and API key.

## 2026-05-09 Builder Promotion

New builders can unlock API credits:

- $5 after email verification
- +$10 after the first successful API call

Start here:
https://www.vectronode.com?aff=nPRB&utm_source=github&utm_medium=repo&utm_campaign=quickstart

## Why Vector Engine API

- Unified access to mainstream LLMs
- OpenAI-compatible `/v1/chat/completions` endpoint
- Quick API key setup
- Usage-based pricing
- Card and USDT payments
- Built for chatbots, RAG apps, and agents

## Quick Start

Set your API key:

```bash
export VECTOR_ENGINE_API_KEY="YOUR_API_KEY"
```

Call the OpenAI-compatible endpoint:

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

## Examples

- [curl](examples/curl.sh)
- [Python requests](examples/python.py)
- [JavaScript fetch](examples/javascript.js)
- [Python OpenAI SDK](examples/openai_sdk_python.py)
- [Node.js OpenAI SDK](examples/openai_sdk_node.mjs)

## OpenAI SDK Compatibility

Use the same SDK shape you already know:

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://www.vectronode.com/v1",
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello from Vector Engine API"}],
)

print(response.choices[0].message.content)
```

## Postman

Import [postman/vector-engine-api.postman_collection.json](postman/vector-engine-api.postman_collection.json),
then set these collection variables:

- `base_url`: `https://www.vectronode.com`
- `api_key`: your Vector Engine API key
- `model`: `gpt-4o-mini`

The collection includes a ready-to-run chat completion request for testing the
API in seconds.
