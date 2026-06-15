# Capability-Based Model Router for Multimodal AI Apps

AI applications rarely stay connected to one model.

A product may begin with text generation, then add document reasoning, agent
tool use, image creation, video generation, audio transcription, or speech
workflows. If every feature calls a provider directly, model-specific
credentials, request formats, timeouts, routes, and error handling quickly
spread across the application.

This guide shows how to build a small TypeScript model access layer that routes
requests by product capability instead of hardcoding one provider into each
workflow.

VectorNode is a pay-as-you-go multi-model AI API platform for independent
developers and small AI teams working with text, image, video, and audio
models. Developers can use one account to test and access GPT, Claude, Gemini,
DeepSeek, Qwen, and hundreds of other supported models through
developer-friendly APIs.

Learn more:

https://www.vectronode.com/

## Route by capability

Product code should request the capability it needs:

- support chat
- document reasoning
- structured agent output
- image generation
- video generation
- audio transcription

The routing layer can then select a configured model, route, API format, and
timeout policy.

```ts
type Capability =
  | "support-chat"
  | "document-reasoning"
  | "structured-agent-output"
  | "image-generation"
  | "video-generation"
  | "audio-transcription";

type ApiFormat =
  | "openai-compatible"
  | "media-job"
  | "specialized";

interface ModelTarget {
  model: string;
  route?: string;
  apiFormat: ApiFormat;
  timeoutMs: number;
}

interface CapabilityTarget {
  primary: ModelTarget;
  fallback?: ModelTarget;
}

type ModelAccessConfig = Record<Capability, CapabilityTarget>;
```

Use exact model and route identifiers from the current VectorNode catalog.
Available models, routes, API formats, and pricing can change.

## Keep selection in configuration

The application should not need a code deployment every time a team tests a
different model or route.

```ts
const modelAccessConfig: ModelAccessConfig = {
  "support-chat": {
    primary: {
      model: process.env.SUPPORT_MODEL ?? "YOUR_TEXT_MODEL_ID",
      route: process.env.SUPPORT_ROUTE,
      apiFormat: "openai-compatible",
      timeoutMs: 15_000,
    },
  },
  "document-reasoning": {
    primary: {
      model: process.env.RAG_MODEL ?? "YOUR_REASONING_MODEL_ID",
      route: process.env.RAG_ROUTE,
      apiFormat: "openai-compatible",
      timeoutMs: 30_000,
    },
  },
  "structured-agent-output": {
    primary: {
      model: process.env.AGENT_MODEL ?? "YOUR_AGENT_MODEL_ID",
      route: process.env.AGENT_ROUTE,
      apiFormat: "openai-compatible",
      timeoutMs: 30_000,
    },
    fallback: {
      model: process.env.AGENT_FALLBACK_MODEL ?? "YOUR_FALLBACK_MODEL_ID",
      route: process.env.AGENT_FALLBACK_ROUTE,
      apiFormat: "openai-compatible",
      timeoutMs: 30_000,
    },
  },
  "image-generation": {
    primary: {
      model: process.env.IMAGE_MODEL ?? "YOUR_IMAGE_MODEL_ID",
      route: process.env.IMAGE_ROUTE,
      apiFormat: "media-job",
      timeoutMs: 120_000,
    },
  },
  "video-generation": {
    primary: {
      model: process.env.VIDEO_MODEL ?? "YOUR_VIDEO_MODEL_ID",
      route: process.env.VIDEO_ROUTE,
      apiFormat: "media-job",
      timeoutMs: 600_000,
    },
  },
  "audio-transcription": {
    primary: {
      model: process.env.AUDIO_MODEL ?? "YOUR_AUDIO_MODEL_ID",
      route: process.env.AUDIO_ROUTE,
      apiFormat: "specialized",
      timeoutMs: 120_000,
    },
  },
};
```

This configuration is intentionally explicit. Text, image, video, and audio
models do not always share the same endpoints or request lifecycle.

## Define one internal request contract

Use a stable request and result shape inside the application.

```ts
interface ModelRequest {
  capability: Capability;
  input: unknown;
  metadata?: {
    application?: string;
    environment?: string;
    workflowId?: string;
  };
}

interface ModelError {
  code: string;
  message: string;
  retryable: boolean;
}

interface ModelResult<T = unknown> {
  success: boolean;
  model: string;
  route?: string;
  latencyMs: number;
  output?: T;
  error?: ModelError;
}
```

This is an internal contract. It does not imply that every external model uses
the same API format.

## Put external formats behind adapters

Each adapter translates the internal request into the format required by a
particular model category.

```ts
interface ModelAdapter {
  execute(
    target: ModelTarget,
    request: ModelRequest
  ): Promise<ModelResult>;
}
```

For a supported text or chat model, an adapter may use an OpenAI-compatible
request shape:

