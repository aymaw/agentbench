# Scope and evidence

AgentBench evaluates observable behavior in a closed synthetic tool environment. It checks outcomes, evidence, effect counts, and attempted policy violations instead of grading only the final answer.

Source, synthetic fixtures, tests, installed commands, and demo artifacts are the
evidence. JSON and HTML examples record completed runs; they are not a hosted
service. Provider tests use mocked responses and do not establish the quality of
any specific running model.

## Limits

This independent educational harness is not affiliated with other projects
or papers named AgentBench. Its 21 authored cases are not representative of all
agent tasks. Reference-policy scores are not model rankings. Wilson intervals
use binomial assumptions; correlated cases limit generalization. Local policy
timings are not model latency benchmarks. Budgets apply between calls; arbitrary
Python candidates are trusted in-process code, not a security sandbox. HTTP model
calls have per-request timeouts and may incur provider costs.

No production scale, vendor connectivity, clinical safety, business outcomes,
or model superiority is claimed. CI configuration and locally passing checks
are separate from a verified remote CI run.
