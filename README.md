![AI Frontier Dispatch](docs/banner.svg)

# AI Frontier Dispatch

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-adapter-8A63D2)](https://code.claude.com/docs/en/skills)
[![Codex](https://img.shields.io/badge/Codex-adapter-111827)](https://developers.openai.com/codex/)

**A personalized, source-disciplined AI + markets briefing that runs in Claude Code or Codex—and keeps its evidence trail local.**

AI Frontier Dispatch gathers frontier releases, builder signal, repositories, markets, deals, and career developments, then filters them against one reader's interests and explicit exclusions. It is a self-run skill: no hosted backend, subscriber list, or shared personal profile.

![A run of AI Frontier Dispatch](docs/demo.gif)

### [Read a real digest →](digests/2026-07-28.md)

## What changed in v2

- One portable dispatch protocol instead of a Claude-only method.
- Thin Claude and Codex adapters for tool and orchestration differences.
- Optional append-only local state for run history and source health.
- Explicit claim records that distinguish facts, theses, and changing deal status.
- JSON Schemas and a dependency-free state CLI with tests.

The digest still works without state. Persistence improves freshness, failure routing, and auditability without turning the project into a hosted application.

## Architecture

```text
reader config
    ↓
portable skill + dispatch method
    ↓
Claude adapter  OR  Codex adapter
    ↓
independent research streams → dedupe → score → evidence rules
    ↓                                  ↘
two-part digest                    local event ledger
```

Personal config and state default to `~/.ai-frontier-dispatch/`, outside the repository.

## What is in the briefing

| Part A — Frontier & Builders | Part B — Markets, Deals & Careers |
|---|---|
| Model releases and capability updates | Consulting and strategy |
| What AI-native builders are shipping | Macro and investment trends |
| Personalized GitHub and Hugging Face scout | Capital markets, M&A, PE/VC, and IPOs |
| AI funding, partnerships, and regulation | Career-track developments |
| Cross-cutting technical patterns | The established AI stack and thesis watch |

The filter scores recency, reader relevance, and substance before spending synthesis tokens. Independent arrival across streams is a positive ranking signal. Primary evidence beats aggregator repetition, and an honest quiet section beats filler.

## Method provenance

The filtering method combines documented patterns from established open-source digest projects:

| Pattern | Source |
|---|---|
| Multi-source corroboration as a positive ranking signal | [ai-news-radar](https://github.com/LearnPrompt/ai-news-radar) |
| Fan out, deduplicate by URL, rank, then filter | [agents-radar](https://github.com/duanyytop/agents-radar) |
| Explicit negative preferences beside positive interests | [ArxivDigest](https://github.com/AutoLLM/ArxivDigest) |
| Separate scoring axes instead of one blended score | [ai-daily-digest](https://github.com/HarrisHan/ai-daily-digest) |
| Never invent content beyond the source | [follow-builders](https://github.com/zarazhangrui/follow-builders) |

See the [case study](CASE_STUDY.md) for the product decisions, tradeoffs, and roadmap.

## Install

### Claude Code plugin

```bash
/plugin marketplace add bakulbadwal/ai-frontier-dispatch
/plugin install ai-frontier-dispatch
```

Invoke with `/ai-frontier-dispatch`.

### Codex skill

```bash
git clone https://github.com/bakulbadwal/ai-frontier-dispatch.git ~/.codex/skills/ai-frontier-dispatch
```

Invoke with `$ai-frontier-dispatch`, or ask for an AI Frontier Dispatch briefing.

### Run from a clone

Claude Code can load the repo with `claude --plugin-dir /path/to/ai-frontier-dispatch`. Codex can use the repository's `SKILL.md` directly when the repo is in its configured skills path.

## Configure

Copy the example to your private state directory:

```bash
mkdir -p ~/.ai-frontier-dispatch
cp config/dispatch.example.yaml ~/.ai-frontier-dispatch/config.yaml
```

Customize:

- `reader_profile`: the role, projects, hiring, recruiting, or investing context that defines relevance.
- `interest_areas` and `github_profile`: the repository scout's taste profile.
- `exclude_topics` and `never_recommend`: explicit negative preferences.
- `career_track`: the roles and companies worth monitoring.
- `thesis_watch`: one falsifiable claim with dated baselines.

The skill also accepts `AI_FRONTIER_DISPATCH_CONFIG` or a user-supplied config path. Never commit a personal config to a public fork.

## Optional live-X pass

Set `XAI_API_KEY` in the environment or in `~/.claude/.env`, then run:

```bash
python3 scripts/grok-x-pass.py --days 3 \
  --prompt "What are AI-native builders shipping or debating on X?"
```

Grok is an optional signal stream, not a hard dependency. The dispatch degrades to primary web research when it is unavailable.

## Local state and evidence

The state CLI writes append-only JSONL to `~/.ai-frontier-dispatch/events.jsonl` by default. It stores run metadata, source checks, and material claims—not API keys or scraped page contents.

```bash
# Open a run
python3 scripts/state.py start-run \
  --harness codex \
  --window-start 2026-07-26 \
  --window-end 2026-07-29

# Record source acquisition health
python3 scripts/state.py record-source \
  --run-id RUN_ID \
  --url https://example.com/primary \
  --stream official \
  --status ok

# Record a corroborated fact
python3 scripts/state.py record-claim \
  --run-id RUN_ID \
  --claim "A material event occurred." \
  --classification fact \
  --confidence corroborated \
  --source https://example.com/primary \
  --source https://example.org/corroboration

# Close and inspect
python3 scripts/state.py finish-run --run-id RUN_ID --status completed
python3 scripts/state.py status
python3 scripts/state.py validate
```

The CLI rejects corroborated claims with fewer than two distinct sources and deal-status claims without an as-of date.

## Source discipline

- Prefer official announcements, filings, model cards, release notes, and repositories.
- Label attributable but unconfirmed material as single-source.
- Keep theses separate from checkable facts.
- Give financing, acquisition, partnership, and IPO status an as-of date.
- Record access failures as source-health events rather than silently dropping a stream.
- Treat stars, trending positions, likes, and downloads as discovery signals—not proof of quality.

## Model and cost tiering

Research fan-out is ingestion; final synthesis is judgment. Use a cost-efficient model for independent extraction when the harness permits it, then reserve the strongest model for ranking, contradictions, evidence classification, and the final patterns. The adapters describe how each harness degrades when model overrides or parallel agents are unavailable.

## Files

| Path | Purpose |
|---|---|
| `SKILL.md` | Portable orchestration protocol |
| `adapters/claude.md` | Claude Code execution adapter |
| `adapters/codex.md` | Codex execution adapter |
| `references/method.md` | Detailed research, scoring, and evidence method |
| `config/dispatch.example.yaml` | Private reader-config template |
| `scripts/state.py` | Append-only run, source-health, and claim ledger |
| `schemas/` | Claim, source, and run contracts |
| `scripts/grok-x-pass.py` | Optional live-X pass through xAI |
| `digests/` | Example and archived briefing output |

## Validation

```bash
python3 -m unittest -v tests/test_state.py
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

## License

MIT — see [LICENSE](LICENSE).

Built by [Bakul Badwal](https://github.com/bakulbadwal), UVA Darden MBA '27.
