#!/usr/bin/env python3
"""Exact overlap removal and node clean-up for TrueType-style outlines (lines + quadratic Beziers).

Why: Bricolage Grotesque's variable 'e' is ONE self-intersecting contour (the crossbar is drawn through the bowl;
the glyph carries OVERLAP_SIMPLE). Browsers fill it with the nonzero rule, but even-odd consumers (Illustrator /
Figma / Inkscape set to even-odd, vinyl and laser cutters, embroidery digitisers, icon-font generators) punch
holes in it, and stroking shows the internal crossbar edges. skia-pathops is not available here, so this module
does the boolean union itself. Segments are ('L', a, b) or ('Q', a, c, b) in font units (y up).

    remove_overlaps(contours) -> contours whose nonzero AND even-odd fills are identical to the input's nonzero fill
    tidy(contour)             -> merges collinear line runs, drops micro-segments
"""
import math

EPS_T = 1e-9


# ------------------------------------------------------------------ segment basics
def pt(s, t):
    if s[0] == 'L':
        a, b = s[1], s[2]
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    a, c, b = s[1], s[2], s[3]
    u = 1 - t
    return (u * u * a[0] + 2 * u * t * c[0] + t * t * b[0], u * u * a[1] + 2 * u * t * c[1] + t * t * b[1])


def tangent(s, t):
    if s[0] == 'L':
        return (s[2][0] - s[1][0], s[2][1] - s[1][1])
    a, c, b = s[1], s[2], s[3]
    d = (2 * (1 - t) * (c[0] - a[0]) + 2 * t * (b[0] - c[0]), 2 * (1 - t) * (c[1] - a[1]) + 2 * t * (b[1] - c[1]))
    if abs(d[0]) + abs(d[1]) < 1e-12:            # degenerate control point: use the chord
        d = (b[0] - a[0], b[1] - a[1])
    return d


def sub(s, t0, t1, p0=None, p1=None):
    """Sub-segment of s between parameters t0 < t1; endpoints optionally forced to canonical points p0 / p1."""
    a = p0 or pt(s, t0)
    b = p1 or pt(s, t1)
    if s[0] == 'L':
        return ('L', a, b)
    # control point of the sub-curve: intersection of the tangents (blossom of the quadratic)
    A, C, B = s[1], s[2], s[3]

    def blossom(u, v):
        # quadratic blossom f(u, v)
        w = lambda p, q, k: (p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k)
        return w(w(A, C, u), w(C, B, u), v)
    return ('Q', a, blossom(t0, t1), b)


def bbox(s):
    xs = [p[0] for p in s[1:]]; ys = [p[1] for p in s[1:]]
    return min(xs), min(ys), max(xs), max(ys)


def flatten(s, n=48):
    if s[0] == 'L':
        return [s[1], s[2]]
    return [pt(s, i / n) for i in range(n + 1)]


def seg_len(s):
    pts = flatten(s, 16)
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))


# ------------------------------------------------------------------ intersections
def _ll(p, q, r, s):
    """line segments p-q and r-s -> (t, u) or None"""
    d1 = (q[0] - p[0], q[1] - p[1]); d2 = (s[0] - r[0], s[1] - r[1])
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-12:
        return None
    w = (r[0] - p[0], r[1] - p[1])
    t = (w[0] * d2[1] - w[1] * d2[0]) / den
    u = (w[0] * d1[1] - w[1] * d1[0]) / den
    return t, u


def _roots_q_line(s, p0, v):
    """parameters t in [0, 1] where quadratic s crosses the infinite line p0 + k v"""
    n = (-v[1], v[0])
    f = lambda q: (q[0] - p0[0]) * n[0] + (q[1] - p0[1]) * n[1]
    a, c, b = f(s[1]), f(s[2]), f(s[3])
    A = a - 2 * c + b; B = 2 * (c - a); C0 = a
    ts = []
    if abs(A) < 1e-12:
        if abs(B) > 1e-12:
            ts = [-C0 / B]
    else:
        disc = B * B - 4 * A * C0
        if disc >= 0:
            r = math.sqrt(disc); ts = [(-B - r) / (2 * A), (-B + r) / (2 * A)]
    return [t for t in ts if -1e-9 <= t <= 1 + 1e-9]


