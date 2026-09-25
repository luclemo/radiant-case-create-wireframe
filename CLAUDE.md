# CLAUDE.md

Notes for whoever picks this repo up next. Current to **2026-09-25**. Some of it dates from
Vincent's 2026-09-08 review and has not been re-verified.

## What this repo is

An interactive wireframe for Radiant's **case-creation form** — a demo artifact for the team and
the PM, not production code. No build, no dependencies, no test runner; one self-contained
`.html` you open in a browser.

Its design idea is **"derive-and-hide"**: any required value the system can work out is dropped
from the form and set behind the scenes (case type comes from the analysis and shows as a badge).

| File | What |
|---|---|
| `case-create-signs-inline.html` | **the wireframe** — version B, picker inline, only the HPO tree and MONDO browser open a modal |
| `docs/index.html` | **the demo — GENERATED, never hand-edit** (see below) |
| `make-demo.py` | builds the demo from the wireframe |
| `case-create-essai.html` | Vincent's family-section trial, kept for comparison |
| `README.md` | demo-facing description (pros/cons, demo tips) |

Version A (`case-create-signs-modal.html`) was **deleted 2026-09-15** after drifting far from B;
it survives in git and on branch `lucas-pre-vf` (`935ad60`). Read that branch, don't build on it.

### The demo build

Run `python3 make-demo.py` after **any** wireframe change and commit both. It exists because
**this repo has already lost a wireframe to drift** — a hand-copied demo would go the same way.
Every replace in it is guarded, so it fails loudly rather than emitting a half-transformed page.
Served by **GitHub Pages from `main` / `/docs`**.

Prove the transform is behaviour-neutral by running the suites against it:

```bash
TARGET=docs/index.html ./tests/run.sh
```

What it changes and nothing else: topbar → a slim strip with the language switcher and an
**ⓘ Instructions** button; the « Codes » toggle kept in the DOM but hidden (its wiring looks the
element up by id); a seven-line instructions panel in both languages; retitled, plus `noindex`.

The instructions are a **panel, not a modal** — they must stay readable while the form is used,
so the block expands *above §1, inside the form column*, covering no field and moving no rail.
A disclosure: no focus trap, no backdrop, and **Esc is deliberately left alone** (it belongs to
the real modals). Lines run in the order the form is read; the lookup one is deliberately longer
because it names both fields by their exact §2 labels. The suggestions line **names no analysis** —
all but RAPIDE and GENOR show the same list, so naming one would imply a specificity the mock
lacks. (If a code is ever needed: **RGDI**; `RDGI` does not exist.)

## Working rules

| Remote | Owner |
|---|---|
| `origin` — `luclemo/radiant-case-create-wireframe` | **Lucas** (UX, designer on this form) |
| `vf` — `vferretti/radiant-case-create-wireframe-vf` | **Vincent** |

**Vincent is reviewing version B** — the only wireframe left to change. There is no separate
review file: feedback happens in conversation and commit messages, and caveats, assumptions and
open questions live **here**.

**Work out whose session this is before answering.** Ask if it isn't obvious.

- **Vincent writes in French → answer in French. Lucas writes in English → answer in English.**
- UI copy is always **French and English** both, or ask which is needed.
- **Only edit a wireframe when asked, explicitly.** They get demoed live; an unrequested edit
  surprises someone mid-demo.
- **Commits are an explicit ask; pushing is a second, separate ask.** Short bodies, no co-author
  trailer.
- Idea recorded, never built: the reviewer's notes as a second tab in `.notes-legend`.

## Working on these files

1.7 MB single HTML files. Habits that make that bearable:

- **Never read a whole file.** `grep -n` to locate, `sed -n 'A,Bp'` to read. Line numbers shift —
  grep for a symbol.
- **Edit with a Python script** (`python3 - <<'PY'`) doing exact replaces behind a count guard.
  `sed -i` on this content is a trap.
  ```python
  def rep(a,b,n=1):
      global s
      assert s.count(a)==n, (a[:70], s.count(a)); s=s.replace(a,b)
  ```
