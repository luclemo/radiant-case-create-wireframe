# Handoff — wireframe → high-fidelity

Written 2026-09-25, at the end of the wireframe phase. The wireframe
(`case-create-signs-inline.html`, demo at `docs/index.html`) is complete enough to stop. The next
phase builds the case-creation form for real, with `radiant-portal`'s Storybook theme and
components.

**Start a new session from `~/Sandbox/radiant-portal`.** This repo's context is wireframe
specifics; that repo has its own conventions to pick up. Either paste this file into the first
message, or point the session at this path and let it read.

---

## What the next phase is, and is not

A **high-fidelity design prototype**. The FE team **will not ship this code**. Its value is:

1. fidelity to the real design system, so the design cannot drift from what exists;
2. a link anyone — PM, clinician, Vincent — can open without a checkout.

Optimise for those two. Not for production quality, test coverage or reusability.

## Workflow

The component library lives in the monorepo and is **not consumable outside it**, so the work
happens inside `radiant-portal`. That is settled; don't re-open it.

- **Branch**: `design/case-creation-hifi` off `main`.
- **No long-lived draft PR.** A PR is a merge request; opening one for code that will never merge
  invites the wrong review (prop naming, coverage) when you want comments on spacing, flow and
  copy. It also rots — weeks of drift against `main`, CI on every push, conflicts nobody benefits
  from, and reviewers tuning it out.
- **Open a short-lived draft PR only for a specific review round**, then close it. The branch
  persists; the PR doesn't.
- **The preview link does the real work.** Check whether the repo has per-branch preview deploys
  or a deployed Storybook; that is how this gets shared.
- Make the status unmistakable: a `README` at the top of the branch saying *prototype, not for
  merge*, and if a PR is opened, prefix the title `[DESIGN PROTOTYPE — DO NOT MERGE]`.

## Orient before writing anything

1. **Which package** in the monorepo hosts the component library, and which hosts the app the
   case-creation form would belong to?
2. **Is Storybook deployed, and can stories be added per-branch?** If page-level stories are a
   thing there, that is the best home: stories are explicitly design artifacts, devs already
   browse them, and iteration is native. Fallback is an unlinked route in the app.
3. **Are there branch preview deploys?**
4. **Find the tokens, and the components for**: searchable select, segmented control, checkbox,
   typeahead, modal, badge, progress bar. Point at the files before editing.

## Port the spec — don't rebuild it from memory

The wireframe's `CLAUDE.md` **is the behavioural spec**. Carry it across as `DESIGN-NOTES.md` on
the branch, and keep recording decisions with their *why*. The load-bearing parts:

- **The gate** — 7 required fields, 9 prenatal; the rail's count *is* its rows; first + last name
  count as **one** item; clinical signs needs one **observed** phenotype.
- **Derive-and-hide** — case type from the analysis, condition from a MONDO code only, the
  mother's record stated not re-asked in §5, the prescriber from the session.
- **Prenatal** — the fetus is the proband and §2 holds the mother's identity; gestational age is
  **stored as a date and derived as an age** (CLIN's formulas, `clin-portal-ui/src/utils/age.ts`);
  Priority prefills STAT unless the basis is « Fœtus décédé »; the pedigree slashes a demise.
- **Clearing** — anything revealed behind a checkbox clears itself when closed. Nothing hidden
  reaches the case.
- **Bilingual FR/EN**, French default, every visible string keyed in both.
- **The pedigree draws the family; the composition badge counts the sequencing batch.** The two
  disagreeing is correct.

## Five open questions become answerable in that repo

Wireframe open questions 8–12 are all about `radiant-portal`'s own schema and API. **You are now
in the repo that answers them**, and each can change the design — resolve them before building on
the assumption:

| # | Question |
|---|---|
| 8 | No prenatal fields exist beyond `category_code`. Adopt CLIN's `gestational_method` + `gestational_date`? |
| 9 | `relation_to_proband_code` accepts only `mother father brother sister sibling proband`; the form offers four more. |
| 10 | `submitter_patient_id_type` is `NOT NULL` but the form dropped the dropdown — what defaults it? |
| 11 | A prenatal case may submit the mother twice against `UNIQUE (organization_code, submitter_patient_id)`. |
| 12 | What does `ordering_physician` hold — free text, or a practitioner reference? Determines whether the unticked path needs a directory typeahead. |

## Working rules that carry over

- UI copy in **French and English** both, or ask which is needed.
- **Commits are an explicit ask; pushing is a second, separate ask.** Short bodies, no co-author
  trailer.
- Point at files before editing. Flag anything touching shared or production code — in a monorepo
  that is easy to do by accident.
- Verify visually and with assertions. Don't claim something works.

## Don't

- Don't treat the prototype as production code, or let a reviewer treat it that way.
- Don't modify the component library or shared packages to make the prototype work. If something
  is missing, that is a finding to report, not a thing to patch.
- Don't rebuild the wireframe's decisions from scratch — they cost a lot of review time to reach.
