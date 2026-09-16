#!/usr/bin/env python3
"""Build the user-facing demo (docs/index.html) from the master wireframe.

    python3 make-demo.py

The demo is GENERATED, never hand-edited. This repo already lost a wireframe to
drift — version A was deleted on 2026-09-15 after diverging from version B — and
a hand-copied demo would go the same way. Edit `case-create-signs-inline.html`,
re-run this, commit both.

What it changes, and nothing else:
  1. retitles the page and adds noindex;
  2. drops the topbar (breadcrumb, title, internal version tag) for a slim strip
     holding only the language switcher and the tips toggle;
  3. keeps the « Codes » toggle in the DOM but hidden — the reviewer annotations
     are internal, and its wiring expects the element to exist;
  4. adds the tips panel above the form, its keys in both languages, and the JS
     that toggles it.

Every replace is guarded: if the master's shape changes, this fails loudly
rather than emitting a half-transformed demo.
"""
import io
import os
import sys

SRC = 'case-create-signs-inline.html'
OUT = os.path.join('docs', 'index.html')

s = io.open(SRC, encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    if s.count(a) != n:
        sys.exit('make-demo: expected %d match(es) for %r, found %d.\n'
                 'The master has changed shape — update make-demo.py.'
                 % (n, a[:70], s.count(a)))
    s = s.replace(a, b)


# ------------------------------------------------------- 1 · title + noindex
# The page is published on the open web so a link can be shared, but it mimics a
# real clinical product for a named hospital. noindex keeps it out of search
# results without affecting the link at all. Drop this line to let it be indexed.
rep('<title>Create case — Version B (inline signs)</title>',
    '<meta name="robots" content="noindex, nofollow">\n'
    '<title>Radiant — Créer un cas (maquette)</title>')

# --------------------------------------------------- 2 · topbar -> slim strip
rep("""  <div class="topbar">
    <div>
      <div class="crumb"><b>Radiant</b> › <b data-i18n="crumb.new">Create case</b></div>
      <h1 data-i18n="app.title">Create case</h1>
    </div>
    <div style="display:flex;align-items:center;gap:12px">
      <span class="tag" data-i18n="app.tag">Version B · signs inline · browser in modal</span>
      <div class="langsw" role="group" aria-label="Documentation annotations"><button type="button" id="docs-toggle" data-i18n="ui.docsToggle">Field codes</button></div>
      <div class="langsw" id="langsw" role="group" aria-label="Language">
        <button type="button" data-lang="fr">FR</button><button type="button" data-lang="en">EN</button>
      </div>
    </div>
  </div>""",
    """  <!-- DEMO BUILD. The topbar is gone: breadcrumb, page title and the internal version
       tag are all team-facing. What is left is what a visitor needs — the language and a
       way into the tips. Right-aligned so the form still starts at the top-left. -->
  <div class="demobar">
    <div class="langsw"><button type="button" id="tips-btn" aria-expanded="false" aria-controls="tips-panel" data-i18n="ui.tips">ⓘ Instructions</button></div>
    <div class="langsw" id="langsw" role="group" aria-label="Language">
      <button type="button" data-lang="fr">FR</button><button type="button" data-lang="en">EN</button>
    </div>
    <!-- the reviewer annotations are internal, so the demo offers no way to turn them on.
         The button stays in the DOM, hidden: its wiring looks the element up by id, and
         `hide` defaults to true, so the annotations simply never show. -->
    <div hidden><button type="button" id="docs-toggle" data-i18n="ui.docsToggle">Field codes</button></div>
  </div>""")

# ------------------------------------------------------------------ 3 · CSS
rep("""  .topbar h1{font-size:16px;margin:2px 0 0}""",
    """  .topbar h1{font-size:16px;margin:2px 0 0}
  /* demo build: the topbar's replacement — controls only, no card around them */
  .demobar{display:flex;justify-content:flex-end;align-items:center;gap:10px;margin-bottom:16px}
  /* demo build: the tips panel. It sits ABOVE the form and inside the form column, so it
     stays readable while the form is used — it is a disclosure, not a dialog, and it never
     covers a field. The accent rule on the left marks it as an aside: without it, a white
     card above section 1 reads as a sixth section of the form. */
  .tipspanel{background:#fff;border:1px solid var(--line);border-left:3px solid var(--accent);
        border-radius:var(--radius);padding:12px 16px 14px;margin-bottom:20px}
  .tipspanel[hidden]{display:none}
  .tipshead{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:9px}
  .tipshead .tipscap{font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--faint)}
  /* one line per tip — these are busy people */
  .tips{margin:0;padding:0 0 0 18px;font-size:12.5px;line-height:1.6;color:var(--mut)}
  .tips li{margin-bottom:7px}
  .tips li:last-child{margin-bottom:0}
  .tips b{color:var(--ink)}""")

# --------------------------------------------------- 4 · the panel, above §1
# Ordered the way the form is: section 1's fields, then 2, then 3 top to bottom
# (the ask, the search, the suggestions), then 5. A reader working down the form
# meets each tip at the point they need it.
TIPS_PANEL = """      <!-- demo build: tips, as an expandable panel rather than a modal — they have to stay
           visible while the form is filled in. Ordered to match the form, top to bottom:
           section 1, then 2, then 3's own internal order, then 5. -->
      <div id="tips-panel" class="tipspanel" hidden>
        <div class="tipshead">
          <span class="tipscap" data-i18n="tips.title">Instructions</span>
          <span class="mclose" id="tips-x" data-i18n-title="tips.close" title="Close">✕</span>
        </div>
        <ul class="tips">
          <li data-i18n-html="tips.1"></li>
          <li data-i18n-html="tips.2"></li>
          <li data-i18n-html="tips.3"></li>
          <li data-i18n-html="tips.4"></li>
          <li data-i18n-html="tips.5"></li>
          <li data-i18n-html="tips.6"></li>
          <li data-i18n-html="tips.7"></li>
        </ul>
      </div>

"""
rep("""    <!-- LEFT: the form -->
    <div>

      <!-- 1. Order & analysis (required) -->""",
    """    <!-- LEFT: the form -->
    <div>

""" + TIPS_PANEL + """      <!-- 1. Order & analysis (required) -->""")

# ------------------------------------------------------------------ 5 · i18n
rep("""      'ui.docsToggle':'Field codes',""",
    """      'ui.docsToggle':'Field codes', 'ui.tips':'ⓘ Instructions',
      'tips.title':'Instructions', 'tips.close':'Close',
      'tips.1':'<b>Analysis menu:</b> filter by name, code, or analysis number.',
      'tips.2':'<b>Prenatal case:</b> tick it in section 1 — the identifier in section 2 becomes the mother’s.',
      'tips.3':'<b>Patient lookup:</b> in section 2, type <b>1234</b> in “Identifier” and pick <b>CHU Sainte-Justine</b> in “Patient organization”. The search runs once both are set and opens a record to confirm; any other identifier gives “new patient”.',
      'tips.4':'<b>Clinical signs:</b> at least one observed phenotype is required.',
      'tips.5':'<b>HPO search follows the language</b> — an English term finds nothing in French.',
      'tips.6':'<b>Suggested phenotypes:</b> most analyses offer a list — in this mock it is the same list whichever one you pick.',
      'tips.7':'<b>Family:</b> add a member for family history and/or for the analysis — a pedigree is drawn in both cases.',""")

rep("""      'ui.docsToggle':'Codes',""",
    """      'ui.docsToggle':'Codes', 'ui.tips':'ⓘ Instructions',
      'tips.title':'Instructions', 'tips.close':'Fermer',
      'tips.1':'<b>Menu Analyse :</b> filtrez par nom, code, ou numéro d’analyse.',
      'tips.2':'<b>Cas prénatal :</b> cochez-le à la section 1 — l’identifiant de la section 2 devient celui de la mère.',
      'tips.3':'<b>Recherche de patient :</b> à la section 2, saisissez <b>1234</b> dans « Identifiant » et choisissez <b>CHU Sainte-Justine</b> dans « Établissement du patient ». La recherche part une fois les deux remplis et ouvre une fiche à confirmer ; tout autre identifiant donne « nouveau patient ».',
      'tips.4':'<b>Signes cliniques :</b> au moins un phénotype observé est requis.',
      'tips.5':'<b>La recherche HPO suit la langue</b> — un terme anglais ne donne rien en français.',
      'tips.6':'<b>Phénotypes suggérés :</b> la plupart des analyses en proposent une liste — dans cette maquette, c’est la même quelle que soit l’analyse choisie.',
      'tips.7':'<b>Famille :</b> ajoutez un membre pour les antécédents familiaux et/ou pour l’analyse — dans les deux cas, un pedigree est tracé.',""")

# -------------------------------------------------------------------- 6 · JS
rep("""  /* ---------- init ---------- */""",
    """  /* demo build: the tips panel is a disclosure, not a dialog — it does not trap focus, has
     no backdrop, and Esc is left alone (Esc belongs to the real modals, and closing this
     panel with it would be a surprise while the HPO tree is open). The button carries the
     open state, so it reads as pressed while the panel shows. */
  (function(){
    var p = document.getElementById('tips-panel'), b = document.getElementById('tips-btn');
    function set(open){
      p.toggleAttribute('hidden', !open);
      b.classList.toggle('on', open);
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    b.addEventListener('click', function(){ set(p.hasAttribute('hidden')); });
    document.getElementById('tips-x').addEventListener('click', function(){ set(false); });
  })();

  /* ---------- init ---------- */""")

if not os.path.isdir('docs'):
    os.mkdir('docs')
io.open(OUT, 'w', encoding='utf-8').write(s)
print('make-demo: wrote %s (%.1f KB)' % (OUT, len(s.encode('utf-8')) / 1024.0))
