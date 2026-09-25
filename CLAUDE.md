# CLAUDE.md

Notes for whoever (human or Claude) picks this repo up next — including on a different machine.
Last brought up to date: **2026-09-25**, when the prescriber became a single checkbox and
« Établissement prescripteur » was removed. Before that, **2026-09-16**, after the seven "minor UI improvements" (required
names, the rail's « Nom » row, « Sexe (mère) », « Famille », clinical signs in the gate,
a clearable consanguinity, a shorter relation placeholder), the move of Create / Save draft to
the head of the rail, and the family-composition badge. Parts of the sections below still date from Vincent's 2026-09-08 review session and have
not been re-verified since.

## What this repo is

An interactive wireframe for Radiant's **case-creation form**, used to gather feedback from the
team and the PM. It is a demo artifact, not production code: no build, no dependencies, no test
runner. Each wireframe is **one self-contained `.html` file** you open in a browser.

The design idea it explores is **"derive-and-hide"**: any required value the system can work out
from something already entered is dropped from the form and set behind the scenes. Case type, for
example, comes from the chosen analysis and shows as a badge instead of a field.

The wireframe is **`case-create-signs-inline.html`** — version **B**, the inline picker: the
picker sits unpacked in the form, and only the HPO tree and the MONDO browser open a modal.
Version A (`case-create-signs-modal.html`, one button opening a picker dialog on top of which the
tree opened a second) was **deleted on 2026-09-15**, untouched since 2026-09-07 and far drifted
from B. Git history and the `lucas-pre-vf` branch (`935ad60`) still have it.

`case-create-essai.html` is Vincent's family-section trial, kept for comparison.

**`docs/index.html` is the user-facing demo, and it is GENERATED — never hand-edit it.**
`make-demo.py` builds it from the master; run `python3 make-demo.py` after any change to the
wireframe and commit both. It is a build step, not a dependency: the output is still one
self-contained file you can open in a browser, and the repo still has nothing to install.
The generator exists because **this repo has already lost a wireframe to drift** — version A was
deleted on 2026-09-15 after diverging from B — and a hand-copied demo would go the same way.
Every replace in it is guarded, so it fails loudly if the master changes shape rather than
emitting a half-transformed page.

What the demo changes, and nothing else: the topbar goes (breadcrumb, page title, internal
version tag) for a slim right-aligned strip holding the language switcher and an
**ⓘ Instructions** button; the « Codes » toggle stays in the DOM but hidden, so the reviewer
annotations have no way in and its wiring still finds the element; a seven-line instructions
panel is added in both languages; the page is retitled and carries `noindex`. It is served by
**GitHub Pages from `main` / `/docs`**.

The instructions are a **panel, not a modal** (2026-09-16, Lucas): they have to stay readable
while the form is being filled in, so the block expands *above section 1, inside the form
column* — it never covers a field and the rail does not move. It is a disclosure, so it traps
no focus, has no backdrop, and **Esc is deliberately left alone**: Esc belongs to the real
modals, and closing this while the HPO tree is open would be a surprise. The button carries the
open state (`.langsw button.on` plus `aria-expanded`).

The lines are **ordered the way the form is read**, top to bottom — §1's analysis menu, §1's
prenatal checkbox, §2's lookup, then §3 in its own internal order (the ask, the search, the
suggestions), then §5. « Instructions » is the same word in French and English, so `ui.tips`
and `tips.title` carry one string in both dictionaries.

Six of the seven lines fit one line; the **lookup line is deliberately longer** (three in FR)
because it names both halves of the key by their exact section 2 labels — « Identifiant » and
« Établissement du patient » — and says a record opens to confirm. The **suggestions line names
no analysis**: every analysis except RAPIDE and GENOR shows the same `SUGGESTIONS_DEFAULT` list,
so pointing at one would imply a specificity the mock does not have. (If a code is ever needed
there, it is **RGDI** — `RDGI` does not exist in the catalog.)

Run the suites against it — that is how the transform is proved behaviour-neutral:

```bash
TARGET=docs/index.html ./tests/run.sh
```

`README.md` is the demo-facing description (pros/cons, demo tips), rewritten on 2026-09-10 and
current as of this session.

## Current work — read this first

**Vincent is reviewing version B (`case-create-signs-inline.html`)** — the only wireframe left
to change.

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

