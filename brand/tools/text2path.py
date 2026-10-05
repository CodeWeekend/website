#!/usr/bin/env python3
"""text2path.py --family "Space Grotesk" --weight 700 --text "codeweekend" --size 100 [--tracking -20] [--opsz 96] [--italic] [--x 0 --y 0]
Converts text set in a Google Font into a single SVG path (outlined glyphs, kerning applied via GPOS pair kerning where
available). --size is font size in px; baseline is at --y; --tracking is extra letter spacing in 1/1000 em.
Prints JSON: {"d": "...", "width": advance_width, "bbox": [xmin,ymin,xmax,ymax], "ascender":..., "descender":..., "xHeight":..., "capHeight":...}
Use --svg to print a ready standalone <svg> instead."""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_font import fetch
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

def kern_pairs(font):
    """Very small GPOS PairPos (format 1 & 2) reader for horizontal kerning."""
    pairs = {}
    if 'GPOS' not in font: return lambda a, b: 0
    gpos = font['GPOS'].table
    cmap_glyphs = None
    lookups = []
    for fr in gpos.FeatureList.FeatureRecord:
        if fr.FeatureTag == 'kern':
            lookups.extend(fr.Feature.LookupListIndex)
    subtables = []
    for li in set(lookups):
        lk = gpos.LookupList.Lookup[li]
        for st in lk.SubTable:
            if lk.LookupType == 9: st = st.ExtSubTable
            if getattr(st, 'LookupType', lk.LookupType) == 2 or st.__class__.__name__ == 'PairPos':
                subtables.append(st)
    def lookup(a, b):
        for st in subtables:
            cov = st.Coverage.glyphs
            if a not in cov: continue
            if st.Format == 1:
                ps = st.PairSet[cov.index(a)]
                for pvr in ps.PairValueRecord:
                    if pvr.SecondGlyph == b:
                        v = pvr.Value1
                        return getattr(v, 'XAdvance', 0) or 0 if v else 0
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs.get(a, 0)
                c2 = st.ClassDef2.classDefs.get(b, 0)
                rec = st.Class1Record[c1].Class2Record[c2]
                v = rec.Value1
                x = getattr(v, 'XAdvance', 0) if v else 0
                if x: return x
        return 0
    return lookup

def build(family, weight, text, size, tracking=0, opsz=None, italic=False, x0=0.0, y0=0.0):
    path = fetch(family, weight, opsz, italic)
    font = TTFont(path)
    upm = font['head'].unitsPerEm
    scale = size / upm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    hmtx = font['hmtx']
    kern = kern_pairs(font)
    pen = SVGPathPen(gs, ntos=lambda v: (f"{v:.2f}".rstrip("0").rstrip(".") or "0"))
    bp = BoundsPen(gs)
    x = 0.0
    names = [cmap.get(ord(ch)) for ch in text]
    for i, (ch, gname) in enumerate(zip(text, names)):
        if gname is None:
            sys.exit(f"glyph missing for {ch!r} in {family}")
        t = (scale, 0, 0, -scale, x0 + x * scale, y0)
        gs[gname].draw(TransformPen(pen, t))
        gs[gname].draw(TransformPen(bp, t))
        adv = hmtx[gname][0]
        if i + 1 < len(names):
            adv += kern(gname, names[i + 1])
            adv += tracking * upm / 1000.0
        x += adv
    os2 = font['OS/2']
    hhea = font['hhea']
    return {
        'font_file': path,
        'd': pen.getCommands(),
        'width': x * scale,
        'bbox': list(bp.bounds) if bp.bounds else None,
        'ascender': hhea.ascent * scale,
        'descender': hhea.descent * scale,
        'xHeight': getattr(os2, 'sxHeight', 0) * scale,
        'capHeight': getattr(os2, 'sCapHeight', 0) * scale,
    }

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--family', required=True); ap.add_argument('--weight', type=int, default=400)
    ap.add_argument('--text', required=True); ap.add_argument('--size', type=float, default=100)
    ap.add_argument('--tracking', type=float, default=0); ap.add_argument('--opsz', type=float)
    ap.add_argument('--italic', action='store_true')
    ap.add_argument('--x', type=float, default=0); ap.add_argument('--y', type=float, default=0)
    ap.add_argument('--svg', action='store_true'); ap.add_argument('--fill', default='#000')
    a = ap.parse_args()
    r = build(a.family, a.weight, a.text, a.size, a.tracking, a.opsz, a.italic, a.x, a.y)
    if a.svg:
        b = r['bbox']; pad = a.size * 0.1
        vb = f"{b[0]-pad:.1f} {b[1]-pad:.1f} {b[2]-b[0]+2*pad:.1f} {b[3]-b[1]+2*pad:.1f}"
        print(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><path fill="{a.fill}" d="{r["d"]}"/></svg>')
    else:
        print(json.dumps(r))
