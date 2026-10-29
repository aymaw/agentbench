# AgentBench walkthrough

Start with `python3 -m agentbench demo --html .runs/demo.html`. This creates a
fresh synthetic scenario, executes it, and prints the actual result. Open the
HTML artifact to inspect evidence and export JSON.

## Work with the CLI

```sh
python3 -m agentbench run --candidate eager --output .runs/baseline.json
python3 -m agentbench run --candidate safe --output .runs/candidate.json
python3 -m agentbench compare .runs/baseline.json .runs/candidate.json
# Reverse the files to demonstrate a failing gate (exit 1).
python3 -m agentbench compare .runs/candidate.json .runs/baseline.json
```

Reports include suite hash, seed, budget, episode trace, outcome, evidence
sufficiency, effect count, violations, duration, rates, and a Wilson interval.
A candidate is a callable `(task, trace) -> action`. It receives JSON copies,
so input mutation cannot rewrite the evaluator's evidence.

## Reproduce and inspect

```sh
python3 -m agentbench demo > demo.json
python3 -m unittest discover -s tests -v
```

`examples/demo.json` was captured from this implementation. Identifiers and
labels are synthetic. AgentBench timings vary with hardware and scheduling;
suite identity and policy outcomes remain reproducible.

## Expected failures

Invalid domain operations print a JSON error to stderr and exit 2. AgentBench's
regression gate exits 1 when a scenario regresses. Tests exercise invalid actions
and verify rejected or rolled-back state changes. No test needs external
credentials or a live model.
