#!/usr/bin/env python3
"""CodeWeekend · Gudiparan, the Bracket Kite: geometry and wordmark (single source of truth).

Units: 1u = 1/24 of the kite's width = 10 file units. y runs downward. x = 0 is the left side vertex.
Reused from the concept build (brand/concepts/bracket-kite/work/build.py): kite(), the glyph-outline tools
(contours_of, split, intersect_line, cut_terminal, con_d) and the GPOS pair reader (tools/text2path.py).
"""
import math, os, urllib.request, re
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import outline as O

HERE = os.path.dirname(os.path.abspath(__file__))
U = 10.0

# ------------------------------------------------------------------ palette (foundation section 4, unchanged)
C = dict(lapis600='#2347B4', lapis200='#C8D9FF', lapis900='#0B1C4B', saffron400='#F5A71E',
         pom600='#B4223B', pom300='#F4858A', ink='#1B2034', paper='#FBF7EF', night='#0E1630', white='#FFFFFF')

# colourways: role -> colour. roles: body (chevrons + stitches), panel, tassel, word
WAYS = {
    'light':      dict(body=C['lapis600'], panel=C['saffron400'], tassel=C['pom600'], word=C['ink']),
    'reverse':    dict(body=C['paper'],    panel=C['saffron400'], tassel=C['pom300'], word=C['paper']),
    'mono-ink':   dict(body=C['ink'],      panel=C['ink'],        tassel=C['ink'],    word=C['ink']),
    'mono-white': dict(body=C['white'],    panel=C['white'],      tassel=C['white'],  word=C['white']),
}

# ------------------------------------------------------------------ body (as built; do not change)
STROKE = 3.6      # u
SPINE_GAP = 2.0   # u
PANEL_SCALE = 0.34
PANEL_Y = 10.5    # u, panel side-vertex axis
SPLIT = 1.0       # u, R2 knockout on x = 12u

H_TOP = 12 / math.tan(math.radians(54))      # 8.7185u  (top vertex 108 deg)
H_BOT = 12 / math.tan(math.radians(36))      # 16.5161u (bottom vertex 72 deg)
BODY_H = H_TOP + H_BOT                       # 25.2346u (outer polygon height = "body height")
TIP_Y = H_TOP + H_BOT * (12 - SPINE_GAP / 2) / 12   # 23.858u (flat spine cuts at the chevron tips)

# ------------------------------------------------------------------ tails (R1, R3)
# start: TRUE clearance (u) between the chevron tips and stitch 1, whose origin sits on x = 12u
# gap / tassel_gap: TRUE clearance (u) between neighbouring tail pieces (see tail())
# stitches: rectangles w (across) x l (along), each along its own angle (deg from vertical, down and left)
# tassel: 72/108 rhombus, long axis `tassel_len` along `tassel_ang`; width = len * tan(36)
TAILS = {
    # Large master lockup tail: 54 / 72 deg, 2.2 x 2.0u stitches, 1.0u gaps, 3.0 x 2.2u tassel at 72 deg
    'lockup':       dict(start=0.8, angles=[54, 72], w=2.2, l=2.0, gap=1.0, tassel_len=3.0, tassel_ang=72, tassel_gap=1.0),
    # Small master (body 20-47px): stitches 2.6u wide (and 2.2u long so that every element is >= 3px at a
    # 36px body: 2.0u would be 2.85px), tassel 3.6u long
    'lockup_small': dict(start=0.8, angles=[54, 72], w=2.6, l=2.2, gap=1.0, tassel_len=3.6, tassel_ang=72, tassel_gap=1.0),
    # Full tail (body >= 96px): the designer's 18 / 36 / 54 curl, stitches 2.2 x 2.4u, 1.4u gaps, tassel
    # (the designer's 2.2u-side girih rhombus, 3.56u long) along 72 deg instead of plumb
    'full':         dict(start=1.0, angles=[18, 36, 54], w=2.2, l=2.4, gap=1.4,
                         tassel_len=2 * 2.2 * math.cos(math.radians(36)), tassel_ang=72, tassel_gap=1.4),
}


def fmt(v):
    s = f"{v:.1f}"
    if s.endswith('.0'):
        s = s[:-2]
    if s in ('-0', '-0.0'):
        s = '0'
    return s


