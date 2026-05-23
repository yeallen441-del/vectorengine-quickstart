# AI API Integration Testing Checklist

When a product uses GPT, Claude, Gemini, DeepSeek, Qwen, or other LLMs through
one API gateway, the first successful request is only the beginning. Teams also
need to test authentication, model names, latency, fallback behavior, structured
output, and SDK compatibility before sending production traffic.

This checklist is designed for developers using an OpenAI-compatible API
gateway such as VectorNode AI.

## 1. Test the Base URL First

Most migration issues come from the base URL, not the application logic.

Recommended setup:

```bash
export VECTOR_ENGINE_API_KEY="YOUR_API_KEY"
export VECTOR_ENGINE_BASE_URL="https://www.vectronode.com/v1"
export VECTOR_ENGINE_MODEL="gpt-4o-mini"
```

If your current app already uses the OpenAI SDK, keep the request shape and
change only:

- the API key
- the `base_url` or `baseURL`
- the model name

## 2. Verify Authentication

Before testing many models, confirm that one simple request works.

```bash
curl https://www.vectronode.com/v1/chat/completions \
  -H "Authorization: Bearer $VECTOR_ENGINE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {
        "role": "user",
        "content": "Reply with one short sentence."
      }
    ],
    "max_tokens": 80
  }'
```

If this fails, debug the key, base URL, and account status before changing
application code.

## 3. Test SDK Compatibility

Python example:

```python
import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ["VECTOR_ENGINE_API_KEY"],
    base_url=os.getenv("VECTOR_ENGINE_BASE_URL", "https://www.vectronode.com/v1"),
)

response = client.chat.completions.create(
    model=os.getenv("VECTOR_ENGINE_MODEL", "gpt-4o-mini"),
    messages=[{"role": "user", "content": "Explain API gateway testing."}],
    max_tokens=160,
)

print(response.choices[0].message.content)
```

Node.js example:

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.VECTOR_ENGINE_API_KEY,
  baseURL: process.env.VECTOR_ENGINE_BASE_URL || "https://www.vectronode.com/v1",
});

const response = await client.chat.completions.create({
  model: process.env.VECTOR_ENGINE_MODEL || "gpt-4o-mini",
  messages: [{ role: "user", content: "Explain API gateway testing." }],
  max_tokens: 160,
});

console.log(response.choices[0].message.content);
```

## 4. Compare More Than One Model

Do not choose a production default from one model test. Run the same prompt set
against several model families:

- GPT for general-purpose quality
- Claude for long-form reasoning and writing
- Gemini for Google ecosystem and multimodal use cases
- DeepSeek for cost-sensitive reasoning and coding tasks
- Qwen or other Chinese LLMs for Chinese-language workflows

Use the same prompts, token limits, and evaluation criteria for each model.

## 5. Check Structured Output

Many production apps depend on JSON. Test structured output separately from
normal chat replies.

Example prompt:

```text
Return valid JSON only:
{
  "intent": "billing|support|sales|unknown",
  "priority": "low|medium|high",
  "summary": "one short sentence"
}
```

Validate:

- the response parses as JSON
- required fields exist
- enum values are stable
- fallback behavior is defined when parsing fails

## 6. Test Latency and Retry Behavior

For each important feature, log:

- model name
- request duration
- success or error status
- retry count
- token usage
- feature name

Test both normal traffic and failure cases. A good gateway integration should
define what happens when a model is slow, temporarily unavailable, or too costly
for a low-value task.

## 7. Use Postman Before Production

Use the Postman collection in this repository to test requests outside your
application first:

```text
postman/vector-engine-api.postman_collection.json
```

Recommended variables:

```text
base_url = https://www.vectronode.com
api_key = YOUR_VECTOR_ENGINE_API_KEY
model = gpt-4o-mini
```

Then change only the `model` variable to compare GPT, Claude, Gemini,
DeepSeek, Qwen, and other models.

## 8. Prepare a Production Checklist

Before release, confirm:

- API keys are stored in environment variables
- billing and usage limits are understood
- default and fallback models are configured
- logs include model, latency, tokens, and errors
- prompt and response privacy rules are documented
- Postman and SDK tests both pass
- the registration and pricing pages are easy for users to find

## Start Testing

Create an account:

```text
https://www.vectronode.com/register?aff=nPRB&utm_source=github&utm_medium=testing-checklist&utm_campaign=developer-seo
```

Compare pricing:

```text
https://www.vectronode.com/pricing?aff=nPRB&utm_source=github&utm_medium=testing-checklist&utm_campaign=developer-seo
```

Read the API docs:

```text
https://www.vectronode.com?aff=nPRB&utm_source=github&utm_medium=testing-checklist&utm_campaign=developer-seo
```
