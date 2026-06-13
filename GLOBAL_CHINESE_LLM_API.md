# Global and Chinese LLM API Gateway

VectorNode is a pay-as-you-go AI model access platform for developers who want
to test and access global and Chinese LLMs from one account.

This guide focuses on model selection, testing strategy, and common product
use cases. For supported OpenAI-compatible models, existing OpenAI SDK users
can keep a familiar SDK shape and point it at the VectorNode base URL.

## Why Use One Gateway

AI products often need more than one model:

- GPT for general reasoning and product assistants
- Claude for long-context writing and analysis
- Gemini for multimodal and Google ecosystem workflows
- DeepSeek for cost-sensitive reasoning and coding use cases
- Qwen or other Chinese LLMs for Chinese-language products and local market
  testing

Managing each provider separately can add extra API keys, billing flows, SDK
differences, and model-name checks. A single gateway keeps the integration
surface smaller while still letting teams compare model quality.

## Endpoint

Use the OpenAI-compatible chat completions endpoint:

```text
https://www.vectronode.com/v1/chat/completions
```

For SDK clients, use this base URL:

```text
https://www.vectronode.com/v1
```

## Model Testing Checklist

Before wiring a model into production, test these items:

1. The model name is available in your VectorNode account.
2. The request works in Postman or curl.
3. The same request works in your application SDK.
4. The response quality fits the use case.
5. The cost fits your expected traffic.

This is especially useful when comparing GPT, Claude, Gemini, DeepSeek, Qwen,
and other LLMs for the same prompt.

## Python Example

```python
import os

from openai import OpenAI


client = OpenAI(
    api_key=os.environ["VECTORNODE_API_KEY"],
    base_url="https://www.vectronode.com/v1",
)

models_to_test = [
    os.environ["VECTORNODE_GLOBAL_MODEL"],
    os.environ["VECTORNODE_CHINESE_MODEL"],
]

for model in models_to_test:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "Summarize why a multi-model API gateway helps AI developers.",
            }
        ],
    )

    print(f"\n=== {model} ===")
    print(response.choices[0].message.content)
```

## Node.js Example

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.VECTORNODE_API_KEY,
  baseURL: "https://www.vectronode.com/v1",
});

const modelsToTest = [
  process.env.VECTORNODE_GLOBAL_MODEL,
  process.env.VECTORNODE_CHINESE_MODEL,
];

for (const model of modelsToTest) {
  const response = await client.chat.completions.create({
    model,
    messages: [
      {
        role: "user",
        content:
          "Summarize why a multi-model API gateway helps AI developers.",
      },
    ],
  });

  console.log(`\n=== ${model} ===`);
  console.log(response.choices[0].message.content);
}
```

## Use Cases

### Chinese-Language Apps

Chinese-language chatbots, knowledge-base products, and customer-support tools
often need to compare global models with Chinese LLMs. A gateway makes it
easier to test model behavior without rebuilding the app.

### AI Agents

Agents may use one model for planning, another for coding, and another for
summarization. Keeping the API format consistent simplifies orchestration.

### RAG Products

RAG apps can compare models for answer quality, citation style, and cost per
query while keeping the retrieval pipeline unchanged.

### SaaS AI Features

SaaS products can start with one default model and later add model selection,
fallbacks, or premium tiers without changing the public product flow.

## Suggested Environment Variables

```bash
export VECTORNODE_API_KEY="YOUR_API_KEY"
export VECTORNODE_GLOBAL_MODEL="YOUR_GLOBAL_MODEL_ID"
export VECTORNODE_CHINESE_MODEL="YOUR_CHINESE_MODEL_ID"
```

Always confirm available model names in your VectorNode dashboard before
running production traffic.

## Start Testing

Create an account and test your first request:

```text
https://www.vectronode.com/
```
