#!/usr/bin/env python3
"""
grok-x-pass.py — pull a live X (Twitter) read from the xAI Grok API.

Grok is (as of 2026) the only frontier model with live grounding to X posts, so
this asks it what the AI/tech world is discussing and shipping over a recent
window. The AI Digest skill folds the answer into its "what builders are doing"
section — so you get X-native signal without having to live on the feed.

Uses the xAI Agent Tools API (POST /v1/responses) with the web_search and
x_search server-side tools. Date filtering isn't a tool param, so the lookback
window is phrased into the prompt.

Auth: reads XAI_API_KEY from the environment, or from ~/.claude/.env
(a line like:  XAI_API_KEY=xai-...). Keep that file private (chmod 600);
this script never prints the key.

Usage:
  python3 grok-x-pass.py --days 4 \
      --prompt "What are top AI-native builders and tech leaders shipping/debating on X?"

Exit codes: 0 ok, 2 no key, 3 API error (error body printed to stderr).
"""
import argparse
import datetime as dt
import json
import os
import sys
import urllib.request
import urllib.error

API_URL = "https://api.x.ai/v1/responses"
ENV_PATH = os.path.expanduser("~/.claude/.env")
DEFAULT_MODEL = "grok-4.5"  # flagship; set a cheaper Grok tier here as a fallback if you like

SYSTEM = (
    "You surface genuine, cutting-edge signal from X (and the web) for a busy reader "
    "who deliberately stays off the feed. Report only substantive posts — launches, "
    "technical debates, notable takes — from credible AI builders, lab leaders, and "
    "tech/VC figures. Skip engagement-bait and unsourced rumor. Attribute each item to "
    "a person, give the gist in one line, and prefer the most recent activity."
)


def load_key():
    key = os.environ.get("XAI_API_KEY")
    if key:
        return key.strip()
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line.startswith("XAI_API_KEY=") and not line.startswith("#"):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def extract_text(data):
    """Handle both the convenience field and the raw Responses output array."""
    if isinstance(data.get("output_text"), str) and data["output_text"].strip():
        return data["output_text"].strip()
    parts = []
    for item in data.get("output", []) or []:
        if item.get("type") == "message":
            for c in item.get("content", []) or []:
                if c.get("type") in ("output_text", "text") and c.get("text"):
                    parts.append(c["text"])
    return "\n".join(parts).strip()


def extract_citations(data):
    cits = data.get("citations")
    if cits:
        return cits
    urls = []
    for item in data.get("output", []) or []:
        for c in item.get("content", []) or []:
            for ann in c.get("annotations", []) or []:
                u = ann.get("url")
                if u and u not in urls:
                    urls.append(u)
    return urls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True, help="what to ask Grok about X")
    ap.add_argument("--days", type=int, default=4, help="lookback window in days")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    key = load_key()
    if not key:
        sys.stderr.write(
            "No XAI_API_KEY found (env or ~/.claude/.env). "
            "Add a line 'XAI_API_KEY=xai-...' to ~/.claude/.env.\n"
        )
        sys.exit(2)

    since = (dt.date.today() - dt.timedelta(days=args.days)).isoformat()
    user = (
        f"{args.prompt}\n\n"
        f"Only include activity from roughly the last {args.days} days "
        f"(since {since}). Focus on X posts; use the web to corroborate."
    )

    body = {
        "model": args.model,
        "instructions": SYSTEM,
        "input": user,
        "tools": [{"type": "web_search"}, {"type": "x_search"}],
    }

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"xAI API error {e.code}: {e.read().decode(errors='replace')}\n")
        sys.exit(3)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"request failed: {e}\n")
        sys.exit(3)

    text = extract_text(data)
    if not text:
        sys.stderr.write(f"empty response; raw keys: {list(data.keys())}\n")
        sys.exit(3)
    print(text)
    cits = extract_citations(data)
    if cits:
        print("\nSources:")
        for c in cits:
            print(f"- {c}")


if __name__ == "__main__":
    main()
