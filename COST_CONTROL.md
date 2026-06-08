# AI API Cost Control with an OpenAI-Compatible Gateway

AI API cost grows quickly when a product moves from testing to real users.
This guide shows a practical way to control GPT, Claude, Gemini, DeepSeek,
Qwen, and other model usage through one unified AI model access layer.

VectorNode lets developers keep the OpenAI SDK request shape while
testing different model families behind the same base URL. That makes it easier
to compare quality, latency, and price before choosing a production default.

## 1. Put Model Choice in Configuration

Do not hard-code model names inside product logic. Use environment variables so
you can change the default model without a deploy.

```bash
export VECTORNODE_API_KEY="YOUR_API_KEY"
export VECTORNODE_BASE_URL="https://www.vectronode.com/v1"
export VECTORNODE_DEFAULT_MODEL="gpt-4o-mini"
export VECTORNODE_EFFICIENT_MODEL="deepseek-chat"
```

Python:

```python
import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ["VECTORNODE_API_KEY"],
    base_url=os.getenv("VECTORNODE_BASE_URL", "https://www.vectronode.com/v1"),
)

model = os.getenv("VECTORNODE_DEFAULT_MODEL", "gpt-4o-mini")

response = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Summarize this support ticket."}],
    max_tokens=300,
)
```

## 2. Match Model Cost to Product Value

Not every task needs the same model.

Use stronger models for:

- paid-user workflows
- complex reasoning
- customer-facing answers
- high-value coding or analysis tasks

Use efficient models for:

- drafts
- classification
- routing
- short summaries
- internal checks
- free-tier usage

A multi-model gateway helps teams test this split without rewriting every API
client.

## 3. Set Token Limits by Feature

Token limits should be intentional. A chat assistant, a background summarizer,
and an agent planning step should not share the same limit.

Example:

```python
FEATURE_TOKEN_LIMITS = {
    "support_summary": 300,
    "chat_reply": 800,
    "agent_plan": 500,
    "rag_answer": 900,
}
```

Start conservative, then raise limits only for features where quality improves.

## 4. Use a Cost-Aware Fallback Path

When cost matters more than maximum quality, route the request to a more
efficient model.

```python
def choose_model(user_tier: str, feature: str) -> str:
    if user_tier == "free":
        return os.getenv("VECTORNODE_EFFICIENT_MODEL", "deepseek-chat")

    if feature in {"classification", "draft", "summary"}:
        return os.getenv("VECTORNODE_EFFICIENT_MODEL", "deepseek-chat")

    return os.getenv("VECTORNODE_DEFAULT_MODEL", "gpt-4o-mini")
```

This pattern is useful for SaaS tools, AI agents, RAG apps, and developer
platforms that need predictable usage cost.

## 5. Track Cost Signals Early

Before traffic grows, log the fields that help you understand API spend:

- feature name
- user tier
- model name
- prompt token count
- completion token count
- latency
- success or error status

Avoid storing private user prompts unless your privacy policy and product
workflow clearly allow it.

## 6. Compare Pricing Before Scaling

Before sending large traffic through one default model, run the same prompt set
against multiple options:

- GPT for general quality
- Claude for long-form writing and analysis
- Gemini for Google ecosystem and multimodal workflows
- DeepSeek for cost-sensitive reasoning and coding
- Qwen or other Chinese LLMs for Chinese-language use cases

The right default is usually not the most expensive model. It is the model that
meets the product quality bar at the lowest sustainable cost.

## 7. Test with Postman First

Use the Postman collection in this repository before changing production code:

```text
postman/vectornode-api.postman_collection.json
```

Recommended variables:

```text
base_url = https://www.vectronode.com
api_key = YOUR_VECTORNODE_API_KEY
model = gpt-4o-mini
```

Then test an efficient model with the same prompt and compare response quality.

## Start Testing

Learn more:

```text
https://www.vectronode.com/
```