Chrome is installed, but **not as `google-chrome` on macOS** — it is
`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` there, so declare it once
(`CHROME="…"`) and call `"$CHROME"`. Copy the file to the scratch directory, inject a `<script>`
before `</body>` that drives the DOM and dumps `PASS`/`FAIL` lines into a `<pre id="TESTOUT">`,
then:

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
is no separate checkbox; then the prescriber, alone on its line and **carrying no field label**
— just ☑ « Je suis médecin prescripteur ou responsable », with « Qui demande cette
analyse » + an input appearing only when it is unticked. See the decision below.
« Établissement prescripteur » (`ordering_organization_code`) was **removed on 2026-09-25**.

**2 · Patient (cas index)** — title becomes « Patient (cas index, mère) » in prenatal mode, where
Sexe is also prefilled Féminin: in a prenatal case **the proband is the fetus**, and this section
holds the *mother's* identity only because a fetus has no Patient record of its own. Everything
in it is hers; the fetus's own facts are the prenatal block at the end. Identifiant\* | Établissement du patient\*, then the lookup status
line spanning the row, then RAMQ | **DDN\* · Sexe\*** sharing one cell, then Prénom\* | Nom\*
(both **required since 2026-09-16**, and counted as one gate item between them).
The pair fits 368 px only because both halves shrink: the label to « DDN » / "DOB" (`lbl.dobShort`,
§2 only — `lbl.dob` still spells it out in §5 and the patient dialog), and Sexe to **initials with
the full word as tooltip**, the treatment §5's cards already use. Full Sexe labels need 393 px.
The rail translates `dataset.value` rather than copying the button text, so it reads « Féminin »
and not « F ». The
prenatal-only block — headed **« Informations fœtales »**, matching the rail's block — opens at
the **end of this section**, driven by the checkbox in section 1: Sexe (fœtus), then Âge
gestationnel as DDM / DPA / Fœtus décédé. **The date sits directly under the option that asks
for it**, 150 px wide and with no label of its own (the option is the label; the `lmp_date` /
`edd_date` annotations moved onto the options), and the **calculated age shows to its right**.

