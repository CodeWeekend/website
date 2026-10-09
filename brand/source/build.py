"""Rebuild the Weekend W vector assets and nine-page brand guide.
Requires fontTools. Run from any directory with Python 3.
"""
from pathlib import Path
from html import escape
import json
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT = Path(__file__).resolve().parents[1]
INK, ORANGE, CREAM, LINE, MUTED = '#182B29', '#F0643B', '#F7F4EC', '#D9DED7', '#52635E'
fonts = {}
for name, source, weight in [('Display','Manrope.ttf',800),('Body','Manrope.ttf',500),('Mono','AtkinsonHyperlegibleMono.ttf',500)]:
    font = TTFont(ROOT/'fonts'/source)
    if 'fvar' in font:
        font = instantiateVariableFont(font, {'wght':weight}, inplace=False)
    font.save(ROOT/'fonts'/f'{name}.ttf')
    fonts[name] = font

def type_svg(text, x, y, size, colour=INK, family='Display', tracking=0):
    font=fonts[family]; gs=font.getGlyphSet(); cmap=font.getBestCmap(); unit=font['head'].unitsPerEm
    cursor=0; paths=[]
    for ch in text:
        glyph=cmap.get(ord(ch),'.notdef'); pen=SVGPathPen(gs); gs[glyph].draw(pen)
        paths.append(f'<path transform="translate({cursor:.3f} 0)" d="{pen.getCommands()}"/>')
        cursor += font['hmtx'][glyph][0] + tracking*unit/size
    return f'<g aria-label="{escape(text)}" fill="{colour}" transform="translate({x} {y}) scale({size/unit} {-size/unit})">'+''.join(paths)+'</g>', cursor*size/unit

W_PATH='M0 0H40V78Q40 96 60 96Q80 96 80 78V0H120V78Q120 96 140 96Q160 96 160 78V0H200V82Q200 132 146 132H139Q113 132 100 119Q87 132 61 132H54Q0 132 0 82Z'
def wmark(x,y,width,colour=ORANGE):
    return f'<path fill="{colour}" transform="translate({x} {y}) scale({width/200})" d="{W_PATH}"/>'
def rect(x,y,w,h,c,rx=0): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>'
def text(s,x,y,size,c=INK,font='Display',tracking=0): return type_svg(s,x,y,size,c,font,tracking)[0]
def svg(w,h,body,title): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title>{body}</svg>'
def save(path,w,h,body,title): (ROOT/path).write_text(svg(w,h,body,title))
def lockup(x,y,width,mark=ORANGE,word=INK):
    letters,advance=type_svg('codeweekend',244,118,144,word,tracking=-3)
    full=244+advance+6
    return f'<g transform="translate({x} {y}) scale({width/full})">{wmark(0,0,200,mark)}{letters}</g>'

# Final production logo, native vector geometry and outlined wordmark.
for name,m,c in [('primary',ORANGE,INK),('reverse',ORANGE,CREAM),('mono-ink',INK,INK),('mono-white','#FFFFFF','#FFFFFF')]:
    letters,width=type_svg('codeweekend',260,134,144,c,tracking=-3)
    save(f'logos/logo-{name}.svg',round(276+width,2),164,wmark(16,16,200,m)+letters,'CodeWeekend - Weekend W')
    save(f'logos/mark-{name}.svg',232,164,wmark(16,16,200,m),'CodeWeekend W symbol')
    sw=type_svg('codeweekend',0,0,70,c,tracking=-1.5)[1]
    save(f'logos/logo-stacked-{name}.svg',600,330,wmark(200,28,200,m)+text('codeweekend',(600-sw)/2,282,70,c,tracking=-1.5),'CodeWeekend stacked logo')
save('logos/avatar.svg',800,800,rect(0,0,800,800,INK)+wmark(160,242,480),'CodeWeekend social avatar')
save('logos/favicon.svg',32,32,rect(0,0,32,32,INK,7)+wmark(6,9.4,20),'CodeWeekend favicon')