def poly_d(pts):
    out = 'M' + fmt(pts[0][0]) + ' ' + fmt(pts[0][1])
    prev = (round(pts[0][0], 1), round(pts[0][1], 1))
    for p in pts[1:]:
        q = (round(p[0], 1), round(p[1], 1))
        if q == prev:
            continue
        if q[1] == prev[1]:
            out += 'H' + fmt(p[0])
        elif q[0] == prev[0]:
            out += 'V' + fmt(p[1])
        else:
            out += 'L' + fmt(p[0]) + ' ' + fmt(p[1])
        prev = q
    return out + 'Z'


def kite():
    """Chevrons and panel, in file units (x10). Reused from the concept build."""
    s = STROKE; g = SPINE_GAP / 2
    hT, hB, H = H_TOP, H_BOT, BODY_H
    iT = s / math.sin(math.radians(54))
    iB = H - s / math.sin(math.radians(36))
    n1 = (math.sin(math.radians(36)), math.cos(math.radians(36)))
    n2 = (math.cos(math.radians(36)), -math.sin(math.radians(36)))
    iL = (s * (n1[0] + n2[0]), hT + s * (n1[1] + n2[1]))
    xc = 12 - g
    top_o = hT * (12 - xc) / 12
    top_i = iT + hT * (12 - xc) / 12
    bot_o = hT + hB * xc / 12
    bot_i = iB - hB * (12 - xc) / 12
    left = [(xc, top_o), (0, hT), (xc, bot_o), (xc, bot_i), iL, (xc, top_i)]
    right = [(24 - x, y) for x, y in left][::-1]
    ps = PANEL_SCALE; sy = PANEL_Y
    panel = [(12, sy - ps * hT), (12 + ps * 12, sy), (12, sy + ps * hB), (12 - ps * 12, sy)]
    # R2: split panel = two halves either side of a SPLIT-wide knockout on x = 12
    T, R, B, L = panel
    h = SPLIT / 2

    def y_on(a, b, x):
        t = (x - a[0]) / (b[0] - a[0]); return a[1] + t * (b[1] - a[1])
    lh = [(12 - h, y_on(L, T, 12 - h)), L, (12 - h, y_on(L, B, 12 - h))]
    rh = [(12 + h, y_on(R, T, 12 + h)), (12 + h, y_on(R, B, 12 + h)), R]
    sc = lambda pts: [(x * U, y * U) for x, y in pts]
    return dict(left=sc(left), right=sc(right), panel=sc(panel), panel_split=[sc(lh), sc(rh)],
                inner_left=iL, xc=xc, top_o=top_o, top_i=top_i, bot_o=bot_o, bot_i=bot_i)


def rect_along(o, d, length, width):
    n = (-d[1], d[0]); w = width / 2
    a = (o[0] + n[0] * w, o[1] + n[1] * w)
    b = (o[0] - n[0] * w, o[1] - n[1] * w)
    return [a, (a[0] + d[0] * length, a[1] + d[1] * length), (b[0] + d[0] * length, b[1] + d[1] * length), b]


def dir_of(deg):
    a = math.radians(deg); return (-math.sin(a), math.cos(a))


