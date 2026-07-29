# Case Study — AI Frontier Dispatch
### A product-thinking write-up (not a README). To run it, see [README](./README.md); this is the *why*.

A personalized AI + markets briefing that runs inside your own agent harness — built to answer the question no newsletter can: not *what happened*, but *what happened that matters to me*.

---

## The problem I was modeling

Keeping up with AI looks like an information problem. It isn't — it's a **filtering** problem wearing an information problem's clothes.

Every newsletter is one editor's relevance function broadcast to thousands of readers with different jobs. The editor is often excellent. But the model is structurally wrong: a researcher, a PM, and someone tracking deal flow all get the same twelve items, and each of them skims nine. Meanwhile the alternative — living on X — is unbounded and optimizes for engagement, not relevance.

The product question: **what if the filter belonged to the reader instead of the publisher?**

## Who it's for

Someone tracking a fast-moving field whose relevance function doesn't match any single editor's. Concretely, people with a **split profile** — one foot in building, one in markets or business — who are currently subscribed to four newsletters because no one publication covers both halves at the right depth.

Primary user was me (n=1, honestly). The generalization step came second, and it's where most of the interesting decisions are.

## The core product insight

**The value isn't my curation — it's that you shouldn't need mine.**

Everything downstream follows from turning the editor's judgment into a config file: a `reader_profile` that describes who you are, the accounts and repos you track, and — the part most tools skip — an explicit list of what to *exclude*. A relevance filter with no negative space keeps surfacing things that are technically on-topic and useless.

The second insight is smaller and more surprising: **independent arrival is evidence**. Most aggregators treat the same story appearing three times as noise to collapse. Inverting that — a story that surfaced independently via a live-X pass, Hacker News, *and* web search scores higher and gets tagged `[3 sources]` — turns the dedup step into a ranking signal. Corroboration is the cheapest quality signal available, and it was sitting unused inside a step everyone already runs.

## Key product decisions & tradeoffs

| Decision | Why | Tradeoff accepted |
|---|---|---|
| **Portable skill plus an optional local event ledger** | The research method remains readable Markdown, while one dependency-free script adds run state, source health, and claim evidence without a hosted backend. | More surface area than the original prompt-only version. State is append-only, local, and optional so portability remains the default. |
| **Ship through thin harness adapters** | Claude and Codex differ in invocation, tools, and model fan-out, but the relevance and evidence method should not fork. | Two small adapters to test and maintain. Worth it because duplicated core prompts would drift much faster. |
| **Corroboration as a positive ranking signal, not just dedup** | Independent arrival across separate streams is real evidence something matters. | Slight bias toward stories with broad pickup. Mitigated because the relevance axis is user-defined and pulls the other way. |
| **Explicit exclude list alongside stated interests** | Negative preferences catch what positive ones can't: the item that matches your topics and still wastes your time. | More configuration for the user to complete. Accepted, and it's prompted rather than optional-in-practice. |
| **Instructed to report "nothing new this window" rather than pad** | An honest empty section is information. Filler trains the reader to skim *every* section, which destroys the product. | Some runs look thin. Correct tradeoff — perceived thoroughness is a vanity metric. |
| **Two halves with a hard divider — frontier vs. markets** | The two need different sources and a different reading posture; blending them dulls both. | Longer output than a single feed. Acceptable: this is a briefing, not a notification. |
| **Tiered models — cost-efficient research fan-out, strongest model for synthesis** | Most token spend is ingestion, while ranking contradictions and implications require judgment. | Harnesses expose model tiering differently, so each adapter must degrade honestly when overrides are unavailable. |
| **Borrowed the ranking logic instead of inventing it** | Five techniques already existed in the top-starred projects in this category and were better than what I'd write cold. Read them, took what worked, documented what I rejected and why. | Obligation to credit precisely and stay honest about what's mine. That's a feature — the [provenance table](./README.md#method-provenance) is itself the argument that the design was researched rather than guessed. |

## Designing for honest failure

Worth separating out, because it's the decision I'd defend hardest.

Search results for AI news are polluted with content farms that invent plausible specifics — fabricated version numbers, invented benchmarks, funding figures that don't trace. A tool that ingests them uncritically produces confident, well-formatted, wrong output, which is worse than no tool.

So the skill is instructed to corroborate before asserting, label anything single-sourced as unverified *inline*, distrust star counts and trending positions as quality signals, and say a category was quiet rather than fill it. In practice this means some sections read "nothing new this window," and one recent run opened by flagging that its own GitHub data looked inflated and refusing to vouch for it.

Most content products optimize the opposite direction. The bet is that a reader who catches the tool padding once stops trusting all of it — so the honest version compounds and the padded version decays.

## How I'd measure success

**North star: repeat voluntary runs by someone who isn't me.** Not stars, not clones. Clones are free and mean nothing; a fork still being run in week four is the only signal that the personalization actually landed.

**Supporting metrics:**
- **Config-completion rate** — what share of installs fill in `reader_profile` versus leaving the template text? This is the activation step and almost certainly the real failure point. A generic profile produces a generic digest, and the user concludes the product is the problem.
- **Read-through depth** — items actually opened versus skimmed past, as a proxy for whether the ranking is working.

**Counter-metric: digest length.** If output grows week over week, the filter is failing and the pre-filter thresholds need to move. Tracking a metric you want to go *down* keeps the tool honest about its own scope creep.

## Roadmap — and where this actually goes

1. **Close the usefulness feedback loop.** Run state and claim evidence now persist, but the system still does not learn which items led to a decision, build, application, or investment view. A lightweight explicit outcome signal should improve ranking without silently rewriting the reader's profile.
2. **Optional research module.** A narrow, off-by-default arXiv path for forkers doing technical work. Deliberately not on by default — for most readers it adds volume, not signal.
3. **Sharper exclusion defaults.** Right now negative preferences start empty. Shipping a sensible starter list would raise first-run quality, which is where adoption is won or lost.

**Explicitly not doing:** hosting it, building a web UI, or offering a mailing list. Every one of those converts it back into the thing it was built to replace — one person's feed, broadcast. The moment there's a subscribe button, the premise is gone.

## Why this write-up exists

This is a product-judgment artifact about a narrower skill than building the tool: **taking something that worked for one person and making it work in someone else's environment.** The build was a weekend; the generalization was the actual work — deciding what was configuration versus what was hardcoded opinion, what stays private versus what ships, and how someone non-technical gets from a link to a working install without asking me for help.

It also documents the less comfortable half of product work: reading the competition closely enough to take five things from it, and stating plainly which three things I chose not to take and why. If you're reading it as a hiring signal — that's the point.

---

*Tech: one portable Markdown skill, Claude and Codex adapters, a dependency-free append-only state CLI, and an optional Python live-X pass. No hosted backend; bring your own key. Part of a broader portfolio at [github.com/bakulbadwal](https://github.com/bakulbadwal).*
