# digests/

Archived runs, one file per digest, named `YYYY-MM-DD.md`.

This folder does two jobs:

**1. It shows people what they're getting.** A briefing tool is hard to evaluate from a feature list. One real, dated output is worth more than any description — and a folder of them shows the thing is actually used, not just published once.

**2. It's how the skill knows what "new" means.** Every run reports on the window *since the last digest*. Getting that window wrong is the most common failure mode: too wide and it re-reports old news as fresh, too narrow and it misses things. `SKILL.md` instructs the skill to read the most recent filename here and compute the gap from it. Archiving your runs turns that from a guess into a lookup.

## Using it

Ask the skill to save its output here when a run finishes:

```
digests/YYYY-MM-DD.md
```

If you'd rather not publish your own briefings, add `digests/` to `.gitignore` — the gap-tracking still works locally, you just don't push the archive. Nothing in the skill depends on these files being public.

## A note on redaction

The archived runs in this repo are lightly redacted — employer name and a few personal project references removed. If you archive your own and the repo is public, do the same pass. Your `reader_profile` is meant to be specific about your work, which means your output will be too.
