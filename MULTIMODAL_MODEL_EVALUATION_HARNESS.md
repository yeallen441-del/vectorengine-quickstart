# Multimodal AI Model Evaluation Harness

AI applications rarely depend on a single model forever.

A product may begin with text generation, then add document analysis, image
creation, audio processing, video generation, or agent workflows. As these
requirements grow, developers need a repeatable way to test models without
scattering provider-specific logic across the codebase.

This guide shows how to design a small, configuration-driven TypeScript
evaluation harness for text, image, video, and audio models.

The goal is not to create a universal benchmark. It is to make model decisions
measurable, repeatable, and easier to update.

VectorNode is a pay-as-you-go multi-model AI API platform for independent
developers and small AI teams. It provides one account for testing and
accessing GPT, Claude, Gemini, DeepSeek, Qwen, and hundreds of other supported
models through developer-friendly APIs.

Learn more:

https://www.vectronode.com/

## What the harness should measure

A practical evaluation harness should:

- define models and routes in configuration
- load realistic product test cases
- run comparable tests against multiple models
- record latency, success, and validation results
- support text requests and asynchronous media jobs
- preserve route and model identifiers in each result
- export records for later comparison

Model output quality is only one part of the evaluation. API behavior, route
availability, processing time, and output format also affect whether a model
fits a production workflow.

## Define the core types

Start with types that keep model targets, test cases, and results separate.

```ts
type Modality = "text" | "image" | "video" | "audio";

interface ModelTarget {
  id: string;
  model: string;
  route?: string;
  modality: Modality;
  enabled: boolean;
}

interface TestCase {
  id: string;
  workflow: string;
  modality: Modality;
  input: unknown;
  expected?: {
    requiredFields?: string[];
    maxLatencyMs?: number;
  };
}

interface EvaluationResult {
  testCaseId: string;
  workflow: string;
  targetId: string;
  model: string;
  route?: string;
  success: boolean;
  latencyMs: number;
  formatValid: boolean;
  error?: string;
  output?: unknown;
}
```

This separation lets the same model participate in several workflow tests and
lets multiple models compete against the same product requirement.

## Keep model targets configurable

Do not hardcode one model throughout the product.

```ts
const targets: ModelTarget[] = [
  {
    id: "support-text",
    model: process.env.SUPPORT_MODEL ?? "YOUR_TEXT_MODEL_ID",
    route: process.env.SUPPORT_ROUTE,
    modality: "text",
    enabled: true,
  },
  {
    id: "rag-reasoning",
    model: process.env.RAG_MODEL ?? "YOUR_REASONING_MODEL_ID",
    route: process.env.RAG_ROUTE,
    modality: "text",
    enabled: true,
  },
  {
    id: "product-image",
    model: process.env.IMAGE_MODEL ?? "YOUR_IMAGE_MODEL_ID",
    route: process.env.IMAGE_ROUTE,
    modality: "image",
    enabled: true,
  },
];
```

Use exact model and route identifiers from the current VectorNode catalog.
Supported models, routes, formats, and pricing may change.

## Create workflow-based test cases

Public benchmarks are useful for discovery. Internal tests should represent
what the product actually needs to do.

```ts
const testCases: TestCase[] = [
  {
    id: "support-001",
    workflow: "support_chat",
    modality: "text",
    input: {
      messages: [
        {
          role: "user",
          content: "Explain how to rotate an API credential safely.",
        },
      ],
    },
    expected: {
      maxLatencyMs: 5000,
    },
  },
  {
    id: "agent-001",
    workflow: "agent_structured_output",
    modality: "text",
    input: {
      task: "Return a support ticket with title, priority, and summary.",
    },
    expected: {
      requiredFields: ["title", "priority", "summary"],
      maxLatencyMs: 8000,
    },
  },
  {
    id: "image-001",
    workflow: "product_image",
    modality: "image",
    input: {
      prompt: "A clean studio product image on a neutral background",
    },
    expected: {
      maxLatencyMs: 60000,
    },
  },
];
```

Start with 10 to 30 examples for each important workflow. Include normal
requests, difficult inputs, multilingual examples, formatting requirements,
and known failure cases.

## Put API differences behind adapters

Text, image, video, and audio models may not share the same endpoint or request
format. Keep these differences behind an internal adapter interface.

