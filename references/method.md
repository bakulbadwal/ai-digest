# Dispatch method

Use this reference for candidate gathering, scoring, source discipline, and final synthesis.

## 1. Establish the window

1. Read the latest completed run from the state ledger when enabled.
2. Otherwise read the most recent `digests/YYYY-MM-DD.md` filename.
3. Use the configured cadence only when neither exists.
4. Date-check every candidate against the resulting window.

## 2. Gather independent streams

Gather these streams independently before ranking:

- Official model-lab, product, and company announcements.
- AI-native builder and researcher activity.
- Hacker News front page, `/show`, and recent high-signal results.
- Personalized GitHub and Hugging Face releases/trending candidates.
- Reputable AI funding, partnership, policy, and regulation coverage.
- Consulting, macro, capital-markets, M&A/VC, career, and established-stack sources.
- Optional live-X pass through Grok.

For Hacker News, fan out across `AI`, `LLM`, `agents`, major labs, and one reader-domain term. Merge, deduplicate by canonical URL, rank by relevance, and inspect only the strongest candidates.

For GitHub and Hugging Face, treat stars, likes, downloads, and trending placement as discovery signals—not proof of quality. Prefer release notes, documentation, commits, model cards, and direct project evidence.

## 3. Normalize and deduplicate

Represent every candidate with:

- canonical URL
- title and event date
- source stream
- one-sentence factual claim
- reader relevance
- source type: primary, established press, aggregator, or social

Merge candidates that describe the same underlying event. Preserve all independent source URLs on the merged record.

## 4. Score before writing

| Axis | Range | Test |
|---|---:|---|
| Recency | 0–2 | New inside the current window |
| Reader relevance | 0–2 | Specifically matches the configured profile |
| Substance | 0–1 | Launch, decision, number, filing, benchmark, or real debate |

Write a full item only at 3/5 or above. Add one ranking point when the story arrived independently through two or more streams. Subtract one when only aggregator/content-farm sources support it. Apply configured exclusions as a hard filter after scoring.

## 5. Enforce claim discipline

Classify material statements before synthesis:

- `fact`: an event, measurement, quotation, product capability, or other checkable statement.
- `thesis`: an interpretation, causal view, forecast, or strategic implication.
- `deal-status`: financing, acquisition, partnership, IPO, or transaction state that can change.

Use these confidence labels:

- `verified`: directly supported by a suitable primary source.
- `corroborated`: supported by at least two independent sources.
- `single-source`: attributable, but not independently confirmed.
- `unverified`: lead or rumor that should usually be omitted.

Deal-status claims must include an as-of date. Never promote a thesis to fact through repetition. If sources conflict, describe the conflict or omit the claim.

## 6. Track source health

Record material source checks when persistence is enabled:

- `ok`: source was reachable and useful.
- `degraded`: reachable but incomplete, stale, or structurally changed.
- `blocked`: access denied, paywalled, robots-blocked, or authentication-gated.
- `failed`: request or parsing failed.

Repeated failure is a routing signal. It does not make the source unreliable; it means the acquisition path needs replacement or repair.

## 7. Synthesize two separate halves

### Part A — Frontier & Builders

- Model releases and major updates.
- What AI-native builders are shipping or debating.
- Personalized GitHub and Hugging Face signal.
- AI funding, partnerships, policy, and regulation.
- Two or three cross-cutting patterns.

### Part B — Markets, Deals & Careers

- Consulting and strategy.
- Macro and investment trends.
- Compact market pulse only when something moved.
- Capital markets, M&A, private equity, venture, and IPO activity.
- Career-track developments.
- The established AI stack.
- Optional thesis watch.
- Two or three cross-cutting patterns.

Keep a hard visual divider between the halves.

## 8. Run a thesis watch that can lose

A thesis watch is the optional Part B section where the reader tracks a standing hypothesis across runs. Configure it only when the reader has one. Its value comes entirely from being falsifiable, so structure it as instrumentation rather than as a recurring argument.

Define each watch with three parts:

- **A primary tell.** The single observable the reader believes moves first, with a numeric baseline and a stated threshold. Without a threshold there is no way to be wrong.
- **Secondary conditions.** Supporting observables that would corroborate the thesis but are not decisive alone.
- **A concealed channel.** Where the same risk would accumulate if the primary tell stayed quiet — off-balance-sheet structures, privately marked assets, lagged or discretionary valuations, adjacent leverage. Most theses fail here rather than being wrong, because the visible instrument is the one everyone else is also watching, and pressure routes around it.

Report only what moved since the last run. Zero lines is a valid result.

Three rules keep the section honest:

1. **Lead with disconfirming movement.** When the primary tell moves against the thesis, say so first and plainly. A watch that surfaces only confirming evidence has stopped being a monitor.
2. **Name divergence as its own state.** A quiet primary tell alongside a deteriorating concealed channel is a specific, reportable condition — risk relocating rather than resolving. It is more informative than either reading alone.
3. **Never silently drop a tell.** Omitting an indicator in the run where it disagrees is the failure mode this structure exists to prevent. If an indicator could not be checked, record it as `blocked` or `failed` rather than leaving it out.

Distinguish a dated measurement from an undated reference figure. Pricing-guide numbers, vendor marketing tables, and stale baselines are not evidence that something moved; label them as background or omit them.

## 9. Output and close

- Use one-line takeaways with direct links.
- Include an insight only when it is distinct from the factual takeaway.
- Label single-source or changing claims inline.
- Say “nothing new in this window” when a section is genuinely quiet.
- Never add filler to reach a target item count.
- Save the digest to `digests/YYYY-MM-DD.md` only when the user has authorized repository writes.
- Finish the state run as `completed`, `partial`, or `failed` and attach the digest path when one was written.
