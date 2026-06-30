# AI Model Catalog for Global and Chinese Frontier Models

Multi-model AI products need a source of truth for model choices.

A production application may use one model for support chat, another for RAG
answers, another for coding agents, another for Chinese document analysis,
another for background automation, and another for multimodal workflows.

VectorNode is a multi-model AI infrastructure platform for developers and AI
teams. It helps teams access, manage, monitor, and optimize global and Chinese
frontier AI models from one developer platform.

This guide shows how to build a practical AI model catalog for organizing GPT,
Claude, Gemini, DeepSeek, Qwen, Kimi, GLM, MiniMax, Doubao, and other model
families by workflow, capability, language, cost, routing, and production
readiness.

Learn more:

https://www.vectronode.com/

## Why a model catalog matters

Model access can grow faster than model governance.

Without a catalog, teams often run into problems:

- developers use old model IDs in production
- teams do not know which model supports which workflow
- costly models are used for low-value background tasks
- Chinese or bilingual tasks are routed to models tested only in English
- fallback models are not clearly defined
- model changes happen without ownership
- usage logs cannot be connected back to workflow decisions

A model catalog reduces this confusion.

It gives developers a shared view of which models exist, what they are good
for, how they should be routed, and whether they are approved for production.

## Catalog by workflow, not only provider

Provider names are useful, but they are not enough.

The catalog should answer workflow questions:

| Workflow | Catalog question |
| --- | --- |
| `support_chat` | Which model is fast, clear, and cost-effective? |
| `rag_answer` | Which model follows retrieved context reliably? |
| `coding_agent` | Which model can complete engineering tasks? |
| `json_automation` | Which model returns valid structured output? |
| `document_analysis` | Which model handles long or domain-specific documents? |
| `multilingual_reply` | Which model works across English and Chinese? |
| `background_task` | Which model has the best cost per successful task? |

This keeps the catalog close to product behavior.

## Core catalog schema

Use one record shape for model entries.

```ts
type ModelStatus =
  | "testing"
  | "approved"
  | "fallback_only"
  | "deprecated"
  | "disabled";

type Modality =
  | "text"
  | "image"
  | "audio"
  | "video"
  | "embedding"
  | "reranking"
  | "multimodal";

type Workflow =
  | "support_chat"
  | "rag_answer"
  | "coding_agent"
  | "json_automation"
  | "document_analysis"
  | "multilingual_reply"
  | "background_task";

type LanguageFit = "en" | "zh" | "bilingual" | "multilingual" | "other";

type ContextTier = "short" | "medium" | "long" | "very_long";

type QualityTier = "unknown" | "weak" | "acceptable" | "good" | "strong";

type CostTier = "low" | "medium" | "high";

type LatencyTier = "fast" | "standard" | "slow";

interface AiModelCatalogEntry {
  modelId: string;
  displayName: string;
  providerFamily:
    | "gpt"
    | "claude"
    | "gemini"
    | "deepseek"
    | "qwen"
    | "kimi"
    | "glm"
    | "minimax"
    | "doubao"
    | "other";
  route?: string;
  modalities: Modality[];
  bestWorkflows: Workflow[];
  languageFit: LanguageFit[];
  contextTier: ContextTier;
  structuredOutputQuality: QualityTier;
  latencyTier: LatencyTier;
  costTier: CostTier;
  status: ModelStatus;
  fallbackModelId?: string;
  owner: string;
  lastReviewed: string;
  notes?: string;
}
```

Use exact model and route identifiers from the current VectorNode catalog.
Available models, routes, API formats, and pricing can change.

## Example catalog entry

```json
{
  "modelId": "YOUR_MODEL_ID",
  "displayName": "Example Frontier Model",
  "providerFamily": "qwen",
  "route": "YOUR_ROUTE_ID",
  "modalities": ["text"],
  "bestWorkflows": ["rag_answer", "coding_agent", "document_analysis"],
  "languageFit": ["en", "zh", "bilingual"],
  "contextTier": "long",
  "structuredOutputQuality": "good",
  "latencyTier": "standard",
  "costTier": "medium",
  "status": "testing",
  "fallbackModelId": "YOUR_FALLBACK_MODEL_ID",
  "owner": "ai-platform-team",
  "lastReviewed": "2026-06-30",
  "notes": "Strong candidate for bilingual RAG and coding workflows. Needs more cost testing."
}
```

This record can live in a configuration file, internal dashboard, database,
spreadsheet, or model management service.

## Lifecycle status

Every model should have a clear status.

| Status | Meaning |
| --- | --- |
| `testing` | The model is being evaluated but is not ready for production traffic |
| `approved` | The model is approved for one or more production workflows |
| `fallback_only` | The model should only be used when a primary model fails |
| `deprecated` | The model should be replaced soon |
| `disabled` | The model should not receive traffic |

Status should be workflow-aware. A model can be approved for English RAG but
still be in testing for Chinese RAG.

## Workflow approval map

Keep workflow approvals separate from the top-level model entry when a model
has mixed results across workflows.

```ts
interface WorkflowApproval {
  modelId: string;
  workflow: Workflow;
  language: LanguageFit;
  status: ModelStatus;
  primaryUseCase?: string;
  fallbackModelId?: string;
  minimumScore?: number;
  maxLatencyMs?: number;
  maxCostPerSuccessfulTaskUsd?: number;
  reviewedAt: string;
  reviewer: string;
}
```

Example:

