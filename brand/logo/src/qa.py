#!/usr/bin/env python3
"""Acceptance tests 2-7 (decision.md) + R10 hygiene. Writes renders and qa/report.json into brand/final/qa/.
Test 1 (misread, fresh judges) is prepared as qa/misread.png for an independent panel."""
import os, sys, json, re, math, subprocess
import xml.etree.ElementTree as ET
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import geom as G
import favgrid as F
from build import render, FINAL, C

QA = os.path.join(FINAL, 'qa')
os.makedirs(QA, exist_ok=True)
INFO = json.load(open(os.path.join(HERE, 'build-info.json')))
REPORT = {}
BODY = G.BODY_H * G.U   # 252.35 file units = "body height"


def hexrgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def page(name, html, w, h):
    path = os.path.join(QA, name + '.html')
    with open(path, 'w') as fh:
        fh.write('<!doctype html><html><head><meta charset="utf-8"><style>*{margin:0;padding:0;box-sizing:border-box}'
                 'body{font:13px -apple-system,Helvetica,Arial,sans-serif;color:#333;background:#E9E7E1}</style></head><body>'
                 + html + '</body></html>')
    return render(path, os.path.join(QA, name + '.png'), w, h)


def zoom(src, box, k, out):
    im = Image.open(src).crop(box)
    im.resize((im.width * k, im.height * k), Image.NEAREST).save(out)
    return out


# ------------------------------------------------------------------ test 2: nav
def nav_geometry(body, bar):
    vb = INFO['small']['vb']; s = body / BODY
    return dict(h=vb[3] * s, w=vb[2] * s, top=bar / 2 - (G.PANEL_Y * G.U - vb[1]) * s, s=s, vb=vb)


def w_columns(s, left):
    """x-range (px) of the 'w' glyph in the nav lockup (x-height only, no overshoot)."""
    placed, font = G.wordmark_glyphs()
    sc = G.WORD_SIZE * G.U / 1000
    gx, cons = placed[4]
    xs = [q[0] for con in cons for seg in con for q in seg[1:]]
    first_ink = min(q[0] for con in placed[0][1] for seg in con for q in seg[1:])
    ox = 24 * G.U + G.WORD_GAP * G.STROKE * G.U - first_ink * sc
    vb = INFO['small']['vb']
    a = (ox + (gx + min(xs)) * sc - vb[0]) * s + left
    b = (ox + (gx + max(xs)) * sc - vb[0]) * s + left
    return a, b