**3 · Signes cliniques** — the ask, then the search row (HPO search + « Parcourir l'arbre HPO »)
**directly under it**, then « Phénotypes observés (n) » and « Suggestions pour cette analyse »
below — **one column, 5 shown, « Afficher n de plus »** (both reworked 2026-09-10; the
suggestions were briefly two columns of 14). Every row in this section is the same checklist
row: checkbox, term, HP id, and — once ticked, and only for observed — an onset menu. A rule,
then the not-observed half, **also reworked on 2026-09-10**: « Phénotypes non
observés (n) », the picks as dismissable badges, and one button « ＋ Phénotypes NON OBSERVÉS »
(`#neg-add-btn`) that opens the HPO browser. It has no checkbox and no inline search — the modal
is the only way in, because this list is a short aside rather than the required list you work
through. Vertical rhythm inside the block: **12 px** under an instruction, **16 px** before a
sub-heading, **6 px** under one.

**4 · Autres informations cliniques (facultatives)** — Consanguinité | Ethnicité(s) (multi-valued,
chips); Indication principale (MONDO) typeahead + « Parcourir l'arbre MONDO »; Note clinique.
Family history **left this section on 2026-09-10** — section 5 owns it now.

**5 · Famille** — under the « Sections facultatives » divider. It was « Analyse familiale »
until 2026-09-16; the section holds both reported family history and the members included in the
analysis, and the old title named only the second half. « Famille » was chosen over the accurate
but long « Antécédents et analyse familiale » (by far the longest of the five titles, and
« familiale » attaching only to « analyse » invites a misparse as « antécédents familiaux ») —
the standing description already carries the ask, and the rail's own « Famille » row now matches. No opt-in checkbox: a
standing description carries the ask (« Rapportez des antécédents familiaux et incluez, le cas
échéant, … »), so the section is always open. Then the member cards and the
« ＋ Ajouter un membre de la famille » button **below** the list. The pedigree is not here —
it moved to the rail on 2026-09-10.

One card per relative, in two halves. The top line is the family-history record every relative
gets — Lien de parenté · Sexe · Statut · Préciser (free text) — with the relationship field kept
as narrow as its labels allow and **Statut shown as initials** (A · NA · I in French, A · NA · U
in English) so the free text takes the width that is left; each initial carries the full word as
its tooltip. Below it the checkbox « Inclure dans l'analyse génétique »: ticking it opens the
patient-identification block (Identifiant | Établissement du patient / RAMQ | Date de naissance /
Prénom | Nom — the proband's fields minus sex and life status), because a member in the analysis
becomes a Patient in Radiant.

**One exception, prenatal only** (2026-09-15): section 2 already holds the mother's identity, so
a « Mère » card ticked into the analysis does not re-ask for it. In place of the block it shows
one derived line, `.probandref` — « Dossier patient : **A-77** · CHU Sainte-Justine ·
Marie-Claude Gagnon » — built by `paintProbandRef()` from section 2 and repainted by every
`recompute()`. The six inputs stay **empty and hidden** behind it, so nothing stale reaches the
case and switching the card to another relative opens a blank block rather than handing her
identifiers to a sister. `mirroredFamRow()` decides: prenatal on **and** relation Mother **and**
in the analysis. Break any one and the ordinary block comes back.

**Rail** — Analyse (+ germline/somatic badge, + a family-composition badge once the case is
not solo) · Catégorie · Priorité · ID cas index ·
Établissement du patient · Sexe · Date de naissance · **Nom** · **Phénotypes**, then
« Ajouts facultatifs »: Indication principale · Consanguinité · Ethnicité(s) · Note clinique ·
Famille, then the **live pedigree** under the Famille row, which now **closes** the card.

**The two actions lead the card** (2026-09-16): Créer le cas · Enregistrer le brouillon · the
progress bar · `x sur 7 champs requis`, then 22px of air, then « Résumé du cas » and its rows.
They used to close it, under the pedigree — and with a pedigree drawn the rail is taller than a
laptop viewport, so Create sat below the fold until you scrolled (the caveat two paragraphs down
described exactly this). At the top they are always in view, and the bar reads as a caption on
the button it gates rather than as the tail of the summary list. The bar and count follow the
buttons rather than leading them because they exist to say *why* Create is unavailable.

« Nom » and « Phénotypes » both joined the required group on 2026-09-16 — see the decisions
below. « Nom » sits last among the identity rows, the way section 2 places the names last in
its own grid. « Phénotypes » sits after it but **above** the prenatal « Informations fœtales »
block, even though section 3 follows section 2 in the form: that block is a *captioned* group,
and a captioned group has to end at the next caption. Left below it, the proband's phenotype
count read as one more fetal fact.

In prenatal mode (2026-09-15) « ID cas index » renames itself to « ID mère » — the identifier is
hers — swapping between two i18n keys the way section 2's title does, so a language switch
repaints it by itself. **« Sexe » becomes « Sexe (mère) » / "Sex (mother)" the same way**
(2026-09-16, `rail.sex` ↔ `rail.sexMother`): that row is hers too, and prenatal prefills it
Féminin, so unqualified it read like the fetus's sex sitting one block above « Sexe fœtal ».
Both swaps go through the one `swapKey()` helper. « Date de naissance » and « Nom » are hers as
well and are **not** qualified — the whole block is her identity and three parentheses in a row
would be noise; the two that swap are the two that were actively misleading. A **« Informations fœtales »** block (`#rail-fetal`, same `.optlabel`
treatment) then carries Sexe fœtal and Âge gestationnel. It sits **above** « Ajouts facultatifs »
because both rows are required in a prenatal case (the gate goes 7 → 9), and disappears
entirely otherwise. The
gestational-age row carries what is stored **and** what is derived from it —
« DDM 2026-04-02 · 24 sem. », or « Fœtus décédé » alone.

The shell is **1200 px** wide and the rail **340 px** (both widened on 2026-09-10 to give the
pedigree somewhere to live). The rail is `position:sticky; top:24px`: with a pedigree drawn it
can still exceed a laptop viewport, so its **bottom** — now the pedigree — sits below the fold
until you scroll. That resolves on scroll, since sticky releases once the page runs out of room;
it is not clipped. **This stopped mattering for the controls on 2026-09-16**, when Create and the
progress bar moved to the head of the card: what falls below the fold is now a picture, not the
button you came for.

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
- **A placeholder names the thing it wants — unless the control is too narrow to show it**
  (2026-09-10, narrowed 2026-09-16): « Sélectionner une étude… », « …un établissement… »,
  « …des ethnicités… » rather than a bare « Sélectionner… », each on its own `ph.sel*` key.
  **`ph.selRelation` is the one exception**: section 5 keeps the relationship field *as narrow
  as its labels allow* so the free-text « Préciser » takes the width that is left, and
  « Sélectionner un lien de parenté… » does not fit that width — it is now
  « Sélectionner… » / "Select…". This is a width problem, not a change of mind, so the other
  five were left alone; a placeholder you cannot read names nothing. The key stays
  `ph.selRelation` rather than collapsing into `ph.select`: one key per control is what lets
  this one change without moving the others, and it keeps `ph.select` a genuine fallback.
  `ph.select` still survives only as the fallback `clearCtrl()` / `renderChips()` /
  `syncFamilyOrg()` reach for when a control declares none — no control in the form does.
  `localize()` copies a div-select's `data-i18n-ph` into `dataset.ph`, which is what makes
  clearing one restore *its* placeholder and not the generic one. Free-text placeholders say
  what to type too: the prescriber's input asks for « Nom du médecin » (« Qui demande cette
  analyse » is its *label* since 2026-09-25, so the placeholder says what to type rather than
  repeating the question). The name fields
  read « Prénom » / « Nom » — they said « Prénom (facultatif) » / « Nom (facultatif) » until
  **2026-09-16, when the names became required** and the parenthetical said the opposite of the
  truth. A bare echo of the label is all that is left to say: unlike the identifier or the
  health number, a name has no format or example to offer. (`ph.optional` and `ph.freetext`
  were retired in 2026-09-10.)
- **« Inconnu » is an answer, so the rail inks it** (2026-09-10). A rail value goes dark
  (`.v.done`) as soon as the user has answered, Unknown included — Consanguinité « Inconnue »
  and Sexe « Inconnu » read like any other filled value. Only the em-dash placeholder stays
  muted. Catégorie and Priorité are inked unconditionally by `#sum-cat, #sum-pri`, since they
  ship with defaults and a muted default made the rail look unanswered.
- **The indication field is a typeahead, not a select**: an `input[data-sel=condition]` whose
  canonical value stays in `dataset.value` while `.value` shows the translated label — `setSel()`
  and `clearCtrl()` branch on `tagName === 'INPUT'`. Free text is never a value: on blur the label
  of the actual selection comes back.
- **Ethnicity is the one multi-valued control**: `bindMultiSelect()` stores the picks
  pipe-separated in `dataset.values` and paints them as removable chips inside the control.
- **Two ways a phenotype is drawn.** `makePRow(id, mode, q)` is the one checklist row used
  everywhere an observed term appears — suggestions, search results and the picked list alike.
  Selection is the row's own **active/inactive state** (`label.check.on`, the accent-filled
  box), so a term is dropped by unticking it; there is no ✓/✗ marker and no row ✕ to learn.
  `makeNegBadge(id)` draws a picked not-observed term as a pill with a ✕. `makeSelRow` was
  deleted on 2026-09-10 — it was the ✓-marker row, and nothing needed a second vocabulary.
  A picked term never appears in two places: it leaves the suggestions for the picked list.
