# Vector Engine API Quickstart

One OpenAI-compatible API for GPT, Claude, Gemini, Llama, and DeepSeek.

Vector Engine API helps AI builders test chatbots, RAG apps, agents, and side
projects with one API key. If your app already uses the OpenAI SDK, you can
usually switch by changing the `base_url` / `baseURL` and API key.

## 2026-05-09 Integration Update

Today's update adds a cleaner quickstart path for builders who want to test an
OpenAI-compatible API relay without changing application logic:

- OpenAI SDK examples for Python and Node.js
- Environment-variable based examples for curl, Python, and JavaScript
- A Postman collection with ready-to-run variables
- A short migration path for apps that already use `base_url` / `baseURL`

Start here:
https://www.vectronode.com?aff=nPRB&utm_source=github&utm_medium=repo&utm_campaign=integration-update

## 2026-05-11 Troubleshooting Update

Today's GitHub update is for developers who are already testing an API relay and
need fast answers when something fails:

- [OpenAI SDK migration troubleshooting](TROUBLESHOOTING.md)
- `401 Unauthorized` API key checks
- `404 Not Found` base URL checks
- `model not found` model-name checks
- Postman verification before changing production code

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

## Migration Guide

Already using the OpenAI SDK? See [MIGRATION.md](MIGRATION.md) for the
copy-paste checklist:

- keep your existing chat-completions code shape
- switch `base_url` / `baseURL` to `https://www.vectronode.com/v1`
- replace the API key with `VECTOR_ENGINE_API_KEY`
- test the same request in Postman before changing production code

If a migrated request fails, use [TROUBLESHOOTING.md](TROUBLESHOOTING.md) to
check the most common setup issues first.

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
