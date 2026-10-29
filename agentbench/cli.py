import argparse
import json
from pathlib import Path

from .benchmark import ModelAgent, compare, eager_agent, evaluate, safe_agent


def demo():
    baseline = evaluate(eager_agent, "eager-baseline")
    candidate = evaluate(safe_agent, "safe-reference")
    return {
        "project": "AgentBench",
        "mode": "synthetic-policy-evaluation",
        "baseline": baseline,
        "candidate": candidate,
        "comparison": compare(baseline, candidate),
        "note": "Reference policies on an authored synthetic suite; these are not real-model rankings.",
    }


def run_cli():
    parser = argparse.ArgumentParser(description="Trace-based agent evaluations")
    sub = parser.add_subparsers(dest="command", required=True)
    demo_command = sub.add_parser("demo")
    demo_command.add_argument("--html", type=Path)
    run = sub.add_parser("run")
    run.add_argument("--candidate", choices=["safe", "eager", "model"], default="safe")
    run.add_argument("--seed", type=int, default=7)
    run.add_argument("--max-steps", type=int, default=10)
    run.add_argument("--output", type=Path)
    diff = sub.add_parser("compare")
    diff.add_argument("baseline", type=Path)
    diff.add_argument("candidate", type=Path)
    args = parser.parse_args()
    if args.command == "demo":
        result = demo()
        if args.html:
            from .report import render

            render(result, args.html)
    elif args.command == "compare":
        result = compare(
            json.loads(args.baseline.read_text()), json.loads(args.candidate.read_text())
        )
    else:
        if args.candidate == "model":
            from .provider import ChatPlanner

            candidate = ModelAgent(ChatPlanner.from_env())
        else:
            candidate = safe_agent if args.candidate == "safe" else eager_agent
        result = evaluate(candidate, args.candidate, args.seed, args.max_steps)
    serialized = json.dumps(result, indent=2)
    if getattr(args, "output", None):
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n")
    print(serialized)
    if args.command == "compare" and not result["passed"]:
        raise SystemExit(1)


def main():
    import sqlite3
    import sys

    try:
        run_cli()
    except (ValueError, KeyError, OSError, sqlite3.Error, RuntimeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        raise SystemExit(2) from None