- **Suggestions are one column with a 5-item cut** (2026-09-10). Two columns forced the eye to
  pick a scan direction before it could read, and five rows plus « Afficher n de plus » is a
  shorter first impression. `#suggestions` no longer sets `columns`, so the old
  read-top-to-bottom rule and its 860px single-column media query are both gone.
- **The two ways in stay pinned under the ask** — type-ahead and « Parcourir l'arbre HPO » sit
  immediately below the instruction, above the picked list, so they don't move as terms
  accumulate.
- **Not-observed badges are deliberately not struck through** (2026-09-10). The block heading
  already says these signs were looked for and absent; struck-through text reads as "removed
  from the list" instead. The earlier strikethrough chips were dropped for the same reason.
- **Only the observed list has an inline search.** `searchIds()` and `renderSearchResults()`
  take no mode — they are observed-only since 2026-09-10. `makePRow`'s negative branch survives
  but nothing reaches it any more.
- **Blocks that open behind a checkbox clear themselves when closed** — prenatal fields and the
  family member's identification block. Nothing hidden should end up in the case. The
  not-observed list no longer works this way: it has no checkbox, so its badges are dropped one
  at a time and never wholesale.
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
- **The identifier leads section 2**, labelled simply « Identifiant » since 2026-09-10 — the
  examples moved into its placeholder, « MRN, code de l'étude, etc… », where they stop competing
  with the label; the id-type dropdown (MRN / Other) is gone, proband and family row alike. The
  existing-patient lookup therefore keys on **organization + identifier**: it fires whenever that
  pair is complete, whichever half moved last, and re-fires when either changes. Mocked in
  `PATIENT_DB`, one record behind a 700 ms delay — **1234** at Sainte-Justine; anything else
  reports "nouveau patient" and takes back only what the lookup itself wrote. While the pair is
  incomplete the line says **nothing** — the two nags (« Choisir l'établissement… » and
  « champs préremplis, à vérifier ») were dropped on 2026-09-10.