- Structure, in order: one `<style>`, form markup, modals, then one `<script>` holding the data
  (`ANALYSES`, `OPTIONS`, `HPO_RAW`, `SUGGESTIONS_*`, `PATIENT_DB`, `AGES`), the i18n dictionaries,
  then the behaviour.
- **Syntax-check after every script edit**, and check tag balance after markup surgery:
  ```bash
  sed -n '/<script>/,/<\/script>/p' case-create-signs-inline.html | sed '1d;$d' > /tmp/check.js
  node --check /tmp/check.js
  python3 -c "import io,re; s=io.open('case-create-signs-inline.html',encoding='utf-8').read(); h=s[:s.index('<script>')]; print(len(re.findall(r'<div\b',h)), len(re.findall(r'</div>',h)))"
  ```

### Testing — no runner, drive headless Chrome

`./tests/run.sh [name-filter]`, or `TARGET=docs/index.html ./tests/run.sh` for the demo. Suites
live in `tests/` (**gitignored — local only**); each is a `<script>` injected before `</body>`
that drives the DOM and dumps PASS/FAIL into `<pre id="TESTOUT">`. `tests/README.md` maps them.

- Chrome on macOS is **not** `google-chrome` — it is
  `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. Declare `CHROME="…"` once.
- `--screenshot=out.png` for a visual check. **Colour needs the screenshot**: position assertions
  once passed on a demise slash that was invisible, dark-on-dark.
- Assert on `getBoundingClientRect()` positions, not on looks.
- **Expect failures after a deliberate change** — read them and update the assertion, don't rerun.
- Timers: lookup resolves after 700 ms, searches debounce 180 ms — wrap late assertions in
  `setTimeout(…, 900)`.
- Selectors: menu item `.menu .mlist button`; clear row `button.clear`; tree row `#tree-root .trow`
  (click its `label.check`).

## Data sources

- **`analysis_catalog_qlin.csv`** — the real catalog (37 analyses, tenant `qlin`), source for
  `ANALYSES`. `name` is French **with the act number as a prefix**.
- The two MONDO/HPO label columns came from the **EBI OLS API**; the French side is a translation,
  not an ontology source, and needs clinical review.
- The full HPO ontology (~18,690 terms) is **inlined** between `/*HPO-DATA-BEGIN*/` and
  `/*HPO-DATA-END*/` — that is what makes the files 1.7 MB.
- **No MONDO hierarchy on disk** — only the 26 conditions the catalog references.

## The form as it stands

Five sections, French by default. `*` = in the required gate.

**1 · Analyse** — Analyse\* | Priorité (Routine; **prefilled STAT in a prenatal case**, see
decisions); ☐ **Cas prénatal**; « Étude de recherche » full width (picking a study *is* the
consent, so no separate checkbox); then the prescriber, alone on its line and **carrying no field
label** — just ☑ « Je suis médecin prescripteur ou responsable », with « Qui demande cette
analyse » + an input appearing only when unticked.

**2 · Patient (cas index)** — Identifiant\* | Établissement du patient\*, the lookup status line
spanning the row, RAMQ | **DDN\* · Sexe\*** sharing one cell, Prénom\* | Nom\*. The DDN·Sexe pair
fits 368 px only because both halves shrink: the label to « DDN » (`lbl.dobShort`, **§2 only** —
`lbl.dob` still spells it out in §5 and the patient dialog), and Sexe to initials with the full
word as tooltip. The rail translates `dataset.value`, so it reads « Féminin » not « F ».

In **prenatal** mode the title becomes « Patient (cas index, mère) » and Sexe prefills Féminin:
**the proband is the fetus**, and this section holds the *mother's* identity only because a fetus
has no Patient record. A prenatal block — **« Informations fœtales »** — then opens at the end of
the section: Sexe (fœtus), then Âge gestationnel as DDM / DPA / Fœtus décédé, **the date directly
under the option that asks for it** (the option is the label) with the derived age to its right.

