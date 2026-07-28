# Sample output — a real run

This is an actual digest produced by this skill on **Tuesday, July 28, 2026**, covering the 3-day window since the previous run. Lightly redacted (employer name and a few personal project references removed); nothing else was cleaned up or improved after the fact.

The `reader_profile` that generated this run was roughly:

> *MBA candidate who builds agent tooling, works at an investment firm, tracks AI infrastructure as an investor, runs an Obsidian second brain, and is targeting tech operating/strategy and Forward-Deployed-Engineer-adjacent roles.*

Notice how much of the output only makes sense **for that reader** — the GitHub picks, the middle-market M&A line, the FDE section, the thesis-watch box. That's the point of the skill. A different `reader_profile` produces a genuinely different briefing from the same sources.

Two things worth calling out as examples of the **source discipline** rules in action:
- The digest opens by flagging that GitHub trending star counts came back implausible and refuses to vouch for them.
- An unverified rate-hike claim is included but explicitly labeled, because the Fed met the next day and it mattered — rather than being silently dropped or silently laundered into fact.

---
---

# 📡 Consolidated Digest — Tuesday, July 28, 2026
**Window covered:** Sat Jul 25 → Tue Jul 28 (3 days) · Grok live-X passes: 2/2 clean (~$0.75 total)

---

# PART A — FRONTIER & BUILDERS

## 1. Model Releases & Major Updates

**Kimi K3 (Moonshot AI) — the window's biggest open-weights event.** 2.8T total params / 104B activated per token, 1M-token context, built on Kimi Delta Attention + Stable-LatentMoE. Claimed GPQA Diamond 93.5, DeepSWE 67.5, BrowseComp 91.2. Important asterisk: it ships under a bespoke "Kimi K3 License," not Apache/MIT — large commercial use requires a separate agreement, so "world's biggest open-weight model" is doing some work in the headlines. [Weights](https://huggingface.co/moonshotai/Kimi-K3) · [Tech report](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)