def _qq(s1, s2, t0=0.0, t1=1.0, u0=0.0, u1=1.0, depth=0, out=None):
    """recursive bbox subdivision for two quadratics"""
    if out is None:
        out = []
    a = sub(s1, t0, t1); b = sub(s2, u0, u1)
    A = bbox(a); B = bbox(b)
    if A[2] < B[0] - 1e-9 or B[2] < A[0] - 1e-9 or A[3] < B[1] - 1e-9 or B[3] < A[1] - 1e-9:
        return out
    if depth > 40 or (max(A[2] - A[0], A[3] - A[1]) < 1e-7 and max(B[2] - B[0], B[3] - B[1]) < 1e-7):
        out.append(((t0 + t1) / 2, (u0 + u1) / 2)); return out
    # nearly flat pieces: solve as lines
    if depth > 12:
        r = _ll(a[1], a[-1], b[1], b[-1])
        if r and -1e-6 <= r[0] <= 1 + 1e-6 and -1e-6 <= r[1] <= 1 + 1e-6:
            out.append((t0 + (t1 - t0) * r[0], u0 + (u1 - u0) * r[1]))
        return out
    tm = (t0 + t1) / 2; um = (u0 + u1) / 2
    for ta, tb in ((t0, tm), (tm, t1)):
        for ua, ub in ((u0, um), (um, u1)):
            _qq(s1, s2, ta, tb, ua, ub, depth + 1, out)
    return out


def intersections(s1, s2):
    if s1[0] == 'L' and s2[0] == 'L':
        r = _ll(s1[1], s1[2], s2[1], s2[2])
        return [r] if r and -1e-9 <= r[0] <= 1 + 1e-9 and -1e-9 <= r[1] <= 1 + 1e-9 else []
    if s1[0] == 'Q' and s2[0] == 'L':
        return [(b, a) for a, b in intersections(s2, s1)]
    if s1[0] == 'L':
        p, q = s1[1], s1[2]; v = (q[0] - p[0], q[1] - p[1]); L2 = v[0] ** 2 + v[1] ** 2
        out = []
        for u in _roots_q_line(s2, p, v):
            x = pt(s2, u); t = ((x[0] - p[0]) * v[0] + (x[1] - p[1]) * v[1]) / L2
            if -1e-9 <= t <= 1 + 1e-9:
                out.append((t, u))
        return out
    raw = _qq(s1, s2)
    out = []
    for t, u in sorted(raw):
        if not any(abs(t - a) < 1e-5 and abs(u - b) < 1e-5 for a, b in out):
            out.append((t, u))
    return out


# ------------------------------------------------------------------ winding
def winding(p, polys):
    """nonzero winding number of point p for flattened closed polygons"""
    w = 0
    x, y = p
    for poly in polys:
        n = len(poly)
        for i in range(n):
            a = poly[i]; b = poly[(i + 1) % n]
            if a[1] <= y:
                if b[1] > y and (b[0] - a[0]) * (y - a[1]) - (x - a[0]) * (b[1] - a[1]) > 0:
                    w += 1
            elif b[1] <= y and (b[0] - a[0]) * (y - a[1]) - (x - a[0]) * (b[1] - a[1]) < 0:
                w -= 1
    return w


def _polys(contours):
    out = []
    for con in contours:
        pts = []
        for s in con:
            pts.extend(flatten(s, 96)[:-1])
        out.append(pts)
    return out