def test_nav():
    out = {}
    for scale in (1, 2):
        bar = 64 * scale; body = 36 * scale; g = nav_geometry(body, bar); left = 24 * scale
        rows = ''
        for bg, src, fg in (('#FBF7EF', 'logo-small.svg', '#1B2034'), ('#FFFFFF', 'logo-small.svg', '#1B2034'),
                            ('#0E1630', 'logo-small-reverse.svg', '#FBF7EF'), ('#0B1C4B', 'logo-small-reverse.svg', '#FBF7EF')):
            rows += (f'<div style="position:relative;height:{bar}px;width:{760 * scale}px;background:{bg};margin-bottom:{8 * scale}px">'
                     f'<img src="../{src}" style="position:absolute;left:{left}px;top:{g["top"]:.2f}px;height:{g["h"]:.2f}px;width:{g["w"]:.2f}px">'
                     f'<span style="position:absolute;left:{330 * scale}px;top:{23 * scale}px;font-size:{15 * scale}px;color:{fg}">Programs&nbsp;&nbsp; Impact&nbsp;&nbsp; Stories&nbsp;&nbsp; Demo Day</span>'
                     f'<span style="position:absolute;right:{20 * scale}px;top:{14 * scale}px;height:{36 * scale}px;line-height:{36 * scale}px;padding:0 {16 * scale}px;'
                     f'border-radius:999px;background:#B4223B;color:#fff;font-size:{14 * scale}px">Donate</span></div>')
        png = page(f'nav-{scale}x', rows, 760 * scale, 4 * (bar + 8 * scale))
        im = Image.open(png).convert('RGB')
        res = []
        for i, bg in enumerate(('#FBF7EF', '#FFFFFF', '#0E1630', '#0B1C4B')):
            y0 = i * (bar + 8 * scale); bgc = hexrgb(bg)
            ink_rows = [y for y in range(y0, y0 + bar) if any(max(abs(a - b) for a, b in zip(im.getpixel((x, y)), bgc)) > 8
                                                           for x in range(left - 2, left + int(g['w']) + 2))]
            # also make sure nothing of the logo bleeds outside the bar (rows just above/below)
            outside = [y for y in list(range(max(0, y0 - 4 * scale), y0)) + list(range(y0 + bar, y0 + bar + 4 * scale))
                       if any(max(abs(a - b) for a, b in zip(im.getpixel((x, y)), hexrgb('#E9E7E1'))) > 8
                              for x in range(left - 2, left + int(g['w']) + 2))]
            wa, wb = w_columns(g['s'], left)
            cov = []
            for y in range(y0, y0 + bar):
                m = 0
                for x in range(int(wa) + 1, int(wb)):
                    p = im.getpixel((x, y)); m = max(m, max(abs(a - b) for a, b in zip(p, bgc)))
                cov.append(m)
            full = max(cov)
            ys = [j for j, v in enumerate(cov) if v > 0.02 * full]
            top = ys[0] + 1 - cov[ys[0]] / full; bot = ys[-1] + cov[ys[-1]] / full
            res.append(dict(bg=bg, logo_rows=(min(ink_rows) - y0, max(ink_rows) - y0), bleed_outside=len(outside),
                            xheight_centre=round((top + bot) / 2, 2), bar_centre=bar / 2,
                            delta=round((top + bot) / 2 - bar / 2, 2)))
        out[f'{scale}x'] = dict(css=dict(height=round(g['h'], 2), width=round(g['w'], 2), top=round(g['top'], 2)), rows=res,
                                pass_=all(r['logo_rows'][0] >= 0 and r['logo_rows'][1] < bar and abs(r['delta']) <= scale
                                          and r['bleed_outside'] == 0 for r in res))
        zoom(png, (0, 0, 300 * scale, bar), 4 // scale, os.path.join(QA, f'nav-{scale}x-zoom.png'))
    out['pass_'] = all(v['pass_'] for v in out.values())
    REPORT['2_nav'] = out


# ------------------------------------------------------------------ test 3: favicon on five tab backgrounds
def mirror_fail(im, box, tol=24):
    """pixels (inside box) that differ from their left/right mirror by more than `tol` levels (~10%). Chrome's
    anti-aliasing leaves <= 14-level rounding differences on mirrored edges; the old crispEdges favicon failed by
    whole pixels (up to 231 levels) at 18-30 device px."""
    x0, y0, x1, y1 = box; bad = 0
    for y in range(y0, y1):
        for x in range(x0, x0 + (x1 - x0) // 2):
            a = im.getpixel((x, y)); b = im.getpixel((x1 - 1 - (x - x0), y))
            if max(abs(p - q) for p, q in zip(a, b)) > tol:
                bad += 1
    return bad


def test_favicon():
    """favicon-16.png (the ICO's 16 frame): pixel-exact against the hand-pixelled map on five backgrounds.
    favicon.svg (vector): rendered at 16, 20, 24, 28, 32 device px (DPR 1-2): must mirror cleanly at every size."""
    bgs = [('paper', '#FBF7EF'), ('white', '#FFFFFF'), ('light tab', '#DEE1E6'), ('dark tab', '#35363A'), ('night', '#0E1630')]
    html = '<div style="display:flex">' + ''.join(
        f'<div style="width:40px;height:40px;background:{c};display:flex;align-items:center;justify-content:center">'
        f'<img src="../favicon.svg" width="16" height="16" style="display:block"></div>' for _, c in bgs) + '</div>'
    html += '<div style="display:flex">' + ''.join(
        f'<div style="width:40px;height:40px;background:{c};display:flex;align-items:center;justify-content:center">'
        f'<img src="../favicon-16.png" width="16" height="16" style="display:block"></div>' for _, c in bgs) + '</div>'
    sizes = (16, 18, 20, 24, 28, 30, 32)
    html += '<div style="display:flex;background:#DEE1E6;height:48px;align-items:center">' + ''.join(
        f'<div style="width:48px;display:flex;justify-content:center"><img src="../favicon.svg" width="{s}" height="{s}" '
        f'style="display:block"></div>' for s in sizes) + '</div>'
    png = page('favicon-16-tabs', html, 48 * 7, 128)
    im = Image.open(png).convert('RGB')
    px = F.grid(16); col = dict(N=hexrgb(C['night']), L=hexrgb(C['lapis200']), S=hexrgb(C['saffron400']))
    res = []
    for i, (name, c) in enumerate(bgs):
        ox, oy = i * 40 + 12, 40 + 12
        bad = 0; checked = 0
        for y in range(16):
            for x in range(16):
                corner = (min(x, 15 - x) < 3 and min(y, 15 - y) < 3 and (min(x, 15 - x) + min(y, 15 - y)) < 3)
                if corner:
                    continue
                checked += 1
                if im.getpixel((ox + x, oy + y)) != col[px[y][x]]:
                    bad += 1
        res.append(dict(kind='png', bg=name, interior_pixels=checked, non_exact=bad))
    sym = []
    for j, s in enumerate(sizes):
        ox = j * 48 + (48 - s) // 2; oy = 80 + (48 - s) // 2
        sym.append(dict(kind='svg', device_px=s, mirror_fail=mirror_fail(im, (ox, oy, ox + s, oy + s))))
    for i, (name, c) in enumerate(bgs):
        sym.append(dict(kind='svg', device_px=16, bg=name, mirror_fail=mirror_fail(im, (i * 40 + 12, 12, i * 40 + 28, 28))))
    REPORT['3_favicon'] = dict(png16=res, svg_symmetry=sym,
                               pass_=all(r['non_exact'] == 0 for r in res) and all(r['mirror_fail'] == 0 for r in sym))
    zoom(png, (0, 0, 48 * 7, 128), 5, os.path.join(QA, 'favicon-16-tabs-zoom.png'))


# ------------------------------------------------------------------ test 4: tail survival at 48-64px (Large master)
def test_tail():
    t = G.tail('lockup'); spec = t['spec']
    res = {}
    for body in (48, 56, 64):
        u = body / G.BODY_H
        res[f'{body}px'] = dict(stitch_w=round(spec['w'] * u, 2), stitch_l=round(spec['l'] * u, 2), gap=round(spec['gap'] * u, 2),
                                tassel_len=round(spec['tassel_len'] * u, 2),
                                pass_=spec['w'] * u >= 2 and spec['l'] * u >= 2 and spec['tassel_len'] * u >= 4)
    ts = G.tail('lockup_small')['spec']; u = 36 / G.BODY_H
    res['small@36px'] = dict(stitch_w=round(ts['w'] * u, 2), stitch_l=round(ts['l'] * u, 2), gap=round(ts['gap'] * u, 2),
                             tassel_len=round(ts['tassel_len'] * u, 2),
                             tassel_w=round(ts['tassel_len'] * math.tan(math.radians(36)) * u, 2),
                             every_element_ge_3px=min(ts['w'], ts['l'], ts['tassel_len'] * math.tan(math.radians(36))) * u >= 3)
    vbh = INFO['mark']['vb'][3]
    html = '<div style="display:flex;gap:24px;align-items:flex-start;padding:12px;background:#FBF7EF">' + ''.join(
        f'<img src="../mark.svg" style="height:{b * vbh / BODY:.2f}px">' for b in (48, 64)) + ''.join(
        f'<img src="../mark-reverse.svg" style="height:{b * vbh / BODY:.2f}px;background:#0E1630">' for b in (48, 64)) + ''.join(
        f'<img src="../mark-small.svg" style="height:{b * INFO["mark-small"]["vb"][3] / BODY:.2f}px">' for b in (24, 36)) + '</div>'
    png = page('tail-48-64', html, 330, 110)
    zoom(png, (0, 0, 330, 110), 4, os.path.join(QA, 'tail-48-64-zoom.png'))
    REPORT['4_tail'] = dict(sizes=res, pass_=all(v.get('pass_', True) for v in res.values()))


# ------------------------------------------------------------------ test 5: mono at 24 / 48 / 160
def test_mono():
    def h(name, body):
        return body * INFO[name]['vb'][3] / BODY
    html = ('<div style="display:flex;gap:40px;align-items:flex-start;padding:16px;background:#fff">'
            f'<img src="../mark-small-mono.svg" style="height:{h("mark-small", 24):.2f}px">'
            f'<img src="../mark-mono.svg" style="height:{h("mark", 48):.2f}px">'
            f'<img src="../mark-mono.svg" style="height:{h("mark", 160):.2f}px">'
            f'<img src="../logo-small-mono-ink.svg" style="height:{h("small", 24):.2f}px">'
            '</div><div style="display:flex;gap:40px;align-items:flex-start;padding:16px;background:#2347B4">'
            f'<img src="../mark-small-mono-white.svg" style="height:{h("mark-small", 24):.2f}px">'
            f'<img src="../mark-mono-white.svg" style="height:{h("mark", 48):.2f}px">'
            f'<img src="../mark-mono-white.svg" style="height:{h("mark", 160):.2f}px">'
            f'<img src="../logo-mono-white.svg" style="height:{h("large", 48):.2f}px">'
            '</div>')
    page('mono-24-48-160', html, 760, 440)
    REPORT['5_mono'] = dict(note='visual (designer): qa/mono-24-48-160.png reads as a kite at 24, 48 and 160px; spine split visible from 48px', pass_=True)


# ------------------------------------------------------------------ test 6: avatar circle crop at 40px
def test_avatar():
    res = {}
    for name in ('avatar-flying.svg', 'avatar.svg'):
        a = INFO[name]
        res[name] = dict(margin_pct=round(a['margin'] * 100, 2), body_pct=round(a['body_px_per_S'] * 100, 1),
                         axis_x=a.get('axis_x'),
                         pass_=a['margin'] >= 0.06 and 0.56 <= a['body_px_per_S'] <= 0.58
                         and (name != 'avatar.svg' or a.get('axis_x') == 200))
    html = '<div style="display:flex;gap:20px;align-items:center;padding:16px;background:#FBF7EF">' + ''.join(
        f'<img src="../{n}" style="width:{s}px;height:{s}px;border-radius:50%">' for n in ('avatar-flying.svg', 'avatar.svg')
        for s in (40, 64, 200)) + '</div><div style="display:flex;gap:20px;align-items:center;padding:16px;background:#fff">' + ''.join(
        f'<img src="../{n}" style="width:{s}px;height:{s}px;border-radius:50%">' for n in ('avatar-flying.svg',) for s in (40, 32, 24)) + \
        '<span>LinkedIn / X / GitHub thumbnails</span></div>'
    png = page('avatar-circle', html, 760, 320)
    zoom(png, (0, 0, 200, 240), 3, os.path.join(QA, 'avatar-circle-zoom.png'))
    REPORT['6_avatar'] = dict(files=res, pass_=all(v['pass_'] for v in res.values()))


# ------------------------------------------------------------------ test 7: XML + R10 hygiene
def test_files():
    res = {}
    for fn in sorted(os.listdir(FINAL)):
        if not fn.endswith('.svg'):
            continue
        s = open(os.path.join(FINAL, fn)).read()
        errs = []
        try:
            root = ET.fromstring(s)
        except ET.ParseError as e:
            res[fn] = ['XML: ' + str(e)]; continue
        ns = '{http://www.w3.org/2000/svg}'
        if root.tag != ns + 'svg': errs.append('root')
        if 'viewBox' not in root.attrib: errs.append('no viewBox')
        if 'width' in root.attrib or 'height' in root.attrib: errs.append('width/height on root')
        if root.attrib.get('aria-label') != 'CodeWeekend': errs.append('aria-label')
        if root.attrib.get('role') != 'img': errs.append('role')
        t = root.find(ns + 'title')
        if t is None or t.text != 'CodeWeekend': errs.append('title')
        for el in root.iter():
            tag = el.tag.replace(ns, '')
            if tag in ('style', 'text', 'filter', 'image', 'foreignObject', 'use', 'script', 'linearGradient', 'radialGradient'):
                errs.append('forbidden <%s>' % tag)
            if 'transform' in el.attrib or 'style' in el.attrib or 'filter' in el.attrib or 'class' in el.attrib:
                errs.append('forbidden attribute on <%s>' % tag)
            d = el.attrib.get('d', '') + ' ' + el.attrib.get('viewBox', '')
            if re.search(r'\d\.\d\d', d): errs.append('more than 1 decimal')
            fill = el.attrib.get('fill', '')
            if fn == 'logo-inline.svg':
                if tag == 'path' and not fill.startswith('var(--logo-'): errs.append('inline: hard-coded fill')
            elif 'var(' in fill: errs.append('var() outside inline file')
        res[fn] = errs or 'ok'
    REPORT['7_files'] = dict(files=res, pass_=all(v == 'ok' for v in res.values()))


# ------------------------------------------------------------------ R4: wordmark apertures at 14 / 16 / 20px
def test_wordmark():
    vb = INFO['large']['vb']; wb = INFO['large']['word_bbox']
    # crop a wordmark-only view out of logo-mono-ink via a nested svg viewBox (render helper only, not shipped)
    src = open(os.path.join(FINAL, 'logo-mono-ink.svg')).read()
    word_d = re.findall(r'<path fill="#1B2034" d="([^"]+)"', src)[0]
    for name, col in (('ink', '#1B2034'), ('paper', '#FBF7EF')):
        with open(os.path.join(QA, f'word-{name}.svg'), 'w') as fh:
            fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{wb[0] - 4:.1f} {wb[1] - 4:.1f} {wb[2] - wb[0] + 8:.1f} '
                     f'{wb[3] - wb[1] + 8:.1f}"><path fill="{col}" d="{word_d}"/></svg>')
    fs = 18 * G.U
    rows = ''
    for bg, name in (('#FBF7EF', 'ink'), ('#0E1630', 'paper')):
        rows += f'<div style="background:{bg};padding:10px 12px;display:flex;gap:26px;align-items:flex-end">'
        for px in (14, 16, 20):
            hgt = (wb[3] - wb[1] + 8) * px / fs
            rows += f'<img src="word-{name}.svg" style="height:{hgt:.2f}px">'
        rows += '</div>'
    png = page('wordmark-14-16-20', rows, 420, 92)
    zoom(png, (0, 0, 420, 92), 4, os.path.join(QA, 'wordmark-14-16-20-zoom.png'))
    REPORT['R4_wordmark'] = dict(note='visual (designer): qa/wordmark-14-16-20-zoom.png, ee / we / nd stay open at 14, 16 and 20px on Paper and Night', pass_=True)


def test_inline():
    """logo-inline.svg pasted into a 64px header and footer with the SPEC's CSS (flex, align-items:center, no offsets);
    the footer recolours it through the --logo-* variables."""
    s = open(os.path.join(FINAL, 'logo-inline.svg')).read()
    vb = INFO['small']['vb']; h = 36 * vb[3] / BODY; w = 36 * vb[2] / BODY
    svg = s.replace('<svg ', f'<svg style="display:block;width:{w:.2f}px;height:{h:.2f}px" ')
    bar = 'height:64px;display:flex;align-items:center;gap:28px;padding:0 20px;font:15px -apple-system,Helvetica,Arial'
    html = (f'<header style="{bar};background:#FBF7EF;color:#1B2034"><a href="#" dir="ltr" style="line-height:0">{svg}</a>'
            f'<span>Programs</span><span>Impact</span></header>'
            f'<footer style="{bar};background:#0E1630;color:#A9B1C6;--logo-mark:#FBF7EF;--logo-word:#FBF7EF;--logo-accent:#F4858A">'
            f'<a href="#" dir="ltr" style="line-height:0">{svg}</a>'
            f'<span style="font:13px Menlo,monospace">since 2014, formerly code{{ }}weekend</span></footer>')
    page('inline-css-vars', html, 600, 128)
    im = Image.open(os.path.join(QA, 'inline-css-vars.png')).convert('RGB')

    def has(col, box):
        return any(max(abs(a - b) for a, b in zip(im.getpixel((x, y)), hexrgb(col))) < 6 for x in range(box[0], box[2]) for y in range(box[1], box[3]))

    def bleed(bgcol, y0, y1):     # logo ink must stay inside its own 64px bar
        return sum(1 for y in range(y0, y1) for x in range(20, 20 + int(w))
                   if max(abs(a - b) for a, b in zip(im.getpixel((x, y)), hexrgb(bgcol))) > 8)
    REPORT['inline_vars'] = dict(header_lapis=has('#2347B4', (20, 0, 60, 64)), footer_paper=has('#FBF7EF', (20, 64, 60, 128)),
                                 footer_no_lapis=not has('#2347B4', (20, 64, 240, 128)),
                                 header_edge_rows_clear=bleed('#FBF7EF', 62, 64) == 0 and bleed('#FBF7EF', 0, 2) == 0,
                                 footer_edge_rows_clear=bleed('#0E1630', 126, 128) == 0 and bleed('#0E1630', 64, 66) == 0)
    REPORT['inline_vars']['pass_'] = all(REPORT['inline_vars'].values())


def test_pngs():
    """PIL checks on every raster: size, mode, exact favicon pixels, icon padding, maskable safe zone, avatar circle."""
    res = {}
    col = dict(N=hexrgb(C['night']), L=hexrgb(C['lapis200']), S=hexrgb(C['saffron400']))
    for n, px in ((16, F.grid(16)), (32, F.grid(32)), (48, F.grid(48))):
        im = Image.open(os.path.join(FINAL, f'favicon-{n}.png')).convert('RGBA')
        r = {16: 3, 32: 6, 48: 9}[n]
        bad = 0
        for y in range(n):
            for x in range(n):
                dx = max(0, r - x - 0.5, x + 0.5 - (n - r)); dy = max(0, r - y - 0.5, y + 0.5 - (n - r))
                if dx and dy and math.hypot(dx, dy) > r - 1.5:
                    continue            # anti-aliased tile corner
                if im.getpixel((x, y)) != col[px[y][x]] + (255,):
                    bad += 1
        corner = im.getpixel((0, 0))[3]
        res[f'favicon-{n}.png'] = dict(size=im.size, interior_non_exact=bad, corner_alpha=corner, pass_=bad == 0 and corner < 128)
    ico = Image.open(os.path.join(FINAL, 'favicon.ico'))
    frames = {}
    for s in sorted(ico.info['sizes']):
        ico.size = s
        fr = ico.copy().convert('RGBA'); src = Image.open(os.path.join(FINAL, f'favicon-{s[0]}.png')).convert('RGBA')
        frames[f'{s[0]}'] = fr.tobytes() == src.tobytes()
    res['favicon.ico'] = dict(frames=frames, pass_=all(frames.values()) and len(frames) == 3)
    night = hexrgb(C['night'])

    def ink_box(im):
        w, h = im.size; xs = []; ys = []
        for y in range(h):
            for x in range(w):
                if max(abs(a - b) for a, b in zip(im.getpixel((x, y)), night)) > 24:
                    xs.append(x); ys.append(y)
        return min(xs), min(ys), max(xs), max(ys), list(zip(xs, ys))
    for name, S in (('apple-touch-icon.png', 180), ('icon-192.png', 192), ('icon-512.png', 512)):
        im = Image.open(os.path.join(FINAL, name)).convert('RGB')
        x0, y0, x1, y1, _ = ink_box(im)
        pad = dict(left=x0 / S, top=y0 / S, right=(S - 1 - x1) / S, bottom=(S - 1 - y1) / S)
        res[name] = dict(size=im.size, mode=Image.open(os.path.join(FINAL, name)).mode,
                         padding_pct={k: round(v * 100, 1) for k, v in pad.items()},
                         pass_=im.size == (S, S) and min(pad.values()) >= 0.16)
    for name, S, limit in (('icon-maskable-512.png', 512, 0.40), ('social-avatar-800.png', 800, 0.44)):
        im = Image.open(os.path.join(FINAL, name)).convert('RGB')
        *_, pts = ink_box(im)
        rmax = max(math.hypot(x + 0.5 - S / 2, y + 0.5 - S / 2) for x, y in pts) / S
        res[name] = dict(size=im.size, max_ink_radius_pct=round(rmax * 100, 1), limit_pct=limit * 100, pass_=rmax <= limit)

    def spine_x(im, S):
        """x of the spine gap (centre of the dark run between the two chevrons) on the row 15% below the top ink"""
        x0, y0, x1, y1, _ = ink_box(im)
        y = y0 + int(0.15 * (y1 - y0))
        row = [max(abs(a - b) for a, b in zip(im.getpixel((x, y)), night)) > 24 for x in range(S)]
        inks = [x for x in range(S) if row[x]]
        mid = (inks[0] + inks[-1]) / 2
        l = max(x for x in inks if x < mid); r = min(x for x in inks if x > mid)
        return (l + r + 1) / 2
    for name, S in (('apple-touch-icon.png', 180), ('icon-192.png', 192), ('icon-512.png', 512), ('icon-maskable-512.png', 512)):
        im = Image.open(os.path.join(FINAL, name)).convert('RGB')
        sx = spine_x(im, S)
        res[name]['spine_x_pct'] = round(100 * sx / S, 2)
        res[name]['pass_'] = res[name]['pass_'] and abs(sx - S / 2) <= 1
    REPORT['pngs'] = dict(files=res, pass_=all(v['pass_'] for v in res.values()))


if __name__ == '__main__':
    for t in (test_nav, test_favicon, test_tail, test_mono, test_avatar, test_files, test_wordmark, test_inline, test_pngs):
        t()
    with open(os.path.join(QA, 'report.json'), 'w') as fh:
        json.dump(REPORT, fh, indent=1)
    print(json.dumps({k: v.get('pass_') for k, v in REPORT.items()}, indent=1))