**3 · Signes cliniques** — the ask, the search row (HPO search + tree button) **pinned directly
under it**, then « Phénotypes observés (n) » and « Suggestions » — one column, 5 shown, « Afficher
n de plus ». Every row is the same checklist row: checkbox, term, HP id, and an onset menu once
ticked (observed only). Below a rule, the not-observed half: picks as dismissable badges and one
button opening the HPO browser — no checkbox, no inline search, because it is a short aside rather
than the list you work through. Rhythm: 12 px under an instruction, 16 px before a sub-heading,
6 px under one.

**4 · Autres informations cliniques (facultatives)** — Consanguinité | Ethnicité(s) (chips);
Indication principale (MONDO typeahead + browse); Note clinique.

**5 · Famille** — under « Sections facultatives ». No opt-in checkbox; a standing description
carries the ask, so the section is always open. One card per relative, in two halves: the
family-history top line (Lien de parenté · Sexe · Statut · Préciser), then ☐ « Inclure dans
l'analyse génétique », which opens the patient-identification block — because a member in the
analysis becomes a Patient in Radiant. Statut shows as initials so the free text takes the width
that is left.

**Prenatal exception**: a « Mère » card in the analysis does not re-ask for §2's identity. It shows
one derived line, `.probandref` (« Dossier patient : **A-77** · CHU Sainte-Justine · Marie-Claude
Gagnon »), built by `paintProbandRef()` and repainted by every `recompute()`. The six inputs stay
**empty and hidden** behind it, so nothing stale reaches the case and switching the card to another
relative opens a blank block. `mirroredFamRow()` decides: prenatal **and** Mother **and** in the
analysis.

**Rail** — the two actions **lead the card**: Créer le cas · Enregistrer le brouillon · progress
bar · `x sur 7 champs requis`, then 22 px, then « Résumé du cas »:

> Analyse (+ germline/somatic badge, + a composition badge once not solo) · Catégorie · Priorité ·
> ID cas index · Établissement du patient · Sexe · Date de naissance · **Nom** · **Phénotypes** ·
> [« Informations fœtales »: Sexe fœtal · Âge gestationnel] · « Ajouts facultatifs »: Indication
> principale · Consanguinité · Ethnicité(s) · Note clinique · Famille · **pedigree**

- « Phénotypes » sits **above** the fetal block even though §3 follows §2, because that block is a
  *captioned* group and a captioned group must end at the next caption — below it, the proband's
  count read as a fetal fact.
- In prenatal mode « ID cas index » → « ID mère » and « Sexe » → « Sexe (mère) », each swapping
  between two i18n keys via `swapKey()` so a language switch repaints by itself. DDN and Nom are
  hers too but are **not** qualified — three parentheses in a row would be noise.
- The gestational row carries what is stored **and** what is derived: « DDM 2026-04-02 · 24 sem. ».
- Shell 1200 px, rail 340 px, `position:sticky; top:24px`. With a pedigree drawn the rail can
  exceed a laptop viewport, but what falls below the fold is now a picture, not the button.

## Conventions inside the wireframe

- **Bilingual, French by default** (`var lang='fr'`). Every visible string is a key in the `en` and
  `fr` dictionaries via `data-i18n` / `-html` / `-ph` / `-title` (the last sets `title` **and**
  `aria-label`). New visible text means **both** keys.
- **`localize()` assigns `textContent`** to the `[data-i18n]` element — so anything else inside it
  (a `<sup>`, a badge) is wiped on every language switch. Wrap the text in a `<span>` and put the
  sibling outside it. Same trick on §5's title and the Save-draft footnote.
- **`[hidden]` is only a `display:none` default** and any display of our own beats it. A revealed
  block needs its own `[hidden]{display:none}` rule or it is never actually hidden.
- **Selects are not `<select>`** — `div.ctrl.select[data-sel]` driven by `openMenu(anchor, items,
  current, onPick, opts)`. Canonical value in `dataset.value`, visible text is the translated
  label. `opts.multi` keeps it open, `opts.search:false` drops the filter box.