# Production-ready communication assets: all lettering is outlined.
b=rect(0,0,1080,1080,CREAM)+lockup(76,75,480)
for s,y in [('Build',348),('something.',460),('Together.',572)]: b+=text(s,70,y,102,INK,tracking=-4)
b+=text('A community for people who build.',76,670,28,INK,'Body')
b+=wmark(76,800,210)+text('codeweekend.net',667,980,23,INK,'Mono')
b+=rect(962,280,118,480,ORANGE)
save('applications/social-square.svg',1080,1080,b,'Build something. Together. CodeWeekend social post')
b=rect(0,0,1080,1350,INK)+lockup(76,75,470,ORANGE,CREAM)
b+=text('WEEKEND / COMMUNITY',76,276,22,CREAM,'Mono',1.5)
for s,y in [('Learn it.',435),('Build it.',551),('Share it.',667)]: b+=text(s,70,y,104,CREAM,tracking=-4)
b+=text('Good things happen when',76,775,31,CREAM,'Body')+text('we make things together.',76,820,31,CREAM,'Body')
b+=wmark(690,961,312)+text('codeweekend.net',76,1249,26,CREAM,'Mono')
save('applications/social-portrait.svg',1080,1350,b,'Learn it. Build it. Share it. CodeWeekend social post')
b=rect(0,0,1200,630,CREAM)+lockup(64,57,425)
b+=text('Build something.',62,323,84,INK,tracking=-3.5)+text('Together.',62,426,84,INK,tracking=-3.5)
b+=text('An inclusive community of developers.',66,542,26,INK,'Body')+wmark(926,355,200)
save('applications/social-banner.svg',1200,630,b,'CodeWeekend social sharing banner')

# Reusable decorative device comes from the W's two open channels.
p=''
for row in range(3):
    for col in range(7): p+=wmark(col*230-60,row*180-25,180,ORANGE if (row+col)%4==0 else '#BCC9BC')
save('applications/pattern.svg',1400,440,rect(0,0,1400,440,CREAM)+p,'CodeWeekend repeating W pattern')

(ROOT/'tokens.css').write_text('''/* CodeWeekend: Weekend W. Display/wordmark: Manrope 800. Body: Manrope 500. */
:root {
  --cw-ink: #182B29;
  --cw-vermilion: #F0643B;
  --cw-cream: #F7F4EC;
  --cw-sage: #BCC9BC;
  --cw-muted: #52635E;
  --cw-line: #D9DED7;
  --cw-font: 'Manrope', sans-serif;
  --cw-mono: 'Atkinson Hyperlegible Mono', monospace;
  --cw-space: 8px;
  --cw-radius: 12px;
}
''')

def img(src,cls='',style=''): return f'<img class="{cls}" style="{style}" src="{src}" alt="{escape(Path(src).stem)}">'
def footer(n): return f'<footer><span>CODEWEEKEND / BRAND GUIDE</span><span>WEEKEND W</span><span>{n:02} / 06</span></footer>'
def page(n,body,cls=''): return f'<section class="page {cls}">{body}{footer(n)}</section>'
pages=[]
pages.append(page(1,f'''<div class="eyebrow">IDENTITY / OCTOBER 2026</div>{img('logos/logo-primary.svg','hero-logo')}
<h1>Build something.<br><em>Together.</em></h1>
<div class="cover-bottom"><p>A welcoming identity for a community<br>of developers, learners and mentors.</p><div><b>THE SELECTED DIRECTION</b><br>Weekend W</div></div>
<div class="cover-mark">{wmark(0,0,390)}</div>''','cover'))
# Put native symbol SVG into the cover's element.
pages[0]=pages[0].replace(f'<div class="cover-mark">{wmark(0,0,390)}</div>',f'<div class="cover-mark">{svg(390,258,wmark(0,0,390),"Weekend W")}</div>')

cards=[]
for i,name,file,desc,verdict in [
 (1,'CW Monogram','01-cw-monogram.png','A connected monogram with a human, informal feel.','The letterforms can be mistaken for “aw”.'),
 (2,'Weekend W','02-weekend-w.png','Two joined channels form one confident, compact W.','Selected: clearest silhouette and strongest small-size use.'),
 (3,'Shared Blocks','03-shared-blocks.png','A modular staircase suggests learning and progress.','The chart-like silhouette feels less specific to the community.')]:
    cards.append(f'<article class="concept {"chosen" if i==2 else ""}"><div class="eyebrow">0{i} / {"SELECTED" if i==2 else "EXPLORATION"}</div><h3>{name}</h3>{img("exploration/"+file)}<p>{desc}</p><p class="reason">{verdict}</p></article>')
pages.append(page(2,'<div class="eyebrow">THREE DIRECTIONS / ONE DECISION</div><h2>A mark that belongs<br>in the everyday.</h2><div class="concepts">'+''.join(cards)+'</div><p class="footnote">Design judgement based on clarity, versatility and fit. Concept images are explorations; the supplied SVG files are the final masters.</p>'))
pages.append(page(3,f'''<div class="eyebrow">THE IDENTITY</div><h2>One W. Built together.</h2><p class="intro">An open, sturdy symbol with the warmth of rounded joins.<br>Two equal channels share a central stem: a quiet idea of learning together.</p>
<div class="logo-panels"><div class="light">{img('logos/logo-primary.svg')}<span>PRIMARY / CREAM OR WHITE</span></div><div class="dark">{img('logos/logo-reverse.svg')}<span>REVERSE / INK</span></div></div>
<div class="logo-rules"><div>{img('logos/mark-mono-ink.svg')}<h4>Works in one colour</h4><p>Use the mono master for stamps,<br>embroidery and single-ink printing.</p></div><div class="space-demo">{img('logos/mark-primary.svg')}<h4>Give it breathing room</h4><p>Leave one stem-width of clear space<br>around the visible logo on every side.</p></div><div>{img('logos/favicon.svg','favicon')}<h4>Keep the small mark simple</h4><p>Use the supplied favicon at 16–32 px.<br>Use the full lockup from 160 px wide.</p></div></div>'''))