```ts
interface ModelAdapter {
  run(target: ModelTarget, test: TestCase): Promise<unknown>;
}
```

For a supported text or chat model, an adapter may use an OpenAI-compatible
request:

```ts
class TextModelAdapter implements ModelAdapter {
  constructor(
    private baseUrl: string,
    private apiKey: string
  ) {}

  async run(target: ModelTarget, test: TestCase): Promise<unknown> {
    const response = await fetch(`${this.baseUrl}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        model: target.model,
        ...(test.input as object),
      }),
    });

    if (!response.ok) {
      const body = await response.text();
      throw new Error(`Request failed (${response.status}): ${body}`);
    }

    return response.json();
  }
}
```

Set the base URL, endpoint path, model identifier, and request body according to
the current documentation. Image, video, audio, and specialized models may
require different adapters.

## Run and record an evaluation

The runner should capture failures without stopping the full test suite.

```ts
async function evaluate(
  adapter: ModelAdapter,
  target: ModelTarget,
  test: TestCase
): Promise<EvaluationResult> {
  const startedAt = performance.now();

  try {
    const output = await adapter.run(target, test);
    const latencyMs = Math.round(performance.now() - startedAt);

    return {
      testCaseId: test.id,
      workflow: test.workflow,
      targetId: target.id,
      model: target.model,
      route: target.route,
      success: true,
      latencyMs,
      formatValid: validateOutput(output, test.expected),
      output,
    };
  } catch (error) {
    return {
      testCaseId: test.id,
      workflow: test.workflow,
      targetId: target.id,
      model: target.model,
      route: target.route,
      success: false,
      latencyMs: Math.round(performance.now() - startedAt),
      formatValid: false,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}

function validateOutput(
  output: unknown,
  expected?: TestCase["expected"]
): boolean {
  if (!expected?.requiredFields) {
    return true;
  }

  if (!output || typeof output !== "object") {
    return false;
  }

  return expected.requiredFields.every(
    (field) => field in (output as Record<string, unknown>)
  );
}
```

For strict structured output, replace the basic validator with JSON Schema,
Zod, or another schema-validation library.

## Handle asynchronous media jobs

Video and some image or audio APIs return a job identifier before the final
asset is ready.

The corresponding adapter should:

1. submit the generation request
2. preserve the returned job identifier
3. poll the documented status endpoint
4. stop after a configured timeout
5. record the completion time
6. save the final asset URL and metadata

Useful media metadata includes:

```ts
interface MediaMetadata {
  width?: number;
  height?: number;
  durationSeconds?: number;
  format?: string;
  jobCompletionMs?: number;
  assetUrl?: string;
}
```

Do not treat a queued job as a completed generation. Record submission success
and final asset completion separately.

## Compare models by workflow

Avoid producing one global model ranking. Summarize results by product
workflow.

```ts
interface WorkflowSummary {
  workflow: string;
  model: string;
  route?: string;
  successRate: number;
  averageLatencyMs: number;
  formatSuccessRate: number;
  averageCost?: number;
}
```

A support chatbot may prioritize latency. A RAG workflow may prioritize
grounded answer quality. An agent may prioritize valid tool arguments. A media
workflow may prioritize asset quality and completion time.

The final selection should balance:

- output quality
- successful request rate
- response or completion latency
- formatting reliability
- route availability
- usage cost
- workflow requirements

Keep the selected model and route configurable after evaluation.

## Continue testing after launch

Initial evaluation is only the beginning. Production traffic exposes new
inputs, failure patterns, and user expectations.

Monitor:

- request success rate
- latency percentiles
- cost by workflow
- invalid structured outputs
- timeout and retry frequency
- media generation failures
- route availability
- user corrections

Add difficult production examples back into the evaluation dataset. Rerun them
when model, route, prompt, or integration settings change.

## Where VectorNode fits

VectorNode gives independent developers and small AI teams one account for
testing and accessing supported text, image, video, and audio models.

Developers can use the Playground for initial exploration, compare available
models and routes, and then move representative evaluations into an automated
test harness.

This workflow can support AI applications, agents, RAG systems, chatbots,
automation workflows, developer tools, and multimodal products.

Start testing with VectorNode:

https://www.vectronode.com/
