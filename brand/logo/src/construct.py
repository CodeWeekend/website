"""construction.html -> construction.png: grid and geometry of the Bracket Kite (documentation image, not a logo file)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import geom as G
import favgrid as F

C = G.C
INK, POM, STONE = C['ink'], C['pom600'], '#5F584C'
GRID_MIN, GRID_MAJ = '#EDE5D7', '#D9CFBE'
FONT = "'Atkinson Hyperlegible Mono', ui-monospace, Menlo, monospace"


def P(pts, s, ox, oy):
    return [(ox + x / G.U * s, oy + y / G.U * s) for x, y in pts]


def poly(pts, fill, extra=''):
    return f'<path fill="{fill}" {extra} d="M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + 'Z"/>'


def line(a, b, col=INK, w=1.0, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="{col}" stroke-width="{w}"{da}/>'


def text(x, y, s, size=12, col=INK, anchor='start', weight=500):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{col}" '
            f'text-anchor="{anchor}">{s}</text>')


def dim(a, b, col=POM):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * 4, dx / L * 4
    return (line(a, b, col, 1.2) + line((a[0] - nx, a[1] - ny), (a[0] + nx, a[1] + ny), col, 1.2)
            + line((b[0] - nx, b[1] - ny), (b[0] + nx, b[1] + ny), col, 1.2))


def arc(c, r, a0, a1, col=POM):
    p0 = (c[0] + r * math.cos(math.radians(a0)), c[1] + r * math.sin(math.radians(a0)))
    p1 = (c[0] + r * math.cos(math.radians(a1)), c[1] + r * math.sin(math.radians(a1)))
    return (f'<path fill="none" stroke="{col}" stroke-width="1.2" d="M{p0[0]:.2f} {p0[1]:.2f}A{r} {r} 0 0 '
            f'{1 if a1 > a0 else 0} {p1[0]:.2f} {p1[1]:.2f}"/>')


def badge(x, y, n):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{POM}"/>'
            + text(x, y + 4, str(n), 11, '#FFFFFF', 'middle', 700))


def symbol_panel():
    s = 18.0                                  # px per u
    k = G.kite(); t = G.tail('lockup')
    cs = 2 * G.STROKE; top_ink = k['top_o']
    ox = 70 + cs * s                          # x of u = 0
    oy = 140 + (cs - top_ink) * s             # y of u = 0
    X = lambda u: ox + u * s
    Y = lambda u: oy + u * s
    out = []
    bx0, by0, bx1, by1 = X(-cs), Y(top_ink - cs), X(24 + cs), Y(G.TIP_Y + cs)
    # grid inside the clear-space box
    u = math.ceil(-cs)
    while X(u) <= bx1:
        out.append(line((X(u), by0), (X(u), by1), GRID_MAJ if u % 4 == 0 else GRID_MIN)); u += 1
    v = math.ceil(top_ink - cs)
    while Y(v) <= by1:
        out.append(line((bx0, Y(v)), (bx1, Y(v)), GRID_MAJ if v % 4 == 0 else GRID_MIN)); v += 1
    out.append(f'<rect x="{bx0:.1f}" y="{by0:.1f}" width="{bx1 - bx0:.1f}" height="{by1 - by0:.1f}" fill="none" '
               f'stroke="{POM}" stroke-width="1.4" stroke-dasharray="7 5"/>')
    # construction polygon + axes
    outer = [(12, 0), (24, G.H_TOP), (12, G.BODY_H), (0, G.H_TOP)]
    out.append(poly([(X(a), Y(b)) for a, b in outer], 'none', f'stroke="{INK}" stroke-width="1" stroke-dasharray="3 4"'))
    out.append(line((X(12), by0), (X(12), by1), POM, 0.8, '2 3'))
    out.append(line((bx0, Y(G.PANEL_Y)), (bx1, Y(G.PANEL_Y)), INK, 1, '8 4'))
    out.append(line((bx0, Y(G.TIP_Y)), (bx1, Y(G.TIP_Y)), INK, 1, '8 4'))
    # artwork
    out.append(poly(P(k['left'], s, ox, oy), C['lapis600'])); out.append(poly(P(k['right'], s, ox, oy), C['lapis600']))
    for h in k['panel_split']:
        out.append(poly(P(h, s, ox, oy), C['saffron400']))
    out.append(poly(P(k['panel'], s, ox, oy), 'none', 'stroke="#976400" stroke-width="1" stroke-dasharray="2 3"'))
    for st in t['stitches']:
        out.append(poly(P(st, s, ox, oy), C['lapis600']))
    out.append(poly(P(t['tassel'], s, ox, oy), C['pom600']))
    # vertex labels (outside the polygon)
    out.append(text(X(12), Y(0) - 40, '(12, 0) · 108°', 12, INK, 'middle'))
    out.append(text(X(24) + 8, Y(G.H_TOP) - 8, '(24, 8.72)', 12))
    out.append(text(X(24) + 8, Y(G.H_TOP) + 8, '90°', 12))
    out.append(text(X(0) - 8, Y(G.H_TOP) - 8, '(0, 8.72)', 12, INK, 'end'))
    out.append(text(X(0) - 8, Y(G.H_TOP) + 8, '90°', 12, INK, 'end'))
    out.append(line((X(12.3), Y(G.BODY_H)), (X(16.2), Y(G.BODY_H)), INK, 0.8)); out.append(text(X(16.5), Y(G.BODY_H) + 4, '(12, 25.24) · 72°', 12))
    # axis tags at the right edge of the box
    out.append(text(bx1 - 6, Y(G.PANEL_Y) - 6, 'y 10.5u', 11, INK, 'end'))
    out.append(text(bx1 - 6, Y(G.TIP_Y) - 6, 'y 23.86u', 11, INK, 'end'))
    # 1 stroke 3.6u (perpendicular to the upper-left edge)
    n = (math.sin(math.radians(36)), math.cos(math.radians(36)))
    e0 = (X(3.2), Y(G.H_TOP - 3.2 * math.tan(math.radians(36))))
    e1 = (e0[0] + n[0] * G.STROKE * s, e0[1] + n[1] * G.STROKE * s)
    out.append(dim(e0, e1)); out.append(badge(e0[0] - 14, e0[1] - 14, 1))
    # 2 spine gap 2u
    out.append(dim((X(11), Y(-1.0)), (X(13), Y(-1.0)))); out.append(badge(X(14.4), Y(-1.0), 2))
    # 3 split 1u
    out.append(dim((X(11.5), Y(13.0)), (X(12.5), Y(13.0)))); out.append(badge(X(14.2), Y(13.6), 3))
    # 4 panel x 0.34
    out.append(badge(X(17.2), Y(9.2), 4))
    # 5 clearance + origin
    o = t['origin']
    out.append(f'<circle cx="{X(o[0]):.2f}" cy="{Y(o[1]):.2f}" r="3.2" fill="{POM}"/>')
    out.append(badge(X(13.4), Y(26.9), 5))
    # 6 stitch angles
    for i, ang in enumerate(t['spec']['angles']):
        st = t['stitches'][i]
        c0 = ((st[0][0] + st[3][0]) / 2 / G.U, (st[0][1] + st[3][1]) / 2 / G.U)
        out.append(line((X(c0[0]), Y(c0[1])), (X(c0[0]), Y(c0[1] + 3.0)), POM, 0.9, '2 2'))
        out.append(arc((X(c0[0]), Y(c0[1])), 2.4 * s, 90, 90 + ang))
        lx = X(c0[0]) + 3.1 * s * math.cos(math.radians(90 + ang * 0.45))
        ly = Y(c0[1]) + 3.1 * s * math.sin(math.radians(90 + ang * 0.45))
        out.append(text(lx, ly + 4, f'{ang}°', 11, POM, 'middle', 700))
    tc = t['tassel'][2]
    out.append(badge(X(tc[0] / G.U) - 14, Y(tc[1] / G.U) + 8, 6))
    # legend
    leg = ['1  stroke 3.6u (15% of width), mitred side vertices, flat spine cuts',
           '2  spine gap 2u at the top and bottom vertices = bracket break + bamboo spine',
           '3  R2 spine split: 1u knockout on x = 12u through the panel (body ≥ 48px, every colourway)',
           '4  panel = the kite × 0.34, side vertices on y = 10.5u (panel axis = wordmark x-height centre)',
           '5  stitch 1 origin on x = 12u, 0.8u clear of the chevron tips; 2.2 × 2.0u at 54°, then 72°',
           '6  1.0u true clearance between pieces; tassel 72°/108° rhombus 3.0 × 2.2u along 72°',
           'dashed box: clear space 2 × stroke (7.2u) from the visible body; the tail may sit inside it']
    yy = by1 + 32
    out.append(text(bx0, yy, 'SYMBOL · 24u GRID (1u = 1/24 of the kite width, y runs down) · LARGE MASTER + LOCKUP TAIL', 12, INK, 'start', 700))
    for i, l in enumerate(leg):
        out.append(text(bx0, yy + 24 + i * 19, l, 11.5, POM if i == len(leg) - 1 else INK))
    return ''.join(out)


def lockup_panel(x0, y0):
    import build as B
    p, wm, vb = B.horizontal('large')
    s = 0.40
    ox, oy = x0 + 40, y0 + 70
    out = [text(x0, y0 + 16, 'HORIZONTAL LOCKUP · LARGE MASTER', 12, INK, 'start', 700)]
    cs = 2 * G.STROKE * G.U
    k = G.kite()
    top = k['top_o'] * G.U; bot = G.TIP_Y * G.U
    bx1 = wm['bbox'][2]
    out.append(f'<rect x="{ox - cs * s:.1f}" y="{oy + (top - cs) * s:.1f}" width="{(bx1 + 2 * cs) * s:.1f}" '
               f'height="{(bot - top + 2 * cs) * s:.1f}" fill="none" stroke="{POM}" stroke-width="1.2" stroke-dasharray="6 5"/>')
    base = wm['base']; xh = wm['xh']; asc = base - 712 / 1000 * wm['size']
    for yy, lab, col in ((asc, 'ascender', INK), (base - xh, 'x-height', INK), (G.PANEL_Y * G.U, 'axis 10.5u', POM), (base, 'baseline', INK)):
        out.append(line((ox - cs * s, oy + yy * s), (ox + (bx1 + cs) * s, oy + yy * s), col, 0.8, '4 3'))
        out.append(text(ox + (bx1 + cs) * s + 6, oy + yy * s + 4, lab, 10, col))
    for f_, d in B.layers(p, 'light', wm['d']):
        out.append(f'<path fill="{f_}" transform="translate({ox} {oy}) scale({s})" d="{d}"/>')
    gx0 = 240; gx1 = 240 + G.WORD_GAP * G.STROKE * G.U
    out.append(dim((ox + gx0 * s, oy + 192 * s), (ox + gx1 * s, oy + 192 * s)))
    out.append(text(ox + gx1 * s + 6, oy + 192 * s + 4, '1.3 × stroke', 10, POM))
    ly = oy + (bot + cs) * s + 22
    out.append(text(x0, ly, 'Bricolage Grotesque 800 · opsz 48 (integer instance) · tracking −15/1000 em · GPOS kerning', 11, STONE))
    out.append(text(x0, ly + 17, 'size 18u · x-height 9.5u centred on y 10.5u · stock k · e apertures opened 30 units', 11, STONE))
    out.append(text(x0, ly + 34, 'clear space 2 × stroke round body + wordmark (dashed); the tail sits inside it', 11, POM))
    return ''.join(out)


def masters_panel(x0, y0):
    out = [text(x0, y0 + 16, 'SIZE MASTERS AND TAILS (no media queries)', 12, INK, 'start', 700)]
    k = G.kite()
    s = 5.4
    items = [('large', 'lockup', 'LARGE · body ≥ 48px', 'split panel, lockup tail'),
             ('small', 'lockup_small', 'SMALL · body 20–47px', 'solid panel, 2.6u stitches'),
             ('large', 'full', 'FULL · body ≥ 96px', '18° / 36° / 54° curl')]
    x = x0 + 30
    for master, tail, h1, h2 in items:
        t = G.tail(tail)
        ox, oy = x, y0 + 40
        out.append(poly(P(k['left'], s, ox, oy), C['lapis600'])); out.append(poly(P(k['right'], s, ox, oy), C['lapis600']))
        for h in (k['panel_split'] if master == 'large' else [k['panel']]):
            out.append(poly(P(h, s, ox, oy), C['saffron400']))
        for st in t['stitches']:
            out.append(poly(P(st, s, ox, oy), C['lapis600']))
        out.append(poly(P(t['tassel'], s, ox, oy), C['pom600']))
        out.append(text(x - 30, y0 + 40 + 39 * s, h1, 11, INK, 'start', 700))
        out.append(text(x - 30, y0 + 40 + 39 * s + 16, h2, 10.5, STONE))
        x += 240
    out.append(text(x0, y0 + 40 + 39 * s + 42, 'No tail only in the favicon tile and in repeat patterns. Mono: every part in the body colour.', 11, INK))
    return ''.join(out)


def favicon_panel(x0, y0):
    out = [text(x0, y0 + 16, 'FAVICON · VECTOR TILE (favicon.svg) + HAND-PIXELLED FRAMES (favicon.ico)', 12, INK, 'start', 700)]
    col = dict(N=C['night'], L=C['lapis200'], S=C['saffron400'])
    x = x0; y = y0 + 34

    def labels(x, y, l1, l2, l3):
        return (text(x, y + 18, l1, 11, INK, 'start', 700) + text(x, y + 34, l2, 10.5, STONE)
                + text(x, y + 49, l3, 10.5, STONE))
    # the vector drawing on its 32-unit grid (every 2 units)
    k = 4.4; n = F.TILE
    v = F.vector()

    def P(pts):
        return ' '.join(f'{x + px * k:.1f},{y + py * k:.1f}' for px, py in pts)
    tile = f'x="{x}" y="{y}" width="{n * k:.1f}" height="{n * k:.1f}" rx="{F.TILE_RX * k:.1f}"'
    out.append(f'<clipPath id="favtile"><rect {tile}/></clipPath><rect {tile} fill="{C["night"]}"/><g clip-path="url(#favtile)">')
    for i in range(2, n, 2):
        out.append(line((x + i * k, y), (x + i * k, y + n * k), '#1F2A52', 0.6))
        out.append(line((x, y + i * k), (x + n * k, y + i * k), '#1F2A52', 0.6))
    out.append('</g>')
    out.append(f'<polygon points="{P(v["left"])}" fill="{C["lapis200"]}"/><polygon points="{P(v["right"])}" fill="{C["lapis200"]}"/>'
               f'<polygon points="{P(v["core"])}" fill="{C["saffron400"]}"/>')
    out.append(labels(x, y + n * k, 'favicon.svg · vector', 'master angles, any DPR', 'gaps x 15–17, core 0.38'))
    x += n * k + 26
    for px, n, k, l1, l2, l3 in ((F.grid(16), 16, 7.0, '16 · ico / png', '3 / 2px ring', 'no spine gap'),
                                 (F.grid(32), 32, 4.4, '32 · ico / png', '36° / 54° steps', 'gaps x 15–16'),
                                 (F.grid(48), 48, 3.2, '48 · ico / png', '36° / 54° steps', 'gaps x 23–24')):
        for r in range(n):
            for c_ in range(n):
                out.append(f'<rect x="{x + c_ * k:.1f}" y="{y + r * k:.1f}" width="{k + 0.05:.2f}" height="{k + 0.05:.2f}" fill="{col[px[r][c_]]}"/>')
        for i in range(1, n):
            out.append(line((x + i * k, y), (x + i * k, y + n * k), '#1F2A52', 0.35 if n > 16 else 0.5))
            out.append(line((x, y + i * k), (x + n * k, y + i * k), '#1F2A52', 0.35 if n > 16 else 0.5))
        out.append(labels(x, y + n * k, l1, l2, l3))
        x += n * k + 26
    return ''.join(out)


def html():
    W, H = 1600, 1180
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<rect width="{W}" height="{H}" fill="{C["paper"]}"/>'
           + text(70, 54, 'CodeWeekend · Gudiparan, the Bracket Kite · construction', 22, INK, 'start', 700)
           + text(70, 80, 'Two code brackets, &lt; and &gt;, make an Afghan kite. Learners build it; the community holds the string.', 13, STONE)
           + symbol_panel()
           + lockup_panel(850, 120) + masters_panel(850, 430) + favicon_panel(850, 780) + '</svg>')
    return ('<!doctype html><html><head><meta charset="utf-8">'
            '<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Mono:wght@400;500;700&display=swap" rel="stylesheet">'
            f'<style>html,body{{margin:0;background:{C["paper"]}}}</style></head><body>{svg}</body></html>'), W, H
