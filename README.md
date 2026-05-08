# Vector Engine API Quickstart

One API for GPT, Claude, Gemini, Llama, and DeepSeek.

Vector Engine API helps AI builders test chatbots, RAG apps, agents, and side projects with one API key.

## Why Vector Engine API

- Unified access to mainstream LLMs
- Quick API key setup
- Usage-based pricing
- Card and USDT payments
- Built for chatbots, RAG apps, and agents

## New Builder Credits

New builders can unlock API credits:

- $5 after email verification
- +$10 after the first successful API call

Start here:
https://www.vectronode.com?aff=nPRB&utm_source=github&utm_medium=repo&utm_campaign=quickstart

## Example Request

```bash
curl https://www.vectronode.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
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
