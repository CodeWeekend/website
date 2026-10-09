"""Accessibility, RTL, imagery and identity review for Weekend W v1.1."""
from pathlib import Path
import json, re, hashlib
from fontTools.ttLib import TTFont

def refine(root, base):
    svg, rect, wmark = [base[k] for k in ('svg','rect','wmark')]
    ink, cream, orange = '#182B29', '#F7F4EC', '#F0643B'
    for folder in ('imagery','research'):
        (root/folder).mkdir(exist_ok=True)
    def save(name,w,h,body,title):
        (root/name).write_text(svg(w,h,body,title))
    def image(src, cls='', alt=''):
        return f'<img src="{src}" class="{cls}" alt="{alt}">'

    # Decorative imagery: no people, personal data or invented learner projects.
    # Geometry derives only from the unchanged, upright W master.
    for name,width,height in [('hero-landscape',1600,1000),('hero-square',1080,1080)]:
        body=rect(0,0,width,height,ink)
        body+=wmark(width*.41,height*.30,width*.69,orange)
        body+=wmark(-width*.19,-height*.22,width*.53,'#29413C')
        body+=wmark(width*.08,height*.78,width*.30,cream)
        save(f'imagery/{name}.svg',width,height,body,'Decorative CodeWeekend W field')
    for name,bg,fg,accent in [('story-build',cream,ink,orange),('story-learn','#EDE9DF',ink,'#BCC9BC'),('story-share',ink,cream,orange)]:
        body=rect(0,0,1200,900,bg)
        body+=wmark(205,190,790,fg)
        body+=rect(72,746,272,24,accent)+rect(368,746,80,24,accent)
        save(f'imagery/{name}.svg',1200,900,body,'Decorative CodeWeekend story tile')
    for name,bg,fg in [('pattern',cream,orange),('pattern-sage',cream,'#BCC9BC')]:
        body=rect(0,0,1400,440,bg)
        for row in range(3):
            for col in range(7): body+=wmark(col*230-60,row*180-25,180,fg)
        save(f'applications/{name}.svg',1400,440,body,'Decorative repeating upright W pattern')

    (root/'tokens.css').write_text('''/* CodeWeekend v1.1 — sRGB. Text pairings are documented in source/contrast.json. */
:root {
  --cw-ink: #182B29; --cw-ink-hover: #29413C; --cw-ink-deep: #0F1D1B;
  --cw-cream: #F7F4EC; --cw-surface-2: #EDE9DF; --cw-white: #FFFFFF;
  --cw-vermilion: #F0643B; --cw-vermilion-light: #FA805E; --cw-vermilion-wash: #FFF0E9;
  --cw-rust: #CC3A10; --cw-rust-dark: #A72D0B; --cw-rust-deep: #822308;
  --cw-sage: #BCC9BC; --cw-muted: #52635E;
  --cw-line: #D9DED7; /* Decorative separators only; not input boundaries. */
  --cw-border: #687B71; /* Functional control boundaries on light surfaces. */
  --cw-error: #B3261E; --cw-error-bg: #FFF0EE;
  --cw-success: #285C3F; --cw-success-bg: #E8F1E8;
  --cw-info: #1F5A7A; --cw-info-bg: #EAF2F7;
  --cw-warning: #775000; --cw-warning-bg: #FFF0C2;
  --cw-text: var(--cw-ink); --cw-background: var(--cw-cream);
  --cw-link: var(--cw-rust-dark); --cw-link-hover: var(--cw-rust-deep);
  --cw-focus: var(--cw-rust-dark);
  --cw-font: 'Manrope', sans-serif;
  --cw-font-rtl: 'Vazirmatn', sans-serif;
  --cw-mono: 'Atkinson Hyperlegible Mono', monospace;
  --cw-space: 8px; --cw-radius: 12px;
}
''')
    (root/'web-components.css').write_text('''/* Portable examples, scoped to .cw-brand. Import tokens.css first.
   Font paths are relative to this file. Keep fonts/ alongside it. */
@font-face {font-family:Manrope;src:url('fonts/Manrope.ttf') format('truetype');font-weight:200 800;font-display:swap}
@font-face {font-family:Vazirmatn;src:url('fonts/Vazirmatn.ttf') format('truetype');font-weight:100 900;font-display:swap}
@font-face {font-family:'Atkinson Hyperlegible Mono';src:url('fonts/AtkinsonHyperlegibleMono.ttf') format('truetype');font-weight:200 800;font-display:swap}
.cw-brand {color:var(--cw-text);background:var(--cw-background);font:400 18px/1.6 var(--cw-font)}
.cw-brand h1,.cw-brand h2,.cw-brand h3 {font-weight:800;line-height:1.15}
.cw-brand a {color:var(--cw-link);text-decoration:underline;text-underline-offset:.2em}
.cw-brand a:hover {color:var(--cw-link-hover);text-decoration-thickness:2px}
.cw-brand a:active {color:var(--cw-rust-deep)}
.cw-brand :focus-visible {outline:3px solid var(--cw-focus);outline-offset:3px}
.cw-brand .cw-button {display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:10px 24px;border:2px solid transparent;border-radius:var(--cw-radius);font:700 1rem/1.3 var(--cw-font);cursor:pointer;background:var(--cw-rust);color:var(--cw-white);text-decoration:none}
.cw-brand .cw-button:hover {background:var(--cw-rust-dark);color:var(--cw-white)}
.cw-brand .cw-button:active {background:var(--cw-rust-deep);color:var(--cw-white)}
.cw-brand .cw-button-accent {background:var(--cw-vermilion);color:var(--cw-ink)}
.cw-brand .cw-button-accent:hover {background:var(--cw-vermilion-light);color:var(--cw-ink)}
.cw-brand .cw-button-accent:active {background:var(--cw-vermilion);color:var(--cw-ink);box-shadow:inset 0 0 0 2px var(--cw-ink)}
.cw-brand input,.cw-brand textarea,.cw-brand select {font:inherit;color:var(--cw-ink);background:var(--cw-cream);border:1px solid var(--cw-border);border-radius:8px;padding:10px 12px;min-height:44px}
.cw-brand [aria-invalid=true] {border:2px solid var(--cw-error)}
.cw-brand .cw-error {color:var(--cw-error);background:var(--cw-error-bg)}
.cw-brand .cw-success {color:var(--cw-success);background:var(--cw-success-bg)}
.cw-brand .cw-info {color:var(--cw-info);background:var(--cw-info-bg)}
.cw-brand .cw-warning {color:var(--cw-warning);background:var(--cw-warning-bg)}
.cw-brand .cw-status {padding:12px 16px;border-radius:8px}
.cw-brand .cw-surface-2 {background:var(--cw-surface-2)}
.cw-brand .cw-dark {background:var(--cw-ink);color:var(--cw-cream);--cw-link:var(--cw-vermilion-light);--cw-link-hover:var(--cw-cream);--cw-focus:var(--cw-cream)}
.cw-brand .cw-dark a:active:not(.cw-button) {color:var(--cw-cream)}
.cw-brand .cw-logo {direction:ltr;unicode-bidi:isolate;display:inline-block}
.cw-brand :lang(fa),.cw-brand :lang(ps),.cw-brand:lang(fa),.cw-brand:lang(ps) {font-family:var(--cw-font-rtl);letter-spacing:normal;line-height:1.8}
.cw-brand .cw-button:lang(fa),.cw-brand .cw-button:lang(ps) {font-family:var(--cw-font-rtl)}
.cw-brand code,.cw-brand pre,.cw-brand code:lang(fa),.cw-brand code:lang(ps),.cw-brand pre:lang(fa),.cw-brand pre:lang(ps) {font-family:var(--cw-mono);direction:ltr;unicode-bidi:isolate;text-align:left}
@media (forced-colors:active) {.cw-brand .cw-button {border:2px solid ButtonText}.cw-brand :focus-visible {outline:3px solid Highlight}}
''')

    # Test the proposed notch at actual sizes. Kept out of production logos.
    notch=base['W_PATH'].replace('80 78V0H120V78','80 78V0H94V16H106V0H120V78')
    body=rect(0,0,1100,420,cream)
    body+=base['text']('APPROVED W',36,48,20)+base['text']('CURSOR NOTCH / NOT SELECTED',36,245,20)
    for x,size in zip([36,110,210,350,560],[16,24,32,64,180]):
        body+=wmark(x,80,size,ink)
        body+=f'<path transform="translate({x} 278) scale({size/200})" fill="{ink}" d="{notch}"/>'
        body+=base['text'](f'{size}px',x,210,12,ink,'Mono')
    save('research/notch-comparison.svg',1100,420,body,'Approved W compared with rejected cursor notch at actual pixel sizes')

    lum=base['luminance']
    def ratio(a,b):
        x,y=sorted([lum(a),lum(b)]); return (y+.05)/(x+.05)
    pairings=[('Body',ink,cream,4.5),('Secondary text','#52635E','#EDE9DF',4.5),('Accent button',ink,orange,4.5),('Accent hover',ink,'#FA805E',4.5),('Primary button','#FFFFFF','#CC3A10',4.5),('Primary hover','#FFFFFF','#A72D0B',4.5),('Primary active','#FFFFFF','#822308',4.5),('Link on cream','#A72D0B',cream,4.5),('Link on surface 2','#A72D0B','#EDE9DF',4.5),('Link hover','#822308','#EDE9DF',4.5),('Link on dark','#FA805E',ink,4.5),('Input border','#687B71','#EDE9DF',3),('Light focus','#A72D0B','#EDE9DF',3),('Dark focus',cream,ink,3),('Error','#B3261E','#FFF0EE',4.5),('Success','#285C3F','#E8F1E8',4.5),('Info','#1F5A7A','#EAF2F7',4.5),('Warning','#775000','#FFF0C2',4.5)]
    checks=[{'role':role,'foreground':fg,'background':bg,'ratio':round(ratio(fg,bg),3),'required':minimum,'pass':ratio(fg,bg)>=minimum} for role,fg,bg,minimum in pairings]
    assert all(p['pass'] for p in checks),checks
    checks += [{'role':'Do not use Vermilion text on Cream','foreground':orange,'background':cream,'ratio':round(ratio(orange,cream),3),'required':4.5,'pass':False}, {'role':'Rust 600 not universal: fails on surface 2','foreground':'#CC3A10','background':'#EDE9DF','ratio':round(ratio('#CC3A10','#EDE9DF'),3),'required':4.5,'pass':False}]
    (root/'source/contrast.json').write_text(json.dumps(checks,indent=2))
    chars='دری پښتو ټ ځ څ ډ ړ ږ ښ ګ ڼ ې ۍ پ چ ژ ک ی'
    cmap=TTFont(root/'fonts/Vazirmatn.ttf').getBestCmap()
    missing=[c for c in set(chars) if not c.isspace() and ord(c) not in cmap]
    assert not missing,missing
    (root/'source/font-checks.json').write_text(json.dumps({'font':'Vazirmatn.ttf','specimen':chars,'missingCharacters':missing,'scope':'Specimen coverage, not a native-speaker translation review.'},ensure_ascii=False,indent=2))

    old=base['pages']
    content=[re.sub(r'<footer>.*?</footer>','',p,flags=re.S) for p in old]
    def page(body,cls=''): return f'<section class="page {cls}">{body}</section>'
    p4=page('''<div class="eyebrow">COLOUR / HIERARCHY</div><h2>Warmth, with room to breathe.</h2>
<div class="palette-layout"><div><div class="palette-foundation"><div style="background:#F7F4EC"><b>Cream</b><code>#F7F4EC</code><p>The canvas. Give it the most space.</p></div><div style="background:#182B29;color:#F7F4EC"><b>Ink</b><code>#182B29</code><p>Text, wordmark and dark surfaces.</p></div></div><div class="palette-support"><span style="background:#BCC9BC"></span><div><b>Sage / #BCC9BC</b><p>A quiet supporting colour. Use in separate compositions.</p></div></div></div><div class="palette-accent"><div style="background:#F0643B;color:#182B29"><b>Vermilion</b><code>#F0643B</code><p>Logo and graphic emphasis.<br>Use Ink lettering.</p></div><div style="background:#CC3A10;color:white"><b>Rust</b><code>#CC3A10</code><p>Primary buttons with white text.</p></div></div></div>
<div class="rule-strip"><b>Choose a colour family per composition.</b><p>Ink + Cream + Vermilion for energy. Ink + Cream + Sage for quieter stories.<br>Avoid equal Ink, Vermilion and Sage stripes; do not arrange them as a tricolour.</p></div>
<p class="footnote">Vermilion on Cream is 2.90:1. Keep that pair out of text and functional icons. The logo is artwork; navigation labels still need accessible text.</p>''')
    rows=''.join(f'<tr><td>{role}</td><td><code>{fg}</code> / <code>{bg}</code></td><td>{ratio(fg,bg):.2f}:1</td></tr>' for role,fg,bg,_ in [pairings[i] for i in [0,2,4,8,11,14]])
    p5=page('''<div class="eyebrow">WEB COLOUR / INTERACTION</div><h2>Every state has a job.</h2><div class="web-grid"><div><div class="eyebrow">REAL COLOUR PAIRINGS</div><div class="demo-controls"><span class="demo-btn">Join the community</span><span class="demo-btn accent">Explore projects</span><a>Read a story</a></div><div class="demo-controls"><span class="demo-btn hover">Hover</span><span class="demo-btn active">Pressed</span><span class="demo-btn focused">Keyboard focus</span></div><div class="demo-field">Email address</div><p class="demo-error">Error: enter a valid email address.</p><p class="small-note">Use text or an icon with every status. Colour alone is never the message.</p></div><div><table class="contrast-table"><thead><tr><th>Role</th><th>Text or edge / surface</th><th>Contrast</th></tr></thead><tbody>'''+rows+'''</tbody></table><p class="small-note">Normal text ≥ 4.5:1. Control edges and focus against their adjacent surface ≥ 3:1. These pairings pass; a website still needs an end-to-end accessibility check.</p></div></div><div class="token-notes"><p><b>Links</b><br>Rust Dark #A72D0B, underlined.<br>Hover #822308. On Ink: #FA805E.</p><p><b>Surfaces & boundaries</b><br>Cream; secondary #EDE9DF.<br>Inputs #687B71; dividers #D9DED7.</p><p><b>Focus & feedback</b><br>3 px outline with 3 px offset.<br>Rust Dark on light; Cream on dark.</p></div><p class="footnote">Rust #CC3A10 passes on Cream (4.57:1), but fails on the secondary surface (4.14:1). Use Rust Dark for links on both. All status pairs are defined in tokens.css.</p>''')
    p6=page('''<div class="eyebrow">TYPOGRAPHY / LATIN & RIGHT-TO-LEFT</div><h2>One voice. Both directions.</h2><div class="language-grid"><div><div class="eyebrow">LATIN / MANROPE</div><div class="specimen">Build something.<br>Together.</div><p>Headings 800. Body 400–500.<br>Web body 18 px / 1.6. Use sentence case.</p><div class="eyebrow mono-sample">ATKINSON HYPERLEGIBLE MONO / 500</div><p class="mono">WEEKEND 01 / BUILD & SHARE</p><p class="small-note">Short technical labels and code.<br>Use Vazirmatn for Arabic-script labels.</p></div><div class="rtl-panel"><div class="eyebrow">DARI & PASHTO / VAZIRMATN</div><div class="rtl-specimen" lang="fa-AF" dir="rtl">دری</div><div class="rtl-specimen" lang="ps-AF" dir="rtl">پښتو</div><p class="rtl-glyphs" lang="ps-AF" dir="rtl">ټ ځ څ ډ ړ ږ ښ ګ ڼ ې ۍ</p><p class="small-note">Retain the site's Vazirmatn. Body 18 px / 1.8.<br>No artificial letter spacing. Natural RTL alignment.</p></div></div><div class="rtl-rules"><div><b>Set language and direction</b><p>Use lang="fa-AF" or "ps-AF" and dir="rtl" on the relevant page or section.</p></div><div><b>Keep the identity LTR</b><p>Isolate the supplied logo with dir="ltr". Do not mirror the W, wordmark or code.</p></div><div><b>Review native copy</b><p>These are script specimens, not translated campaign copy. Have native speakers review published text.</p></div></div>''')
    p7=page('''<div class="eyebrow">IMAGERY / THE W FIELD</div><h2>Show the energy of making.</h2><div class="imagery-grid"><div>'''+image('imagery/hero-landscape.svg','hero-art')+'''<p class="small-note">Hero artwork / 1600 × 1000. Square crop also supplied.<br>Set page headlines beside the artwork in live HTML.</p></div><div><h4>Geometry carries the story.</h4><p>Use large, upright W forms with deliberate crops and clear space. Flat colour, an 8 px layout grid and one accent family per composition.</p><h4>Privacy is part of the direction.</h4><p>Use these abstract tiles as defaults. Future story images can show sanitised project screens or objects; remove faces, names, account details and identifying surroundings.</p><h4>Keep the content honest.</h4><p>Do not invent learner projects or imply an abstract image documents a real event. Avoid cultural motifs and rescue narratives.</p></div></div><div class="story-tiles">'''+''.join(image('imagery/'+n+'.svg') for n in ['story-build','story-learn','story-share'])+'''<div><b>Build / learn / share</b><p>1200 × 900 story tiles.<br>Titles belong in HTML.<br>Decorative images: alt="".</p></div></div><p class="footnote">Patterns are supporting artwork, never substitute logos. Keep busy patterns away from body text. Meaningful project images need alt text describing the work, not the learner's identity.</p>''')
    p9=page('''<div class="eyebrow">HANDOFF / VERSION 1.1 / 09 OCTOBER 2026</div><h2>The files behind the identity.</h2><div class="handoff-grid"><div><h4>Logo masters</h4><p>Horizontal and stacked SVGs.<br>Colour, reverse and mono masters.<br>Transparent PNGs, avatar and favicon.</p><h4>Web foundations</h4><p>Semantic colour tokens and sample CSS.<br>Manrope, Atkinson Hyperlegible Mono<br>and Vazirmatn, with licences.</p><h4>Imagery & communication</h4><p>Hero in landscape and square formats.<br>Three story tiles; two pattern families.<br>Square, portrait and banner social artwork.</p></div><div class="decision-card"><div class="eyebrow">DECISION / KEEP THE APPROVED W</div><h3>The simple form holds up.</h3><p>The tested cursor notch is under one pixel wide at favicon scale and loses its intended meaning. Keep the original geometry and use the full CodeWeekend lockup where space allows.</p><p>A consistent wordmark, palette and layout do more here than a fragile extra detail.</p></div></div><div class="screening-note"><b>Preliminary name and visual screen</b><p>Canadian register: 0 matches for CODEWEEKEND and “CODE WEEKEND” on 9 October 2026. Unrelated events using Code Weekend were found elsewhere. Orange W marks also exist, notably Wattpad. This is not trademark clearance.</p><p>Before a major print run, obtain a professional name and design review in the intended markets. Research scope, sources and limitations are in research/brand-screening.txt.</p></div><p class="footnote">The website has not been changed. This package supplies the design rules and assets for its next implementation. SVGs are the vector masters; PNGs are digital exports.</p>''')
    pages=content[:3]+[p4,p5,p6,p7,content[4],p9]
    for i,p in enumerate(pages):
        foot=f'<footer><span>CODEWEEKEND / BRAND GUIDE V1.1</span><span>WEEKEND W</span><span>{i+1:02} / 09</span></footer>'
        pages[i]=p.replace('</section>',foot+'</section>')
    css=base['css']+'''
@font-face{font-family:Vazirmatn;src:url(fonts/Vazirmatn.ttf)}
code{font-family:Mono;font-size:.88em}.palette-layout{display:grid;grid-template-columns:2fr 1fr;gap:28px}.palette-foundation{display:grid;grid-template-columns:1.15fr 1fr;border:1px solid #D9DED7}.palette-foundation>div{padding:26px;min-height:206px}.palette-layout b{font-size:23px}.palette-layout code{display:block;margin:10px 0 24px}.palette-layout p{font-size:13px}.palette-support{display:flex;gap:20px;align-items:center;margin-top:28px}.palette-support span{display:block;width:72px;height:72px;border-radius:50%;flex-shrink:0}.palette-support b{font-size:16px}.palette-accent{display:grid;grid-template-columns:1fr;gap:16px}.palette-accent>div{padding:20px 24px}.palette-accent code{margin:6px 0 12px}.palette-accent b{font-size:20px}.rule-strip{margin-top:30px;border-top:1px solid #D9DED7;padding-top:22px}.rule-strip p{margin-top:8px;font-size:14px}.web-grid{display:grid;grid-template-columns:1fr 1.2fr;gap:40px}.demo-controls{display:flex;gap:14px;align-items:center;margin:22px 0;flex-wrap:wrap}.demo-controls a{color:#A72D0B;font-size:14px;text-decoration:underline}.demo-btn{display:inline-block;background:#CC3A10;color:white;padding:12px 17px;border-radius:10px;font-size:13px;font-weight:700}.demo-btn.accent{color:#182B29;background:#F0643B}.demo-btn.hover{background:#A72D0B}.demo-btn.active{background:#822308}.demo-btn.focused{outline:3px solid #A72D0B;outline-offset:3px}.demo-field{border:1px solid #687B71;border-radius:8px;padding:12px;font-size:14px;margin-top:24px}.demo-error{font-size:13px;color:#B3261E;background:#FFF0EE;padding:10px;margin-top:8px}.small-note{font-size:12px;color:#52635E;line-height:1.55;margin-top:14px}.contrast-table{border-collapse:collapse;width:100%;font-size:12px}.contrast-table th{text-align:left;font-size:10px;color:#52635E;padding:0 8px 12px 0}.contrast-table td{border-top:1px solid #D9DED7;padding:13px 8px 13px 0}.contrast-table code{font-size:10px}.token-notes{display:grid;grid-template-columns:repeat(3,1fr);gap:35px;border-top:1px solid #D9DED7;margin-top:28px;padding-top:20px}.token-notes p{font-size:13px}.language-grid{display:grid;grid-template-columns:1.15fr 1fr;gap:65px}.language-grid .specimen{font-size:49px}.rtl-panel{background:#EDE9DF;padding:24px 28px}.rtl-specimen{font-family:Vazirmatn;font-size:53px;line-height:1.35;font-weight:700}.rtl-specimen:first-of-type{margin-top:16px}.rtl-glyphs{font-family:Vazirmatn;font-size:29px;margin-top:4px}.rtl-rules{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;border-top:1px solid #D9DED7;padding-top:22px;margin-top:30px}.rtl-rules b{font-size:15px}.rtl-rules p{font-size:13px;margin-top:8px}.imagery-grid{display:grid;grid-template-columns:1.1fr 1fr;gap:36px}.hero-art{width:100%;height:270px;object-fit:cover}.imagery-grid h4{margin:0 0 6px}.imagery-grid h4:not(:first-child){margin-top:14px}.imagery-grid p{font-size:12px}.story-tiles{display:flex;gap:18px;margin-top:23px;align-items:center}.story-tiles img{width:212px;height:128px;object-fit:cover}.story-tiles>div{padding-left:16px}.story-tiles p{font-size:12px;margin-top:7px}.handoff-grid{display:grid;grid-template-columns:1fr 1.1fr;gap:65px}.handoff-grid h4{margin:0 0 7px}.handoff-grid h4:not(:first-child){margin-top:20px}.handoff-grid p{font-size:14px}.decision-card{background:#EDE9DF;padding:28px 32px}.decision-card h3{margin:18px 0}.decision-card p+p{margin-top:16px}.screening-note{border-top:1px solid #D9DED7;padding-top:20px;margin-top:26px}.screening-note p{font-size:13px;margin-top:7px}.page:last-child .footnote{font-size:11px}
'''
    (root/'brand-guide.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>CodeWeekend / Brand Guide v1.1</title><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
    (root/'source/logo-hashes.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root/'logos').glob('*.svg'))},indent=2))
    print(f'v1.1: {len(pages)} pages; {len(pairings)} approved contrast pairings; Vazirmatn specimen covered.')
