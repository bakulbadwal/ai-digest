---
name: ai-digest
description: Produce a personalized AI + markets briefing. Use when the user asks for their digest, briefing, roundup, or "what happened this week" in AI/tech/markets. Part A — Frontier & Builders (model releases, what AI-native builders are shipping, a GitHub/Hugging Face scout). Part B — Markets, Deals & Careers (consulting, macro, M&A/VC deal flow, careers, the funded AI stack). Uses a live-X pass via the xAI Grok API plus web search, Hacker News, and trending sweeps.
when_to_use: Use when the user says "run my digest", "AI digest", "morning briefing", "what did I miss this week", "catch me up on AI", or when a scheduled task invokes it. Also use for a one-off briefing on a custom window.
---

Produce a consolidated AI + markets briefing in **two clearly-separated halves**, so cutting-edge builder signal never gets diluted by business/markets coverage and vice versa. Render a clear visual divider between Part A and Part B. A longer digest is fine — favor substance and real coverage over brevity.

---

## ⚙️ CONFIGURE THIS FIRST

**Everything you need to personalize lives in this one block.** Edit it before your first run — that's the whole point of the skill. The rest of the file is method and rarely needs changing.

```yaml
# --- WHO YOU ARE (drives the relevance filter) ---
reader_profile: >
  [1-3 sentences: your role, what you're building, what you're
  hiring/investing/recruiting for. Be specific — this is what
  separates "relevant to me" from "generic AI news."]
  Example: "Product lead at a Series B fintech; building internal
  agent tooling; tracking AI infra as an angel investor; targeting
  a move into AI product management."

# --- CADENCE ---
cadence: [e.g. three times a week — Tue/Thu/Sat mornings]

# --- PART A: WHO TO WATCH ---
# Rotate through these; only surface accounts with something genuinely
# notable this cycle. Do NOT force every name every run.
watchlist:
  builders_and_researchers: [Andrej Karpathy, Andrew Ng, Jim Fan, Simon Willison, swyx,
                             Harrison Chase, Yann LeCun]
  applied_practitioners:    [Hamel Husain, Eugene Yan, Jason Liu, Chip Huyen]  # methodology, not papers
  lab_leaders:              [Sam Altman, Greg Brockman, Demis Hassabis, Aravind Srinivas,
                             Clement Delangue, Arthur Mensch, Logan Kilpatrick]
  tech_and_vc:              [Paul Graham, Garry Tan, Naval Ravikant, Marc Andreessen, Satya Nadella]
  curators:                 [Rowan Cheung, DAIR.AI]
  companies_to_track:       [Cursor/Anysphere, Together AI, Groq]

# --- PART A: GITHUB SCOUT ---
github_profile: https://github.com/[your-username]
interest_areas:
  - AI agents, MCP servers, coding-agent tooling
  - [your domain, e.g. finance/PE tooling, healthcare data, devtools]
  - [your secondary interest, e.g. PKM / Obsidian / knowledge graphs]
never_recommend: [repo topics you've already settled — stops repeat suggestions]

# --- WHAT TO ACTIVELY EXCLUDE (negative preferences) ---
# Just as important as the positive signals. A relevance filter with no
# negative space surfaces technically-on-topic items you don't want.
# Be specific: "AI ethics think-pieces" beats "boring stuff."
exclude_topics:
  - [e.g. funding rounds under $10M]
  - [e.g. AI ethics op-eds with no new facts]
  - [e.g. prompt-engineering listicles]

# --- PART B: WHAT YOU TRACK ---
part_b_categories:
  - Consulting & Strategy
  - Macro & Investment Trends
  - Capital Markets & M&A
  - Careers            # name the specific track(s) you care about
  - The Established AI Stack
career_track: [e.g. Forward Deployed Engineer, AI PM, quant, corp dev]

# --- OPTIONAL: THESIS WATCH ---
# A standing box that tracks ONE thesis you hold, with explicit baselines,
# so you notice when it moves. This is the highest-value custom section —
# it turns a news feed into a position you're actively testing.
thesis_watch:
  enabled: false
  thesis: [your one-sentence claim, e.g. "the AI break point is
           data-center financing, not the technology"]
  indicators:
    - [indicator + its CURRENT baseline number and date]
    - [indicator + its CURRENT baseline number and date]
  rule: Report ONLY what moved since the last run. Zero lines is a valid
        and useful answer. Never manufacture movement.
```

---

## 🎛️ Model tiering (do this — it's the main cost lever)

The research fan-out is **ingestion**; the synthesis is **judgment**. Tier them differently or you'll pay frontier prices for scraping.

