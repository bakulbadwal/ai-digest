# Codex adapter

Use this adapter when running AI Frontier Dispatch in Codex.

## Invocation and paths

- Invoke the installed skill with `$ai-frontier-dispatch`, or ask for an AI Frontier Dispatch briefing.
- Resolve bundled scripts from the skill directory that contains `SKILL.md`.
- Keep the final digest in the current task; do not create a separate task unless the user explicitly asks.

## Research fan-out

- Run independent source streams concurrently with parallel web requests or available agents.
- Use a cost-efficient model for extraction when model overrides are available; reserve the strongest model for scoring, contradiction handling, and synthesis.
- If model tiering is unavailable, preserve the fan-out/synthesis separation in prompts rather than pretending a different model was used.

## Tools

- Use primary web sources for current claims; use official repositories, model cards, filings, and company announcements when available.
- Use the GitHub connector or `gh` for repository facts when available.
- Run `scripts/grok-x-pass.py` only when the local key exists and the user has authorized the external API call.
- Run `scripts/state.py` locally for run state, source health, and claim-evidence records.

## Degradation

- Never invent a connector or unavailable tool.
- If no parallel-agent capability is available, batch independent web queries and keep final judgment in the main context.
- If a source stream fails, record the failure and continue with a partial run when the remaining evidence is sufficient.
