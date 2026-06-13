# Building Multimodal AI Products with a Model Access Platform

Many AI products start with one chat-completions request. As the product grows,
teams often need more than chat: vision, image generation, speech, video,
embeddings, reranking, tool calling, search, and model fallback.

This guide explains how to plan a multimodal AI access layer without assuming
that every model category uses the same endpoint or request format.

VectorNode is a pay-as-you-go multi-model AI API platform. One account can be
used to test and access hundreds of supported models across text, image, video,
and audio workflows.

Supported text and chat models can use familiar OpenAI-compatible integration
patterns. Image, video, audio, and provider-specific models may use different
endpoints or request formats. Check the current catalog and documentation
before implementing a production workflow.

## Why Multimodal Access Matters

A modern AI app may need different model types for different product features:

- chat and assistant workflows
- vision and image understanding
- image generation and editing
- speech or text-to-speech
- video generation and video understanding
- embeddings and reranking
- search-enabled answers
- agent workflows with tool calls

Using a separate account, balance, and integration for every provider creates
operational overhead. A model access layer keeps product code simpler while
still allowing model choice.

## Start with a Stable API Boundary

Keep product code focused on business logic. Put model access behind a small
service boundary:

```text
app feature -> ai service -> model access client -> selected model
```

This makes it easier to change the model behind a feature without rewriting the
feature itself.

Recommended environment variables:

```bash
export VECTORNODE_API_KEY="YOUR_API_KEY"
export VECTORNODE_BASE_URL="https://www.vectronode.com/v1"
export VECTORNODE_CHAT_MODEL="YOUR_CHAT_MODEL_ID"
export VECTORNODE_VISION_MODEL="YOUR_VISION_MODEL_ID"
export VECTORNODE_MEDIA_MODEL="YOUR_IMAGE_OR_VIDEO_MODEL_ID"
```

## Use One SDK Shape Where Possible

For chat-style and OpenAI-compatible requests, keep the same SDK shape and only
change the base URL, API key, and model name.

Python:

```python
import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ["VECTORNODE_API_KEY"],
    base_url=os.getenv("VECTORNODE_BASE_URL", "https://www.vectronode.com/v1"),
)

response = client.chat.completions.create(
    model=os.environ["VECTORNODE_CHAT_MODEL"],
    messages=[
        {"role": "user", "content": "Summarize this product feedback."}
    ],
    max_tokens=240,
)

print(response.choices[0].message.content)
```

Node.js:

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.VECTORNODE_API_KEY,
  baseURL: process.env.VECTORNODE_BASE_URL || "https://www.vectronode.com/v1",
});

const response = await client.chat.completions.create({
  model: process.env.VECTORNODE_CHAT_MODEL,
  messages: [{ role: "user", content: "Summarize this product feedback." }],
  max_tokens: 240,
});

console.log(response.choices[0].message.content);
```

## Map Product Features to Model Types

Do not choose models only by popularity. Start with product workflows.

Example mapping:

| Product feature | Model type | What to optimize |
| --- | --- | --- |
| customer support chatbot | chat model | reliability and cost |
| screenshot analysis | vision model | visual accuracy |
| marketing image generation | image model | style quality |
| voice output | speech model | latency and voice quality |
| RAG search | embeddings and reranking | relevance |
| developer agent | tool-capable reasoning model | planning and code quality |
| Chinese user workflow | Chinese or bilingual LLM | language quality |

This keeps model choice tied to business value.

## Plan for Global and Chinese Model Coverage

Many teams need both global models and Chinese-language models. Depending on
the current catalog, model families may include:

- GPT, Claude, Gemini, and Grok for global use cases
- DeepSeek, Qwen, Doubao, Moonshot, GLM, Wenxin, and Spark for Chinese-language
  and regional workflows
- supported image, video, and audio model families for media workflows

One platform account makes it easier to test available options side by side.

## Test Pricing and Throughput Before Scaling

A multimodal app can create different cost patterns:

- chat requests are usually token-based
- image requests may be per generation
- video requests may depend on duration or size
- embeddings and reranking may be high-volume background workloads
- premium reasoning models may be expensive for free-tier usage

Before scaling, test:

- input price
- output price
- cache-hit pricing
- per-image or per-video pricing
- concurrency behavior
- fallback behavior
- model availability

## Add Observability Early

Log enough data to understand the system:

- feature name
- model name
- model provider
- request type
- latency
- input tokens
- output tokens
- retry count
- fallback model
- success or error status

This data helps answer practical questions:

- Which features are using the most API spend?
- Which models are slow for real users?
- Which fallback paths are actually being used?
- Which models should be promoted to production defaults?

## Use the Playground Before Integration

Use the VectorNode Playground to confirm that a model fits the workflow before
adding it to application code. Record the exact model ID, route, request format,
response shape, and expected pricing for the selected option.

## Use Postman for OpenAI-Compatible Testing

For supported OpenAI-compatible text and chat models, test requests through
Postman with variables:

```text
base_url = https://www.vectronode.com
api_key = YOUR_VECTORNODE_API_KEY
model = YOUR_MODEL_ID
```

Then change only the model variable to compare model families.

## Start Small, Then Expand

A practical rollout path:

1. Start with one chat model.
2. Add one efficient model for background tasks.
3. Add one vision or multimodal model.
4. Add model routing by feature.
5. Add fallback rules.
6. Add observability and cost reports.
7. Expand into image, audio, video, embeddings, and reranking when the product
   workflow needs them.

## Start Testing

Learn more:

```text
https://www.vectronode.com/
```

Review the current catalog and pricing:

```text
https://www.vectronode.com/pricing
```