- **Every dropdown is clearable** back to its placeholder via the `↺` row `withClear()` prepends
  while a control is `filled` — except a required one, which keeps no clear.
- **A placeholder names the thing it wants, unless the control is too narrow to show it.**
  « Sélectionner une étude… », « …un établissement… », each on its own `ph.sel*` key.
  **`ph.selRelation` is the one exception** (« Sélectionner… »): §5 keeps that field as narrow as
  its labels allow, and a placeholder you cannot read names nothing. `ph.select` survives only as
  the fallback for a control that declares none — none does. `localize()` copies `data-i18n-ph`
  into `dataset.ph`, which is what makes clearing restore *its* placeholder.
- **Free-text placeholders say what to type**: the prescriber's input asks « Nom du médecin »
  (« Qui demande cette analyse » is its *label*); the names read « Prénom » / « Nom », a bare echo,
  because a name has no format or example to offer.
- **« Inconnu » is an answer, so the rail inks it.** A value goes dark (`.v.done`) as soon as the
  user has answered, Unknown included; only the em-dash stays muted. Catégorie and Priorité ink
  unconditionally — they ship with defaults.
- **The indication field is a typeahead, not a select** — `input[data-sel=condition]`, canonical
  value in `dataset.value`. Free text is never a value: on blur the real label comes back.
- **Ethnicity is the one multi-valued control** — `bindMultiSelect()`, picks pipe-separated in
  `dataset.values`, painted as removable chips.
- **One way a phenotype is drawn**: `makePRow()` everywhere an observed term appears. Selection is
  the row's own active state (`label.check.on`) — a term is dropped by unticking it, no ✓/✗ marker
  and no row ✕. `makeNegBadge()` draws a not-observed pick as a pill with a ✕. A picked term never
  appears twice: it leaves the suggestions for the picked list.
- **Only the observed list has an inline search.** `searchIds()` / `renderSearchResults()` take no
  mode.
- **Not-observed badges are deliberately not struck through** — the heading already says these were
  looked for and absent; strikethrough reads as "removed from the list".
- **Blocks that open behind a checkbox clear themselves when closed** — prenatal fields, the family
  identification block, the prescriber input. Nothing hidden should reach the case. (The
  not-observed list is the exception: no checkbox, so badges are dropped one at a time.)
- **User text is never concatenated into `innerHTML`.** There is no escaping helper here; mixed
  content is built with `createTextNode` / `createElement` (`markMatch`, `renderChips`,
  `paintProbandRef`). An identifier is free text, so this matters.
- **Reviewer annotations** — `field_code` hints, footnotes `note.1`…`note.8`, the `.notes-legend`
  block — toggle on the **Codes** button (`#docs-toggle`, flips `body.hide-docs`), hidden by
  default. **When a label is dropped, its annotations move to whatever replaced it.**
- Comments in the file explain *why*. Match that when adding code.

## Decisions already made (don't re-litigate)

### Analysis, catalog, phenotypes

- **The menu is searchable** once a list passes `MENU_SEARCH_MIN` (8). Matches `name` **and**
  `code`, **anywhere in the string** (names start with the act number, so prefix-only would never
  find "muscul"), accent- and case-insensitive, and highlights the run.
