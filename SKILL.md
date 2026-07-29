---
name: ai-frontier-dispatch
description: Produce a personalized, source-disciplined AI and markets briefing with portable Claude and Codex workflows, optional live-X research, persistent run and source-health state, and explicit claim-evidence records. Use for a digest, briefing, roundup, morning dispatch, what-did-I-miss request, or scheduled AI and markets review.
---

# AI Frontier Dispatch

Produce one personalized briefing in two separate halves: frontier and builders; then markets, deals, and careers. Filter for the reader instead of summarizing a generic news feed.

## Load the right guidance

1. Read [references/method.md](references/method.md) for gathering, scoring, evidence, and output rules.
2. In Claude Code, also read [adapters/claude.md](adapters/claude.md).
3. In Codex, also read [adapters/codex.md](adapters/codex.md).
4. Do not load both adapter files unless comparing harness behavior.

## Resolve configuration

Look for a user-supplied path, `AI_FRONTIER_DISPATCH_CONFIG`, `~/.ai-frontier-dispatch/config.yaml`, then current task context. Use [config/dispatch.example.yaml](config/dispatch.example.yaml) only as the schema and starter.

Before a first personalized run, obtain the reader profile, interests, exclusions, career track, requested window, and GitHub profile when repo scouting is requested. Never write personal configuration into the public repository unless the user explicitly asks.

## Separate ingestion from judgment

Fan out independent research streams concurrently. Use a cost-efficient model for extraction when the harness permits model tiering. Keep candidate scoring, contradiction handling, claim classification, and final synthesis on the strongest available model.

If tiering or parallel agents are unavailable, preserve the logical separation with batched searches and a distinct final synthesis pass. Never claim to have used a model or tool that was unavailable.

## Open a persistent run

State is optional but recommended. It defaults to `~/.ai-frontier-dispatch/events.jsonl` and stays outside Git.

Before research, run:

```bash
python3 <skill-dir>/scripts/state.py start-run \
  --harness <claude|codex|other> \
  --window-start YYYY-MM-DD \
  --window-end YYYY-MM-DD
```

Retain the emitted `run_id`. If local execution is unavailable, continue without persistence and mention the missing audit trail only when it matters.

## Research and filter

Follow [references/method.md](references/method.md):

1. Establish the freshness window.
2. Gather independent source streams.
3. Normalize and deduplicate candidates.
4. Score recency, reader relevance, and substance before writing.
5. Apply exclusions as a hard filter.
6. Classify material statements as fact, thesis, or deal-status.
7. Prefer primary sources and preserve uncertainty.

Use `scripts/grok-x-pass.py` only when the xAI key is available and the external call is authorized. A failed live-X pass must degrade to primary web research, not block the briefing.

## Record source health

For material source checks, record `ok`, `degraded`, `blocked`, or `failed`:

```bash
python3 <skill-dir>/scripts/state.py record-source \
  --run-id <run_id> \
  --url <url> \
  --stream <stream> \
  --status <status>
```

Record acquisition health, not a sweeping judgment about source truthfulness.

## Record material claims

Record claims that carry numbers, capabilities, causal implications, or changing deal status:

```bash
python3 <skill-dir>/scripts/state.py record-claim \
  --run-id <run_id> \
  --claim <claim> \
  --classification <fact|thesis|deal-status> \
  --confidence <verified|corroborated|single-source|unverified> \
  --source <url>
```

Use repeated `--source` arguments for corroboration. Corroborated claims require at least two distinct URLs. Deal-status claims require `--as-of YYYY-MM-DD`.

## Write the dispatch

### Part A — Frontier & Builders

- model releases and major updates
- AI-native builders and researchers
- personalized GitHub and Hugging Face signal
- AI funding, partnerships, policy, and regulation
- two or three cross-cutting patterns

### Part B — Markets, Deals & Careers

- consulting and strategy
- macro and investment trends
- material market moves
- capital markets, M&A, private equity, venture, and IPOs
- career-track developments
- established AI-stack companies
- optional thesis watch
- two or three cross-cutting patterns

Use a hard visual divider. Prefer one-line takeaways with direct links. Label changing or single-source claims inline. Say “nothing new in this window” when true. Never pad a quiet section.

## Close the run

When the digest is complete, save it only if repository writes are authorized, then run:

```bash
python3 <skill-dir>/scripts/state.py finish-run \
  --run-id <run_id> \
  --status <completed|partial|failed> \
  --digest <optional-path>
```

Validate the ledger when a run behaved unexpectedly:

```bash
python3 <skill-dir>/scripts/state.py validate
```

End with the full formatted digest as the final user-facing response.
