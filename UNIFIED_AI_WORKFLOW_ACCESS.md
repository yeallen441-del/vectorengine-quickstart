# Unified Model Access for AI Workflows

AI products often begin with one model call, but production applications
usually grow into several workflows with different requirements.

A support chatbot may prioritize response time. A RAG system may need stronger
reasoning over retrieved context. An agent may need reliable tool use. An
automation task may require predictable structured output.

This guide shows how to place one configurable model access layer between those
workflows and the models they use.

VectorNode is an AI model access platform for developers, AI builders, and
automation workflows. It provides a unified, OpenAI-compatible API for accessing
GPT, Claude, Gemini, DeepSeek, Qwen, and other available models.

Learn more:

https://www.vectronode.com/

## Architecture

Keep product behavior, workflow requirements, and model access as separate
concerns:

```text
Product feature
    |
Workflow contract
    |
Model access layer
    |
Configured model
```

The product feature should describe the task. The workflow contract should
define the expected behavior. The model access layer should handle connection
details, model selection, and request logging.

This structure prevents model names and provider settings from spreading across
the application.

## Define workflow contracts

Start by documenting the main AI workflows in the product.

```js
const workflows = {
  supportChat: {
    modelEnv: "SUPPORT_CHAT_MODEL",
    systemPrompt: "Answer clearly and concisely.",
    temperature: 0.3,
  },
  ragAnswer: {
    modelEnv: "RAG_ANSWER_MODEL",
    systemPrompt: "Answer only from the supplied context.",
    temperature: 0.1,
  },
  automationTask: {
    modelEnv: "AUTOMATION_MODEL",
    systemPrompt: "Return a concise result for the downstream workflow.",
    temperature: 0,
  },
};
```

The workflow configuration can evolve without changing the product feature that
uses it.

Use model names that are currently available to your VectorNode account rather
than copying example model identifiers blindly.

## Configure the API client

Install the OpenAI JavaScript SDK:

```bash
npm install openai
```

Set the required environment variables:

```bash
export VECTORNODE_API_KEY="YOUR_API_KEY"
export VECTORNODE_BASE_URL="https://www.vectronode.com/v1"
export SUPPORT_CHAT_MODEL="YOUR_CHAT_MODEL"
export RAG_ANSWER_MODEL="YOUR_RAG_MODEL"
export AUTOMATION_MODEL="YOUR_AUTOMATION_MODEL"
```

Create one shared client:

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.VECTORNODE_API_KEY,
  baseURL:
    process.env.VECTORNODE_BASE_URL ??
    "https://www.vectronode.com/v1",
});
```

Keeping the API key, base URL, and model choices outside the application code
makes testing and deployment safer.

## Build one workflow runner

The workflow runner converts a product task into a model request.

```js
async function runWorkflow({ workflowName, input, context }) {
  const workflow = workflows[workflowName];

  if (!workflow) {
    throw new Error(`Unknown AI workflow: ${workflowName}`);
  }

  const model = process.env[workflow.modelEnv];

  if (!model) {
    throw new Error(`Missing model setting: ${workflow.modelEnv}`);
  }

  const messages = [
    {
      role: "system",
      content: workflow.systemPrompt,
    },
  ];

  if (context) {
    messages.push({
      role: "user",
      content: `Context:\n${context}\n\nTask:\n${input}`,
    });
  } else {
    messages.push({
      role: "user",
      content: input,
    });
  }

  const startedAt = Date.now();

  try {
    const response = await client.chat.completions.create({
      model,
      messages,
      temperature: workflow.temperature,
    });

    const output = response.choices[0]?.message?.content ?? "";

    console.info({
      event: "ai_workflow_completed",
      workflowName,
      model,
      latencyMs: Date.now() - startedAt,
      inputTokens: response.usage?.prompt_tokens,
      outputTokens: response.usage?.completion_tokens,
    });

    return output;
  } catch (error) {
    console.error({
      event: "ai_workflow_failed",
      workflowName,
      model,
      latencyMs: Date.now() - startedAt,
      error: error instanceof Error ? error.message : String(error),
    });

    throw error;
  }
}
```

Product features can now call workflows without managing connection details:

```js
const reply = await runWorkflow({
  workflowName: "supportChat",
  input: "How do I update my billing email?",
});
```

A RAG feature can use the same access layer with retrieved context:

```js
const answer = await runWorkflow({
  workflowName: "ragAnswer",
  input: "What is the cancellation policy?",
  context: retrievedDocuments,
});
```

## Keep evaluation workflow-specific

Do not select one model for every feature based on a generic benchmark.

Evaluate models against representative examples from each workflow:

| Workflow | What to evaluate |
| --- | --- |
| Support chat | latency, clarity, consistency |
| RAG answers | grounding, context use, factual accuracy |
| Agent planning | tool choice, step quality, reliability |
| Structured extraction | schema validity, missing fields |
| Content generation | tone, instruction following, editing effort |
| Automation | repeatability, parseability, error handling |

Record both machine-readable metrics and human review notes. A model that works
well for one workflow may not be the best choice for another.

## Production checklist

Before routing production traffic through the shared layer:

- keep API credentials in environment variables or a secret manager
- verify every configured model name
- test each workflow with realistic examples
- validate structured outputs before downstream actions
- log workflow name, model name, latency, usage, and errors
- define timeouts and retry limits
- add fallback behavior only where the product requires it
- avoid logging sensitive prompts or user data
- review model choices when product requirements change

## Why use a unified access layer?

The value is not simply connecting to more models.

The value is giving the product one stable place to manage model access while
allowing each workflow to evolve independently.

This approach helps teams:

- reduce duplicated integration code
- test different models without rewriting product features
- organize model choices by workflow
- monitor model behavior consistently
- add new AI capabilities with less architectural friction

For AI apps, agents, RAG systems, chatbots, developer tools, and automation
workflows, a unified model access layer provides a cleaner foundation for
continued development.
