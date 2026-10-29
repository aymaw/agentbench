<p align="center"><img src="docs/banner.svg" alt="AgentBench — Evaluate what the agent did." width="100%"></p>

<p align="center">
<a href="https://github.com/aymaw/agentbench/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/aymaw/agentbench/actions/workflows/ci.yml/badge.svg"></a>
<img alt="Python 3.11+" src="https://img.shields.io/badge/python-3.11%2B-3776AB?style=flat-square">
<img alt="Standard library runtime" src="https://img.shields.io/badge/runtime-standard_library-263844?style=flat-square">
<a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-64748b?style=flat-square"></a>
</p>

<p align="center"><b>A small evaluation harness for tool behavior, faults, and unsafe attempts.</b></p>
<p align="center"><a href="#try-it-in-a-minute">Quickstart</a> · <a href="docs/architecture.md">Architecture</a> · <a href="docs/tutorial.md">Walkthrough</a> · <a href="docs/demo.html">Run explorer</a> · <a href="docs/scope.md">Scope</a></p>

AgentBench evaluates observable behavior in a closed synthetic tool environment. It checks outcomes, evidence, effect counts, and attempted policy violations instead of grading only the final answer.

## Why this exists

An agent can produce the right sentence after taking the wrong action. AgentBench makes the trace the unit of evaluation: Did it inspect inventory, respect the budget, obtain approval, and stop after an uncertain write?

## Try it in a minute

Python 3.11 or later. The demo needs no packages, account, model download, or API key.

```sh
git clone https://github.com/aymaw/agentbench.git
cd agentbench
python3 -m agentbench demo --html .runs/demo.html
python3 -m unittest discover -s tests -v
```

Open `.runs/demo.html` in a browser to inspect the recorded run. JSON is printed
to stdout. The explorer filters records and shows their exact evidence; it does
not execute tools or make network requests. A captured run is in
[`examples/demo.json`](examples/demo.json). Download [`docs/demo.html`](docs/demo.html)
to open the checked-in viewer; GitHub source view does not execute HTML.

```text
reference policy: 21 / 21 scenarios pass
reference safety: 100%
eager baseline: unsafe attempts detected
model evaluation: opt-in, not measured by this demo
```

The default is a **deterministic synthetic demonstration**. The optional model
path calls your explicitly configured endpoint. Demo results are not live model
measurements. All included records and entities are fictional.

<details>
<summary>See the recorded run explorer</summary>

![Recorded synthetic demonstration](docs/preview.png)

</details>

## What is implemented

| Capability | Concrete behavior |
| --- | --- |
| **21 reproducible scenarios** | Normal operations, capacity, denial, read faults, uncertain writes, injection, and 12 seeded variations. |
| **Attempt-aware safety** | The runtime blocks unsafe writes; the evaluator still counts attempted violations. |
| **Evidence-grounded scoring** | Guessed refusals and unsupported success claims cannot pass on matching final text alone. |
| **Paired regression gate** | Compare suite hashes and budgets; fail on previously passing or safe scenarios that regress. |

## How it works

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

The [architecture contract](docs/architecture.md) explains state transitions,
transaction boundaries, failure handling, and the exact guarantees.

## Use it from Python

```python
from agentbench.benchmark import evaluate, safe_agent, eager_agent, compare

baseline = evaluate(eager_agent, "eager-baseline", seed=7)
candidate = evaluate(safe_agent, "safe-reference", seed=7)
assert candidate["success_rate"] == 1.0
assert compare(baseline, candidate)["passed"]
# Supply your own callable or ModelAgent to evaluate().
```

For an installed command, run `python3 -m pip install .`, then `agentbench --help`.
Installation needs setuptools as a build dependency; the runtime has no external
dependencies. Module commands above run directly from the checkout offline.

## Bring a model

The optional JSON transport works with a compatible local or remote chat endpoint.
It sends no data until a model command is called.

```sh
export MODEL_BASE_URL=http://127.0.0.1:11434/v1
export MODEL_NAME=your-installed-model
# For an authenticated endpoint, set MODEL_API_KEY in your environment.
python3 -m agentbench run --candidate model --seed 7 --output .runs/model.json
```

Use a model already installed at that endpoint. No weights are downloaded or
distributed. Remote endpoints require HTTPS. Redirects are disabled, requests
are bounded to 64 KB, responses to 1 MB, and requests time out after 30 seconds.
Model proposals pass deterministic checks before domain changes. Read the
[transport contract](docs/model-provider.md) and [security notes](SECURITY.md).

## Engineering checks

Reference outcomes, unsafe attempts, missing evidence, injected tool names, denials, uncertain effects, read limits, malformed actions, trace isolation, and regression gates.

CI tests, builds and installs the package, checks formatting and lint, compiles
modules, and produces a demo artifact. The configured matrix covers Python
3.11–3.14 on Linux and Python 3.13 on macOS and Windows. A verified green remote
run requires publication and an actual successful Actions run.

```sh
make check
# Optional contributor tooling:
python3 -m pip install '.[dev]'
ruff check .
ruff format --check .
```

Local evidence: [verification record](docs/validation.md).

## Scope

This independent educational harness is not affiliated with other projects
or papers named AgentBench. Its 21 authored cases are not representative of all
agent tasks. Reference-policy scores are not model rankings. Wilson intervals
use binomial assumptions; correlated cases limit generalization. Local policy
timings are not model latency benchmarks. Budgets apply between calls; arbitrary
Python candidates are trusted in-process code, not a security sandbox. HTTP model
calls have per-request timeouts and may incur provider costs.

Original personal portfolio work, with no employer affiliation or copied company
implementation. [Provenance](docs/provenance.md) · [MIT license](LICENSE) ·
[Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md)
