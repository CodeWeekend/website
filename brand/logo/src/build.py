#!/usr/bin/env python3
"""CodeWeekend logo kit: ONE script builds every production file in brand/final/ (R10).

    python3 build.py            # SVGs + PNGs + ICO + construction.png + sheet.png
    python3 build.py --qa       # ... then acceptance tests (qa.py -> qa/report.json) and the judges' renders
    python3 build.py --svg      # SVGs only (fast)

Geometry and the outlined wordmark live in geom.py, the hand-pixelled favicon grids in favgrid.py.
PNGs are rendered with tools/render.sh (headless Chrome) from exact-size HTML wrappers and verified with PIL.
"""
import math, os, sys, json, subprocess, shutil
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import geom as G
import favgrid as F

FINAL = os.path.dirname(HERE)
SP = os.path.abspath(os.path.join(FINAL, '..'))   # brand/ — holds tools/render.sh and tools/sheet-template.html
RENDER = os.path.join(SP, 'tools', 'render.sh')
TMP = os.path.join(HERE, 'tmp')
C = G.C
U = G.U
PAD = 1.0 * U          # tight, even padding round every lockup / mark (1u)
TITLE = 'CodeWeekend'
fmt = G.fmt


# ------------------------------------------------------------------ parts
def parts(master='large', tail='lockup', tf=None):
    """master: 'large' (spine split through the panel, R2) or 'small' (solid panel).
    tail: 'lockup' | 'lockup_small' | 'full' | None.   tf: optional point transform (avatar tilt, placement)."""
    k = G.kite()
    tf = tf or (lambda pts: pts)
    out = dict(body=[tf(k['left']), tf(k['right'])], stitches=[], tassel=[],
               panel=[tf(h) for h in k['panel_split']] if master == 'large' else [tf(k['panel'])])
    if tail:
        t = G.tail(tail)
        out['stitches'] = [tf(s) for s in t['stitches']]
        out['tassel'] = [tf(t['tassel'])]
    return out


def all_pts(p):
    return [q for key in ('body', 'stitches', 'panel', 'tassel') for poly in p[key] for q in poly]


def bbox(pts):
    xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    return min(xs), min(ys), max(xs), max(ys)


def d_of(polys):
    return ''.join(G.poly_d(pl) for pl in polys)


def layers(p, way, word_d=None, inline=False):
    """Paths in paint order. Same-colour roles are merged into one path."""
    col = G.WAYS[way] if isinstance(way, str) else way
    if inline:
        fills = dict(body=f'var(--logo-mark, {G.WAYS["light"]["body"]})', panel=f'var(--logo-panel, {G.WAYS["light"]["panel"]})',
                     tassel=f'var(--logo-accent, {G.WAYS["light"]["tassel"]})', word=f'var(--logo-word, {G.WAYS["light"]["word"]})')
    else:
        fills = col
    out = [(fills['body'], d_of(p['body']) + d_of(p['stitches'])), (fills['panel'], d_of(p['panel']))]
    if p['tassel']:
        out.append((fills['tassel'], d_of(p['tassel'])))
    if word_d:
        out.append((fills['word'], word_d))
    if not inline:   # merge identical fills (mono): fewer nodes, identical rendering (no overlaps)
        merged = []
        for f, d in out:
            if merged and merged[-1][0] == f:
                merged[-1] = (f, merged[-1][1] + d)
            else:
                merged.append((f, d))
        out = merged
    return out


def svg_doc(vb, paths, extra_attrs='', ground=None):
    x, y, w, h = vb
    vbs = f'{fmt(x)} {fmt(y)} {fmt(w)} {fmt(h)}'
    body = ''
    if ground:
        body += f'<path fill="{ground}" d="M{fmt(x)} {fmt(y)}h{fmt(w)}v{fmt(h)}h-{fmt(w)}Z"/>'
    body += ''.join(f'<path fill="{f}" d="{d}"/>' for f, d in paths)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vbs}"{extra_attrs} role="img" aria-label="{TITLE}">'
            f'<title>{TITLE}</title>{body}</svg>\n')


def write(name, s):
    path = os.path.join(FINAL, name)
    with open(path, 'w') as fh:
        fh.write(s)
    return path


