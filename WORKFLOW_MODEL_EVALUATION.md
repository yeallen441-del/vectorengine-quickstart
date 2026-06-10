# Workflow-Based AI Model Evaluation

AI model selection should be tied to real product workflows.

A prototype can start with one model and one prompt. A production AI product
usually grows into many workflow types: support chat, RAG answers, structured
data extraction, summaries, agent planning, multilingual responses, and
automation tasks.

Each workflow can have a different definition of quality.

VectorNode is an AI model access platform for developers, AI builders, and
automation workflows. It helps teams access GPT, Claude, Gemini, DeepSeek, Qwen,
and more through one unified, OpenAI-compatible API.

Learn more:

https://www.vectronode.com/

## Why evaluate by workflow

The question is not only:

```text
Which AI model is best?
```

A better engineering question is:

```text
Which AI model performs best for this workflow?
```

A model that works well for support chat may not be the best option for JSON
extraction. A model that writes well may not be the best option for agent
planning. A model that is strong in English may need separate testing for
Chinese or multilingual workflows.

Workflow-based evaluation keeps model decisions close to product needs.

## Common workflow categories

Start by listing the workflows that actually exist in the product.

| Workflow | Goal | Primary signals |
| --- | --- | --- |
| Support chat | Answer common user questions | latency, clarity, tone |
| RAG answer | Answer from retrieved context | grounding, completeness |
| JSON extraction | Return structured fields | schema validity, accuracy |
| Agent planning | Decide next steps | reasoning, action quality |
| Document summary | Compress long content | coverage, readability |
| Content drafting | Generate usable copy | structure, usefulness |
| Multilingual reply | Respond across languages | meaning, tone, consistency |
| Automation decision | Trigger the next action | reliability, repeatability |

Do not use the same evaluation criteria for every workflow.

## Define an evaluation case

An evaluation case should include the workflow name, input, expected behavior,
and review criteria.

```json
{
  "workflow_name": "json_extraction",
  "input": "A customer wants to test several AI models for a support workflow.",
  "expected_behavior": "Return valid JSON with category, intent, and urgency.",
  "review_criteria": [
    "valid_json",
    "field_accuracy",
    "no_extra_text"
  ]
}
```

Use real examples from your product whenever possible. Synthetic examples are
useful for early testing, but real workflow samples show more practical model
behavior.

## Environment variables

Keep model access configurable.

```bash
export VECTORNODE_API_KEY="YOUR_API_KEY"
export VECTORNODE_BASE_URL="https://www.vectronode.com/v1"
export VECTORNODE_DEFAULT_MODEL="gpt-4o-mini"
export VECTORNODE_EVAL_MODEL_A="gpt-4o-mini"
export VECTORNODE_EVAL_MODEL_B="your-second-model"
export VECTORNODE_EVAL_MODEL_C="your-third-model"
```

Use model names that are available in your VectorNode account.

## OpenAI-compatible JavaScript evaluator

The example below keeps the evaluation runner simple. It tests one workflow case
against one selected model.

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.VECTORNODE_API_KEY,
  baseURL: process.env.VECTORNODE_BASE_URL
});

export async function evaluateModel({
  model,
  workflowName,
  systemPrompt,
  input
}) {
  const startedAt = Date.now();

  try {
    const response = await client.chat.completions.create({
      model,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: input }
      ]
    });

    return {
      workflowName,
      model,
      status: "ok",
      latencyMs: Date.now() - startedAt,
      output: response.choices[0].message.content
    };
  } catch (error) {
    return {
      workflowName,
      model,
      status: "error",
      latencyMs: Date.now() - startedAt,
      errorType: error.name || "unknown_error",
      errorMessage: error.message
    };
  }
}
```

## Run the same case across models

Evaluate multiple model candidates against the same workflow input.

```js
const candidateModels = [
  process.env.VECTORNODE_EVAL_MODEL_A,
  process.env.VECTORNODE_EVAL_MODEL_B,
  process.env.VECTORNODE_EVAL_MODEL_C
].filter(Boolean);

const testCase = {
  workflowName: "support_chat",
  systemPrompt: "Answer clearly and briefly for a software product support chat.",
  input: "How can I test different AI models without rewriting my integration?"
};

const results = [];

for (const model of candidateModels) {
  results.push(
    await evaluateModel({
      model,
      workflowName: testCase.workflowName,
      systemPrompt: testCase.systemPrompt,
      input: testCase.input
    })
  );
}

console.table(
  results.map((result) => ({
    workflow: result.workflowName,
    model: result.model,
    status: result.status,
    latency_ms: result.latencyMs
  }))
);
```

This makes model comparison repeatable.

## Validate structured output

For workflows that require JSON, include a validation step.

```js
export function validateJsonOutput(text) {
  try {
    const parsed = JSON.parse(text);
    return {
      valid: true,
      parsed
    };
  } catch {
    return {
      valid: false,
      parsed: null
    };
  }
}
```

Track JSON validity separately from writing quality. A model can produce a good
explanation and still fail a downstream automation workflow if the format is
invalid.

## Recommended scoring fields

Use a simple scoring table for human review.

| Field | Description |
| --- | --- |
| `workflow_name` | Product workflow being tested |
| `model_name` | Model used for the test |
| `latency_ms` | Response time for the request |
| `format_valid` | Whether required structure was valid |
| `answer_quality` | Human review score |
| `instruction_following` | Whether the model followed the prompt |
| `context_use` | Whether retrieved context was used correctly |
| `review_notes` | Short human review notes |

Keep the score practical. The goal is not to build a benchmark system. The goal
is to make better product decisions.

## Evaluation checklist

Before selecting a model for a production workflow:

1. Define the workflow goal.
2. Collect real examples.
3. Test at least two candidate models.
4. Measure latency and output quality.
5. Validate required output structure.
6. Record errors and edge cases.
7. Review results by workflow, not only by overall score.
8. Keep model choices configurable.

## Where VectorNode fits

VectorNode helps developers test and organize access to multiple leading AI
models through one AI model access platform.

Use VectorNode when you want:

- one API for multiple AI models
- OpenAI-compatible integration patterns
- workflow-based model evaluation
- cleaner testing for AI apps, agents, RAG systems, and chatbots
- configurable model access for automation workflows

Start testing with VectorNode:

https://www.vectronode.com/