# ------------------------------------------------------------------ boolean union (nonzero)
def remove_overlaps(contours, eps=0.35):
    """Return contours describing the nonzero fill of `contours` with no self- or mutual intersections.
    Output orientation matches TrueType (filled region on the RIGHT of travel, y up), so holes come out reversed and
    both fill rules agree."""
    segs = [(ci, si, s) for ci, con in enumerate(contours) for si, s in enumerate(con)]
    cuts = {k: [] for k in range(len(segs))}       # seg index -> [(t, point)]
    n = len(segs)
    for i in range(n):
        for j in range(i + 1, n):
            ci, si, s1 = segs[i]; cj, sj, s2 = segs[j]
            b1 = bbox(s1); b2 = bbox(s2)
            if b1[2] < b2[0] - 1e-6 or b2[2] < b1[0] - 1e-6 or b1[3] < b2[1] - 1e-6 or b2[3] < b1[1] - 1e-6:
                continue
            for t, u in intersections(s1, s2):
                # skip the shared vertex of neighbours in the same contour
                if ci == cj:
                    L = len(contours[ci])
                    if (sj == (si + 1) % L and t > 1 - 1e-6 and u < 1e-6) or (si == (sj + 1) % L and u > 1 - 1e-6 and t < 1e-6):
                        continue
                    if L == 2 or (si == 0 and sj == L - 1 and t < 1e-6 and u > 1 - 1e-6):
                        continue
                p = pt(s1, t)
                cuts[i].append((t, p)); cuts[j].append((u, p))
    polys = _polys(contours)
    pieces = []
    for k, (ci, si, s) in enumerate(segs):
        ts = sorted(c for c in cuts[k] if EPS_T < c[0] < 1 - EPS_T)
        bounds = [(0.0, s[1])] + ts + [(1.0, s[-1])]
        for (t0, p0), (t1, p1) in zip(bounds, bounds[1:]):
            if t1 - t0 < 1e-9:
                continue
            piece = sub(s, t0, t1, p0, p1)
            tm = 0.5
            m = pt(piece, tm); d = tangent(piece, tm); dl = math.hypot(*d)
            nrm = (-d[1] / dl, d[0] / dl)          # left normal (y up)
            left = winding((m[0] + nrm[0] * eps, m[1] + nrm[1] * eps), polys) != 0
            right = winding((m[0] - nrm[0] * eps, m[1] - nrm[1] * eps), polys) != 0
            if left == right:
                continue                            # interior or exterior edge: drop
            if left:                                # filled side must be on the right: reverse
                piece = ('L', piece[2], piece[1]) if piece[0] == 'L' else ('Q', piece[3], piece[2], piece[1])
            pieces.append(piece)
    # chain pieces into closed loops
    def key(p):
        return (round(p[0], 4), round(p[1], 4))
    starts = {}
    for idx, pc in enumerate(pieces):
        starts.setdefault(key(pc[1]), []).append(idx)
    used = [False] * len(pieces)
    out = []
    for idx in range(len(pieces)):
        if used[idx]:
            continue
        loop = []; cur = idx
        while not used[cur]:
            used[cur] = True; loop.append(pieces[cur])
            nxt = [j for j in starts.get(key(pieces[cur][-1]), []) if not used[j]]
            if not nxt:
                break
            if len(nxt) > 1:      # pick the sharpest right turn (keeps loops simple at touching vertices)
                d0 = tangent(pieces[cur], 1.0)
                def turn(j):
                    d1 = tangent(pieces[j], 0.0)
                    return math.atan2(d0[0] * d1[1] - d0[1] * d1[0], d0[0] * d1[0] + d0[1] * d1[1])
                nxt.sort(key=turn)
            cur = nxt[0]
        assert key(loop[-1][-1]) == key(loop[0][1]), 'open loop in overlap removal'
        out.append(loop)
    return out


# ------------------------------------------------------------------ tidy
def _collinear(s1, s2, tol_deg=0.25):
    if s1[0] != 'L' or s2[0] != 'L':
        return False
    d1 = (s1[2][0] - s1[1][0], s1[2][1] - s1[1][1]); d2 = (s2[2][0] - s2[1][0], s2[2][1] - s2[1][1])
    l1 = math.hypot(*d1); l2 = math.hypot(*d2)
    if l1 < 1e-9 or l2 < 1e-9:
        return True
    cross = (d1[0] * d2[1] - d1[1] * d2[0]) / (l1 * l2); dot = (d1[0] * d2[0] + d1[1] * d2[1]) / (l1 * l2)
    return dot > 0 and abs(math.degrees(math.asin(max(-1, min(1, cross))))) < tol_deg


def tidy(con, min_len=3.0):
    """Drop micro-segments (< min_len font units; their end point is absorbed by the next segment) and merge runs
    of collinear lines into one line."""
    con = list(con)
    changed = True
    while changed and len(con) > 2:
        changed = False
        for i, s in enumerate(con):
            if seg_len(s) < min_len:
                nxt = (i + 1) % len(con); prv = (i - 1) % len(con)
                # the previous segment now ends where the micro-segment ended
                p = con[prv]; end = s[-1]
                con[prv] = ('L', p[1], end) if p[0] == 'L' else ('Q', p[1], p[2], end)
                del con[i]; changed = True; break
        if changed:
            continue
        for i in range(len(con)):
            j = (i + 1) % len(con)
            if _collinear(con[i], con[j]):
                merged = ('L', con[i][1], con[j][2])
                if j == 0:
                    con[0] = merged; del con[i]
                else:
                    con[i] = merged; del con[j]
                changed = True; break
    return con


def signed_area(con):
    pts = []
    for s in con:
        pts.extend(flatten(s, 24)[:-1])
    return 0.5 * sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))


def self_intersections(con):
    """count of proper crossings inside one contour (for QA)"""
    hits = 0; L = len(con)
    for i in range(L):
        for j in range(i + 1, L):
            for t, u in intersections(con[i], con[j]):
                if (j == i + 1 and t > 1 - 1e-6 and u < 1e-6) or (i == 0 and j == L - 1 and t < 1e-6 and u > 1 - 1e-6):
                    continue
                hits += 1
    return hits
