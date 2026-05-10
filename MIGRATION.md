# Migrate an OpenAI SDK App to Vector Engine API

This guide is for apps that already use the OpenAI SDK and want to test Vector
Engine API as an OpenAI-compatible relay.

## What changes

Most apps only need two configuration changes:

| Setting | Before | After |
| --- | --- | --- |
| API key | `OPENAI_API_KEY` | `VECTOR_ENGINE_API_KEY` |
| Base URL | OpenAI default | `https://www.vectronode.com/v1` |

The chat-completions request shape can stay the same.

## Python

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["VECTOR_ENGINE_API_KEY"],
    base_url="https://www.vectronode.com/v1",
)

response = client.chat.completions.create(
    model=os.getenv("VECTOR_ENGINE_MODEL", "gpt-4o-mini"),
    messages=[
        {"role": "user", "content": "Test Vector Engine API in one sentence."}
    ],
)

print(response.choices[0].message.content)
```

## Node.js

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.VECTOR_ENGINE_API_KEY,
  baseURL: "https://www.vectronode.com/v1",
});

const response = await client.chat.completions.create({
  model: process.env.VECTOR_ENGINE_MODEL ?? "gpt-4o-mini",
  messages: [
    { role: "user", content: "Test Vector Engine API in one sentence." },
  ],
});

console.log(response.choices[0].message.content);
```

## Environment Variables

Copy `.env.example`, then add your real key:

```bash
VECTOR_ENGINE_API_KEY="YOUR_API_KEY"
VECTOR_ENGINE_MODEL="gpt-4o-mini"
VECTOR_ENGINE_BASE_URL="https://www.vectronode.com/v1"
```

## Verify Before Production

1. Import `postman/vector-engine-api.postman_collection.json` into Postman.
2. Set the collection variable `api_key`.
3. Run `POST /v1/chat/completions`.
4. Move the same `base_url` and API key into your app config.

Start here:
https://www.vectronode.com?aff=nPRB&utm_source=github&utm_medium=migration-guide&utm_campaign=integration-update
