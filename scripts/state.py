#!/usr/bin/env python3
"""Append-only local state for AI Frontier Dispatch.

The ledger stores no API keys and defaults to ~/.ai-frontier-dispatch/events.jsonl.
Set AI_FRONTIER_DISPATCH_HOME or pass --state-file to use another private path.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid


SCHEMA_VERSION = 1
EVENT_TYPES = {"run_started", "source_checked", "claim_recorded", "run_finished"}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def default_state_file() -> Path:
    home = os.environ.get("AI_FRONTIER_DISPATCH_HOME")
    base = Path(home).expanduser() if home else Path.home() / ".ai-frontier-dispatch"
    return base / "events.jsonl"


def event_id(prefix: str) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}_{stamp}_{uuid.uuid4().hex[:8]}"


def read_events(state_file: Path) -> list[dict]:
    if not state_file.exists():
        return []
    events: list[dict] = []
    with state_file.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
            if event.get("schema_version") != SCHEMA_VERSION:
                raise ValueError(f"Unsupported schema version on line {line_number}")
            if event.get("event_type") not in EVENT_TYPES:
                raise ValueError(f"Unknown event type on line {line_number}")
            events.append(event)
    return events


def append_event(state_file: Path, event: dict) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(event, ensure_ascii=False, sort_keys=True)
    with state_file.open("a", encoding="utf-8") as handle:
        handle.write(f"{payload}\n")
        handle.flush()
        os.fsync(handle.fileno())


def run_events(events: list[dict], run_id: str) -> list[dict]:
    return [event for event in events if event.get("run_id") == run_id]


def require_open_run(events: list[dict], run_id: str) -> None:
    matching = run_events(events, run_id)
    if not any(event["event_type"] == "run_started" for event in matching):
        raise ValueError(f"Unknown run id: {run_id}")
    if any(event["event_type"] == "run_finished" for event in matching):
        raise ValueError(f"Run is already finished: {run_id}")


def start_run(args: argparse.Namespace, state_file: Path) -> dict:
    if args.window_start > args.window_end:
        raise ValueError("window-start must be on or before window-end")
    event = {
        "schema_version": SCHEMA_VERSION,
        "event_type": "run_started",
        "event_id": event_id("evt"),
        "run_id": event_id("run"),
        "recorded_at": utc_now(),
        "harness": args.harness,
        "profile": args.profile,
        "window": {"start": args.window_start, "end": args.window_end},
    }
    append_event(state_file, event)
    return event


def record_source(args: argparse.Namespace, state_file: Path) -> dict:
    events = read_events(state_file)
    require_open_run(events, args.run_id)
    source_id = hashlib.sha256(args.url.encode("utf-8")).hexdigest()[:16]
    event = {
        "schema_version": SCHEMA_VERSION,
        "event_type": "source_checked",
        "event_id": event_id("evt"),
        "run_id": args.run_id,
        "recorded_at": utc_now(),
        "source_id": source_id,
        "url": args.url,
        "stream": args.stream,
        "status": args.status,
    }
    if args.title:
        event["title"] = args.title
    if args.error:
        event["error"] = args.error
    append_event(state_file, event)
    return event


def record_claim(args: argparse.Namespace, state_file: Path) -> dict:
    events = read_events(state_file)
    require_open_run(events, args.run_id)
    sources = list(dict.fromkeys(args.source or []))
    if args.confidence == "verified" and not sources:
        raise ValueError("verified claims require at least one source")
    if args.confidence == "corroborated" and len(sources) < 2:
        raise ValueError("corroborated claims require at least two distinct sources")
    if args.classification == "deal-status" and not args.as_of:
        raise ValueError("deal-status claims require --as-of")
    event = {
        "schema_version": SCHEMA_VERSION,
        "event_type": "claim_recorded",
        "event_id": event_id("evt"),
        "run_id": args.run_id,
        "recorded_at": utc_now(),
        "claim_id": event_id("claim"),
        "claim": args.claim,
        "classification": args.classification,
        "confidence": args.confidence,
        "sources": sources,
    }
    if args.as_of:
        event["as_of"] = args.as_of
    if args.notes:
        event["notes"] = args.notes
    append_event(state_file, event)
    return event


def finish_run(args: argparse.Namespace, state_file: Path) -> dict:
    events = read_events(state_file)
    require_open_run(events, args.run_id)
    event = {
        "schema_version": SCHEMA_VERSION,
        "event_type": "run_finished",
        "event_id": event_id("evt"),
        "run_id": args.run_id,
        "recorded_at": utc_now(),
        "status": args.status,
    }
    if args.digest:
        event["digest"] = args.digest
    if args.notes:
        event["notes"] = args.notes
    append_event(state_file, event)
    return event


def materialize(events: list[dict]) -> dict:
    runs: dict[str, dict] = {}
    sources: dict[str, dict] = {}
    for event in events:
        run_id = event["run_id"]
        run = runs.setdefault(run_id, {"run_id": run_id, "sources": [], "claims": []})
        if event["event_type"] == "run_started":
            run.update(
                {
                    "harness": event["harness"],
                    "profile": event["profile"],
                    "window": event["window"],
                    "started_at": event["recorded_at"],
                    "status": "running",
                }
            )
        elif event["event_type"] == "source_checked":
            check = {key: value for key, value in event.items() if key not in {"schema_version", "event_type"}}
            run["sources"].append(check)
            health = sources.setdefault(
                event["source_id"],
                {
                    "source_id": event["source_id"],
                    "url": event["url"],
                    "checks": 0,
                    "failures": 0,
                    "consecutive_failures": 0,
                },
            )
            health["checks"] += 1
            health["last_checked_at"] = event["recorded_at"]
            health["last_status"] = event["status"]
            if event["status"] in {"failed", "blocked"}:
                health["failures"] += 1
                health["consecutive_failures"] += 1
                if event.get("error"):
                    health["last_error"] = event["error"]
            else:
                health["consecutive_failures"] = 0
                health["last_success_at"] = event["recorded_at"]
                health.pop("last_error", None)
        elif event["event_type"] == "claim_recorded":
            run["claims"].append(
                {key: value for key, value in event.items() if key not in {"schema_version", "event_type"}}
            )
        elif event["event_type"] == "run_finished":
            run["status"] = event["status"]
            run["finished_at"] = event["recorded_at"]
            if event.get("digest"):
                run["digest"] = event["digest"]
            if event.get("notes"):
                run["notes"] = event["notes"]
    ordered_runs = sorted(runs.values(), key=lambda run: run.get("started_at", ""), reverse=True)
    return {
        "schema_version": SCHEMA_VERSION,
        "run_count": len(ordered_runs),
        "source_count": len(sources),
        "runs": ordered_runs,
        "source_health": sorted(sources.values(), key=lambda source: source["url"]),
    }


def validate(events: list[dict]) -> dict:
    known_runs: set[str] = set()
    finished_runs: set[str] = set()
    for event in events:
        run_id = event["run_id"]
        if event["event_type"] == "run_started":
            if run_id in known_runs:
                raise ValueError(f"Duplicate run_started event: {run_id}")
            known_runs.add(run_id)
            continue
        if run_id not in known_runs:
            raise ValueError(f"Event references unknown run: {run_id}")
        if run_id in finished_runs:
            raise ValueError(f"Event appears after run_finished: {run_id}")
        if event["event_type"] == "claim_recorded":
            if event["confidence"] == "corroborated" and len(set(event["sources"])) < 2:
                raise ValueError(f"Corroborated claim has fewer than two sources: {event['claim_id']}")
            if event["classification"] == "deal-status" and not event.get("as_of"):
                raise ValueError(f"Deal-status claim is missing as_of: {event['claim_id']}")
        if event["event_type"] == "run_finished":
            finished_runs.add(run_id)
    return {"valid": True, "event_count": len(events), "run_count": len(known_runs)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Frontier Dispatch local state ledger")
    parser.add_argument("--state-file", type=Path, default=default_state_file())
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start-run", help="open a digest run")
    start.add_argument("--harness", required=True, choices=["claude", "codex", "other"])
    start.add_argument("--profile", default="default")
    start.add_argument("--window-start", required=True)
    start.add_argument("--window-end", required=True)

    source = subparsers.add_parser("record-source", help="record one source check")
    source.add_argument("--run-id", required=True)
    source.add_argument("--url", required=True)
    source.add_argument("--stream", required=True)
    source.add_argument("--status", required=True, choices=["ok", "degraded", "blocked", "failed"])
    source.add_argument("--title")
    source.add_argument("--error")

    claim = subparsers.add_parser("record-claim", help="record a claim and its evidence")
    claim.add_argument("--run-id", required=True)
    claim.add_argument("--claim", required=True)
    claim.add_argument("--classification", required=True, choices=["fact", "thesis", "deal-status"])
    claim.add_argument(
        "--confidence",
        required=True,
        choices=["verified", "corroborated", "single-source", "unverified"],
    )
    claim.add_argument("--source", action="append", default=[])
    claim.add_argument("--as-of")
    claim.add_argument("--notes")

    finish = subparsers.add_parser("finish-run", help="close a digest run")
    finish.add_argument("--run-id", required=True)
    finish.add_argument("--status", required=True, choices=["completed", "partial", "failed"])
    finish.add_argument("--digest")
    finish.add_argument("--notes")

    export = subparsers.add_parser("export-run", help="print one materialized run")
    export.add_argument("--run-id", required=True)

    subparsers.add_parser("status", help="print materialized runs and source health")
    subparsers.add_parser("validate", help="validate the append-only ledger")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    state_file = args.state_file.expanduser().resolve()
    try:
        if args.command == "start-run":
            result = start_run(args, state_file)
        elif args.command == "record-source":
            result = record_source(args, state_file)
        elif args.command == "record-claim":
            result = record_claim(args, state_file)
        elif args.command == "finish-run":
            result = finish_run(args, state_file)
        elif args.command == "status":
            result = materialize(read_events(state_file))
        elif args.command == "validate":
            result = validate(read_events(state_file))
        elif args.command == "export-run":
            materialized = materialize(read_events(state_file))
            result = next((run for run in materialized["runs"] if run["run_id"] == args.run_id), None)
            if result is None:
                raise ValueError(f"Unknown run id: {args.run_id}")
        else:
            parser.error(f"Unknown command: {args.command}")
            return 2
    except (OSError, ValueError) as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