- **The real 37-analysis catalog replaced the fake one**, in CSV order.
- **Primary condition derives only from a MONDO code** — an HPO code or a blank leaves it empty
  (RHAB, RAPIDE, GENOR don't derive). Raw code kept in `conditionCode` either way.
- **Case type (germline/somatic) comes from `analysis_type_code`** — one per analysis.
- **Suggested phenotypes are one placeholder list for every analysis** (`SUGGESTIONS_DEFAULT`),
  except RAPIDE and GENOR which get none. Drafted per-analysis lists sit unread in
  `SUGGESTIONS_DRAFTS`.
- **HPO search is scoped to the displayed language** — each term carries `_ffr`/`_fen` haystacks.
  Searching "hearing" in French returns nothing, on purpose. The HP id is in both.
- **The MONDO browser is a shell** — with no hierarchy on disk it lists the catalog's conditions
  flat and says so on screen. A real subtree drops in.
- **Long HPO labels wrap** rather than truncate, except on a row showing its onset menu, where the
  name ellipsizes with the full term in its tooltip. `minmax(0,1fr)` + `min-width:0` stop a
  130-character label widening the column.

### The patient and the lookup

- **« Établissement du patient »** (not "issuing site") — FHIR's `managingOrganization`, not
  HL7v2's sending facility. Internal key stays `issuing`. **No default value.**
- **The identifier leads §2**, labelled simply « Identifiant »; examples live in its placeholder.
  No id-type dropdown. So the lookup keys on **organization + identifier** — it fires whenever the
  pair is complete, whichever half moved last. Mocked in `PATIENT_DB`: **1234** at Sainte-Justine,
  700 ms delay; anything else reports "nouveau patient". While the pair is incomplete the line
  says **nothing**.
- **A found patient is confirmed before any PHI is written.** A match opens `#patient-modal`
  showing the record in full — names, sex, DOB, RAMQ — and only « Utiliser ce patient » writes it.
  Full PHI deliberately: the dialog exists so a human can tell two siblings apart.
- **Rejecting a match means the key is wrong**, not "ignore that record" — org + identifier is
  unique, so there is deliberately **no "use it anyway"**. Rejecting marks the identifier in error,
  warns, and **blocks Create** while leaving Save draft alone. What was typed is never erased.
  `lookupDecision` records one answer per key, so a rejected key never re-opens the modal in a loop.

### The gate

- **7 required fields, 9 in a prenatal case.** Analysis, identifier, patient organization, sex,
  date of birth, **name**, **clinical signs**; prenatal adds fetal sex and gestational age.
- **The rail's count *is* its rows** — `recompute()` builds `rows[]` as `[rail row id, satisfied]`
  pairs and the gate is how many are inked.
- **First and last name count as ONE item**, because they share one rail row. Both halves are
  needed to tick it. `validateConditionals()` checks them **separately** on a §5 card, because that
  function marks fields, and a field is either filled or not.
- **Clinical signs is satisfied by at least one OBSERVED phenotype** — a not-observed term is an
  aside. The row's *text* still counts every term, so the count answers "what does this case
  record" while the ink answers "is the requirement met". `sumPheno()` sets text only;
  `recompute()` owns the ink.
- §5's « Dossier patient » line **keeps** its no-name fallback: it repaints on every keystroke, so
  it is read long before the names are typed. Only *Create* is gated.

### Prenatal

- **The fetus is the proband; the mother is the patient of record.** A fetus has no Patient record,
  so §2 carries her identity. Such a case is **solo by default**, and the mother is then an
  ordinary relative, added and removed like any other.
- **Her identification is stated, not re-asked** — derive-and-hide applied to §5. A read-only copy
  of §2 was built first and cut: six inert fields cost 240 px to say nothing new, and fields that
  look editable but are not invite clicks that do nothing. The one line replaced it at 43 px.
- **Leaving « Mère » clears the block; a relationship correction does not.** Those values are §2's
  and the user never typed them there — keeping them would hand her identifiers to a sister. On an
  ordinary card the same edit keeps what was typed: that is the user's own input.
- **The pedigree's proband node reads the fetal sex**, not §2's Sexe (which prenatal prefills
  Féminin). Both segments use the same `M|F|U` codes.
- **Gestational age is stored as a date and derived as an age.** `gestState()` reads basis + date;
  `round(days/7)` from a DDM, `round((280 − daysUntil)/7)` from a DPA, UTC midnights so a DST
  boundary cannot shift a day. **These are CLIN's formulas** (`clin-portal-ui`, `src/utils/age.ts`,
  `HybridPatientFoetus`). An age is only true on the day it is computed, so the date is the value
  and the age is always a view. `prenatalReqs()` reads the same `gestState()`, so gate and display
  cannot drift.
