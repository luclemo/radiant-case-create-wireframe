# Case creation — wireframe

Interactive wireframe for the new case-creation form, exploring **"derive-and-hide"**: any
required value the system can work out from something already entered is dropped from the form
and set behind the scenes. Case type, for example, is derived from the analysis and shown as a badge.

Open **`case-create-signs-inline.html`** in a real browser (double-click, or `open <file>`). The
form reacts as you fill it, so a static preview won't work.

`case-create-signs-modal.html` is an abandoned earlier version — ignore it.

## The form

Five sections — **Analyse · Patient (cas index) · Signes cliniques · Autres informations
cliniques · Famille** — plus a summary rail tracking required fields.

- **Analysis menu** — the real 37-analysis catalog (`analysis_catalog_qlin.csv`), searchable.
  Matches anywhere in the string, since names are prefixed with act numbers.
- **Patient lookup is identifier-first** — keys on identifier + patient organization. `1234` at
  Sainte-Justine prefills health number, names, sex, date of birth; anything else reports a new
  patient. Resolves after a deliberate ~700 ms delay.
- **Clinical signs** — observed (green ✓, with onset), and not-observed (red ✗) behind an opt-in
  checkbox.
- **HPO search matches the displayed language only** — "hearing" in French returns nothing, by design.
- **MONDO browser is a shell** — no hierarchy on disk, so it lists the catalog's conditions flat
  and says so on screen.
- **Cas prénatal** retitles section 2 « Patient (cas index, mère) », prefills Sexe as Féminin, and
  opens the prenatal block (fetal sex, gestational age, DDM/DPA) at the end of that section. Does
  **not** change priority.

## Controls (top right)

- **Field codes** (« Codes » in FR) — toggles the `field_code` hints and numbered reviewer notes.
  Off = the clean user view.
- **EN / FR** — French is the default. Switching keeps what you've entered.

## Demo tips

- Turn Field codes **off** before showing users.
- Leave the language on French unless the audience needs English.
- Have `1234` / Sainte-Justine ready for the lookup — it's the only record in the mock.

## Still pending

- **French HPO terms need clinical review** — largely machine-translated; some common terms fixed by hand.
- **French MONDO labels too** — resolved from the EBI OLS API, translated for the mock.
- **Phenotype suggestions are placeholder** — one generic list for every analysis except RAPIDE
  and GENOR (none). Real per-analysis lists are an unmade clinical call.
- **No MONDO hierarchy** behind the browse button.
- **Two possible catalog errors** — NPC and NEUTP both read « Neutropénie congénitale »; HLEB and
  HLH both carry act number 55412.
- **Performing-lab derivation still open (dependency #35)** — depends on unresolved backend questions.
