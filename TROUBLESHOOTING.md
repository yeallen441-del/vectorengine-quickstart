# OpenAI SDK API Relay Troubleshooting

Use this guide when an OpenAI SDK app does not work after switching to Vector
Engine API.

The most common migration problems are configuration problems, not code
problems. Check these items before changing your application logic.

## Quick Checklist

- `base_url` / `baseURL` is `https://www.vectronode.com/v1`
- API key is set as `VECTOR_ENGINE_API_KEY`
- The request uses `Authorization: Bearer YOUR_API_KEY`
- The endpoint is `/v1/chat/completions`
- The model name matches a model available in your account
- The same request works in Postman before it is used in production

## 401 Unauthorized

This usually means the API key is missing, invalid, or not being loaded by the
runtime.

Check Python:

```python
import os

print(bool(os.getenv("VECTOR_ENGINE_API_KEY")))
```

Check Node.js:

```js
console.log(Boolean(process.env.VECTOR_ENGINE_API_KEY));
```

If the value is `False` or `false`, your app is not loading the environment
variable.

## 404 Not Found

This usually means the base URL or endpoint path is wrong.

Use:

```text
https://www.vectronode.com/v1
```

Do not use:

```text
https://www.vectronode.com
https://www.vectronode.com/v1/chat/completions
```

The SDK adds the endpoint path for you. The base URL should stop at `/v1`.

## Model Not Found

If the API returns a model error, try the default test model first:

```text
gpt-4o-mini
```

After the request works, switch to the model you want to use in production.

## Empty or Unexpected Response

Start with a minimal chat request:

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "user",
      "content": "Reply with one short sentence."
    }
  ]
}
```

This removes app-level prompt, tool, streaming, and JSON-schema complexity while
you validate the relay connection.

## Postman Verification

Before changing production code:

1. Import `postman/vector-engine-api.postman_collection.json`.
2. Set `api_key` in the collection variables.
3. Keep `base_url` as `https://www.vectronode.com`.
4. Run `POST Chat Completions`.

If Postman works but your app fails, the issue is probably in your local
environment variables or SDK configuration.

## Known-Good SDK Configuration

Python:

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://www.vectronode.com/v1",
)
```

Node.js:

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "YOUR_API_KEY",
  baseURL: "https://www.vectronode.com/v1",
});
```

Start here:
https://www.vectronode.com?aff=nPRB&utm_source=github&utm_medium=troubleshooting&utm_campaign=integration-update