```json
{
  "modelId": "YOUR_MODEL_ID",
  "workflow": "rag_answer",
  "language": "zh",
  "status": "testing",
  "primaryUseCase": "Chinese policy document answers",
  "fallbackModelId": "YOUR_BILINGUAL_FALLBACK_MODEL",
  "minimumScore": 4.2,
  "maxLatencyMs": 9000,
  "maxCostPerSuccessfulTaskUsd": 0.25,
  "reviewedAt": "2026-06-30",
  "reviewer": "ai-platform-team"
}
```

This allows teams to avoid broad approvals that are too vague for production.

## Connect catalog and scorecard

The catalog and scorecard should work together.

The catalog answers:

```text
What models can we use?
```

The scorecard answers:

```text
How well did each model perform in real workflow tests?
```

After scorecard results improve, the catalog status can change:

- `testing` to `approved`
- `approved` to `fallback_only`
- `approved` to `deprecated`
- `testing` to `disabled`

Keep a review trail so model changes can be explained later.

```ts
interface ModelCatalogReview {
  modelId: string;
  workflow?: Workflow;
  previousStatus: ModelStatus;
  nextStatus: ModelStatus;
  reason: string;
  scorecardIds: string[];
  reviewedAt: string;
  reviewer: string;
}
```

## Routing from the catalog

A catalog becomes more useful when it feeds model routing.

```ts
interface WorkflowRoutingRule {
  workflow: Workflow;
  primaryModelId: string;
  fallbackModelId?: string;
  language?: LanguageFit;
  userTier?: "free" | "pro" | "enterprise";
  maxEstimatedCostUsd?: number;
}

export function getRoutingRule(
  rules: WorkflowRoutingRule[],
  input: {
    workflow: Workflow;
    language?: LanguageFit;
    userTier?: "free" | "pro" | "enterprise";
  }
): WorkflowRoutingRule | undefined {
  return rules.find((rule) => {
    if (rule.workflow !== input.workflow) return false;
    if (rule.language && rule.language !== input.language) return false;
    if (rule.userTier && rule.userTier !== input.userTier) return false;
    return true;
  });
}
```

Routing should be based on catalog data, scorecard results, usage analytics,
and production behavior.

## Validate catalog entries

Add basic validation so invalid model entries do not reach production.

```ts
export function validateCatalogEntry(entry: AiModelCatalogEntry): string[] {
  const errors: string[] = [];

  if (!entry.modelId) errors.push("modelId is required");
  if (!entry.displayName) errors.push("displayName is required");
  if (entry.modalities.length === 0) errors.push("at least one modality is required");
  if (entry.bestWorkflows.length === 0) errors.push("at least one workflow is required");
  if (entry.languageFit.length === 0) errors.push("at least one language fit is required");
  if (!entry.owner) errors.push("owner is required");
  if (!entry.lastReviewed) errors.push("lastReviewed is required");
  if (entry.status === "approved" && !entry.fallbackModelId) {
    errors.push("approved models should define a fallbackModelId");
  }

  return errors;
}
```

Validation does not need to be complex at first. The goal is to avoid missing
fields and unclear ownership.

## Cost fields

If pricing data is available, keep it near the catalog.

```ts
interface ModelCostProfile {
  modelId: string;
  inputUsdPerMillionTokens?: number;
  outputUsdPerMillionTokens?: number;
  averageCostPerRequestUsd?: number;
  averageCostPerSuccessfulTaskUsd?: number;
  approvedUserTiers: Array<"free" | "pro" | "enterprise">;
  dailyBudgetLimitUsd?: number;
  monthlyBudgetLimitUsd?: number;
  updatedAt: string;
}
```

Cost should be tied to workflow value.

A model that is acceptable for enterprise document analysis may be too
expensive for free-tier background classification.

## Language and region notes

Global AI teams should track language behavior explicitly.

English performance and Chinese performance should not be assumed to be the
same.

Use separate catalog notes or workflow approvals for:

- English prompts
- Chinese prompts
- bilingual prompts
- Chinese RAG documents
- Chinese support conversations
- technical documents with mixed English and Chinese terms

This is especially important when comparing GPT, Claude, Gemini, DeepSeek,
Qwen, Kimi, GLM, MiniMax, Doubao, and other global or Chinese frontier models.

## Suggested catalog views

Start with a few useful views:

1. Approved models by workflow.
2. Testing models by workflow.
3. Fallback-only models.
4. Deprecated or disabled models.
5. Models approved for Chinese or bilingual workflows.
6. Models by cost tier.
7. Models by latency tier.
8. Models missing recent review.

These views help teams maintain the catalog as model choices change.

## Where VectorNode fits

Direct provider integration can make model catalogs fragmented.

Each provider may have separate model names, dashboards, billing exports,
pricing pages, request formats, route behavior, and error patterns.

VectorNode gives developers and AI teams one infrastructure layer for accessing
and managing global and Chinese frontier AI models. That makes it easier to
organize model options, connect usage data to workflows, monitor request
behavior, and control cost.

For teams building chatbots, RAG systems, AI agents, automation workflows,
document analysis tools, and AI SaaS products, a model catalog helps turn
scattered API keys into managed model access.

## Model catalog checklist

Before scaling a multi-model AI product, make sure the team can answer:

1. Which models are approved for each workflow?
2. Which models are still in testing?
3. Which models should only be used as fallback?
4. Which models are deprecated or disabled?
5. Which models are approved for Chinese or bilingual workflows?
6. Which model should each workflow fallback to?
7. Which team owns each model configuration?
8. When was each model last reviewed?
9. What is the expected cost tier for each model?
10. How does the catalog connect to scorecards, routing, and usage analytics?

A useful model catalog does not slow developers down.

It gives them a clearer path to choose the right model for the right workflow.