```ts
class OpenAICompatibleAdapter implements ModelAdapter {
  constructor(
    private baseUrl: string,
    private apiKey: string
  ) {}

  async execute(
    target: ModelTarget,
    request: ModelRequest
  ): Promise<ModelResult> {
    const startedAt = performance.now();

    try {
      const response = await fetch(`${this.baseUrl}/chat/completions`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: target.model,
          ...(request.input as object),
        }),
        signal: AbortSignal.timeout(target.timeoutMs),
      });

      if (!response.ok) {
        return {
          success: false,
          model: target.model,
          route: target.route,
          latencyMs: Math.round(performance.now() - startedAt),
          error: {
            code: `HTTP_${response.status}`,
            message: await response.text(),
            retryable: response.status === 429 || response.status >= 500,
          },
        };
      }

      return {
        success: true,
        model: target.model,
        route: target.route,
        latencyMs: Math.round(performance.now() - startedAt),
        output: await response.json(),
      };
    } catch (error) {
      return {
        success: false,
        model: target.model,
        route: target.route,
        latencyMs: Math.round(performance.now() - startedAt),
        error: {
          code: "REQUEST_FAILED",
          message: error instanceof Error ? error.message : "Unknown error",
          retryable: true,
        },
      };
    }
  }
}
```

Set the base URL, endpoint path, request fields, and model identifier according
to the current documentation for the selected model.

OpenAI compatibility is one useful technical format. It is not the complete
definition of a multimodal platform.

## Handle asynchronous media jobs separately

Image, video, audio, and specialized models may return a job identifier before
the final asset is ready.

```ts
interface MediaJob {
  id: string;
  status: "queued" | "running" | "succeeded" | "failed";
  output?: unknown;
  error?: string;
}

abstract class MediaJobAdapter implements ModelAdapter {
  async execute(
    target: ModelTarget,
    request: ModelRequest
  ): Promise<ModelResult> {
    const startedAt = performance.now();

    try {
      const job = await this.createJob(target, request);
      const output = await this.waitForCompletion(job.id, target.timeoutMs);

      return {
        success: true,
        model: target.model,
        route: target.route,
        latencyMs: Math.round(performance.now() - startedAt),
        output,
      };
    } catch (error) {
      return {
        success: false,
        model: target.model,
        route: target.route,
        latencyMs: Math.round(performance.now() - startedAt),
        error: {
          code: "MEDIA_JOB_FAILED",
          message: error instanceof Error ? error.message : "Unknown error",
          retryable: false,
        },
      };
    }
  }

  protected abstract createJob(
    target: ModelTarget,
    request: ModelRequest
  ): Promise<MediaJob>;

  protected abstract waitForCompletion(
    jobId: string,
    timeoutMs: number
  ): Promise<unknown>;
}
```

Keep media job creation, polling, asset retrieval, and output normalization
inside the relevant adapter.

## Add the router

The router selects the adapter and only uses a fallback for failures that have
been classified as temporary.

```ts
class CapabilityRouter {
  constructor(
    private config: ModelAccessConfig,
    private adapters: Record<ApiFormat, ModelAdapter>
  ) {}

  async execute(request: ModelRequest): Promise<ModelResult> {
    const target = this.config[request.capability];
    const primaryAdapter = this.adapters[target.primary.apiFormat];
    const primaryResult = await primaryAdapter.execute(
      target.primary,
      request
    );

    if (
      primaryResult.success ||
      !target.fallback ||
      !primaryResult.error?.retryable
    ) {
      return primaryResult;
    }

    const fallbackAdapter = this.adapters[target.fallback.apiFormat];
    return fallbackAdapter.execute(target.fallback, request);
  }
}
```

Application code can now request a capability:

```ts
const result = await router.execute({
  capability: "document-reasoning",
  input: {
    messages: [
      {
        role: "user",
        content: "Summarize the retrieved documents.",
      },
    ],
  },
  metadata: {
    application: "knowledge-assistant",
    environment: "production",
  },
});
```

The workflow does not need to know which configured model or route handled the
request.

## Validate before accepting a fallback

Fallback behavior must be tested by workflow.

A second model may return a technically successful response with an
incompatible structure. Agent and automation workflows should validate their
output before passing it downstream.

```ts
function isValidAgentOutput(value: unknown): boolean {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  return "action" in value && "arguments" in value;
}
```

Do not retry authentication failures, malformed requests, unsupported
parameters, or failed validation without understanding the cause.

## Record every routing decision

Create a usage record for every request.

```ts
interface UsageRecord {
  timestamp: string;
  application?: string;
  environment?: string;
  capability: Capability;
  model: string;
  route?: string;
  success: boolean;
  latencyMs: number;
  estimatedCost?: number;
  errorCode?: string;
}
```

These records make it possible to compare:

- success rate by capability
- latency by model and route
- spending by workflow
- timeout and retry frequency
- fallback frequency
- invalid structured outputs
- media generation failures

## Production checklist

Before routing important traffic:

1. Test every capability with realistic inputs.
2. Confirm the exact model and route identifiers.
3. Verify API format and parameter support.
4. Measure latency distribution, not one successful request.
5. Test timeout and error behavior.
6. Validate structured outputs.
7. Test media job polling and asset retrieval.
8. Confirm that fallback output is compatible.
9. Keep credentials outside source control.
10. Monitor usage, cost, failures, and route availability.

Run a controlled pilot before moving a production workload.

Teams that require formal enterprise certifications, contractual service
levels, or specialized data residency controls should complete a separate
enterprise evaluation.

## Where VectorNode fits

VectorNode gives independent developers and small AI teams one account for
testing and accessing hundreds of supported text, image, video, and audio
models.

The platform provides Playground testing, multiple model and routing options,
usage records, and different supported API formats. This can reduce the need
to maintain a separate account, balance, and integration for every model
family.

VectorNode can support AI applications, agents, RAG systems, chatbots,
automation workflows, developer tools, and multimodal products.

Start testing with VectorNode:

https://www.vectronode.com/
