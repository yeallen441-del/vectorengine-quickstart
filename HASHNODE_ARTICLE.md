# Migrating an OpenAI SDK App to an API Relay

Yesterday's post covered the basic Vector Engine API offer. Today's note is
more practical: how to move an existing OpenAI SDK integration to an
OpenAI-compatible API relay with the smallest possible code change.

The useful part is that most apps already have the right abstraction. If your
code uses the OpenAI SDK, you usually only need to change the API key and the
base URL.

## What Changes

In a direct OpenAI setup, the SDK sends requests to the default OpenAI endpoint.
With Vector Engine API, you keep the same SDK shape and point it at:

```text
https://www.vectronode.com/v1
```

That means your existing chat completion flow can stay familiar:

- Same `messages` array
- Same `model` field
- Same `chat.completions.create` call
- Same environment-variable based deployment pattern

## Python Migration

Before:

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_KEY")
```

After:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["VECTOR_ENGINE_API_KEY"],
    base_url="https://www.vectronode.com/v1",
)
```

Then keep the request shape the same:

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Explain API relay migration in one sentence.",
        }
    ],
)

print(response.choices[0].message.content)
```

## Node.js Migration

Before:

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});
```

After:

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.VECTOR_ENGINE_API_KEY,
  baseURL: "https://www.vectronode.com/v1",
});
```

Then call chat completions as usual:

```js
const response = await client.chat.completions.create({
  model: "gpt-4o-mini",
  messages: [
    {
      role: "user",
      content: "Explain API relay migration in one sentence.",
    },
  ],
});

console.log(response.choices[0].message.content);
```

## Validate with curl

Before changing a production app, verify the key and endpoint with curl:

```bash
curl https://www.vectronode.com/v1/chat/completions \
  -H "Authorization: Bearer $VECTOR_ENGINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {
        "role": "user",
        "content": "Reply with a short integration check message."
      }
    ]
  }'
```

## Validate with Postman

I also prepared a Postman collection for quick testing. Set these variables:

- `base_url`: `https://www.vectronode.com`
- `api_key`: your Vector Engine API key
- `model`: `gpt-4o-mini`

Then run the `Chat Completions` request. This is a simple way to confirm that
your key, model, and endpoint are working before you wire the relay into an app.

## When This Is Useful

This migration pattern is useful for:

- Chatbot demos
- RAG prototypes
- Agent experiments
- Multi-model testing
- Apps that already use OpenAI-compatible request formats

Start here:
https://www.vectronode.com?aff=nPRB&utm_source=hashnode&utm_medium=article&utm_campaign=integration-update
