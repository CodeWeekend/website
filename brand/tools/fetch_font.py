#!/usr/bin/env python3
"""fetch_font.py "Family Name" WEIGHT [--opsz N] [--italic]
Downloads a static instance of a Google Font at the given weight (and optical size, if the family has opsz)
into ../fonts/ and prints the local path. Cached."""
import sys, os, re, urllib.request, argparse, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', 'fonts')
os.makedirs(FONTS, exist_ok=True)

def fetch(family, weight, opsz=None, italic=False):
    key = f"{family}-{weight}-{opsz}-{'i' if italic else 'n'}".replace(' ', '_')
    out = os.path.join(FONTS, key + '.woff2')
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        return os.path.abspath(out)
    fam = family.replace(' ', '+')
    axes, vals = [], []
    if italic: axes.append('ital'); vals.append('1')
    if opsz is not None: axes.append('opsz'); vals.append(str(opsz))
    axes.append('wght'); vals.append(str(weight))
    url = f"https://fonts.googleapis.com/css2?family={fam}:{','.join(axes)}@{','.join(vals)}"
    def get_css(u):
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'})
        return urllib.request.urlopen(req, timeout=30).read().decode()
    try:
        css = get_css(url)
    except Exception:
        # family may lack opsz/ital axis: retry with weight only
        css = get_css(f"https://fonts.googleapis.com/css2?family={fam}:wght@{weight}")
    blocks = re.findall(r'/\* ([a-z\-]+) \*/\s*@font-face \{(.*?)\}', css, re.S)
    pick = [b for name, b in blocks if name == 'latin'] or [css]
    m = re.search(r'url\((https://[^)]+)\)', pick[0])
    if not m:
        sys.exit(f"no font url in css for {family}: {css[:300]}")
    data = urllib.request.urlopen(urllib.request.Request(m.group(1), headers={'User-Agent': 'Mozilla/4.0'}), timeout=60).read()
    with open(out, 'wb') as f: f.write(data)
    return os.path.abspath(out)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('family'); ap.add_argument('weight', type=int)
    ap.add_argument('--opsz', type=float); ap.add_argument('--italic', action='store_true')
    a = ap.parse_args()
    print(fetch(a.family, a.weight, a.opsz, a.italic))
