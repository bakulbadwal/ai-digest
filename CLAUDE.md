# AI Frontier Dispatch — agent instructions

A personalized AI + markets briefing that runs inside a user's own harness. **This is a
distributed plugin other people install** — changes affect strangers' setups, not just Bakul's.
Treat it as a product with users, not a personal script.

## What that means in practice

- **The dispatch protocol is portable by design.** One protocol, thin adapters in `adapters/` for
  Claude Code and Codex. Do not push harness-specific behavior into the protocol — that's what the
  adapters exist for, and collapsing them was the exact thing v2 fixed.
- **Schemas are a contract.** `schemas/` defines the claim records and state format; `tests/`
  guards them. Adding a field is fine; changing or removing one breaks existing users' local state.
- **State is optional and append-only.** The digest must still work with no persistence at all.
  Never make state a hard dependency.

## Source discipline is the product

The briefing's value is that it distinguishes what's known from what's claimed:

- **Claim records separate facts from theses from changing deal status.** Preserve that distinction
  in any prompt or template edit; collapsing them into flat prose destroys the point.
- **Two-source corroboration** for material claims. An empty section is a correct output — never
  pad a digest to look fuller.
- **Never cite an unverified hook** (half-remembered videos, "X launched today"). Verify or omit.
- Evidence trail stays **local**. No hosted backend, no shared profile, no subscriber list.

## Practical

- Default branch is **`master`**, not `main`.
- `config/` holds the reader's interests and explicit exclusions — it is *configuration as product*.
  Personal values belong there, never hardcoded into the protocol.
- `digests/` holds real published runs; they're public examples, so treat them as shipped work.
- `docs/demo.gif` and `docs/banner.svg` are reused on the GitHub profile README.
- Grok API supplies live X signal; keys come from `~/.claude/.env`, never committed.

Shared personal context (global conventions, memory index, cached research): see
`~/.codex/AGENTS.md` for the map, or `~/.claude/CLAUDE.md` directly.
