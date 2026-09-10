# CLAUDE.md

Notes for whoever (human or Claude) picks this repo up next — including on a different machine.
Last brought up to date: **2026-09-09**, when Lucas pulled Vincent's fork back into the
original repo. Everything below the "Working rules" section is Vincent's, from the 2026-09-08
review session, and has not been re-verified since.

## What this repo is

An interactive wireframe for Radiant's **case-creation form**, used to gather feedback from the
team and the PM. It is a demo artifact, not production code: no build, no dependencies, no test
runner. Each wireframe is **one self-contained `.html` file** you open in a browser.

The design idea it explores is **"derive-and-hide"**: any required value the system can work out
from something already entered is dropped from the form and set behind the scenes. Case type, for
example, comes from the chosen analysis and shows as a badge instead of a field.

| File | Version | Picker placement |
|---|---|---|
| `case-create-signs-inline.html` | **B — inline** | version A's picker unpacked into the form; only the HPO tree and the MONDO browser open a modal |
| `case-create-signs-modal.html` | A — modal | one button opens a picker dialog; the tree opens a second modal on top |

`README.md` is the demo-facing description (pros/cons, demo tips). It has **not** been updated
through this session — it still describes the pre-review form. Fix it before the next demo.

## Current work — read this first

**Vincent is reviewing version B (`case-create-signs-inline.html`).** Version A has not been
touched since 2026-09-07 and the two have drifted far apart: A still has the consent checkbox, the
old section titles, the id-type dropdown, the fake analyses' suggestion lists. Do not assume a
change made in B exists in A.

There is no longer a separate review file. `revue-maquette-inline.md` was deleted on 2026-09-08,
once version B had changed enough that a running changelog stopped earning its keep — feedback now
happens directly in conversation and in commit messages. Technical caveats, assumptions and open
questions live here in CLAUDE.md.

## Working rules

Two people work in this repo, from two remotes:

| Remote | Owner | What it is |
|---|---|---|
| `origin` — `luclemo/radiant-case-create-wireframe` | **Lucas** (UX) | the original repo, where both wireframes started |
| `vf` — `vferretti/radiant-case-create-wireframe-vf` | **Vincent** | the fork holding the 2026-09-08 review work |

On 2026-09-09 Lucas fast-forwarded `origin/main` onto Vincent's fork, so the two are level.
The branch **`lucas-pre-vf`** (`935ad60`) marks the last commit before that integration — the
original two-version wireframe, kept for reference and diffing. Read it, don't build on it.

**Work out whose session this is before answering.** Ask if it isn't obvious.

- **Vincent writes in French. Answer in French.**
- **Lucas writes in English. Answer in English.** He is the designer on this form. When he asks
  for UI copy, give French and English both, or ask which he needs — the product ships in both.

Discipline that holds for either of them, unless that person says otherwise:

- **Only edit a wireframe when asked to, explicitly.** These are demo artifacts shown live in
  review sessions; an unrequested edit can surprise someone mid-demo. Otherwise the point belongs
  in the conversation or a commit message, not in the file.
- **Commits are an explicit ask, and pushing is a second, separate ask.**
- Idea recorded but never built: surface the reviewer's notes inside the wireframe as a second tab
  in the `.notes-legend` block, under the **Codes** toggle.

## Data sources

- **`analysis_catalog_qlin.csv`** — the real analysis catalog (37 analyses, tenant `qlin`), the
  source for `var ANALYSES`. Columns: `id`, `code`, `name` (French, **with the act number as a
  prefix**), `description`, `primary_condition`, `primary_condition_label_en`,
  `primary_condition_label_fr`, `condition_code_system`, `analysis_type_code`, `tenant_code`.
- **The two label columns were added on 2026-09-08**, resolved from the EBI OLS API
  (`ontologies/mondo` and `ontologies/hp`); the French side is my translation, not an ontology
  source, and needs a clinician's review.
- The full HPO ontology (~18,690 terms) is **inlined** in each HTML file, between
  `/*HPO-DATA-BEGIN*/` and `/*HPO-DATA-END*/`. That is what makes the files ~1.6 MB.
- **No MONDO hierarchy anywhere on disk** — only the 26 conditions the catalog references.

## Working on these files

Single 1.6 MB HTML files. Habits that make that bearable:

- **Never read a whole file.** `grep -n` to locate, then `sed -n 'A,Bp'` to read the region.
- **Edit with a Python script** (`python3 - <<'PY'`) doing exact string replaces behind an
  `assert s.count(old)==1` guard. `sed -i` on this content is a trap. A helper worth re-declaring
  each time:
  ```python
  def rep(a,b,n=1):
      global s
      assert s.count(a)==n, (a[:70], s.count(a)); s=s.replace(a,b)
  ```
- Structure, in order: one `<style>`, the form markup, the modals, then one big `<script>` holding
  the data (`ANALYSES`, `OPTIONS`, `HPO_RAW`, `SUGGESTIONS_*`, `PATIENT_DB`, `AGES`), the i18n
  dictionaries, and the behaviour. Line numbers shift constantly — grep for a symbol.
- **Syntax-check after every script edit:**
  ```bash
  sed -n '/<script>/,/<\/script>/p' case-create-signs-inline.html | sed '1d;$d' > /tmp/check.js
  node --check /tmp/check.js
  ```
- After markup surgery, check the tags balance:
  ```bash
  python3 -c "import io,re; s=io.open('case-create-signs-inline.html',encoding='utf-8').read(); h=s[:s.index('<script>')]; print(len(re.findall(r'<div\b',h)), len(re.findall(r'</div>',h)))"
  ```

### Testing — no runner, drive headless Chrome

`google-chrome` is installed. Copy the file to the scratch directory, inject a `<script>` before
`</body>` that drives the DOM and dumps `PASS`/`FAIL` lines into a `<pre id="TESTOUT">`, then:

```bash
google-chrome --headless --disable-gpu --no-sandbox \
  --virtual-time-budget=12000 --window-size=1280,1400 --dump-dom test.html \
  | sed -n '/<pre id="TESTOUT">/,/<\/pre>/p' | sed 's/<[^>]*>//g'
```

`--screenshot=out.png` on the same command gives a visual check. Every change in this session was
verified this way (10–30 assertions each) — do the same rather than claiming something works.
Useful patterns:

- Measure layout with `getBoundingClientRect()` and assert on positions, not on looks.
- Re-run older suites against the current file by re-injecting their `<script>` block. Expect
  failures from assertions the user has since asked you to change — read them, don't just rerun.
- Timers: the patient lookup resolves after 700 ms and searches debounce 180 ms, so wrap late
  assertions in `setTimeout(…, 900)`.
- A menu item is `.menu .mlist button`; the clear row is `button.clear`; a tree row is
  `#tree-root .trow` and you click its `label.check`.

## The form as it stands

Five sections, French by default.

**1 · Analyse** — Analyse\* (searchable menu over the 37 catalog entries) | Priorité (Routine);
under them the ☐ **Cas prénatal** checkbox (it carries the `category_code` annotation and
footnote 2, the "Catégorie" label having been dropped); « Étude de recherche (consentement
obtenu) » (Pragmatic · Care4Rare · RQDM), full width — picking a study *is* the consent, so there
is no separate checkbox; Médecin prescripteur | Établissement prescripteur.

**2 · Patient (cas index)** — title becomes « Patient (cas index, mère) » in prenatal mode, where
Sexe is also prefilled Féminin. Identifiant\* | Établissement du patient\*, then the lookup status
line spanning the row, then RAMQ | Date de naissance\*, Sexe\* | Statut vital\*, Prénom | Nom. The
prenatal-only block (sexe fœtal, âge gestationnel, dates DDM/DPA) opens at the **end of this
section**, driven by the checkbox in section 1.