- **The date bounds are asymmetric, deliberately.** DDM capped at **today**, no floor. DPA capped
  at **today + 280 days**, no floor (an overdue pregnancy has a due date behind it). Out of range:
  no age, muted rail row, failed gate, marked field — never a silent block.
- **The pedigree slashes the proband on a fetal demise** — « Fœtus décédé » is the only death the
  form records and it is the *proband's*, and standard notation slashes a stillbirth. Prenatal
  only. Drawn **white on a filled symbol**, since the proband is hardcoded affected.
- **Priority is prefilled, never derived** (2026-09-08, revised 2026-09-25). Ticking « Cas
  prénatal » sets **STAT**, *unless* the basis is « Fœtus décédé » — nothing to rush for. The
  control stays open throughout and the change flashes.
  - **Two inputs decide it**, so one idempotent function (`syncPriorityPrefill`) reconciles the
    checkbox and the basis; they can be toggled in any order.
  - **Two flags, not one.** `priorityBeforePrenatal` holds what to put back and is non-null while
    the form owns the value; `priorityUserSet` is the separate question of whether it may take it
    at all. With one flag, letting go on a demise let the form grab the value back on the way to
    DDM, overwriting a deliberate call. Only a fresh tick clears `priorityUserSet`.
  - **The user's own answer wins and keeps winning** for that episode. Contrast Sex, which prenatal
    genuinely *knows* and therefore restores unconditionally.

### Family (§5)

- **One section, two roles** — a relative who is only *reported* and one who is also *sequenced*.
  Vincent's essai "approach A", done in B's shape: a per-member checkbox. No opt-in checkbox on the
  section, so it never clears itself; a card is dropped with its ✕.
- **The per-member checkbox gates the required fields.** A reported-only relative needs nothing past
  the top line. Unticking runs `emptyFamSeq()`, which **blanks** the inputs rather than just hiding
  them.
- **The pedigree draws the family, not the sequencing batch** — every member with a relationship,
  in or out of the analysis. There is **no sequenced ring** in the notation.
- **The composition badge counts the batch** — proband + every card ticked in — as « Duo » ·
  « Trio » · « Quatuor »/"Quad", and past four the count (« 5 séquencés »). Deliberately the
  **opposite** of the pedigree: the Famille row counts cards, this counts the batch, and the two
  disagreeing is correct. **Solo shows nothing** (the default, so a badge would say nothing). It
  uses the plain `.badge` so the only colour in the row stays on the case type, and it shows even
  with no analysis picked. « Quatuor » is proper French but **worth checking with Vincent** — lab
  usage may be "quad" in both.
- **§5 offers the full relation list** (`OPTIONS.relation`, 8 entries), not the four sequenceable
  ones — family history can name a half-sibling or an « Autre ». See open question 9.

### The prescriber

- **One checkbox, no field label** (2026-09-25). Default: ☑ « Je suis médecin prescripteur ou
  responsable », nothing else. Unticking reveals « Qui demande cette analyse » **and** its input,
  together. A field label in the default state would have labelled nothing.
- **Both states feed the one `ordering_physician`** — ticked, the system captures the **current
  user**; unticked, the **typed name**. Hence the annotation riding the checkbox line.
- **This derives from the session, not from the page**, which is new: every other derive-and-hide
  value here reads another field. See open question 12.
- **« Établissement prescripteur » (`ordering_organization_code`) was removed outright** — markup,
  `OPTIONS.ordering`, `state.orderingSet`, both key pairs, and its footnote. `ORGS` stays.

### The rail

- **Create and Save draft lead the card.** They used to close it, below the pedigree — which made
  the primary action sit below the fold. The whole block moved together (buttons, bar, count),
  because the bar and count explain the button and are useless apart from it.
- **`flashNote()` writes to `#railflash`**, empty at rest and collapsed by `:empty{display:none}`,
  so it costs no height. A flash pushes the summary down for 2.4 s — a deliberate trade for keeping
  feedback under the button that raised it. A language switch clears a live flash.
