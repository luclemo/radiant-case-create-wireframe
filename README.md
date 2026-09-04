# Case creation — wireframe

An interactive wireframe for the new case-creation form. It explores a **"derive-and-hide"**
idea: any required value that the system can work out from something the user already entered is
dropped from the form and set behind the scenes. Fewer fields to fill, less room for error. Case
type, for example, comes from the chosen analysis and shows as a small badge instead of a field.

There are **two versions** to compare. They are identical except for how the clinical-signs
(HPO phenotype) picker is placed.

## The two versions

**Version A — signs in a modal** (`case-create-signs-modal.html`)
One "Add clinical signs" button opens a picker dialog with search, suggestions, and the
not-observed list; browsing the full HPO tree opens a second window on top.
- Pros: the form stays short; picking phenotypes feels like one focused task; a single Cancel
  backs out of all the phenotype edits at once.
- Cons: an extra click before you even see the suggestions; two stacked windows when browsing the tree.

**Version B — signs inline** (`case-create-signs-inline.html`)
The suggestions and the selected / not-observed lists sit directly in the form; only the HPO tree
browser opens in a window.
- Pros: suggestions are visible immediately once an analysis is picked; fewer layers; reads as
  part of the form.
- Cons: the clinical section gets taller (more scrolling); edits are live, so there's no single "cancel all".

Both are bilingual, share the same grayscale style, and use the same HPO tree browser.

## How to open it

Open either `.html` file **in a real browser** (double-click, or `open <file>`). It needs a real
browser because the form reacts as you fill it — a static preview won't run those toggles.

Two controls sit at the top right:
- **Field codes** — toggles the small grey developer annotations (the `field_code` hints and the
  numbered reviewer notes) on and off. Off = the clean view a real user would see.
- **EN / FR** — switches the language. **French is the default**; switching keeps everything you've
  already entered.

Checking the **Prenatal case** box reveals the prenatal-only fields (fetal sex, gestational age)
and bumps the case to STAT priority — a good thing to show live.

## Demo tips

- **Lead with one version.** Pick A or B up front rather than flipping between them mid-demo —
  the difference is subtle and the switch reads as indecision.
- **Turn Field codes OFF before showing users.** The codes are for us; users should see the clean form.
- Leave the language on French unless the audience needs English.

## Still pending

- **French HPO terms need clinical review.** Much of the ontology's French is machine-translated
  and reads oddly. A handful of common terms were fixed by hand; the rest need a French clinician's eye.
- **TSOL (solid tumour) suggestions need confirming.** The suggested phenotypes per analysis are a
  first guess from HPO, not a clinical source. TSOL especially — somatic oncology intake may not
  use HPO phenotypes this way.
- **Prenatal is now in scope.** These fields are a first pass for feedback (this reverses an earlier
  note that prenatal was out of scope).
- **Performing-lab derivation is still open (dependency #35).** Whether the lab can be hidden and
  derived after intake depends on unresolved backend questions.

_Working notes, the full change log, and the backend-mapping detail live in `NOTES-internal.md`
(not part of the demo)._