def tight_vb(pts, pad=PAD):
    x0, y0, x1, y1 = bbox(pts)
    # snap outward to 0.1 so the padding stays even after 1-decimal rounding
    x0 = math.floor((x0 - pad) * 10) / 10; y0 = math.floor((y0 - pad) * 10) / 10
    x1 = math.ceil((x1 + pad) * 10) / 10; y1 = math.ceil((y1 + pad) * 10) / 10
    return (x0, y0, round(x1 - x0, 1), round(y1 - y0, 1))


# ------------------------------------------------------------------ lockups
def horizontal(master='large'):
    """R5 horizontal: wordmark 18u, x-height centred on the panel axis y = 10.5u, gap 1.3 x stroke from the right
    side vertex to the first ink, plus the lockup tail (Small master: lockup_small tail, solid panel)."""
    p = parts(master, 'lockup' if master == 'large' else 'lockup_small')
    size = G.WORD_SIZE * U
    xh = 528 / 1000 * size
    base = G.PANEL_Y * U + xh / 2
    wm = G.wordmark(24 * U + G.WORD_GAP * G.STROKE * U, base, size)
    pts = all_pts(p) + [(wm['bbox'][0], wm['bbox'][1]), (wm['bbox'][2], wm['bbox'][3])]
    vb = tight_vb(pts)
    if master == 'small':
        vb = axis_vb(vb)
    return p, wm, vb


def axis_vb(vb):
    """Nav / embed files (Small master): extend the top of the box so it is symmetric about the panel axis, which
    is also the wordmark's x-height centre. Plain centring (flex align-items:center, CMS headers, logo walls) then
    puts the wordmark on the slot's centre line; the tail hangs below it, as a kite does. Left, right and bottom
    padding stay 1u."""
    x, y, w, h = vb
    axis = G.PANEL_Y * U
    half = (y + h) - axis
    top = math.floor((axis - half) * 10) / 10
    return (x, top, w, round((y + h) - top, 1))


def stacked():
    """R5 stacked: kite centred over the wordmark (wordmark ink width = 3.4 x kite width), gap 2 x stroke from the
    chevron tips to the ascender line; Large master with the lockup tail."""
    p = parts('large', 'lockup')
    probe = G.wordmark(0, 0, 1000)
    size = 1000 * (3.4 * 24 * U) / (probe['bbox'][2] - probe['bbox'][0])
    asc = 712 / 1000 * size
    base = G.TIP_Y * U + 2 * G.STROKE * U + asc
    wm = G.wordmark(0, base, size)
    ww = wm['bbox'][2] - wm['bbox'][0]
    dx = ww / 2 - 12 * U            # move the kite so its axis sits on the wordmark's ink centre
    tf = lambda pts: [(x + dx, y) for x, y in pts]
    p = parts('large', 'lockup', tf)
    pts = all_pts(p) + [(wm['bbox'][0], wm['bbox'][1]), (wm['bbox'][2], wm['bbox'][3])]
    return p, wm, tight_vb(pts), dict(dx=dx, size=size, base=base, asc_line=base - asc)


def mark(master='large', tail='lockup'):
    p = parts(master, tail)
    return p, tight_vb(all_pts(p))


def mark_square(way):
    """R7: square slot. Body (outer kite, 25.24u) = 64% of the side; body centre 46% from the top; lockup tail."""
    p = parts('large', 'lockup')
    S = G.BODY_H * U / 0.64
    cy = G.BODY_H * U / 2
    vb = (12 * U - S / 2, cy - 0.46 * S, S, S)
    vb = tuple(round(v, 1) for v in vb)
    assert bbox(all_pts(p))[3] < vb[1] + vb[3] - U, 'tail must stay inside the square'
    return p, vb


def mec(pts, iters=20000):
    """Approximate minimum enclosing circle (Badoiu-Clarkson)."""
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    for i in range(1, iters):
        far = max(pts, key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2)
        cx += (far[0] - cx) / (i + 1); cy += (far[1] - cy) / (i + 1)
    r = max(math.hypot(p[0] - cx, p[1] - cy) for p in pts)
    return cx, cy, r