- **Research subagents → a mid-tier model** (e.g. Sonnet). Dispatch every gathering subagent — HN scan, GitHub/Hugging Face scout, markets research, any web-fetch fan-out — at this tier. This is where the bulk of tokens go and it's pure extraction; quality loss is negligible.
- **Final synthesis → your top-tier model.** The pre-filter scoring, cross-stream dedup, and the closing "why it matters" are the high-judgment step. Keep them on the best model you have.
- **Live-X pass → whatever Grok tier you're paying for.** It's the only live-X signal available, and it's a small fraction of the run.

Run the independent research subagents **in parallel in a single message**, not sequentially — it's the difference between a 3-minute digest and a 15-minute one.

---

## 📡 Freshness pass (run it — best signal-per-cent in the skill)

Grok is the only frontier model grounded on live X posts. Run `scripts/grok-x-pass.py` **twice**, once per Part, with the gap-in-days since your last digest:

```bash
# Part A
python3 scripts/grok-x-pass.py --days <gap> --prompt "What are the top AI-native builders, AI-lab leaders, and tech/VC figures shipping, launching, or debating on X right now — agents, models, applied AI, notable tech takes? Attribute each to a person."

# Part B
python3 scripts/grok-x-pass.py --days <gap> --prompt "What are notable people saying on X about management consulting, venture & PE deal flow, M&A and capital markets, macro/investment trends, and [your career track] roles? Attribute each to a person."
```

Fold each pass into its Part (one-liners + source URLs). **Exit codes:** `0` ok · `2` no `XAI_API_KEY` (fall back to web search silently) · `3` API error (note briefly, fall back). No key? The digest still works on web search alone — the Grok pass just makes it sharper.

