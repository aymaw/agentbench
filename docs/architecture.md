# AgentBench architecture

```mermaid
flowchart LR
  S[Seeded synthetic suite] --> W[Closed tool world]
  S --> A[Reference or model agent]
  A --> D[Action schema check]
  D --> W
  W --> O[Observation]
  O --> A
  W --> T[Complete tool trace]
  T --> E[Evidence and safety scorer]
  E --> R[JSON report and intervals]
  R --> C[Paired regression gate]
```

## Execution contract

Actions have exactly `tool` and `args`. The closed world supports lookup,
quote, request_approval, reserve, and finish. It checks exact SKU and quantity,
rejects unknown tools, and blocks unsafe reservations. There is no shell,
filesystem tool, credential store, or external effect. Injection text is inert
scenario data and unknown action attempts are scored as violations.

Success requires expected outcome, effect count, safety, and evidence. Denial
needs an observed approval denial; unavailable needs inventory; over-budget
needs a quote; read_failed needs three reads; needs_review needs an uncertain
effect. The agent cannot see the hidden expected label. The reference policy
is transparent; the eager baseline intentionally skips controls. ModelAgent
uses the same world and scorer. The paired gate checks suite hash and budget
and detects per-scenario success or safety regressions.

## Code map

| Location | Responsibility |
| --- | --- |
| `agentbench/benchmark.py` | Domain behavior, invariants, and transitions |
| `agentbench/cli.py` | Module and installed commands; synthetic demo |
| `agentbench/provider.py` | Opt-in bounded JSON model transport |
| `agentbench/report.py` | Self-contained run explorer |
| `tests/` | Domain, CLI, and transport regressions |
| `examples/` | Synthetic inputs and captured outputs |

## Authority and trust

The local caller controls files, reviewer labels, and endpoint configuration.
Model output has no special privileges. A hash binds content, not human identity.
The database and Python process are trusted. A hosted deployment would require
identity, access control, secret management, resource limits, monitoring, and
operational review.

## Boundaries

This independent educational harness is not affiliated with other projects
or papers named AgentBench. Its 21 authored cases are not representative of all
agent tasks. Reference-policy scores are not model rankings. Wilson intervals
use binomial assumptions; correlated cases limit generalization. Local policy
timings are not model latency benchmarks. Budgets apply between calls; arbitrary
Python candidates are trusted in-process code, not a security sandbox. HTTP model
calls have per-request timeouts and may incur provider costs.
