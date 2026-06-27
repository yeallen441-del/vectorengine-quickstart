# AI Model Incident Response Runbook for Multi-Model Apps

Production AI systems can fail even when the integration is correct.

A model route can become slow. A provider can return errors. JSON output can
start failing validation. A workflow can suddenly use too many tokens. A
fallback model can recover requests but make latency unacceptable. A Chinese or
bilingual workflow can regress while English traffic still looks normal.

For teams building chatbots, RAG systems, AI agents, automation workflows,
internal tools, and AI SaaS products, these issues need an incident response
process.

VectorNode is a multi-model AI infrastructure platform for developers and AI
teams. It helps teams access, manage, monitor, and optimize global and Chinese
frontier AI models from one developer platform.

This runbook shows how to detect, triage, mitigate, and review model incidents
in multi-model AI applications.

Learn more:

https://www.vectronode.com/

## What counts as an AI model incident?

An AI model incident is any production issue where model behavior, model
access, routing, latency, output format, usage, or cost creates user impact or
operational risk.

Examples:

- API requests to a model route start timing out
- error rate increases for one workflow
- p95 latency becomes too high for chat
- RAG answers stop using retrieved context correctly
- agent tool arguments become invalid
- JSON extraction fails validation
- fallback rate increases unexpectedly
- token usage spikes for one feature
- cost per successful task rises sharply
- Chinese or bilingual responses regress
- one provider route becomes unavailable

The incident may affect all traffic, one workflow, one model family, one
region, one language, or one user tier.

## Start with severity levels

Define severity before an incident happens.

| Severity | Meaning | Example |
| --- | --- | --- |
| SEV1 | Major user impact or production outage | all model requests fail |
| SEV2 | Important workflow degraded | RAG answers fail or chat latency is unusable |
| SEV3 | Limited workflow or user tier impact | free-tier automation has high retry rate |
| SEV4 | Internal issue with no clear user impact | staging route is slow |

Severity should consider user impact, business impact, data risk, and whether
there is a working fallback.

## Detect incidents by workflow

Do not rely only on one global health check.

Track signals by workflow:

| Workflow | Incident signals |
| --- | --- |
| `support_chat` | high latency, weak answers, high fallback rate |
| `rag_answer` | grounding failures, long prompts, context mismatch |
| `agent_planning` | invalid tool arguments, repeated retries |
| `json_extraction` | schema validation failures, parse errors |
| `automation_task` | batch failures, cost spikes, retry loops |
| `multilingual_reply` | English/Chinese quality regression |

This helps the team identify whether the issue is global or workflow-specific.

## Use an incident record

Create one structured incident record.

```ts
type IncidentSeverity = "SEV1" | "SEV2" | "SEV3" | "SEV4";

type IncidentStatus =
  | "investigating"
  | "mitigating"
  | "monitoring"
  | "resolved";

type Workflow =
  | "support_chat"
  | "rag_answer"
  | "agent_planning"
  | "json_extraction"
  | "automation_task"
  | "multilingual_reply";

interface AiModelIncident {
  id: string;
  openedAt: string;
  resolvedAt?: string;
  severity: IncidentSeverity;
  status: IncidentStatus;
  affectedWorkflows: Workflow[];
  affectedModels: string[];
  affectedRoutes?: string[];
  affectedUserTiers?: Array<"free" | "pro" | "enterprise">;
  symptoms: string[];
  currentMitigation?: string;
  owner: string;
  notes: string[];
}
```

The record should be simple enough to fill out during an incident.

## First 10 minutes

The first goal is not to find the perfect root cause.

The first goal is to limit user impact.

Checklist:

1. Confirm the affected workflow.
2. Confirm the affected model or route.
3. Check whether the issue is new or already known.
4. Check whether fallback is working.
5. Check whether cost or token usage is spiking.
6. Assign an owner.
7. Decide whether to disable a model, reduce traffic, or switch routes.
8. Start a short incident log.

Avoid debating long-term architecture during the first response window.

## Useful detection queries

The exact query system depends on your logging stack, but the questions are
usually the same.

Ask:

- Did error rate increase by workflow?
- Did timeout rate increase by model?
- Did p95 latency increase by route?
- Did validation failure rate increase?
- Did fallback rate increase?
- Did token usage increase for one workflow?
- Did cost per successful task increase?
- Did the issue affect only one language or region?

The model incident response process should use the same usage analytics fields
that the application already logs.

## Mitigation options

Use the smallest mitigation that reduces user impact.

Common options:

- switch a workflow to a fallback model
- reduce candidate model traffic to zero
- disable one broken route
- lower max tokens temporarily
- disable a non-critical workflow
- pause batch automation jobs
- move free-tier traffic to an efficient model
- route enterprise traffic to the stable model
- turn off tool use for one agent workflow
- add stricter JSON validation and retry rules

The right mitigation depends on the workflow.

A support chatbot may need a faster fallback. A RAG system may need stricter
context limits. An automation workflow may be safe to pause. An enterprise
workflow may need to stay on the most stable model path.

## Model health state

Keep model health in configuration so the application can react quickly.

```ts
type ModelHealthState = "healthy" | "degraded" | "disabled";

interface ModelHealth {
  model: string;
  route?: string;
  state: ModelHealthState;
  reason?: string;
  updatedAt: string;
}

function canUseModel(health: ModelHealth): boolean {
  return health.state === "healthy";
}
```