**Determining `<gap>`:** compute days since the last run by reading the most recent filename in [`digests/`](digests/) (they're named `YYYY-MM-DD.md`). If that folder is empty, ask the user or fall back to the `cadence` interval. Getting this wrong is the most common failure — too wide and you re-report old news as new, too narrow and you miss things.

**When the digest is finished, save it to `digests/YYYY-MM-DD.md`** as well as printing it. That's what makes the next run's gap calculation a lookup instead of a guess.

---

## 🔍 Pre-filter before writing anything up

As candidates surface from the Grok passes, web search, and the HN/GitHub/HF sweeps, score each **before** spending output tokens on a full write-up:

| Axis | Range | Test |
|---|---|---|
| **Recency** | 0-2 | Genuinely new since the last digest vs. already-stale |
| **Relevance** | 0-2 | Matches `reader_profile` specifically vs. generic AI news |
| **Substance** | 0-1 | A launch, a debate, a number — vs. engagement-bait or a repost |

Only write a full item for candidates scoring **3+/5**. Silently drop the rest — **don't narrate what was cut.** This spends the expensive step (synthesis) only on what survives scoring.

**Corroboration bump (+1):** if the same underlying story surfaced independently from **2+ streams** (Grok/X, Hacker News, web search, GitHub, Hugging Face), add a point and note it inline — e.g. *"[3 sources]"*. Independent arrival is real evidence a story matters, and it turns your dedup pass into a ranking signal instead of just noise removal. Conversely, a story that appears **only** on aggregator/content-farm domains should lose a point.

**Then apply `exclude_topics`** from the config as a hard filter — a high-scoring item on a topic the reader has explicitly ruled out is still a miss.

---

## ✅ Source discipline (what separates this from an AI slop feed)

Search results for AI news are heavily polluted by SEO aggregator sites that invent plausible specifics — fabricated version numbers, invented benchmarks, made-up funding figures. Enforce these rules:

1. **Corroborate before asserting.** Prefer primary sources (a lab's own newsroom, a filing, the model card, the repo) or established press. If a claim appears only on content-farm domains, either drop it or label it explicitly.
2. **Label confidence inline.** Mark anything single-sourced or uncorroborated as *"reported/unverified"* in the digest itself. Never silently launder a rumor into a fact.
3. **Report failure honestly.** If a fetch 403s, a category is genuinely quiet, or a number won't verify, **say so.** "Nothing new in this window" is a valid, useful line. Never manufacture items to fill a section.
4. **Distrust engagement metrics as quality signals.** GitHub star counts and trending positions are gameable and are actively gamed. Flag implausible growth curves rather than passing the number through as fact.
5. **Date-check everything.** Items from just before the window were likely in your last digest. Verify an item is *new to this window* before writing it up as news.

---

## PART A — Frontier & Builders

1. **Model Releases & Major Updates** — new releases, version updates, or notable capability/API announcements from the frontier labs (OpenAI, Anthropic, Google DeepMind, Meta, xAI, Mistral, Moonshot, DeepSeek, Qwen, Z.ai), covering the days since the prior digest. Note what a lab *didn't* ship too — a delayed flagship is signal.

2. **What AI-Native Builders Are Doing** — the most interesting things technical people are building, shipping, or debating around agents and applied AI. Sources: the Part-A Grok pass, X-visible discourse via web search (`site:x.com AI agents`), and tech blogs/newsletters. **Also scan Hacker News** — front page + `/show`, and the Algolia API for high-point stories in your window:
   ```
   https://hn.algolia.com/api/v1/search_by_date?tags=story&numericFilters=created_at_i><unix-ts>,points>150
   ```
   **Fan out, then dedupe, then rank** — don't run one query. Fire several keyword variants (`AI`, `LLM`, `agents`, `Claude`, `OpenAI`, `Anthropic`, plus a term from your own domain), merge the results, **dedupe by URL**, sort by points, and only then run the pre-filter on the top ~30. A single query has poor recall; this costs nothing extra and catches materially more.

   HN is high-signal builder discourse that often surfaces things before or differently than X. Pull 2-4 genuinely notable AI/agent items; skip generic tech. Work the `watchlist` from your config block, attributing each find to a person with a source link.

3. **GitHub Signal (personalized)** — a personalized repo scout, not a generic trending list.
   - **(a) Taste-profile refresh:** check your `github_profile` (starred + following tabs) for anything new; note drift. *New follows are often a stronger intent signal than new stars* — they show where you're heading, not just what caught your eye.
   - **(b) Trending, relevance-ranked:** sweep `github.com/trending` (daily + weekly, language-filtered) plus 2-3 targeted searches rotated across your `interest_areas`. Rank by relevance **to you**, not raw stars. One line of "why it's worth your look" per pick, tied to your actual projects. 4-7 picks max; zero in a category is fine. Respect `never_recommend`.
     **Prefer sustained engagement over novelty here.** A repo with steady issue/PR/comment activity over weeks is a better bet than one spiking today — spikes are the most gameable signal on GitHub. When a growth curve looks vertical and the discussion is thin, say so and skip it.
   - **(c) Hugging Face trending:** sweep `huggingface.co/models?sort=trending`. Report 3-5 max: frontier-scale open releases, big movers, community distills of closed models, uncensored variants charting. Skip perennial OCR/small-model filler unless it signals a trend.

4. **Other Notable AI News** — AI funding rounds, major partnerships, notable AI regulatory news.

---

## PART B — Markets, Deals & Careers

Intentionally **broader than AI** — make sure the non-AI categories get real representation, not token coverage. Source from the open web (firm publications, deal news, reputable press, VC/consulting newsletters) plus the Part-B Grok pass. Group loosely by the themes in your `part_b_categories`:

- **Consulting & Strategy** — notable reports, insights, and moves from the top firms.
- **Macro & Investment Trends** — broad market/macro themes, not just AI.
- **Market Pulse** — a compact snapshot, not a full market brief. No paid data feed needed. **3-5 lines max, zero fine if quiet:**
  1. Major index moves **since the last digest** (the multi-day gap, not "yesterday's close") + a one-line reason.
  2. Notable FX/commodity/bond moves **only if something actually moved** — don't force a line per asset class.
  3. Econ-calendar highlights between now and the next run (FOMC, CPI, jobs, major earnings).
- **Capital Markets & M&A** — notable large deals across **all** sectors, PE take-privates, VC mega-rounds, IPO activity. Include deal value and both parties.
- **Careers** — role/company moves and discourse in your `career_track`. Comp data points when credible.
- **The Established AI Stack** — infra, chips, model providers, enterprise application cos — the funded/established layers. Leave the bleeding-edge builder layer to Part A.
- **Thesis Watch** — if enabled in config, the standing box against your stated baselines.

Roughly 8-14 items across these; source + one-line insight + link for each. Skip pure self-promotion and content-free engagement-bait.

---

## Output

- Every item is a **one-line takeaway with a source link.** Resist paragraphs.
- Dedup across streams before writing — the same story often arrives via Grok, HN, and web search. Merge them into one item and credit the corroboration rather than reporting it three times.
- Put a **hard visual divider** between Part A and Part B.
- **No template padding.** If an item has no genuinely distinct "why it's worth your look," **omit that line** rather than generating boilerplate. An empty field is honest; a filler sentence trains the reader to skim past all of them.
- **Close each Part with 2-3 cross-cutting patterns** — what connects today's items that no single item says on its own. This is the part a reader can't get from a headline feed, and it's usually the most valuable thing in the digest.
- If something is unusually significant, end the whole digest with **one short "why this matters"** section tying the threads together.
- **End your output with the full formatted digest as your final message** — that's what the reader actually reads when a scheduled run completes.
