# Claude adapter

Use this adapter when running AI Frontier Dispatch in Claude Code.

## Invocation and paths

- Invoke the installed plugin with `/ai-frontier-dispatch`.
- Resolve bundled scripts from `$CLAUDE_PLUGIN_ROOT` when installed as a plugin.
- If running from a clone, resolve paths from the directory containing `SKILL.md`.

## Research fan-out

- Run independent gathering tasks in parallel.
- Use a cost-efficient research model for extraction and the strongest available model for final ranking and synthesis.
- Give gathering agents only the source stream, date window, profile, and output schema they need.
- Do not let gathering agents write the final digest or assign final confidence.

## Tools

- Use Claude Code web/search capabilities for primary-source research.
- Run `scripts/grok-x-pass.py` only when `XAI_API_KEY` is available.
- Run `scripts/state.py` through Bash for state and evidence records.

## Degradation

- If subagents are unavailable, parallelize independent searches where possible and synthesize in the main context.
- If the Grok pass is unavailable, continue with primary web sources and state the missing stream only when it materially affects coverage.