- **A found patient is confirmed before any PHI is written** (2026-09-10). The lookup no longer
  fills the form on its own: a match opens `#patient-modal` showing the record in full — names,
  sex, date of birth, RAMQ — and only « Utiliser ce patient » writes it. Full PHI, deliberately:
  this dialog exists so a human can tell two siblings apart, and it is shown before anything
  reaches the case, so a mistyped identifier fills nothing.
- **Rejecting a match means the key is wrong, not "ignore that record".** Organization +
  identifier is unique, so there is no coherent way to keep the identifier and enter a different
  person — hence deliberately **no "use it anyway"** third button. « Ce n'est pas le bon
  patient » (also ✕, Esc and a backdrop click, all of which write nothing) marks the identifier
  in error, warns on the lookup line, returns focus to the field and **blocks Create** while
  leaving Save draft alone. What the user typed is never erased: they may have one digit wrong
  and need to see it. `lookupDecision` records one answer per key, so a key you already answered
  for is never asked again — and a rejected key keeps its warning rather than re-opening the
  modal in a loop.
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
- **In a prenatal case the fetus is the proband, and the mother is the patient of record**
  (2026-09-15, Lucas). A fetus has no Patient record, so section 2 carries her identity. Such a
  case is **solo by default** — section 5 does nothing until the user adds someone — and the
  mother is then an ordinary relative of the fetus, added and removed like any other. What the
  kickoff called "« Mère » is the proband" was wrong, and reversing it is what fixed the
  pedigree; don't re-derive it from the old wording.
- **The mother's identification is stated, not re-asked** (2026-09-15). This is derive-and-hide
  applied to section 5: a read-only copy of section 2 was built first and cut, because six inert
  fields cost 240 px — 40% of section 5 — to say nothing new, and fields that look editable but
  are not invite clicks that do nothing. The one line replaced it at 43 px. « Inclure dans
  l'analyse génétique » stays on her card either way: solo vs trio is a real clinical decision
  and is not derivable.
- **Leaving « Mère » clears the block, a relationship correction does not.** `famApplyRelation()`
  empties a bound card on the way out, because those values are section 2's and the user never
  typed them there — keeping them would hand the mother's identifiers to a sister. On an ordinary
  card the same edit keeps what was typed: that is the user's own input, and a relationship fix
  is usually a correction to the *relationship*, not the person.
- **The pedigree's proband node reads the fetal sex in prenatal mode**, not section 2's Sexe,
  which prenatal prefills Féminin. Both segments use the same `M|F|U` codes. Before this it drew
  the mother twice — once as « Cas index », once as « Mère ».
- **Gestational age is stored as a date and derived as an age** (2026-09-15). `gestState()` reads
  the basis + date; `Math.round(days/7)` from a DDM, `Math.round((280 − daysUntil)/7)` from a DPA,
  UTC midnights so a DST boundary cannot shift a day. **These are CLIN's formulas** — see
  `clin-portal-ui`, `src/utils/age.ts`, whose `HybridPatientFoetus` holds `gestational_method`
  (DDM | DPA | DECEASED) + `gestational_date` and derives the weeks in the view. An age is only
  true on the day it is computed, so the date is the value and the age is always a view.
  `prenatalReqs()` reads the same `gestState()`, so the gate and the display cannot drift.
- **The date bounds are asymmetric, deliberately.** DDM is capped at **today** — a last menstrual
  period is in the past, full stop — with no floor. DPA is capped at **today + 280 days**, past
  which the implied age is negative, and has **no floor**: an overdue pregnancy has a due date
  behind it. A typed out-of-range date shows no age, leaves the rail row muted, fails the gate
  and marks the field (`err.gestPast` / `err.gestSoon`) rather than blocking Create in silence.
- **Statut vital left the form** (2026-09-16, team decision). At case creation the value would
  always be Alive — a case is not opened on a patient nobody intends to sequence — so the field
  asked a question with one answer. **Radiant is making `life_status_code` nullable** to match;
  until that ships, the column is `NOT NULL` on `public.patient`, so something has to supply it
  server-side. It is a **patient-level** value, shared by every case that patient appears in —
  only `family` holds per-case values (relationship, affected status) — which is part of why the
  form is the wrong place to set it. A fetal demise is unaffected: it lives in « Âge
  gestationnel » as « Fœtus décédé », which describes the pregnancy, not a person.