def placed_axis(master, tail, S, body_frac=None, fit_r=None):
    """Upright kite with its body axis (x = 12u) on the vertical centre line of an S x S square. The vertical position
    minimises the radius of the circle (centred on the square) that holds body + tail; the tail stays inside the
    body's footprint (x >= 2.4u), so this costs little scale. Scale: body height = body_frac * S, or that radius =
    fit_r * S."""
    base = parts(master, tail)
    pts = all_pts(base)
    cx = 12 * U
    lo, hi = min(p[1] for p in pts), max(p[1] for p in pts)
    best = None
    for i in range(2001):
        cy = lo + (hi - lo) * i / 2000
        r = max(math.hypot(p[0] - cx, p[1] - cy) for p in pts)
        if best is None or r < best[1]:
            best = (cy, r)
    cy, r = best
    s = body_frac * S / (G.BODY_H * U) if body_frac else fit_r * S / r
    tf = lambda pts: [((x - cx) * s + S / 2, (y - cy) * s + S / 2) for x, y in pts]
    p = parts(master, tail, tf)
    return p, dict(scale=s, r=r * s, margin=(S / 2 - r * s) / S, body_px_per_S=G.BODY_H * U * s / S, axis_x=S / 2)


def placed(tail, tilt, S, body_frac=None, fit_r=None, ground_way='reverse', master='large'):
    """Place the kite in an S x S square, rotation baked into the coordinates (no transform attribute).
    Scale: body height = body_frac * S, or the enclosing circle radius = fit_r * S. Centred on the enclosing circle."""
    base = parts(master, tail)
    a = math.radians(tilt)
    rot = lambda pts: [(x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    pts = rot(all_pts(base))
    cx, cy, r = mec(pts)
    s = body_frac * S / (G.BODY_H * U) if body_frac else fit_r * S / r
    tf = lambda pts: [((x - cx) * s + S / 2, (y - cy) * s + S / 2) for x, y in rot(pts)]
    p = parts(master, tail, tf)
    return p, dict(scale=s, r=r * s, margin=(S / 2 - r * s) / S, body_px_per_S=G.BODY_H * U * s / S)


# ------------------------------------------------------------------ favicon SVGs
def favicon_svg(mono=False):
    """favicon.svg / mask-icon.svg: the vector drawing (favgrid.vector), no shape-rendering hint, so it rasterises
    natively and symmetrically at every DPR. mask-icon: one colour, no tile (Safari fills it with `color`)."""
    v = F.vector()
    ring = G.poly_d(v['left']) + G.poly_d(v['right']); core = G.poly_d(v['core'])
    n = F.TILE
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" role="img" aria-label="{TITLE}">'
            f'<title>{TITLE}</title>')
    if mono:
        return head + f'<path fill="#000000" d="{ring}{core}"/></svg>\n'
    return (head + f'<path fill="{C["night"]}" d="{F.tile_d()}"/><path fill="{C["lapis200"]}" d="{ring}"/>'
            f'<path fill="{C["saffron400"]}" d="{core}"/></svg>\n')


def frame_svg(px, n, radius):
    """Render source for a hand-pixelled frame (src/favicon-N.svg, not public): pixel runs, drawn 1:1 only."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" shape-rendering="crispEdges" role="img" '
            f'aria-label="{TITLE}"><title>{TITLE}</title>'
            f'<rect width="{n}" height="{n}" rx="{radius}" fill="{C["night"]}" shape-rendering="geometricPrecision"/>'
            f'<path fill="{C["lapis200"]}" d="{F.runs_d(px, "L")}"/><path fill="{C["saffron400"]}" d="{F.runs_d(px, "S")}"/></svg>\n')


# ------------------------------------------------------------------ rendering helpers
def render(html_or_svg, out, w, h):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    r = subprocess.run([RENDER, html_or_svg, out, str(w), str(h)], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)
    im = Image.open(out)
    assert im.size == (w, h), (out, im.size)
    return out


def wrap_html(name, src, w, h, bg):
    os.makedirs(TMP, exist_ok=True)
    path = os.path.join(TMP, name + '.html')
    rel = os.path.relpath(src, TMP)
    with open(path, 'w') as fh:
        fh.write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;padding:0;background:{bg};'
                 f'width:{w}px;height:{h}px;overflow:hidden}}img{{display:block;width:{w}px;height:{h}px}}</style></head>'
                 f'<body><img src="{rel}"></body></html>')
    return path


def png_opaque(src_svg, out, w, h, bg):
    render(wrap_html(os.path.basename(out), src_svg, w, h, bg), out, w, h)
    Image.open(out).convert('RGB').save(out, optimize=True)
    return out


def png_transparent(src_svg, out, w, h):
    """Difference matting: render on black and on white; alpha = 1 - (white - black) / 255."""
    b = render(wrap_html('b_' + os.path.basename(out), src_svg, w, h, '#000'), os.path.join(TMP, 'b_' + os.path.basename(out)), w, h)
    wh = render(wrap_html('w_' + os.path.basename(out), src_svg, w, h, '#fff'), os.path.join(TMP, 'w_' + os.path.basename(out)), w, h)
    B = Image.open(b).convert('RGB'); W = Image.open(wh).convert('RGB')
    o = Image.new('RGBA', (w, h))
    for y in range(h):
        for x in range(w):
            pb = B.getpixel((x, y)); pw = W.getpixel((x, y))
            a = 255 - max(0, min(255, round(sum(pw[i] - pb[i] for i in range(3)) / 3)))
            if a == 0:
                o.putpixel((x, y), (0, 0, 0, 0))
            else:
                o.putpixel((x, y), tuple(max(0, min(255, round(pb[i] * 255 / a))) for i in range(3)) + (a,))
    o.save(out, optimize=True)
    return out


# ------------------------------------------------------------------ build
def build_svgs():
    files = {}
    # --- horizontal lockups: Large (body >= 48px) and Small (nav, body 20-47px)
    info = {}
    for master, prefix in (('large', 'logo'), ('small', 'logo-small')):
        p, wm, vb = horizontal(master)
        info[master] = dict(vb=vb, base=wm['base'], xh=wm['xh'], word_bbox=wm['bbox'])
        for way, suffix in (('light', ''), ('reverse', '-reverse'), ('mono-ink', '-mono-ink'), ('mono-white', '-mono-white')):
            files[f'{prefix}{suffix}.svg'] = svg_doc(vb, layers(p, way, wm['d']))
        if master == 'small':
            files['logo-inline.svg'] = svg_doc(vb, layers(p, 'light', wm['d'], inline=True))
    # --- stacked
    p, wm, vb, st = stacked()
    info['stacked'] = dict(vb=vb, **st)
    for way, suffix in (('light', ''), ('reverse', '-reverse'), ('mono-ink', '-mono-ink'), ('mono-white', '-mono-white')):
        files[f'logo-stacked{suffix}.svg'] = svg_doc(vb, layers(p, way, wm['d']))
    # --- marks
    p, vb = mark('large', 'lockup'); info['mark'] = dict(vb=vb)
    files['mark.svg'] = svg_doc(vb, layers(p, 'light'))
    files['mark-reverse.svg'] = svg_doc(vb, layers(p, 'reverse'))
    files['mark-mono.svg'] = svg_doc(vb, layers(p, 'mono-ink'))
    files['mark-mono-white.svg'] = svg_doc(vb, layers(p, 'mono-white'))
    p, vb = mark('small', 'lockup_small'); info['mark-small'] = dict(vb=vb)
    files['mark-small.svg'] = svg_doc(vb, layers(p, 'light'))
    files['mark-small-reverse.svg'] = svg_doc(vb, layers(p, 'reverse'))
    files['mark-small-mono.svg'] = svg_doc(vb, layers(p, 'mono-ink'))
    files['mark-small-mono-white.svg'] = svg_doc(vb, layers(p, 'mono-white'))
    p, vb = mark('large', 'full'); info['mark-full'] = dict(vb=vb)
    files['mark-full.svg'] = svg_doc(vb, layers(p, 'light'))
    files['mark-full-reverse.svg'] = svg_doc(vb, layers(p, 'reverse'))
    files['mark-full-mono.svg'] = svg_doc(vb, layers(p, 'mono-ink'))
    p, vb = mark_square('light'); info['mark-square'] = dict(vb=vb)
    files['mark-square.svg'] = svg_doc(vb, layers(p, 'light'))
    files['mark-square-reverse.svg'] = svg_doc(vb, layers(p, 'reverse'))
    # --- avatars (R8): Night ground, full tail, body 57% of the side, inside the inscribed circle.
    # Avatars display at 24-48px (body 14-27px: Small-master range), so they use the Small master's SOLID panel;
    # the Large master's 1u split turns into a brown streak there. The upright one keeps its body axis on x = 200.
    S = 400
    p, a = placed('full', 8, S, body_frac=0.57, master='small')
    info['avatar-flying.svg'] = a
    files['avatar-flying.svg'] = svg_doc((0, 0, S, S), layers(p, 'reverse'), ground=C['night'])
    p, a = placed_axis('small', 'full', S, body_frac=0.57)
    info['avatar.svg'] = a
    files['avatar.svg'] = svg_doc((0, 0, S, S), layers(p, 'reverse'), ground=C['night'])
    # --- favicon family
    files['favicon.svg'] = favicon_svg()
    files['mask-icon.svg'] = favicon_svg(mono=True)
    for name, s in files.items():
        write(name, s)
    # pattern source only (not public): tail-less kite for repeat patterns / Her Kite tiles
    os.makedirs(os.path.join(HERE, 'pattern'), exist_ok=True)
    p, vb = mark('large', None)
    with open(os.path.join(HERE, 'pattern', 'kite-notail.svg'), 'w') as fh:
        fh.write(svg_doc(vb, layers(p, 'light')))
    p, vb = mark('small', None)
    with open(os.path.join(HERE, 'pattern', 'kite-notail-small.svg'), 'w') as fh:
        fh.write(svg_doc(vb, layers(p, 'light')))
    # hand-pixelled 16 / 32 / 48 frames (PNG + ICO render sources, not public)
    for n, r in ((16, 3), (32, 6), (48, 9)):
        with open(os.path.join(HERE, f'favicon-{n}.svg'), 'w') as fh:
            fh.write(frame_svg(F.grid(n), n, r))
    with open(os.path.join(HERE, 'build-info.json'), 'w') as fh:
        json.dump(info, fh, indent=1, default=lambda o: list(o) if isinstance(o, tuple) else str(o))
    return files, info


def icon_svg(S, content_frac, name, fit='bbox'):
    """Opaque Night app icon: Large master + lockup tail, reverse colours.
    fit='bbox': ink bbox fills `content_frac` of the side, centred (apple-touch / icon-192 / icon-512)
    fit='circle': the enclosing circle has radius content_frac * S (maskable safe zone)."""
    if fit == 'bbox':
        base = parts('large', 'lockup')
        x0, y0, x1, y1 = bbox(all_pts(base))
        s = content_frac * S / max(x1 - x0, y1 - y0)
        tf = lambda pts: [((x - (x0 + x1) / 2) * s + S / 2, (y - (y0 + y1) / 2) * s + S / 2) for x, y in pts]
        p = parts('large', 'lockup', tf); meta = dict(scale=s, body_px=G.BODY_H * U * s * 1.0)
    else:
        p, meta = placed_axis('large', 'lockup', S, fit_r=content_frac)
    path = os.path.join(HERE, name)
    with open(path, 'w') as fh:
        fh.write(svg_doc((0, 0, S, S), layers(p, 'reverse'), ground=C['night']))
    return path, meta


def build_pngs(info):
    out = {}
    # favicons: the hand-pixelled 16 / 32 / 48 frames; transparent outside the rounded tile
    png_transparent(os.path.join(HERE, 'favicon-16.svg'), os.path.join(FINAL, 'favicon-16.png'), 16, 16)
    png_transparent(os.path.join(HERE, 'favicon-32.svg'), os.path.join(FINAL, 'favicon-32.png'), 32, 32)
    png_transparent(os.path.join(HERE, 'favicon-48.svg'), os.path.join(FINAL, 'favicon-48.png'), 48, 48)
    ims = [Image.open(os.path.join(FINAL, f'favicon-{n}.png')).convert('RGBA') for n in (16, 32, 48)]
    ims[2].save(os.path.join(FINAL, 'favicon.ico'), format='ICO', sizes=[(16, 16), (32, 32), (48, 48)],
                append_images=ims[:2])
    # app icons: 18% padding -> content 64% of the side
    src, meta = icon_svg(180, 0.64, 'icon-180.svg'); out['apple-touch-icon'] = meta
    png_opaque(src, os.path.join(FINAL, 'apple-touch-icon.png'), 180, 180, C['night'])
    src, meta = icon_svg(192, 0.64, 'icon-192.svg'); out['icon-192'] = meta
    png_opaque(src, os.path.join(FINAL, 'icon-192.png'), 192, 192, C['night'])
    src, meta = icon_svg(512, 0.64, 'icon-512.svg'); out['icon-512'] = meta
    png_opaque(src, os.path.join(FINAL, 'icon-512.png'), 512, 512, C['night'])
    # maskable: body axis on x = 256; whole kite + tail inside a centred circle of radius 0.36 S (safe zone 0.40 S)
    src, meta = icon_svg(512, 0.36, 'icon-maskable-512.svg', fit='circle'); out['icon-maskable-512'] = meta
    png_opaque(src, os.path.join(FINAL, 'icon-maskable-512.png'), 512, 512, C['night'])
    shutil.copyfile(os.path.join(FINAL, 'icon-maskable-512.png'), os.path.join(FINAL, 'icon-512-maskable.png'))
    # social avatar
    png_opaque(os.path.join(FINAL, 'avatar-flying.svg'), os.path.join(FINAL, 'social-avatar-800.png'), 800, 800, C['night'])
    png_opaque(os.path.join(FINAL, 'avatar.svg'), os.path.join(HERE, 'avatar-upright-800.png'), 800, 800, C['night'])
    with open(os.path.join(HERE, 'icon-info.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    return out


def build_sheet():
    """Standard contact sheet: tools/sheet-template.html with the brand vars set (see the comment in sheet.html)."""
    s = open(os.path.join(SP, 'tools', 'sheet-template.html')).read()
    rep = [
        (":root{ --paper:#FAF7F0; --dark:#0B1D3A; --ink:#14213D; --muted:#6B7280; }",
         f":root{{ --paper:{C['paper']}; --dark:{C['night']}; --ink:{C['ink']}; --muted:#5F584C; }}"),
        ("<h1>CONCEPT NAME <small>one-line idea</small></h1>",
         "<h1>CodeWeekend · Gudiparan, the Bracket Kite <small>Two code brackets, &lt; and &gt;, make an Afghan kite. "
         "Learners build it; the community holds the string. (production kit)</small></h1>"),
        ('<img src="logo-mono.svg" style="height:80px">', '<img src="logo-mono-ink.svg" style="height:80px">'),
        ('.nav img{height:30px;width:auto}', '.nav img{height:%.2fpx;width:auto}'),
        ('<div class="nav"><img src="logo.svg">', '<div class="nav"><img src="logo-small.svg">'),
        ('.avatar img{width:76px;height:76px}', '.avatar img{width:120px;height:120px}'),
        ('<div class="avatar"><img src="mark-reverse.svg"></div>', '<div class="avatar"><img src="avatar-flying.svg"></div>'),
        ('body{width:1600px;height:1100px;', 'body{width:1600px;height:1140px;'),
    ]
    info = json.load(open(os.path.join(HERE, 'build-info.json')))
    vb = info['small']['vb']; sc = 36 / (G.BODY_H * U)
    h = vb[3] * sc                    # 36px body; the box is symmetric about the panel axis, so flex centring works
    for a, b in rep:
        assert a in s, a
        s = s.replace(a, b % h if '%.2f' in b else b)
    s = s.replace(s[s.index('<!-- Standard'):s.index('-->') + 3],
                  '<!-- Standard contact sheet (tools/sheet-template.html) for the production kit, built by src/build.py.\n'
                  '     Changes from the template: logo-mono.svg -> logo-mono-ink.svg; the nav shows the Small master\n'
                  '     (logo-small.svg, plain align-items:center) at its documented size (36px body); the avatar\n'
                  '     circle shows the shipped avatar-flying.svg; height 1140 so the nav card is not cropped.\n'
                  '     mark.svg has a tight non-square viewBox (R7), so it letterboxes inside the 160 / 64 boxes. -->')
    with open(os.path.join(FINAL, 'sheet.html'), 'w') as fh:
        fh.write(s)
    render(os.path.join(FINAL, 'sheet.html'), os.path.join(FINAL, 'sheet.png'), 1600, 1140)


def build_construction():
    import construct
    html, W, H = construct.html()
    with open(os.path.join(FINAL, 'construction.html'), 'w') as fh:
        fh.write(html)
    render(os.path.join(FINAL, 'construction.html'), os.path.join(FINAL, 'construction.png'), W, H)


if __name__ == '__main__':
    files, info = build_svgs()
    print('svg:', len(files))
    if '--svg' in sys.argv:
        sys.exit()
    print(build_pngs(info))
    build_construction()
    build_sheet()
    shutil.rmtree(TMP, ignore_errors=True)
    if '--qa' in sys.argv:          # acceptance tests 2-7
        subprocess.run([sys.executable, os.path.join(HERE, 'qa.py')], check=True)