def _dseg(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = dx * dx + dy * dy
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def poly_dist(P, Q):
    """Minimum distance between two (non-overlapping) convex polygons, in the polygons' units."""
    m = min(_dseg(p, Q[i], Q[(i + 1) % len(Q)]) for p in P for i in range(len(Q)))
    return min(m, min(_dseg(p, P[i], P[(i + 1) % len(P)]) for p in Q for i in range(len(P))))


def _place(make, prev_polys, clearance, lo=0.0, hi=8.0):
    """Smallest offset t in [lo, hi] at which make(t) clears every polygon in prev_polys by `clearance` (u)."""
    for _ in range(60):
        mid = (lo + hi) / 2
        if min(poly_dist(make(mid), P) for P in prev_polys) >= clearance:
            hi = mid
        else:
            lo = mid
    return hi


def tassel_poly(p, ang, L):
    d = dir_of(ang); n = (-d[1], d[0]); hw = L / 2 * math.tan(math.radians(36))
    c = (p[0] + d[0] * L / 2, p[1] + d[1] * L / 2)
    return [p, (c[0] + n[0] * hw, c[1] + n[1] * hw), (p[0] + d[0] * L, p[1] + d[1] * L), (c[0] - n[0] * hw, c[1] - n[1] * hw)]


def tail(kind='lockup', **over):
    """Every gap in the tail is a TRUE clearance (minimum distance between neighbouring pieces), not a centreline
    offset: the first stitch's origin slides down x = 12u until it clears the chevron tips by `start`, and each
    later piece slides along its own direction until it clears the previous piece by `gap`. This keeps the
    stitch rhythm even where the curl turns, and stops stitch 1 kissing the left chevron tip."""
    t = dict(TAILS[kind]); t.update(over)
    k = kite()
    chev = [[(x / U, y / U) for x, y in k['left']], [(x / U, y / U) for x, y in k['right']]]
    d0 = dir_of(t['angles'][0])
    s = _place(lambda s: rect_along((12.0, TIP_Y + s), d0, t['l'], t['w']), chev, t['start'])
    p = (12.0, TIP_Y + s)
    stitches = [rect_along(p, d0, t['l'], t['w'])]
    p = (p[0] + d0[0] * t['l'], p[1] + d0[1] * t['l'])
    for ang in t['angles'][1:]:
        d = dir_of(ang); q = p
        g = _place(lambda g: rect_along((q[0] + d[0] * g, q[1] + d[1] * g), d, t['l'], t['w']), [stitches[-1]], t['gap'])
        o = (q[0] + d[0] * g, q[1] + d[1] * g)
        stitches.append(rect_along(o, d, t['l'], t['w']))
        p = (o[0] + d[0] * t['l'], o[1] + d[1] * t['l'])
    d = dir_of(t['tassel_ang']); q = p
    g = _place(lambda g: tassel_poly((q[0] + d[0] * g, q[1] + d[1] * g), t['tassel_ang'], t['tassel_len']),
               [stitches[-1]], t['tassel_gap'])
    tas = tassel_poly((q[0] + d[0] * g, q[1] + d[1] * g), t['tassel_ang'], t['tassel_len'])
    sc = lambda pts: [(x * U, y * U) for x, y in pts]
    return dict(stitches=[sc(x) for x in stitches], tassel=sc(tas), spec=t, origin=(12.0, TIP_Y + s))


# ------------------------------------------------------------------ wordmark (R4)
VF = os.path.join(HERE, 'fonts', 'BricolageGrotesque-VF-latin.woff2')
INST = os.path.join(HERE, 'fonts', 'BricolageGrotesque-800-opsz48.ttf')
OPSZ, WGHT, TRACK, E_OPEN = 48, 800, -15, 30
WORD = 'codeweekend'
WORD_SIZE = 18.0   # u, horizontal lockup font size
WORD_GAP = 1.3     # x stroke, kite right vertex -> first ink


def font_instance():
    """Re-instance Bricolage Grotesque from the variable font at an INTEGER opsz (fixes the text2path float bug)."""
    if not os.path.exists(INST):
        if not os.path.exists(VF):
            os.makedirs(os.path.dirname(VF), exist_ok=True)
            ua = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
            css = urllib.request.urlopen(urllib.request.Request(
                'https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800', headers=ua)).read().decode()
            blk = dict(re.findall(r'/\* ([a-z\-]+) \*/\s*@font-face \{(.*?)\}', css, re.S))['latin']
            url = re.search(r'url\((https://[^)]+)\)', blk).group(1)
            open(VF, 'wb').write(urllib.request.urlopen(url).read())
        from fontTools.varLib import instancer
        vf = TTFont(VF)
        inst = instancer.instantiateVariableFont(vf, {'opsz': int(OPSZ), 'wght': int(WGHT)})
        inst.flavor = None
        inst.save(INST)
    return TTFont(INST)


def kern_pairs(font):
    """GPOS PairPos (format 1 & 2) horizontal kerning (from tools/text2path.py)."""
    if 'GPOS' not in font:
        return lambda a, b: 0
    gpos = font['GPOS'].table
    lookups = []
    for fr in gpos.FeatureList.FeatureRecord:
        if fr.FeatureTag == 'kern':
            lookups.extend(fr.Feature.LookupListIndex)
    subtables = []
    for li in sorted(set(lookups)):
        lk = gpos.LookupList.Lookup[li]
        for st in lk.SubTable:
            if lk.LookupType == 9:
                st = st.ExtSubTable
            if st.__class__.__name__ == 'PairPos':
                subtables.append(st)

    def lookup(a, b):
        for st in subtables:
            cov = st.Coverage.glyphs
            if a not in cov:
                continue
            if st.Format == 1:
                for pvr in st.PairSet[cov.index(a)].PairValueRecord:
                    if pvr.SecondGlyph == b:
                        v = pvr.Value1
                        return (getattr(v, 'XAdvance', 0) or 0) if v else 0
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs.get(a, 0); c2 = st.ClassDef2.classDefs.get(b, 0)
                v = st.Class1Record[c1].Class2Record[c2].Value1
                x = getattr(v, 'XAdvance', 0) if v else 0
                if x:
                    return x
        return 0
    return lookup


def contours_of(gs, gname):
    rp = RecordingPen(); gs[gname].draw(rp)
    cons, cur, start, last = [], [], None, None
    for op, args in rp.value:
        if op == 'moveTo':
            start = args[0]; last = start; cur = []
        elif op == 'lineTo':
            cur.append(('L', last, args[0])); last = args[0]
        elif op == 'qCurveTo':
            offs, end = list(args[:-1]), args[-1]
            for i, c in enumerate(offs):
                e = end if i == len(offs) - 1 else ((c[0] + offs[i + 1][0]) / 2, (c[1] + offs[i + 1][1]) / 2)
                cur.append(('Q', last, c, e)); last = e
        elif op in ('closePath', 'endPath'):
            if last != start:
                cur.append(('L', last, start))
            cons.append(cur)
    return cons


def split(s, t):
    if s[0] == 'L':
        a, b = s[1], s[2]; m = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        return ('L', a, m), ('L', m, b)
    a, c, b = s[1], s[2], s[3]
    ac = (a[0] + (c[0] - a[0]) * t, a[1] + (c[1] - a[1]) * t)
    cb = (c[0] + (b[0] - c[0]) * t, c[1] + (b[1] - c[1]) * t)
    m = (ac[0] + (cb[0] - ac[0]) * t, ac[1] + (cb[1] - ac[1]) * t)
    return ('Q', a, ac, m), ('Q', m, cb, b)


def intersect_line(s, p0, v):
    n = (-v[1], v[0])
    fn = lambda q: (q[0] - p0[0]) * n[0] + (q[1] - p0[1]) * n[1]
    if s[0] == 'L':
        d0, d1 = fn(s[1]), fn(s[2])
        if (d0 > 0) == (d1 > 0) or d0 == d1:
            return []
        return [d0 / (d0 - d1)]
    a, c, b = fn(s[1]), fn(s[2]), fn(s[3])
    A = a - 2 * c + b; B = 2 * (c - a); Cc = a
    ts = []
    if abs(A) < 1e-9:
        if abs(B) > 1e-12:
            ts = [-Cc / B]
    else:
        disc = B * B - 4 * A * Cc
        if disc >= 0:
            r = math.sqrt(disc); ts = [(-B - r) / (2 * A), (-B + r) / (2 * A)]
    return sorted(t for t in ts if 0 <= t <= 1)


def cut_terminal(con, cut_idx, p0, v, search=6):
    n = len(con)
    ii = it = oi = ot = None
    for k in range(1, search):
        j = (cut_idx - k) % n; ts = intersect_line(con[j], p0, v)
        if ts:
            ii, it = j, ts[-1]; break
    for k in range(1, search):
        j = (cut_idx + k) % n; ts = intersect_line(con[j], p0, v)
        if ts:
            oi, ot = j, ts[0]; break
    first, _ = split(con[ii], it)
    _, second = split(con[oi], ot)
    new = [second]
    j = (oi + 1) % n
    while j != ii:
        new.append(con[j]); j = (j + 1) % n
    new.append(first)
    new.append(('L', first[-1], second[1]))
    return new


def con_d(con, tf):
    p0 = tf(con[0][1])
    out = f"M{fmt(p0[0])} {fmt(p0[1])}"
    prev = (round(p0[0], 1), round(p0[1], 1))
    segs = con[:-1] if con[-1][0] == 'L' else con
    for s in segs:
        if s[0] == 'L':
            q = tf(s[2]); qr = (round(q[0], 1), round(q[1], 1))
            if qr == prev:
                continue
            if qr[1] == prev[1]:
                out += 'H' + fmt(q[0])
            elif qr[0] == prev[0]:
                out += 'V' + fmt(q[1])
            else:
                out += f"L{fmt(q[0])} {fmt(q[1])}"
            prev = qr
        else:
            c = tf(s[2]); q = tf(s[3])
            out += f"Q{fmt(c[0])} {fmt(c[1])} {fmt(q[0])} {fmt(q[1])}"
            prev = (round(q[0], 1), round(q[1], 1))
    return out + 'Z'


_FONT = None


def wordmark_glyphs(text=WORD, e_open=E_OPEN):
    """Returns ([(x_advance_origin, contours)], font). Stock k (R4: slit removed); e terminals opened by e_open."""
    global _FONT
    if _FONT is None:
        _FONT = font_instance()
    font = _FONT
    gs = font.getGlyphSet(); cm = font.getBestCmap(); hm = font['hmtx']
    kern = kern_pairs(font)
    names = [cm[ord(c)] for c in text]
    x = 0; placed = []
    for i, g in enumerate(names):
        # 1. boolean union first: the stock opsz-48 'e' is one self-intersecting contour (crossbar drawn through
        #    the bowl, OVERLAP_SIMPLE). After the union every glyph fills identically under nonzero and even-odd.
        cons = O.remove_overlaps(contours_of(gs, g))
        if g == 'e' and e_open:
            # 2. aperture: the lower terminal's cut edge moves e_open units into the terminal. The cut line meets
            #    exactly the two flanks of the terminal, so this is a clean half-plane subtraction on a simple contour.
            k = next(k for k, con in enumerate(cons) if any(sg[0] == 'L' and sg[2][0] - sg[1][0] > 80
                                                             and max(sg[1][1], sg[2][1]) < 260 for sg in con))
            con = cons[k]
            ci = next(i for i, sg in enumerate(con) if sg[0] == 'L' and sg[2][0] - sg[1][0] > 80
                      and max(sg[1][1], sg[2][1]) < 260)
            a0, a1 = con[ci][1], con[ci][2]
            v = (a1[0] - a0[0], a1[1] - a0[1]); nl = math.hypot(*v)
            nrm = (v[1] / nl, -v[0] / nl)
            p0 = (a0[0] + nrm[0] * e_open, a0[1] + nrm[1] * e_open)
            cons[k] = cut_terminal(con, ci, p0, v)
        # 3. clean nodes: merge collinear line runs, drop sub-3-unit micro-segments left by the cut
        cons = [O.tidy(con) for con in cons]
        placed.append((x, cons))
        adv = hm[g][0]
        if i + 1 < len(names):
            adv += kern(g, names[i + 1]) + TRACK
        x += adv
    return placed, font


def wordmark(ox, base, size, text=WORD):
    """Outlined wordmark: font size `size` (file units), first-ink left edge at ox, baseline at base.
    Returns d, bbox (xmin, ymin, xmax, ymax) and metrics."""
    placed, font = wordmark_glyphs(text)
    sc = size / font['head'].unitsPerEm
    xmin0 = min(q[0] for gx, cons in placed[:1] for con in cons for s in con for q in s[1:])
    shift = ox - xmin0 * sc
    ds = []; xs = []; ys = []
    for gx, cons in placed:
        tf = lambda q, gx=gx: (shift + (gx + q[0]) * sc, base - q[1] * sc)
        for con in cons:
            ds.append(con_d(con, tf))
            for s in con:   # true ink extents (sample the quadratic arcs, not their control points)
                pts = [s[1], s[2]] if s[0] == 'L' else [split(s, i / 16)[0][-1] for i in range(17)]
                for q in pts:
                    X, Y = tf(q); xs.append(X); ys.append(Y)
    os2 = font['OS/2']
    return dict(d=''.join(ds), bbox=(min(xs), min(ys), max(xs), max(ys)),
                xh=os2.sxHeight * sc, asc=712 * sc, size=size, base=base)