- **The pedigree slashes the proband on a fetal demise** (2026-09-16). The flag used to read
  section 2's Statut vital; « Fœtus décédé » is now the only death the form records, and it is
  the *proband's* death whatever field it is filed under — standard notation slashes a
  stillbirth. **Prenatal only**: a postnatal case records no death at all, and a relative never
  could (a family card carries relation · sex · affected status, never a life status).
  The slash is drawn **white on a filled symbol** — the proband is hardcoded `aff:'Affected'`,
  so a `#1f2328` slash on a `#1f2328` fill was invisible. Position assertions found it and
  passed; only the screenshot showed it was not there. Colour needs the screenshot.
- **First and last name are required, and count as ONE gate item** (2026-09-16). The base gate
  went **5 → 7**: the five it was (analysis, identifier, patient organization, sex, date of
  birth) plus the name row plus clinical signs; **9 in a prenatal case**, with fetal sex and
  gestational age. One item and not two because the rail's count *is* its rows — `recompute()`
  builds `rows[]` as `[rail row id, satisfied]` pairs and the gate is how many of those are
  inked — and the two names share one rail row. Both halves are needed to tick it: a first name
  on its own is a half-answer and the row stays muted while showing what there is.
  `validateConditionals()` checks the two **separately** on a section 5 card ticked into the
  analysis, because that function marks fields rather than counting rows, and a field is either
  filled or it is not. The placeholders were rewritten in the same change — see the placeholder
  convention above.
  - The mirrored « Mère » card is still skipped there: her identity is section 2's, which the
    core gate already requires.
  - §5's « Dossier patient » line **keeps** its no-name fallback. It looks unreachable now that
    the names are required, but the line repaints on every `recompute()` — i.e. on every
    keystroke — so it is read long before the names are typed. Only *Create* is gated.

- **Clinical signs joined the required gate** (2026-09-16). Section 3's instruction has carried a
  required `*` since it was written, while the rail filed « Phénotypes » under « Ajouts
  facultatifs » — the two said opposite things and the rail was the one that was wrong. The row
  moved into the required group and into `rows[]`, satisfied by **at least one OBSERVED
  phenotype**: a not-observed term is an aside, and section 3 asks for an observed one. The row's
  **text still counts every term**, observed and not-observed together, so the count answers
  "what does this case record" while the ink answers "is the requirement met". `sumPheno()`
  therefore sets the text only and `recompute()` owns the ink, so the two cannot drift; the three
  call sites that used to call `sumPheno()` on a phenotype change now call `recompute()`.

- **Consanguinity is the one segment you can clear** (2026-09-16). Clicking the selected option
  again unsets it, and the rail falls back to its muted em-dash. Deliberately special-cased on
  `data-seg="consang"` rather than made general: every other `.seg` in the form is required —
  Sexe, and section 5's own sex and affected-status segments — so a general toggle would let a
  stray second click un-answer a required field. Consanguinity is optional, and « Inconnu » is a
  claim (nobody knows) rather than the absence of one, so "no answer" needed a way back.

- **Create and Save draft lead the rail card** (2026-09-16, Lucas). They used to close it, below
  the pedigree; a drawn pedigree makes the rail taller than a laptop viewport, so the primary
  action sat below the fold. The whole action block moved together — buttons, progress bar,
  count — because the bar and the count explain the button and are useless apart from it.
  22px then separates the block from « Résumé du cas », the same value `.notes-legend` uses for
  its own break. This also retires the "Create sits below the fold" caveat, which was a parked
  item rather than a fixed one.
  - **The standing hint under the buttons became the Save-draft footnote** (numbered 9 then,
    **8 since 2026-09-25**, when the ordering-site note was removed and the rest shifted down).
    « Enregistrez un brouillon à tout
    moment… » explained a *feature*; the reviewer annotations are where this file explains
    features, and the rail is where it reports *state*. The `rail.note.hint` keys were retired
    and `note.8` carries the copy, anchored by a `<sup class="fn">8</sup>` on Save draft itself —
    every other note has an anchor, and the button is the thing it describes. The marker is
    wrapped in a `<span>` with the label: `.cta` is `display:grid`, so a bare `<sup>` sibling
    becomes a second row instead of a superscript, and `localize()` would overwrite it if it
    shared the element carrying `data-i18n`.
  - **`flashNote()` now writes to `#railflash`**, a line that is **empty at rest** and collapsed
    by `.railflash:empty{display:none}`, so it costs no height and the summary starts directly
    under the count. A flash pushes the summary down for its 2.4 s and lets it back up — a
    deliberate trade for keeping the feedback under the button that raised it, rather than
    reserving dead space for a message that is usually absent. A language switch clears a live
    flash instead of leaving a message stranded in the old language.