swatches=''.join(f'<div class="swatch" style="background:{colour};color:{fg}"><b>{name}</b><span>{colour}</span></div>' for name,colour,fg in [('Ink',INK,CREAM),('Vermilion',ORANGE,INK),('Cream',CREAM,INK),('Sage','#BCC9BC',INK)])
pages.append(page(4,f'''<div class="eyebrow">COLOUR & TYPOGRAPHY</div><h2>Warm. Clear. Confident.</h2><div class="swatches">{swatches}</div>
<div class="type-grid"><div><div class="eyebrow">MANROPE / 800</div><div class="specimen">Make your<br>next thing.</div><p>Headlines and wordmark. Sentence case.<br>Tight but open spacing. Strong, simple lines.</p></div><div><div class="eyebrow">MANROPE / 400–500</div><p class="body-sample">You bring the curiosity.<br>We learn by building together.</p><p>Body text: 18 px / 1.6 on the web.<br>Keep paragraphs short and instructions direct.</p><div class="eyebrow mono-sample">ATKINSON HYPERLEGIBLE MONO / 500</div><p class="mono">WEEKEND 01 / BUILD & SHARE</p></div></div>
<p class="footnote">Use Ink for text on Cream, Sage and Vermilion. Use Cream on Ink. Vermilion is an accent, not small text on Cream.</p>'''))
pages.append(page(5,f'''<div class="eyebrow">VOICE & APPLICATION</div><h2>Invite people to build.</h2>
<div class="voice-grid"><div><div class="eyebrow">POSITIONING</div><p class="position">An inclusive community<br>of developers.</p><div class="eyebrow">SIGNATURE LINE</div><p class="position">Build something. Together.</p><div class="eyebrow">HOW WE SOUND</div><p>Warm, specific and practical. Speak to learners as people who make things. Show the work and give a clear next step.</p><p><b>Use:</b> learn, build, practise, share, join.<br><b>Avoid:</b> hype, jargon and rescue narratives.</p><p><b>Name:</b> CodeWeekend in prose.<br>Lowercase only in the logo.</p></div><div class="application-previews">{img('applications/social-square.svg')}{img('applications/social-portrait.svg')}</div></div>'''))
pages.append(page(6,f'''<div class="eyebrow">A SYSTEM YOU CAN USE</div><h2>Ready for the next weekend.</h2>{img('applications/social-banner.svg','banner-preview')}
<div class="handoff"><div><h4>Logo kit</h4><p>Horizontal and stacked SVGs.<br>Colour, reverse and mono masters.<br>Transparent PNGs, avatar and favicon.</p></div><div><h4>Communication kit</h4><p>Square post, portrait post and banner.<br>Reusable W pattern and CSS tokens.<br>Open-source fonts with licences.</p></div><div><h4>Keep it consistent</h4><p>Use supplied masters. Never stretch,<br>outline, rotate or add effects.<br>Keep the W upright in every use.</p></div></div>
<p class="footnote">SVG files are the vector masters. PNG files are ready for digital use. Open-source font licences are included.</p>'''))

