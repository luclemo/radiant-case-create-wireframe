# Case creation — wireframe

Interactive wireframe for the new case-creation form, exploring **"derive-and-hide"**: any
required value the system can work out from something already entered is dropped from the form
and set behind the scenes. Case type, for example, is derived from the analysis and shown as a badge.

Open **`case-create-signs-inline.html`** in a real browser (double-click, or `open <file>`). The
form reacts as you fill it, so a static preview won't work.

One other file sits beside it, not the current design:

- `case-create-essai.html` — a trial exploring the same one-family-section idea in a different
  shape (badge and accent border per member, a composition banner). Kept for comparison; the
  answer that shipped into the inline version is the per-member checkbox described below.

## The form

Five sections — **Analyse · Patient (cas index) · Signes cliniques · Autres informations
cliniques · Famille** — plus a summary rail tracking the seven required fields (nine
in a prenatal case).

- **Analysis menu** — the real 37-analysis catalog (`analysis_catalog_qlin.csv`), searchable.
  Matches anywhere in the string, since names are prefixed with act numbers.
- **Patient lookup is identifier-first, and confirmed before anything is written** — it keys on
  identifier + patient organization. A match opens a dialog showing the record in full (names,
  sex, date of birth, RAMQ); only « Utiliser ce patient » fills the form, so a mistyped
  identifier plants nothing in the case. Rejecting means the key is wrong — organization +
  identifier is unique, so there is deliberately no "use it anyway" — and it blocks Create until
  the identifier changes. Resolves after a deliberate ~700 ms delay.
- **Clinical signs** — one checklist row throughout: tick it to pick a phenotype, and a ticked
  observed row grows an onset menu. Suggestions are a single column cut at 5, « Afficher n de
  plus » for the rest. Not-observed signs sit behind a button that opens the HPO browser and come
  back as dismissable badges.
- **HPO search matches the displayed language only** — "hearing" in French returns nothing, by design.
- **MONDO browser is a shell** — no hierarchy on disk, so it lists the catalog's conditions flat
  and says so on screen.
- **Cas prénatal** — the proband is the **fetus**; section 2 holds the mother's identity only
  because a fetus has no patient record of its own, so it retitles to « Patient (cas index,
  mère) » and prefills Sexe as Féminin. An « Informations fœtales » block opens at the end of
  that section: sexe fœtal, then DDM / DPA / fœtus décédé with the date tucked under the option
  it belongs to and the **calculated gestational age** beside it. The rail renames « ID cas
  index » to « ID mère » and grows a matching fetal block. Does **not** change priority.
- **A prenatal case is solo by default.** Section 5 stays empty until you add someone; the mother
  is then an ordinary relative of the fetus, and ticking her into the analysis states the patient
  record already captured in section 2 rather than asking for it twice.
- **Famille owns both family roles** — one card per relative records the family history
  (lien de parenté · sexe · statut · préciser), and ticking « Inclure dans l'analyse génétique »
  opens the patient-identification fields, because a member in the analysis becomes a Patient in
  Radiant. The live **pedigree** is drawn in the summary rail, under the Famille row, from every
  member with a relationship — it is a picture of the family, not of the sequencing batch.

## Controls (top right)

- **Field codes** (« Codes » in FR) — toggles the `field_code` hints and numbered reviewer notes.
  Off = the clean user view.
- **EN / FR** — French is the default. Switching keeps what you've entered.

## Demo tips

- Turn Field codes **off** before showing users.
- Leave the language on French unless the audience needs English.
- Have `1234` / Sainte-Justine ready for the lookup — it's the only record in the mock. Show both
  paths: confirming the patient, and rejecting to see Create block.
- Add two family members and tick one into the analysis — that draws the pedigree in the rail.

## Still pending

- **French HPO terms need clinical review** — largely machine-translated; some common terms fixed by hand.
- **French MONDO labels too** — resolved from the EBI OLS API, translated for the mock.
- **Phenotype suggestions are placeholder** — one generic list for every analysis except RAPIDE
  and GENOR (none). Real per-analysis lists are an unmade clinical call.
- **No MONDO hierarchy** behind the browse button.
- **Two possible catalog errors** — NPC and NEUTP both read « Neutropénie congénitale »; HLEB and
  HLH both carry act number 55412.
- **Performing-lab derivation still open (dependency #35)** — depends on unresolved backend questions.
- **Confirming a candidate patient should probably be audited** — viewing a record is an auditable
  event in most clinical systems, and the confirm dialog is where that would be logged. Not
  modelled here; worth deciding before the real lookup is wired.
