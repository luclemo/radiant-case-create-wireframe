#!/usr/bin/env python3
"""Build the user-facing demo (docs/index.html) from the master wireframe.

    python3 make-demo.py

The demo is GENERATED, never hand-edited. This repo already lost a wireframe to
drift — version A was deleted on 2026-09-15 after diverging from version B — and
a hand-copied demo would go the same way. Edit `case-create-signs-inline.html`,
re-run this, commit both.

What it changes, and nothing else:
  1. drops the topbar (breadcrumb, title, internal version tag) for a slim strip
     holding only the language switcher and an ⓘ Tips button;
  2. keeps the « Field codes » toggle in the DOM but hidden — the reviewer
     annotations are internal, and its wiring expects the element to exist;
  3. adds the tips sheet, its keys in both languages, and the JS that opens it;
  4. retitles the page for people who are not on the team.

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

# ------------------------------------------------- 2 · topbar -> slim strip
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
       way in. Right-aligned so the form still starts at the top-left of the page. -->
  <div class="demobar">
    <div class="langsw"><button type="button" id="tips-btn" data-i18n="ui.tips">ⓘ Tips</button></div>
    <div class="langsw" id="langsw" role="group" aria-label="Language">
      <button type="button" data-lang="fr">FR</button><button type="button" data-lang="en">EN</button>
    </div>
    <!-- the reviewer annotations are internal, so the demo offers no way to turn them on.
         The button stays in the DOM, hidden: its wiring looks the element up by id, and
         `hide` defaults to true, so the annotations simply never show. -->
    <div hidden><button type="button" id="docs-toggle" data-i18n="ui.docsToggle">Field codes</button></div>
  </div>""")

rep("""  .topbar h1{font-size:16px;margin:2px 0 0}""",
    """  .topbar h1{font-size:16px;margin:2px 0 0}
  /* demo build: the topbar's replacement — controls only, no card around them */
  .demobar{display:flex;justify-content:flex-end;align-items:center;gap:10px;margin-bottom:16px}""")

# ------------------------------------------------------------ 3 · tips sheet
rep("""  .modal .instr{font-size:12px;color:var(--mut);margin:0 0 12px}""",
    """  /* demo build: the ⓘ sheet. One line per tip — these are busy people. */
  .tipsmodal{max-width:560px}
  .tips{margin:0;padding:0 0 0 18px;font-size:12.5px;line-height:1.6;color:var(--mut)}
  .tips li{margin-bottom:10px}
  .tips li:last-child{margin-bottom:0}
  .tips b{color:var(--ink)}
  .modal .instr{font-size:12px;color:var(--mut);margin:0 0 12px}""")

TIPS_MARKUP = """  <!-- demo build: « à savoir » sheet, opened from the ⓘ button in the top strip -->
  <div id="tips-modal" class="modal-overlay" hidden>
    <div class="modal tipsmodal" role="dialog" aria-modal="true" aria-labelledby="tips-title">
      <header>
        <h2 id="tips-title" data-i18n="tips.title">Good to know</h2>
        <span class="mclose" id="tips-x" data-i18n-title="tips.close" title="Close">✕</span>
      </header>
      <div class="mbody">
        <ul class="tips">
          <li data-i18n-html="tips.1"></li>
          <li data-i18n-html="tips.2"></li>
          <li data-i18n-html="tips.3"></li>
          <li data-i18n-html="tips.4"></li>
          <li data-i18n-html="tips.5"></li>
          <li data-i18n-html="tips.6"></li>
          <li data-i18n-html="tips.7"></li>
          <li data-i18n-html="tips.8"></li>
        </ul>
      </div>
      <div class="mfoot">
        <div class="cta ghost" id="tips-close" data-i18n="tips.close">Close</div>
      </div>
    </div>
  </div>

"""
rep("""  <div id="mondo-modal" class="modal-overlay tree-layer" hidden>""",
    TIPS_MARKUP + """  <div id="mondo-modal" class="modal-overlay tree-layer" hidden>""")

# ------------------------------------------------------------------ 4 · i18n
rep("""      'ui.docsToggle':'Field codes',""",
    """      'ui.docsToggle':'Field codes', 'ui.tips':'ⓘ Tips',
      'tips.title':'Good to know', 'tips.close':'Close',
      'tips.1':'<b>Nothing is saved.</b> “Create case” just shows a message.',
      'tips.2':'<b>Patient lookup:</b> <b>1234</b> + CHU Sainte-Justine, the only record in the mock.',
      'tips.3':'<b>Prenatal case:</b> tick it in section 1 — section 2 then describes the mother.',
      'tips.4':'<b>Clinical signs:</b> at least one observed phenotype is required.',
      'tips.5':'<b>Family:</b> tick a member into the analysis — the pedigree and badge follow.',
      'tips.6':'<b>Analysis menu:</b> filter by word or act number, matched anywhere in the name.',
      'tips.7':'<b>HPO search follows the language</b> — an English term finds nothing in French.',
      'tips.8':'<b>FR / EN</b> switches the interface and keeps what you have entered.',""")

rep("""      'ui.docsToggle':'Codes',""",
    """      'ui.docsToggle':'Codes', 'ui.tips':'ⓘ Astuces',
      'tips.title':'À savoir', 'tips.close':'Fermer',
      'tips.1':'<b>Rien n’est enregistré.</b> « Créer le cas » affiche un message, rien de plus.',
      'tips.2':'<b>Recherche de patient :</b> <b>1234</b> + CHU Sainte-Justine, le seul dossier existant.',
      'tips.3':'<b>Cas prénatal :</b> cochez-le à la section 1 — la section 2 décrit alors la mère.',
      'tips.4':'<b>Signes cliniques :</b> au moins un phénotype observé est requis.',
      'tips.5':'<b>Famille :</b> cochez un membre dans l’analyse — le pedigree et le badge suivent.',
      'tips.6':'<b>Menu Analyse :</b> filtrez par mot ou numéro d’acte, n’importe où dans le nom.',
      'tips.7':'<b>La recherche HPO suit la langue</b> — un terme anglais ne donne rien en français.',
      'tips.8':'<b>FR / EN</b> change l’interface et conserve ce que vous avez saisi.',""")

# -------------------------------------------------------------------- 5 · JS
rep("""  /* ---------- init ---------- */""",
    """  /* demo build: the ⓘ sheet. Same open/close vocabulary as the other modals —
     ✕, a Close button, a backdrop click and Esc, none of which change any data. */
  (function(){
    var m = document.getElementById('tips-modal');
    function shut(){ m.setAttribute('hidden',''); }
    document.getElementById('tips-btn').addEventListener('click', function(){ m.removeAttribute('hidden'); });
    document.getElementById('tips-x').addEventListener('click', shut);
    document.getElementById('tips-close').addEventListener('click', shut);
    m.addEventListener('click', function(e){ if(e.target === m) shut(); });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape' && !m.hasAttribute('hidden')) shut();
    });
  })();

  /* ---------- init ---------- */""")

if not os.path.isdir('docs'):
    os.mkdir('docs')
io.open(OUT, 'w', encoding='utf-8').write(s)
print('make-demo: wrote %s (%.1f KB)' % (OUT, len(s.encode('utf-8')) / 1024.0))
