# HPO phenotype picker — notes for PM

Living notes on the HPO "Clinical signs" picker in the case-creation wireframe
(`case-create-signs-modal.html`). Hand off alongside the mock (`github.com/vferretti/radiant-maquette/hpo`).
Lucas + Claude are still iterating on this, so expect it to change.

_Last updated: 2026-09-03._

## What it is

A dialog launched from the "Add clinical signs" button in Section 3. It captures observed and
not-observed phenotypes together: a search box, an analysis-specific suggestions checklist, an
onset dropdown per observed term, and an optional not-observed section. Submit fills the form.

## Two layouts under evaluation

Two files, same feature, different placement — to compare with the team:

- **Version A — `case-create-signs-modal.html`** (modal-in-modal). Section 3 stays compact: one
  "Add clinical signs" button opens a picker dialog holding search + suggestions + not-observed;
  the HPO tree opens as a second modal on top.
  - Pros: form stays short; phenotypes feel like one focused task; a single Cancel backs out of all
    phenotype edits at once.
  - Cons: an extra click to even see suggestions; two stacked modals when browsing the tree.

- **Version B — `case-create-signs-inline.html`** (inline). Suggestions and the selected /
  not-observed sections live directly in the form; the two buttons ("Parcourir l'arbre HPO" and
  "+ Signes non observés") open the HPO browser modal. Only one modal, ever.
  - Pros: suggestions are visible immediately (once an analysis is picked); fewer layers; reads as
    part of the form.
  - Cons: Section 3 gets taller (more scrolling); edits are live (no single "cancel all").

Both are bilingual, share the same grayscale design language, and use the same full HPO tree browser.

## Open questions for the PM

1. **Suggestion lists per analysis are a first guess.** Each panel (RGDI / EPI4 / CARDIO / TSOL)
   shows its own suggested phenotypes. These were drafted from HPO, not from a clinical source —
   they need review. **TSOL (solid tumour) especially**: it currently lists tumour-type HPO terms,
   but somatic oncology intake may not use HPO phenotypes the same way. Confirm what (if anything)
   should show there.
2. **French labels are machine-translated for much of the ontology.** Now that the full HPO tree is
   in (see changelog), search and the tree expose the whole ontology — and a large share of the
   French is machine-translated and reads oddly. Pulled from the mock, which flags the same issue.
   A handful of common/suggestion terms were fixed by hand (e.g. the "Epilépsie" bug →
   "Crise d'épilepsie"); the rest need a French clinical review. This is the main open content item.

## Decisions already made (for context)

- Full HPO tree browser now included (opens in its own modal over the picker); flat search kept too.
- Adopted the mock's HPO onset value set (Anténatale … Adulte sénior).
- One dialog handles observed + not-observed (not two separate flows).
- Suggestions are keyed to the selected analysis.
- Observed terms carry an onset; not-observed do not.

## Changelog

- 2026-09-03 — First integration: dialog, per-analysis suggestions, search, onset, not-observed,
  bilingual EN/FR.
- 2026-09-03 — Dialog reworked to mirror the mock's sectioning: search-picked observed terms sit in
  their own "Selected from HPO (N)" section on top; checked suggestions float to the top of the
  suggestions list (alphabetical); not-observed signs get their own "(N)" section. Signs can now be
  removed both from the form (✕) and inside the dialog (uncheck). Form: generic "Phenotypes" label
  in the empty state; trigger is a secondary button.
- 2026-09-03 — Full HPO hierarchical tree added (the whole ontology, ~18,690 terms, inlined; decode
  ~50 ms). Lazy-rendered, expand/collapse, full DAG (a term can appear under several parents and
  stays in sync), search with ancestor roll-up + highlight. Apply drops the picks into the observed
  / not-observed sections.
- 2026-09-03 — Split into two layouts to compare (see "Two layouts under evaluation"): Version A
  keeps the picker in a dialog (modal-in-modal); Version B moves suggestions + sections inline and
  reserves the modal for the tree browser only. Both verified.