- **Consanguinity is the one segment you can clear** — clicking the selected option again unsets
  it, and the rail falls back to the muted em-dash. Special-cased on `data-seg="consang"`: every
  other `.seg` is required, so a general toggle would let a stray click un-answer one.
- **Statut vital left the form** (team decision). At case creation the value is always Alive.
  Radiant is making `life_status_code` nullable; until then the column is `NOT NULL`, so something
  supplies it server-side. It is a **patient-level** value — only `family` holds per-case ones.

### Reviewer annotations

- **Eight notes, numbered in reading order**: §1 (1, 2, 3), §2 (4, 5), §3 (6), §5 (7 on the section
  title, 5 again on the card), rail (8).
- **The `<ol>` renumbers itself; the `<sup class="fn">N</sup>` anchors do not.** Removing a note
  means renumbering every anchor *and* key after it. Checking the order needs the **rendered page**
  — the rail's markup sits before the family-row template but after §5 on screen.
- **Note 7 hangs off §5's title, not a field.** On the family card's « Établissement du patient »
  it was ambiguous (§2's field of the same name carries note 4) and buried, since that block only
  opens once a member is ticked in.

## Open questions

Ranked by how much they block work.

1. **MONDO labels come from EBI OLS** — confirm the source is acceptable and get the French
   reviewed. There is still **no MONDO hierarchy** for the browse button.
2. **Real per-analysis phenotype suggestions** — a clinical call nobody has made.
3. **The catalog has no English names.** In EN the form shows the French name.
4. **Category is not in the catalog**; Postnatal assumed for all 37.
5. **French HPO terms are largely machine-translated** and need a clinician's review.
6. **Two apparent catalog duplicates**: NPC / NEUTP both « Neutropénie congénitale »; HLEB / HLH
   both act 55412. Error, or a real distinction?
7. Whether search should apply to **« Établissement du patient »** — the real Quebec list would
   trip the 8-entry threshold on its own. **On hold** since 2026-09-15.
8. **Radiant has no prenatal fields at all.** Checked against `radiant-network/radiant-portal`:
   across all 20 migrations, `public.cases`, `public.patient` and the `CaseBatch` API, the only
   prenatal thing is `category_code ∈ {prenatal, postnatal}` — **no** gestational age, LMP/EDD date
   or fetal sex. So this form's `(gestational_age)`, `(lmp_date)`, `(edd_date)` and
   `(fetal_sex_code)` are **proposals, not references**. CLIN already ships the shape — should
   Radiant adopt it? CLIN also has `NEW_BORN` alongside `PRENATAL`; Radiant does not.
9. **§5's relation list is wider than Radiant accepts.** The API constrains
   `relation_to_proband_code` to `mother father brother sister sibling proband`; the form offers
   four more and neither `sibling` nor `proband`. Widening it was a deliberate call for family
   history — the gap is real either way.
10. **`submitter_patient_id_type` is `NOT NULL`** in `public.patient`, and the form dropped the
    id-type dropdown. The batch API does not carry it, so something defaults it server-side.
    Confirm what, rather than assume.
11. **A prenatal case may submit the mother twice.** The proband row carries her identifiers (the
    fetus has none), so adding « Mère » in §5 sends the same organization + identifier again under
    `relation_to_proband_code: mother`, against `UNIQUE (organization_code, submitter_patient_id)`.
12. **What does `ordering_physician` hold, and can it be derived from the session?** The ticked
    checkbox is meant to capture the current user. That rests on two unconfirmed things: that the
    form knows who the user is, and what the field stores. **If free text**, both paths yield a
    name and the control is right. **If a practitioner reference**, the ticked path has an id and
    the typed path does not — a free-text input would be the wrong control.
    **A starting point, not a decision** (Lucas): make the unticked path a **typeahead over the
    member directory** — a hit records the **id**, a miss falls back to **free text**. Nothing of
    this is built.
