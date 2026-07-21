---
name: ai-digest
description: A three-times-a-week personalized AI + markets briefing. Part A — Frontier & Builders (model releases, what AI-native builders are shipping/debating, a personalized GitHub scout). Part B — Markets, Deals & Careers (consulting, macro, M&A/VC deal flow, careers, the funded AI stack). Uses a live-X pass via the xAI Grok API plus web search, Hacker News, and a GitHub trending sweep. Run on a schedule or on demand.
---

Produce a consolidated AI + markets digest in **two clearly-separated halves**, so cutting-edge builder signal never gets diluted by business/markets coverage and vice versa. Render a clear visual divider between Part A and Part B. A longer digest is fine — favor substance and real coverage over brevity.

> **Customize this file.** The watchlists, categories, and GitHub-scout targets below are a starting template. Edit them to your interests before your first run — that's the whole point. Anything in _[brackets]_ is a placeholder to replace.

**Freshness pass (run it — it's the best signal, costs pennies):** Grok is the only frontier model grounded on live X posts. Run `scripts/grok-x-pass.py` **twice**, once per Part, with the gap-in-days since your last digest:
- Part A: `python3 scripts/grok-x-pass.py --days <gap> --prompt "What are the top AI-native builders, AI-lab leaders, and tech/VC figures shipping, launching, or debating on X right now — agents, models, applied AI, notable tech takes? Attribute each to a person."`
- Part B: `python3 scripts/grok-x-pass.py --days <gap> --prompt "What are notable people saying on X about management consulting, venture & PE deal flow, M&A and capital markets, macro/investment trends, and forward-deployed-engineer (FDE) roles? Attribute each to a person."`
Fold each pass into its Part (one-liners + source URLs). Exit codes: 0 ok; 2 = no `XAI_API_KEY` (fall back to web search silently); 3 = API error (note briefly, fall back). No key? The digest still works on web search alone — the Grok pass just makes it sharper.

**Pre-filter before writing anything up (cost discipline):** as candidates surface from the Grok passes, web search, and HN/GitHub/HF sweeps, score each one **before** spending output tokens on a full write-up:
- **Recency** (0-2): genuinely new since the last digest vs. already-stale.
- **Relevance** (0-2): matches _your_ actual stated interests (edit the rubric weights to match what you track) vs. generic AI news.
- **Substance** (0-1): real signal (a launch, a debate, a number) vs. engagement-bait or a repost of something already covered.
Only write a full item for candidates scoring **3+/5**. Silently drop the rest — don't narrate what was cut. This keeps the expensive step (synthesis) spent only on things that survive scoring, not everything encountered — the same discipline behind any good filter-then-generate pipeline, just applied at the instruction level rather than in code.

---

## PART A — Frontier & Builders

1. **Model Releases & Major Updates** — new model releases, version updates, or notable capability announcements from the frontier labs (OpenAI, Anthropic, Google DeepMind, Meta, xAI, Mistral, Moonshot, etc.), covering the days since the prior digest.

2. **What AI-Native Builders Are Doing** — the most interesting things technical/AI-native people are building, shipping, or debating around agents and applied AI. Use the Part-A Grok pass, plus X-visible discourse via web search (e.g. `site:x.com AI agents`) and tech blogs/newsletters. **Also scan Hacker News** (news.ycombinator.com front page + "Show HN") — high-signal builder/engineer discourse that often surfaces things before or differently than X; pull 2-4 genuinely notable AI/agent items, skip generic tech.

   **Watchlist (your substitute for living on X):** each run, surface what these accounts have posted/shipped. Rotate through it — only surface accounts with something genuinely notable this cycle. _Edit this list to match who you actually want to track._
      - _AI/agent builders & researchers:_ Andrej Karpathy, Andrew Ng, Jim Fan, Simon Willison, swyx, Harrison Chase, Yann LeCun
      - _Lab & frontier-company leaders:_ Sam Altman, Greg Brockman, Demis Hassabis, Aravind Srinivas, Clément Delangue (Hugging Face), Arthur Mensch (Mistral), Logan Kilpatrick (Google AI Studio)
      - _Broader tech / VC leaders:_ Paul Graham, Garry Tan (YC), Naval Ravikant, Marc Andreessen, Satya Nadella
      - _Curators (catch what the above amplify):_ Rowan Cheung (The Rundown AI), DAIR.AI (paper threads)
   Attribute each find to the person with a source link.

3. **GitHub Signal (personalized)** — a personalized repo scout, not a generic trending list.
   - **(a) Your taste profile:** check _[your GitHub profile URL]_ (starred + following tabs) for anything new; note drift.
   - **(b) Trending, relevance-ranked:** sweep github.com/trending (daily + weekly) plus 2-3 targeted searches across _[your interest areas — e.g. AI agents / MCP servers / finance tooling / PKM]_. **Also scan Hugging Face trending** (huggingface.co/models?sort=trending) for notable open-weight model drops. Rank by relevance to _you_, not raw stars; one line of "why it's worth your look" per pick tied to your interests. 4-7 picks max; be skeptical of inflated trending entries.

4. **Other Notable AI News** — AI funding rounds, major partnerships, notable AI regulatory news.

---

## PART B — Markets, Deals & Careers

Intentionally **broader than AI** — make sure the non-AI categories get real representation. Source from the open web (firm publications, deal news, reputable press, VC/consulting newsletters) + the Part-B Grok pass. Group loosely by theme:
- **Consulting & Strategy** — McKinsey / Bain / BCG and top firms: notable reports, insights, moves (esp. AI or market-trend related).
- **Macro & Investment Trends** — broad market/macro themes, not just AI.
- **Market Pulse** — a compact snapshot, not a full daily market brief (no paid data feed needed — plain web search on any solid free source: index/quote sites, financial news, econ-calendar pages). 3-5 lines max, zero fine if quiet: (1) major index moves since the last digest (S&P/Nasdaq/etc. + a one-line reason — the multi-day gap since the last run, not "yesterday's close"), (2) notable FX/commodity/bond moves only if something actually moved meaningfully, (3) upcoming econ-calendar highlights (FOMC/CPI/jobs/etc.) before the next run.
- **Capital Markets & M&A** — notable large deals, PE/VC mega-rounds, M&A across sectors.
- **Careers** — notable role/company moves and discourse in the tracks _you_ care about (e.g. FDE / product / BD / strategy).
- **The Established AI Stack** — infra, chips, model providers, enterprise application cos — the funded/established layers (leave the bleeding-edge builder layer to Part A).

Roughly 8-14 items across these; author/source + one-line insight + link for each. Skip pure self-promotion and content-free engagement-bait.

---

Keep each item a one-line takeaway with a source link. If something is unusually significant, end the whole digest with one line on why it matters. End your output with the full formatted digest as your final message.