**3 · Signes cliniques** — the ask, then « Phénotypes observés (n) » (each row: green ✓, term,
HP id, onset menu, ✕), the search row (HPO search + « Parcourir l'arbre HPO »), then
« Suggestions pour cette analyse » (two columns read top to bottom, 6 shown, « Afficher n de
plus »). A rule, then a **checkbox** « Sélectionnez des phénotypes NON OBSERVÉS pertinents
(facultatif) » that reveals the same shape for the not-observed list (red ✗ instead of ✓, no
onset). Vertical rhythm inside the block: **12 px** under an instruction, **16 px** before a
sub-heading, **6 px** under one.

**4 · Autres informations cliniques (facultatives)** — Consanguinité | Ethnicité(s) (multi-valued,
chips); Indication principale (MONDO) typeahead + « Parcourir l'arbre MONDO »; Note clinique.
Family history **left this section on 2026-09-10** — section 5 owns it now.

**5 · Analyse familiale** — under the « Sections facultatives » divider. No opt-in checkbox: a
standing description carries the ask (« Rapportez des antécédents familiaux et incluez, le cas
échéant, … »), so the section is always open. Then the member cards, the
« ＋ Ajouter un membre de la famille » button **below** the list, and the live pedigree.

One card per relative, in two halves. The top line is the family-history record every relative
gets — Lien de parenté · Sexe · Statut · Préciser (free text) — with the relationship field kept
as narrow as its labels allow and **Statut shown as initials** (A · NA · I in French, A · NA · U
in English) so the free text takes the width that is left; each initial carries the full word as
its tooltip. Below it the checkbox « Inclure dans l'analyse génétique »: ticking it opens the
patient-identification block (Identifiant | Établissement du patient / RAMQ | Date de naissance /
Prénom | Nom — the proband's fields minus sex and life status), because a member in the analysis
becomes a Patient in Radiant.

**Rail** — Analyse (+ germline/somatic badge) · Catégorie · Priorité · ID cas index ·
Établissement du patient · Sexe · Date de naissance, then « Ajouts facultatifs »: Indication
principale · Phénotypes · Consanguinité · Ethnicité(s) · Note clinique · Famille, and the
`x sur 5 champs requis` gate.

### Conventions inside the wireframe

- **Bilingual, French by default** (`var lang = 'fr'`). Every user-visible string is a key in the
  `en` and `fr` dictionaries, referenced from markup by `data-i18n` / `data-i18n-html` /
  `data-i18n-ph` / `data-i18n-title` (the last one sets `title` **and** `aria-label`). Adding
  visible text means adding both keys.
- **Selects are not `<select>`**. They are `div.ctrl.select[data-sel]` driven by `openMenu()`; the
  canonical value lives in `dataset.value`, the visible text is the translated label. `openMenu`
  takes `(anchor, items, current, onPick, opts)` where `opts.multi` keeps it open and ticks the
  picks, `opts.search:false` suppresses the filter box, `opts.selected()` re-reads the selection.
- **Every dropdown is clearable** back to its placeholder through the `↺` row `withClear()`
  prepends whenever a control is `filled`.
- **The indication field is a typeahead, not a select**: an `input[data-sel=condition]` whose
  canonical value stays in `dataset.value` while `.value` shows the translated label — `setSel()`
  and `clearCtrl()` branch on `tagName === 'INPUT'`. Free text is never a value: on blur the label
  of the actual selection comes back.
- **Ethnicity is the one multi-valued control**: `bindMultiSelect()` stores the picks
  pipe-separated in `dataset.values` and paints them as removable chips inside the control.
- **Two kinds of phenotype row**: `makePRow(id, mode, q)` for a list you pick *from* (checkbox,
  optional match highlight), `makeSelRow(id, mode)` for a term already picked (✓/✗ marker, onset
  for observed, ✕ to drop). A picked term never appears in both.
- **Blocks that open behind a checkbox clear themselves when closed** — prenatal fields, family
  history, not-observed phenotypes. Nothing hidden should end up in the case.
- **Reviewer annotations** — the `field_code` hints, footnotes `note.1`…`note.8` and the
  `.notes-legend` block — are toggled by the **Codes** button (`#docs-toggle`, flips
  `body.hide-docs`), hidden by default. When a label is dropped, its annotations move to whatever
  replaced it rather than disappearing.
- Comments in the file explain *why* a thing is the way it is. Match that when adding code.

## Decisions already made (don't re-litigate)

- **Analysis menu is searchable.** `openMenu()` grows a filter box once a list passes
  `MENU_SEARCH_MIN` (8 entries). It matches `name` **and** `code`, **anywhere in the string** —
  analysis names start with the act number, so a prefix-only match would never find "muscul" —
  accent- and case-insensitively, and highlights the run it matched.
- **The real 37-analysis catalog replaced the 4 fake ones**, in CSV order.
- **The primary condition is derived only from a MONDO code.** An HPO code or a blank leaves the
  field empty. 34 of 37 derive; RHAB (HPO), RAPIDE and GENOR (blank) do not. The raw catalog code
  is kept in `conditionCode` either way.
- **Case type (germline/somatic) comes from `analysis_type_code`** — one type per analysis in the
  real catalog, which settles the open assumption in footnote 1.
- **Priority is never derived.** Prenatal used to force STAT and a fetal demise used to undo it;
  both rules were dropped — the user always picks.
- **The field once called "issuing site" is « Établissement du patient » / "Patient organization"**
  — it is FHIR's `managingOrganization`, not HL7v2's sending facility. The internal key stays
  `issuing`. **No default value.**
- **The identifier leads section 2**, labelled « Identifiant (numéro de dossier médical, code de
  l'étude, …) »; the id-type dropdown (MRN / Other) is gone, proband and family row alike. The
  existing-patient lookup therefore keys on **organization + identifier**: it fires whenever that
  pair is complete, whichever half moved last, re-fires when either changes, and says which field
  it is waiting for. Mocked in `PATIENT_DB`, one record behind a 700 ms delay — **1234** at
  Sainte-Justine prefills health number, names, sex and date of birth; anything else reports
  "nouveau patient" and takes back only what the lookup itself wrote.
- **HPO search is scoped to the displayed language**: each term carries `_ffr` and `_fen`
  haystacks and both the inline searches and the tree read the one matching `lang`. Searching
  "hearing" in French returns nothing, on purpose. The HP id is in both haystacks.
- **Suggested phenotypes are one placeholder list for every analysis** (`SUGGESTIONS_DEFAULT`),
  except RAPIDE and GENOR which get none — they are the non-specific analyses. The drafted
  per-analysis lists sit unread in `SUGGESTIONS_DRAFTS`; `EPI4` was renamed to the real code
  `EPIL`, and `CARDIO`/`TSOL` are orphaned rather than reassigned (a clinical call).
- **The MONDO browser is a shell.** With no hierarchy on disk it lists the catalog's conditions
  flat, behind the HPO tree's chrome, and says so on screen. A real subtree drops into it.
- **Long HPO labels wrap** rather than truncate, except on a row that shows its onset menu, where
  the name ellipsizes and keeps the full term in its tooltip. `.layout` uses `minmax(0,1fr)` +
  `min-width:0` so a 130-character label can never widen the column again.
- **One family section, two roles** (2026-09-10, Lucas). Family history left section 4 and
  section 5 now records both a relative who is only *reported* and one who is also *sequenced*.
  This is Vincent's `case-create-essai.html` "approach A" idea, done in version B's own shape —
  a per-member checkbox rather than essai's badge-and-accent-border card. The section lost its
  opt-in checkbox in the process, so it no longer clears itself; a card is dropped with its ✕.
- **The per-member checkbox gates the required fields.** A reported-only relative needs nothing
  past the top line; `validateConditionals()` skips its row entirely. Unticking runs
  `emptyFamSeq()`, which blanks the identification inputs rather than only hiding them — the
  same "nothing hidden reaches the case" rule as the other reveal blocks.
- **The pedigree draws the family, not the sequencing batch.** Every member with a relationship
  is drawn whether or not they are in the analysis. It came back on 2026-09-10 after the
  2026-09-08 redesign dropped its host div; `renderPedigree()` had survived untouched, but two
  of its selectors had rotted — it read sex from a field the card no longer had, and status from
  `.seg:not([data-fam-seg])`, which the renamed segment no longer matched. Hence Sexe returning
  to the card. There is **no sequenced ring** in the notation, despite what the old comment said.
- **Section 5 offers the full relation list again** (`OPTIONS.relation`, 8 entries), not the four
  sequenceable ones: now that it carries family history, a reported relative can be a
  half-sibling or an « Autre ». The pedigree still lists those rather than placing them.

## Open questions

Ranked by how much they block work:

1. **MONDO labels come from EBI OLS**, fetched on Vincent's go-ahead. Confirm that source is
   acceptable, and get the French translations reviewed. There is still **no MONDO hierarchy** to
   put behind the browse button.
2. **Real per-analysis phenotype suggestions** — a clinical call nobody has made. Vincent can
   supply lists, or I draft them from HPO as provisional.
3. **The catalog has no English names.** In EN the form shows the French name.
4. **Category is not in the catalog**; Postnatal is assumed for all 37.
5. **French HPO terms are largely machine-translated** and need a French clinician's review.
6. **Two apparent duplicates in the catalog**: NPC and NEUTP both read « Neutropénie congénitale »;
   HLEB and HLH both carry act number 55412. Data-entry error, or a real distinction?
7. **Switching analysis does not clear an already-derived indication** — MMG → RAPIDE (no derived
   condition) leaves « Maladie neuromusculaire » in the field. *Clearing* the analysis does clear
   it. Only the switch case is inconsistent.
8. Whether the search should also apply to **établissement prescripteur / du patient** — plugging
   in the real Quebec establishment list would trip the 8-entry threshold on its own.
9. **`README.md` is stale**, and **version A** has not followed any of this.