When a model is degraded, the router can reduce traffic or limit it to
low-risk workflows. When a model is disabled, the router should use a fallback
or return a controlled error.

## Fallback should be workflow-aware

Fallback is not always the same for every workflow.

```ts
interface WorkflowFallbackPolicy {
  workflow: Workflow;
  primaryModel: string;
  fallbackModel: string;
  fallbackOn: Array<"timeout" | "rate_limit" | "server_error" | "validation_failed">;
  maxFallbackLatencyMs: number;
}
```

Examples:

- `support_chat` can fallback on timeout or server error
- `rag_answer` may require a model that handles long context
- `json_extraction` may fallback only when validation fails
- `automation_task` may retry later instead of using a more expensive model
- `multilingual_reply` may fallback to a model tested for Chinese or bilingual
  quality

Fallback should improve the user experience. If fallback makes latency or
quality worse, it may not be the right mitigation.

## Cost spike response

Cost spikes need a separate response path.

Common causes:

- prompts became longer after a product change
- a RAG workflow retrieved too many passages
- an agent loop made too many model calls
- fallback used a more expensive model too often
- free-tier traffic hit a high-cost workflow
- a candidate model produced longer responses than expected

Immediate actions:

1. identify the workflow creating the spike
2. reduce max input or output tokens
3. pause non-critical batch jobs
4. move low-value traffic to an efficient model
5. disable expensive fallback for non-critical workflows
6. review the prompt, retrieval, or agent loop that changed

Cost incidents should be measured by cost per successful task, not only total
spend.

## Latency incident response

Latency issues should be handled by workflow.

For chat, high latency can directly hurt the user experience. For background
automation, the same latency may be acceptable.

Immediate actions:

- lower max output tokens for chat workflows
- switch chat to a faster fallback model
- reduce retrieved context size for RAG
- pause slow agent loops
- move batch jobs out of peak traffic windows
- separate interactive and background workflows

Track p50 and p95 latency separately. Averages can hide the tail latency that
users actually feel.

## JSON and structured output incidents

Structured output incidents are common in agent and automation workflows.

Symptoms:

- parse errors
- missing required fields
- invalid enum values
- extra prose around JSON
- tool arguments do not match the schema
- retries succeed but cost increases

Mitigation:

- add stricter validation before accepting output
- retry with a more explicit schema prompt
- fallback to a model with better structured output behavior
- temporarily disable downstream automation actions
- log validation failures by workflow and model

Do not let invalid structured output trigger irreversible product actions.

## Chinese and bilingual workflow incidents

Global products should track language-specific regressions.

Symptoms:

- Chinese answers become less natural
- mixed English and Chinese prompts are misunderstood
- terminology changes unexpectedly
- Chinese RAG passages are not used correctly
- bilingual summaries lose important details
- coding prompts with Chinese comments perform worse

Mitigation:

- route Chinese workflows to a tested model
- use a language-specific fallback policy
- reduce rollout traffic for bilingual workflows
- review examples with native speakers when quality matters
- separate English and Chinese evaluation dashboards

Models such as GPT, Claude, Gemini, DeepSeek, Qwen, Kimi, GLM, MiniMax, and
Doubao may behave differently across language and workflow combinations.

## Communication during an incident

Keep communication short and factual.

Internal update format:

```text
Status: investigating
Severity: SEV2
Affected workflow: rag_answer
Affected model/route: candidate reasoning route
User impact: higher latency and validation failures for document answers
Mitigation: routing production traffic back to stable model
Next update: 15 minutes
```

If customers are affected, explain the product impact without exposing internal
provider details that are not useful to users.

## Resolution criteria

Do not close an incident just because one request succeeds.

Close it when:

- error rate returns to normal
- latency returns to an acceptable range
- fallback rate returns to normal
- validation failures return to normal
- cost per successful task is stable
- affected workflows are back on stable routing
- the team has captured the timeline and follow-up tasks

Keep monitoring after mitigation. Some model incidents reappear when traffic
patterns change.

## Post-incident review

Every meaningful incident should produce a short review.

Include:

- what happened
- which workflows were affected
- which models or routes were involved
- how the issue was detected
- what mitigation worked
- what mitigation did not work
- whether fallback helped or hurt
- whether cost, latency, or quality was most affected
- what should change in monitoring, routing, rollout, or evaluation

The goal is not blame. The goal is to make the next incident smaller.

## Where VectorNode fits

Direct provider integration can make incident response fragmented.

Each provider may have different error formats, dashboards, billing views,
latency patterns, rate limits, model names, and support workflows.

VectorNode helps developers and AI teams work with global and Chinese frontier
models through one infrastructure platform. That gives teams a clearer place
to manage model access, monitor request behavior, compare model choices, and
adjust routing when production behavior changes.

For teams building chatbots, RAG systems, AI agents, automation workflows, and
AI SaaS products, a model incident response runbook makes multi-model
operations more predictable.

## Runbook checklist

Before the next incident, make sure your team has:

- workflow-level usage and latency tracking
- error rate and timeout alerts by model
- validation failure alerts for structured output
- fallback policies by workflow
- model health state in configuration
- cost spike alerts
- language-specific checks when needed
- a kill switch for risky models or routes
- an incident owner during production issues
- a post-incident review process

Multi-model AI systems are easier to operate when incidents are expected,
measured, and reversible.