- **The Analyse row carries a second badge for family composition** (2026-09-16, Lucas):
  « Duo » · « Trio » · « Quatuor » / "Quad", and past four the count itself
  (« 5 séquencés » / "5 sequenced"). It counts the **proband plus every card ticked into the
  analysis** — a reported-only relative does not count, because a trio means three people
  sequenced, not three relatives mentioned. That is the same split the rest of section 5 draws,
  and deliberately the **opposite** of the pedigree's, which draws the family rather than the
  batch; the Famille row counts cards, this badge counts the batch, and the two disagreeing is
  correct.
  - **Solo shows nothing.** It is the default and the common case, so a badge would put a word
    on nearly every case to say nothing. This was the ask, and it is also why the ladder has no
    « Solo » key.
  - **The named ladder stops at four.** Duo, trio and quad are the terms clinicians use; nobody
    says "sextet", so five and up fall back to `comp.many`. « Quatuor » is proper French but
    **worth checking with Vincent** — lab usage may well be "quad" in both languages, and it is
    a one-key change. Duo and Trio are identical in the two languages, so `comp.4` and
    `comp.many` are the only keys that actually differ.
  - **It uses the plain `.badge`**, the neutral variant, so the only colour in the row stays on
    the case type — that is a derived clinical fact, while composition is a count.
  - **It shows even with no analysis picked**, beside the em-dash: the composition is true
    whether or not the analysis field has been answered, and the row stays muted regardless.
  - Ticking a card, adding one and removing one all call `recompute()` now. They used to call
    some mixture of `syncProbandLink()`, `sumFamily()` and `renderPedigree()`, none of which
    repaints the Analyse row.

- **The prescriber is one checkbox with no field label, and the ordering site is gone**
  (2026-09-25, Lucas). In its default state the prescriber has **no label and no input** — just
  ☑ **« Je suis médecin prescripteur ou responsable »** / "I am the ordering or responsible
  physician", ticked. Unticking reveals a label **« Qui demande cette analyse »** / "Who is
  requesting this analysis" **and** its input, together. Derive-and-hide applied to free text:
  the person filling the form is usually the prescriber, so the common answer is the default and
  the field costs no height at all until it is wrong. A field label in the default state would
  have labelled nothing — the checkbox is the whole statement — which is why it was dropped
  rather than kept above the box.
  - **Both states feed the one `ordering_physician` field.** Ticked, the system is meant to
    capture **the current user** as the ordering physician; unticked, the **typed name**. One
    field, two sources — which is why the `(ordering_physician)` annotation **moved onto the
    checkbox line**, the way `(category_code)` rides the prenatal one: the checkbox is the
    field's primary control now and the input is only the fallback path. (That is also the
    standing rule — a dropped label takes its annotations with it rather than losing them.)
  - **This derives from the session, not from the page**, which is new. Every other
    derive-and-hide value in this form is worked out from something else the user entered; this
    one assumes the form knows who is filling it in and can resolve them. See open question 12.
  - Re-ticking **clears** what was typed — the same "nothing hidden reaches the case" rule as
    the prenatal block and the family identification block. Unticking focuses the input, since
    it only appeared because the user asked for it. **Not in the gate**: the field was optional
    before and still is.
  - **`.physwho[hidden]{display:none}` is not optional.** `hidden` only sets `display:none` as a
    *default*, and any display of our own beats it — the first version set `display:flex` on the
    revealed block and it was never actually hidden. A measured assertion caught it; nothing
    that only looked at the markup would have.
  - **« Établissement prescripteur » (`ordering_organization_code`) was removed outright** — the
    markup, `OPTIONS.ordering`, `state.orderingSet`, both `lbl.ordering` and `ph.selOrdering`
    keys, and its footnote. `ORGS` stays: « Établissement du patient » still uses it.
  - **The legend lost a note, so everything after it shifted.** The reviewer notes are an `<ol>`,
    which renumbers itself, but the `<sup class="fn">N</sup>` anchors are literal — so removing
    the ordering-site note meant renumbering the anchors *and* the keys. There are now
    **eight** notes.
  - **They are numbered in reading order**, down the form column and then the rail: §1 (1, 2, 3),
    §2 (4, 5), §3 (6), §5 (7 on the section title, and 5 again on the card), rail (8). Study and
    patient organization were the wrong way round — 4 in §1 above 3 in §2 — and were swapped on
    2026-09-25. Checking this needs the rendered page, not the markup: the rail's block sits
    *before* the family-row template in the file but *after* §5 on screen.
  - **Note 7 hangs off §5's title, not off a field.** It used to sit on the family card's
    « Établissement du patient », which was ambiguous — §2's field of the same name carries
    note 4 — and buried, since that block only opens once a member is ticked into the analysis.
    The note describes the whole section, so the title is its place, and every anchor is now in
    the DOM from the start. The title's text is wrapped in a `<span>` so `localize()` cannot
    wipe the marker (it assigns `textContent` to the `[data-i18n]` element), and so the `<sup>`
    is not flung to the right margin by the `h2`'s `flex:1`. Same trick as the Save-draft
    footnote. The card keeps its own health-number anchor.
  - Note 4 lost the clause « C'est ce champ, **et non l'établissement prescripteur**, qui
    contrôle… » with that field. The PHI-visibility rationale stayed: it is still true, and it
    is still the answer to "why is this one not derived like the others?". Note 7 then lost its
    own « (il pilote le masquage des RPI par patient) » on 2026-09-25 — the same point, made
    twice, and note 4 is where it belongs.

