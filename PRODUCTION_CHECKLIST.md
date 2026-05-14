# Production Checklist for an OpenAI-Compatible AI API Gateway

This checklist is for teams moving an AI feature from a local test to real
users with an OpenAI-compatible API gateway.

Vector Engine API lets developers access GPT, Claude, Gemini, DeepSeek, Qwen,
and other model families through one API entry point. The integration is simple,
but production traffic still needs a clear checklist for keys, model routing,
fallbacks, logging, latency, and cost control.

## 1. Keep the SDK Integration Small

If your app already uses the OpenAI SDK, keep the request shape stable and move
provider-specific settings into configuration.

Python:

```python
import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ["VECTOR_ENGINE_API_KEY"],
    base_url=os.getenv("VECTOR_ENGINE_BASE_URL", "https://www.vectronode.com/v1"),
)
```

Node.js:

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.VECTOR_ENGINE_API_KEY,
  baseURL: process.env.VECTOR_ENGINE_BASE_URL ?? "https://www.vectronode.com/v1",
});
```

The goal is to avoid hard-coding API keys, base URLs, and model names in
business logic.

## 2. Define a Default Model and a Backup Model

Production apps should not depend on only one model name.

Start with two environment variables:

```bash
VECTOR_ENGINE_PRIMARY_MODEL="gpt-4o-mini"
VECTOR_ENGINE_FALLBACK_MODEL="deepseek-chat"
```

Use the primary model for normal traffic and keep a fallback model ready for
temporary provider issues, quota limits, or cost-sensitive flows.

Example routing idea:

```python
primary_model = os.getenv("VECTOR_ENGINE_PRIMARY_MODEL", "gpt-4o-mini")
fallback_model = os.getenv("VECTOR_ENGINE_FALLBACK_MODEL", "deepseek-chat")
```

Do not assume the backup model behaves exactly the same. Test prompts, JSON
output, safety behavior, and language quality before using it with users.

## 3. Test Global and Chinese LLMs Separately

For products serving global and Chinese-speaking users, compare model behavior
before picking defaults.

Useful test groups:

- English product support prompts
- Chinese customer-support prompts
- code-generation prompts
- long-context summarization prompts
- RAG answer prompts with citations
- agent planning prompts

Models such as GPT, Claude, Gemini, DeepSeek, Qwen, and other LLMs can differ
in style, latency, output length, and cost. A gateway makes the comparison
easier, but the product team should still evaluate each model by use case.

## 4. Validate with Postman Before Shipping

Before changing production code, run the same request outside your app.

Use the Postman collection in this repository:

```text
postman/vector-engine-api.postman_collection.json
```

Set these variables:

```text
base_url = https://www.vectronode.com
api_key = YOUR_VECTOR_ENGINE_API_KEY
model = gpt-4o-mini
```

If Postman works but your app fails, the issue is usually local configuration:
environment variables, base URL, model name, or request formatting.

## 5. Add Minimal Request Logging

Log enough information to debug production issues without storing sensitive
prompt data by default.

Recommended fields:

- timestamp
- route or feature name
- model name
- request ID if available
- latency
- success or error status
- token usage if available
- user tier or workspace ID, not raw private content

Avoid logging full user prompts unless you have a clear privacy policy and user
permission.

## 6. Track Latency by Feature

Average latency is less useful than feature-level latency.

Track latency separately for:

- chat replies
- background summarization
- RAG answer generation
- agent tool calls
- code-generation requests
- batch jobs

Some features can tolerate slower responses. Others, such as chat and coding
assistants, need faster defaults.

## 7. Set Cost Guardrails

Cost guardrails should exist before traffic grows.

Start with:

- default max output tokens per feature
- stricter limits for free users
- separate limits for batch jobs
- alerts for unusual request volume
- model selection by user tier or feature tier

Use cheaper models for drafts, classification, routing, and internal checks.
Reserve stronger or more expensive models for tasks where quality matters.

## 8. Handle Common Errors Clearly

Map common errors to developer-friendly messages:

| Error | Likely Cause | First Check |
| --- | --- | --- |
| `401 Unauthorized` | Missing or invalid API key | `VECTOR_ENGINE_API_KEY` |
| `404 Not Found` | Wrong base URL | Use `https://www.vectronode.com/v1` |
| model error | Model unavailable or misspelled | Test `gpt-4o-mini` first |
| timeout | Network or model latency | Retry or fallback |
| invalid JSON | Prompt or model output issue | Add validation and retry |

For more details, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## 9. Keep a Small Production Smoke Test

Create one smoke test that runs after deployment:

```bash
curl https://www.vectronode.com/v1/chat/completions \
  -H "Authorization: Bearer $VECTOR_ENGINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {
        "role": "user",
        "content": "Reply with one sentence confirming the API gateway works."
      }
    ],
    "max_tokens": 60
  }'
```

This catches key, base URL, and model-routing problems before users report
them.

## 10. Launch with One Clear Integration Path

For the first production version, keep the setup simple:

1. Use the OpenAI SDK.
2. Set `base_url` / `baseURL` to `https://www.vectronode.com/v1`.
3. Store `VECTOR_ENGINE_API_KEY` in your secret manager.
4. Choose one primary model and one fallback model.
5. Test the same request in Postman.
6. Add latency, error, and usage logging.
7. Watch the first real users closely.

After the first version is stable, add more advanced routing by model quality,
language, cost, or user tier.

## Start Testing

Create an account and test your first API request:

```text
https://www.vectronode.com/register?aff=nPRB&utm_source=github&utm_medium=production-checklist&utm_campaign=developer-seo
```

Compare pricing before sending production traffic:

```text
https://www.vectronode.com/pricing?aff=nPRB&utm_source=github&utm_medium=production-checklist&utm_campaign=developer-seo
```