**Anthropic published its position on open-weights models (Jul 27), authored by Dario Amodei.** Core claims: they have never advocated banning open weights, view non-dangerous open models as a public good, but want chip/export controls on China, a crackdown on industrial-scale distillation, and mandatory safety testing for sufficiently capable models — open *or* closed. Highest-engagement AI story of the window (1,005 pts / 1,477 comments on HN). [Anthropic](https://www.anthropic.com/news/position-open-weights-models)

**SSI ↔ NVIDIA strategic partnership (Jul 27).** Ilya Sutskever's Safe Superintelligence gets access to NVIDIA's Vera Rubin platform to roughly 10x compute over 12 months; Bloomberg reports ~$5B equity alongside. Notable as the first time SSI has taken a visible commercial/compute dependency. [NVIDIA newsroom](https://nvidianews.nvidia.com/news/ilya-sutskevers-safe-superintelligence-inc-and-nvidia-announce-long-term-strategic-partnership)

**Two labs shipped cyber-specialized models in the same week** — a category forming in real time. Microsoft announced **MAI-Cyber-1-Flash** inside MDASH, and Google's **Gemini 3.5 Flash Cyber** (government/trusted-partner pilot only) landed days earlier. Security-tuned frontier variants going to restricted distribution is a pattern worth tracking. [Microsoft](https://microsoft.ai/news/introducing-mai-cyber-1-flash-inside-mdash/)

**OpenAI's push is agentic ChatGPT Work, not a new model.** The capability worth noting: agents can now handle **login-required websites via persistent sessions** — that's the wall most computer-use agents hit. [@gdb](https://x.com/gdb/status/2081877298538746165)

**Google's flagship is still missing.** The Jul 21 drop was Gemini 3.6 Flash, 3.5 Flash-Lite, and Flash Cyber — but **no 3.5 Pro**. Bloomberg reported internal delays hitting performance targets. A frontier lab shipping only cheap tiers is itself a signal. [TechCrunch](https://techcrunch.com/2026/07/21/google-releases-three-new-gemini-models-but-no-3-5-pro/)

> *Dropped as unverified:* a widely-summarized claim that Meta shipped a proprietary "Muse Spark 1.1" marking a pivot away from open-weight Llama. The source 403'd on direct fetch and nothing corroborated it. Flagged for a re-check rather than reported.

---

## 2. What AI-Native Builders Are Doing

**swyx: the cost metric is shifting from $/token to $/task.** This is the more honest frame now that long-horizon agents burn wildly different token counts for the same outcome — and it's the metric that matters if you're pricing an agent product. [@swyx](https://x.com/swyx/status/2081904230768816487)

**A $500 RL fine-tune of a 9B open model beat frontier models on catalog review** (239 pts). The most useful builder proof point of the window: narrow task, tiny budget, beats the frontier. This is the economic argument for evals + fine-tuning over prompt-engineering a big model. [fermisense.com](https://fermisense.com/when-machines-take-the-wheel/)

**"Using an open model feels surprisingly good"** (300 pts) — builder discourse on running open weights as a daily driver rather than as a benchmark exercise. The open-vs-closed gap is now being argued from experience, not leaderboards. [matthewsaltz.com](https://matthewsaltz.com/blog/using-an-open-model-feels-surprisingly-good/)

**Simon Willison surfaced an investigation into the LLM token relay market** — a marketplace reselling API access through proxies that exploit free trials and unprotected endpoints. An arbitrage/fraud layer forming underneath the model providers. [vectoral.com](https://vectoral.com/blog/token-relay-market)

**Ethan Mollick's updated "which AI to use" guide has shifted from chat interfaces toward agentic systems.** Mollick is the best barometer of what the informed non-engineer should be doing; the pivot in his recommendations is the signal. [One Useful Thing](https://www.oneusefulthing.org/p/an-opinionated-guide-to-which-ai-b22)

**Applied-AI practitioner watch — thin week.** Simon Willison was the only one of five with in-window posts. Hamel Husain's most recent is **"LLM Evals: Everything You Need to Know"** (Jul 18), an FAQ built from teaching 700+ engineers and PMs — ten days old, flagged anyway for relevance. Eugene Yan, Jason Liu, Chip Huyen: nothing new in 7 days. [hamel.dev](https://hamel.dev/blog/posts/evals-faq/)

> *Show HN was a dud this window* — scanned, nothing above the noise floor. Saying so rather than padding.

---

## 3. GitHub Signal (personalized)

### (a) Taste profile refresh — two real drifts

**Newly following the entire LLM-eval community: `hamelsmu`, `jxnl`, `shreyashankar`, `chiphuyen`, `eugeneyan`**, plus stars on `hamelsmu/claude-review-loop` and `hamelsmu/evals-skills`. That's the clearest intent signal in the profile — a previously-identified gap now has a reading list attached.

**Second drift: widening from pure agent-orchestration into the core ML stack** — new stars on `huggingface/transformers`, `diffusers`, `datasets`, `smolagents`, `open-webui`. Previously the stars were almost entirely orchestration-layer.

Smaller signals: a cluster of **three separate "mission-control" repos** — scouting the agent-dispatch-control-plane *category*, not one tool.

### (b) Trending picks — ranked by relevance

⚠️ *Star counts came back from the trending scrape looking inflated and did not verify cleanly. Judge these on description, not numbers.*

1. **[dgunning/edgartools](https://github.com/dgunning/edgartools)** — clean Python SEC EDGAR reader with a **built-in MCP server and Claude Skills**. The most directly usable pick: comps and diligence pulls, wired to tooling already in use.
2. **[tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph)** — local-first code-intelligence graph over MCP/CLI.
3. **[drewburchfield/obsidian-graph](https://github.com/drewburchfield/obsidian-graph)** — semantic knowledge graph over Obsidian vaults via embeddings + pgvector.
4. **[ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)** — curated Claude Skills collection; mining material.
5. **[likec4/likec4](https://github.com/likec4/likec4)** — live software-architecture diagramming. The most organic growth curve on the list.

**Explicitly skipped:** one agent-harness repo whose own thread brags about star count with a farmed-looking growth curve, and two near-identical themed repos launched the same week with velocity out of proportion to substance. **Zero picks** in the deck-gen/research-automation category — nothing new spiked, and returning zero beats padding.

### (c) Hugging Face trending

- **[moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3)** — 2.8T params, ~99K downloads. Frontier-scale.
- **zai-org/GLM-5.2** — 753B params, **1.27M downloads** — volume leader by a wide margin.
- **thinkingmachines/Inkling** — 952B params. A closed-frontier-adjacent lab putting real weights in the open.
- **poolside/Laguna-S-2.1** — 118B, coding-focused lab shipping open.
- **A community uncensored Qwen merge at 737K downloads** — the uncensored-variant tier charting near the top on raw pulls is its own trend line.

**The thread:** three frontier-scale open releases in one window, two of them Chinese, one from a lab that didn't have to. The open-vs-closed gap narrowing is showing up in download volume and in builders calling open models fine as daily drivers.

---

## 4. Other Notable AI News

- **NVIDIA / Amkor — $1.5B** to expand US advanced chip packaging in Arizona. Packaging is the underrated constraint in the compute story.
- **AMD → Anthropic, up to $5B**, with Anthropic deploying 2GW of Instinct MI450 GPUs. Anthropic is now multi-sourced across AMD, NVIDIA, and Google silicon. [CNBC](https://www.cnbc.com/2026/07/22/amd-anthropic-ai-chip-investment.html)
- **Databricks raising at $188B**, led by existing investor Coatue — largest pending private round in the market.
- **OpenAI and Anthropic together absorbed ~43–60% of all US VC dollars in H1 2026** (~$217B combined). The numerator behind everyone else's fundraising difficulty.

---
---

# PART B — MARKETS, DEALS & CAREERS

## Consulting & Strategy

- **McKinsey is cutting ~10% of its global workforce (3,000–4,000 roles)** — largest reduction since 2008, concentrated in back-office and junior research areas compressed by GenAI. Bain, BCG, and Deloitte cutting or slowing hiring.
- **BCG's CEO survey is the sharpest number here:** nearly **90% of CEOs report cost or revenue benefit** from targeted AI use, but **>50% see no clear link between AI and P&L**, and only **14% define P&L impact for all AI initiatives.** That gap is the actual consulting engagement of 2026 — and the commercial case for eval infrastructure. [BCG](https://www.bcg.com/press/22july2026-ceos-cost-revenue-benefits-ai-struggling-scale)
- **"Why does MBB still exist?"** — the argument that consultants sell CEOs *insurance*, not analysis: when a bet fails you can say McKinsey signed off, and AI doesn't provide that cover. Cynical, but the most durable defense of the model articulated this cycle. [@realbasilchatha](https://x.com/realbasilchatha/status/2081799135188197413)

## Investment & Deal Flow

- **easyJet / Castlelake — ~£5.5B ($7.3B) take-private agreed**, after four rejected bids.
- **argenx / Forte Biosciences — $2.2B** (immunology). *Value via secondary summary — verify before citing.*
- **Criteo** subject to a bid reportedly from **Vista Equity Partners and Quinti Capital**. Value unverified.
- **The aggregate picture is a value rebound with fewer, larger deals:** global M&A **+48% YoY in H1 2026** per Goldman, already past 2021 highs; LSEG put Q1 at **$1.2T, +27% YoY**.
- **Average PE deal size jumped ~50% to ~$910M.** Uncertainty pushes capital to megafunds; large-cap quality closes while **the middle market stays slow.** [@IlliquidInsight](https://x.com/IlliquidInsight/status/2081926884233707917)
- **The venture barbell, quantified:** US venture hit a record **~$413B in H1 2026, but >81% went to rounds of $100M+.** Mid- and pre-seed is materially harder than the headline suggests. [@tvykruta](https://x.com/tvykruta/status/2081013419541516786)

## Careers & FDE

- **Palantir's commercial business is now 46% of revenue**, with the FDE model credited as a driver — though the freshest substantive piece explicitly interrogates how much to credit FDE vs. general AI demand. Worth reading skeptically. [Forbes](https://www.forbes.com/sites/stevebanker/2026/07/10/palantir-and-forward-deployed-engineering-what-should-we-believe/)
- **FDE and FDE-adjacent postings reportedly up >800% YoY.** Comp data points: $250K–$400K+ for the senior posture; OpenAI FDE roles quoted ~$162–280K.
- **The most useful framing this week:** the market shifted from "everyone wants an AI engineer" to "everyone wants an FDE," but candidates prepare for the *title and frameworks* rather than the work — **diagnosing unarticulated business problems, architecting under constraint, building trust with both engineers and execs, owning outcomes.** [@iamKierraD](https://x.com/iamKierraD/status/2081435159744680057)
- **No company-specific FDE news** from the tracked list this window. Quiet, not hidden.

## 📊 Market Pulse

| | Fri 7/24 → Mon 7/27 close |
|---|---|
| **Dow** | 51,947 → 52,210 (**+0.51%**) — led by the oil retreat |
| **S&P 500** | 7,412 → 7,413 (**+0.02%**, flat) |
| **Nasdaq Comp** | 24,976 → 24,932 (**−0.18%**) — dragged by chips |

- **Today pre-close:** Nasdaq 100 **−0.66%**, Dow **+0.26%** — a continued semiconductor selloff on AI circular-financing fears.
- **Commodities/rates:** WTI fell **~8% to ~$81–82** on the US–Iran hostilities pause — the week's most meaningful macro move. Gold ~$4,046. 10Y ~4.63%.
- **Calendar:** **FOMC Wed Jul 29.** **Microsoft and Meta report Wed after close** (capex guidance is the story). **Amazon Thu.**
- ⚠️ **Treat with caution:** aggregator sources claim BofA now projects three 25bp *hikes*. Could not confirm at primary-source level. It would be a violent reversal, so it matters if true — but don't act on it until Fed language confirms or kills it.

## 🫧 Thesis Watch — AI infrastructure credit cycle

*Thesis: the break point is data-center/neocloud financing (duration mismatch), not the technology.*

**The big one — NVIDIA's circular financing broke wide open (Bloomberg, Jul 27).** NVIDIA is reportedly discussing **guaranteeing up to $250B in lease payments** so OpenAI can occupy a 10GW data center, plus considering **$350B in financing for OpenAI's GPU purchases.** Stacked on prior deals, analysts put total circular-style commitments at **>$540B this year.** This triggered the semiconductor selloff. [Bloomberg](https://www.bloomberg.com/news/articles/2026-07-27/nvidia-s-750-billion-deals-revive-fear-of-ai-circular-financing)

**Hyperscaler capex is going the wrong way for the softening thesis.** Alphabet **raised** 2026 capex guidance to **$185–205B** and fell **7%** on negative FCF and suspended buybacks. Guidance up, equity punished — the market repricing the *financing* of capex rather than management trimming it.

**Quiet or unchanged:** data-center ABS spreads (no dated tick against the ~+160bps baseline); Oracle (no new action since the Jul 9 cut to BBB-); OpenAI IPO (no new pricing/delay language); GPU spot rental (no fresh move).

---
---

## Why this one matters

**The thesis moved from op-ed to price this week.** The mechanism — that the break point is data-center and neocloud *financing*, not the technology — is exactly what markets traded on. Semiconductors sold off on a story about **lease guarantees and vendor financing**, not about demand, not about a model failing, not about a capex cut. NVIDIA underwriting its own customer's ability to pay is the duration mismatch made explicit, and at >$540B the market is now pricing it as counterparty risk rather than growth.

Two things make the next 48 hours unusually informative: the **FOMC decision** lands into a possible hawkish repricing, and **Microsoft, Meta, and Amazon guide capex within 24 hours of each other.** If capex guidance keeps rising while equity keeps getting punished, that's the tell arriving through the equity channel before the credit channel.