- **User text is never concatenated into `innerHTML`.** There is no escaping helper in this file;
  mixed content is built from `createTextNode` / `createElement` (`markMatch`, `renderChips`,
  `paintProbandRef`). An identifier is free text, so this matters.

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
7. Whether the search should also apply to **« Établissement du patient »** — plugging in the
   real Quebec establishment list would trip the 8-entry threshold on its own. **On hold** as of
   2026-09-15. It used to cover the prescriber's establishment too; that field was removed on
   2026-09-25, so only the patient's is left.
8. **Radiant has no prenatal fields at all.** Checked on 2026-09-15 against
   `radiant-network/radiant-portal`: across all 20 migrations, `public.cases`, `public.patient`
   and the `CaseBatch` API, the only prenatal thing in the model is
   `category_code ∈ {prenatal, postnatal}`. There is **no** gestational age, LMP/EDD date or
   fetal sex. So this form's `(gestational_age)`, `(lmp_date)`, `(edd_date)` and
   `(fetal_sex_code)` annotations are **proposals, not references**. CLIN already ships the
   shape (`gestational_method` + `gestational_date`, weeks derived in the view) — should Radiant
   adopt it? Note CLIN also has `NEW_BORN` alongside `PRENATAL`, which Radiant's `category_code`
   does not.
9. **Section 5's relation list is wider than Radiant accepts.** The API constrains
   `relation_to_proband_code` to `mother father brother sister sibling proband`; this form offers
   Mother · Father · Sister · Brother · **Daughter · Son · Half-sibling · Other**. The last four
   would be rejected, and the form offers neither `sibling` nor `proband`. Widening the list was
   a deliberate call for family history (2026-09-10) — the gap is real either way.
10. **`submitter_patient_id_type` is `NOT NULL` in `public.patient`**, and this form dropped the
    id-type dropdown on 2026-09-10. The batch API does not carry it, so something defaults it
    server-side. Confirm what, rather than assume.
11. **A prenatal case may submit the mother twice.** The proband patient row carries her
    identifiers (the fetus has none), so adding « Mère » in section 5 sends the same
    organization + identifier again under `relation_to_proband_code: mother`, against
    `UNIQUE (organization_code, submitter_patient_id)`. The schema has clearly thought about
    fetuses — the `jhn` index comments "newborns/fetuses have none yet" — so this is worth
    asking the Radiant team.
12. **What does `ordering_physician` hold, and can it be derived from the session?** Since
    2026-09-25 the prescriber is a checkbox whose ticked state is meant to capture the current
    user (see the decision above). That rests on two unconfirmed things: that the form knows who
    the user is and can resolve them, and what the field actually stores. **If it is free text**,
    both paths yield a name and the control we have is right. **If it is a reference to a
    practitioner record**, the ticked path has an id available but the typed path does not, and a
    free-text input is the wrong control for it — the two paths would produce different kinds of
    value for the same field.
    **A starting point for that discussion, not a decision** (Lucas, 2026-09-25): make the
    unticked path a **typeahead over the member/practitioner directory** — a hit records that
    **id**, a miss falls back to the **typed name as free text**. The two paths then agree
    whenever the directory knows the person, and degrade gracefully when it does not. Nothing
    of this is built; the form still has a plain text input.