css='''@font-face{font-family:Manrope;src:url(fonts/Manrope.ttf)}@font-face{font-family:Mono;src:url(fonts/Mono.ttf)}
*{box-sizing:border-box}body{margin:0;background:#DFE3DB;color:#182B29;font-family:Manrope,sans-serif;font-size:16px} .page{position:relative;width:1200px;height:750px;padding:52px 60px 72px;margin:24px auto;background:#F7F4EC;overflow:hidden;break-after:page}.eyebrow{font-family:Mono,monospace;font-size:11px;letter-spacing:1.7px;font-weight:500}.page>.eyebrow{color:#52635E}h1,h2,h3,h4,p{margin:0}h1{font-size:92px;line-height:1.03;letter-spacing:-5px;font-weight:800}h2{font-size:48px;line-height:1.08;letter-spacing:-2px;margin:18px 0 25px}h3{font-size:24px;letter-spacing:-.8px;margin-top:14px}h4{font-size:17px;margin:14px 0 8px}p{line-height:1.6;font-size:15px}em{font-style:normal;color:#182B29}footer{position:absolute;bottom:28px;left:60px;right:60px;display:flex;justify-content:space-between;border-top:1px solid #D9DED7;padding-top:15px;font-family:Mono;font-size:9px;letter-spacing:1px;color:#52635E}.hero-logo{display:block;width:470px;margin:54px 0 52px}.cover h1{position:relative;z-index:2}.cover-bottom{display:flex;gap:110px;margin-top:36px;font-size:14px}.cover-bottom b{font:10px Mono;letter-spacing:1px}.cover-mark{position:absolute;right:58px;bottom:127px;width:300px}.cover-mark svg{width:100%;height:auto}.concepts{display:flex;gap:18px;margin-top:30px}.concept{width:348px;border:1px solid #D9DED7;padding:22px 20px;background:#FFFFFF44}.concept.chosen{border:2px solid #F0643B;padding:21px 19px}.concept img{width:100%;height:180px;object-fit:contain;margin:4px 0 12px}.concept p{font-size:14px;line-height:1.5}.concept .reason{border-top:1px solid #D9DED7;margin-top:16px;padding-top:13px;font-weight:700;min-height:60px}.concept .eyebrow{font-size:9px}.footnote{font-size:11px;color:#52635E;line-height:1.5;margin-top:20px}.intro{font-size:18px;margin-bottom:24px}.logo-panels{display:grid;grid-template-columns:1fr 1fr;gap:18px}.logo-panels>div{height:163px;padding:35px 30px 16px;border:1px solid #D9DED7;display:flex;flex-direction:column;justify-content:space-between}.logo-panels img{width:100%;max-height:69px}.logo-panels span{font:9px Mono;letter-spacing:1px}.dark{background:#182B29;color:#F7F4EC}.logo-rules{display:grid;grid-template-columns:repeat(3,1fr);gap:38px;margin-top:24px}.logo-rules img{height:63px;width:94px;object-fit:contain;object-position:left}.logo-rules .favicon{width:48px;height:63px}.logo-rules p{font-size:13px}.logo-rules h4{margin-top:8px}.space-demo img{padding:8px;border:1px dashed #52635E}.swatches{display:grid;grid-template-columns:repeat(4,1fr);height:122px;border:1px solid #D9DED7;margin-bottom:32px}.swatch{padding:21px;display:flex;flex-direction:column;justify-content:space-between}.swatch span{font:12px Mono}.type-grid{display:grid;grid-template-columns:1fr 1fr;gap:70px}.specimen{font-size:58px;font-weight:800;line-height:1.04;letter-spacing:-2.5px;margin:16px 0}.body-sample{font-size:26px;line-height:1.4;margin:18px 0}.mono-sample{margin-top:28px;font-size:10px}.mono{font-family:Mono;font-size:14px;margin-top:12px}.voice-grid{display:grid;grid-template-columns:420px 1fr;gap:55px}.voice-grid .eyebrow{margin:20px 0 8px}.voice-grid .eyebrow:first-child{margin-top:0}.position{font-size:25px;line-height:1.35;font-weight:800;letter-spacing:-.6px}.voice-grid p+p{margin-top:14px}.application-previews{display:flex;align-items:center;gap:16px}.application-previews img:first-child{width:270px;border:1px solid #D9DED7}.application-previews img:last-child{width:275px}.banner-preview{width:670px;height:352px;object-fit:contain;display:block;background:#F7F4EC;border:1px solid #D9DED7;margin:0 auto 26px}.handoff{display:grid;grid-template-columns:repeat(3,1fr);gap:32px}.handoff h4{margin:0 0 8px}.handoff p{font-size:13px}.page:last-child .footnote{font-size:10px;margin-top:15px}@page{size:1200px 750px;margin:0}@media print{body{background:#F7F4EC}.page{margin:0;box-shadow:none}.page:last-child{break-after:auto}}'''
(ROOT/'brand-guide.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>CodeWeekend / Weekend W Brand Guide</title><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')

def luminance(hex):
    v=[int(hex[i:i+2],16)/255 for i in (1,3,5)]
    lin=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in v]
    return sum(a*b for a,b in zip(lin,[.2126,.7152,.0722]))
contrast={}
for a,b in [(INK,CREAM),(INK,ORANGE),(INK,'#BCC9BC'),(CREAM,INK),(ORANGE,CREAM)]:
    x,y=sorted([luminance(a),luminance(b)])
    contrast[f'{a} on {b}']=round((y+.05)/(x+.05),2)
(ROOT/'source'/'contrast.json').write_text(json.dumps(contrast,indent=2))
print('Built vector masters, applications, tokens and guide. Contrast:',contrast)
from refine import refine
refine(ROOT, globals())
