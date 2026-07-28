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
  builders_and_researchers: [Andrej Karpathy, Simon Willison, swyx, Jim Fan, Harrison Chase]
  applied_practitioners:    [Hamel Husain, Eugene Yan, Jason Liu, Chip Huyen]  # methodology, not papers
  lab_leaders:              [Sam Altman, Demis Hassabis, Logan Kilpatrick, Arthur Mensch, Clement Delangue]
  tech_and_vc:              [Paul Graham, Garry Tan, Naval Ravikant, Satya Nadella]
  curators:                 [Rowan Cheung, DAIR.AI]
  companies_to_track:       [Cursor/Anysphere, Together AI, Groq]

# --- PART A: GITHUB SCOUT ---
github_profile: https://github.com/[your-username]
interest_areas:
  - AI agents, MCP servers, coding-agent tooling
  - [your domain, e.g. finance/PE tooling, healthcare data, devtools]
  - [your secondary interest, e.g. PKM / Obsidian / knowledge graphs]
never_recommend: [topics you've already settled — stops repeat suggestions]

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
- **Live-X pass → whatever Grok tier you're paying for.** It's cheap and it's the only live-X signal.

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

**Determining `<gap>`:** compute days since the last run. If you don't know when that was, check the most recent file in `digests/` (if you archive them), ask the user, or default to your `cadence` interval. Getting this wrong is the most common failure — too wide and you re-report old news as new, too narrow and you miss things.

---

## 🔍 Pre-filter before writing anything up

As candidates surface from the Grok passes, web search, and the HN/GitHub/HF sweeps, score each **before** spending output tokens on a full write-up:

| Axis | Range | Test |
|---|---|---|
| **Recency** | 0-2 | Genuinely new since the last digest vs. already-stale |
| **Relevance** | 0-2 | Matches `reader_profile` specifically vs. generic AI news |
| **Substance** | 0-1 | A launch, a debate, a number — vs. engagement-bait or a repost |

Only write a full item for candidates scoring **3+/5**. Silently drop the rest — **don't narrate what was cut.** This spends the expensive step (synthesis) only on what survives scoring.

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
   HN is high-signal builder discourse that often surfaces things before or differently than X. Pull 2-4 genuinely notable AI/agent items; skip generic tech. Work the `watchlist` from your config block, attributing each find to a person with a source link.

3. **GitHub Signal (personalized)** — a personalized repo scout, not a generic trending list.
   - **(a) Taste-profile refresh:** check your `github_profile` (starred + following tabs) for anything new; note drift. *New follows are often a stronger intent signal than new stars* — they show where you're heading, not just what caught your eye.
   - **(b) Trending, relevance-ranked:** sweep `github.com/trending` (daily + weekly, language-filtered) plus 2-3 targeted searches rotated across your `interest_areas`. Rank by relevance **to you**, not raw stars. One line of "why it's worth your look" per pick, tied to your actual projects. 4-7 picks max; zero in a category is fine. Respect `never_recommend`.
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
- Dedup across streams before writing — the same story often arrives via Grok, HN, and web search.
- Put a **hard visual divider** between Part A and Part B.
- If something is unusually significant, end the whole digest with **one short "why this matters"** section connecting the threads.
- **End your output with the full formatted digest as your final message** — that's what the reader actually reads when a scheduled run completes.
