# CodeWeekend logo: production specification

**Gudiparan, the Bracket Kite** · v1.1 · 2026-10-03 · every file comes from one build script, so the masters stay in sync (section 8 says where each file lives)

v1.1 (QA round) changes the favicon set, the nav-lockup boxes, the avatars and the maskable icon, and cleans the wordmark outlines. The reasons are in section 10, items 8–12.

> **Two code brackets, `<` and `>`, make an Afghan kite. Learners build it; the community holds the string.**

The kite is a made object: parts joined by hand, with patience. We never draw a flyer, hands, ribbons, bows or curly strings, and we never reference *The Kite Runner*.

Visual references, in this folder: [`sheet.png`](sheet.png) (standard contact sheet) and [`construction.png`](construction.png) (grid and geometry). The acceptance-test results are summarised in section 9. Brand context: [`../foundation.md`](../foundation.md); team guidelines: [`../README.md`](../README.md).

---

## 1. Construction

**Units.** 1u = 1/24 of the kite's width (10 units in the files). y runs downward. x = 0 is the left side vertex. **Body height** = the outer kite polygon height, 25.24u. Every size in this document ("a 36px body") refers to that height.

| Element | Value |
|---|---|
| Outer polygon | top (12, 0) · right (24, 8.72) · bottom (12, 25.24) · left (0, 8.72). Angles: 108° top, 90° sides, 72° bottom (girih set) |
| Chevrons `<` `>` | stroke 3.6u (15% of the width), mitred side vertices, flat vertical cuts at the spine |
| Spine gap | 2u at the top and bottom vertices. Ink runs from y 0.73u to the chevron tips at y 23.86u |
| Saffron panel | the kite × 0.34: (12, 7.54) · (16.08, 10.5) · (12, 16.12) · (7.92, 10.5). Its side vertices sit on the **panel axis, y = 10.5u** |
| Spine split (R2) | a 1.0u vertical knockout on x = 12u splits the panel in two, continuing the spine as a bamboo spar. Large master only (body ≥ 48px), in every colourway including mono |

### Tails (R1)

The tail never hangs straight down. It always curls left at girih angles. Stitches are straight, flat-cut rectangles in the body colour. The tassel is a 72°/108° rhombus. **Every gap in a tail is a true clearance**: the minimum distance between neighbouring pieces, not a centreline offset (see section 10).

| Tail | Used for | Geometry |
|---|---|---|
| **Lockup tail** (Large) | every lockup, `mark.svg`, any kite at 48–95px body | Stitch 1 has its origin on x = 12u and sits 0.8u clear of the chevron tips. Stitches are 2.2u wide × 2.0u long, at 54° and then 72° from vertical, down and left, with 1.0u clearances. The tassel is 3.0 × 2.2u, its long axis at 72°, 1.0u clear of stitch 2. It adds 5.6u below the tips and stays at x ≥ 3.4u |
| **Lockup tail** (Small) | the Small master, 20–47px body (nav) | Same curl, with 2.6 × 2.2u stitches and a 3.6 × 2.6u tassel, so every element is ≥ 3px at a 36px body (3.7 × 3.1px stitches, 5.1 × 3.7px tassel, 1.4px gaps). It adds 6.3u below the tips |
| **Full tail** | avatars, hero, print, stickers, OG card, any body ≥ 96px | The 18° → 36° → 54° curl. Stitches 2.2 × 2.4u with 1.4u clearances, 1.0u clear of the tips. The tassel is a girih rhombus 3.56 × 2.59u (side 2.2u) lying along 72° |
| **No tail** | only the favicon tile and repeat patterns (kite lattice, Her Kite tiles) | The tail-less kite is a pattern source only. It is not part of the public kit |

### Size masters (R3): two drawings, no media queries

| Master | Body height | Drawing | Files |
|---|---|---|---|
| **Large** | ≥ 48px · ≥ 12mm in print | split panel + lockup tail (full tail at ≥ 96px / 25mm) | `logo*.svg`, `logo-stacked*.svg`, `mark.svg`, `mark-mono*.svg`, `mark-reverse.svg`, `mark-square*.svg`, `mark-full*.svg` |
| **Small** | 20–47px · 5–12mm in print | solid panel + Small lockup tail | `logo-small*.svg`, `logo-inline.svg`, `mark-small*.svg` |
| **Favicon** | 16–48px tiles | no tail. A vector tile built on the master angles (`favicon.svg`), plus hand-pixelled 16/32/48 frames inside `favicon.ico` | `static/favicon.svg`, `static/favicon.ico` |
| **Avatar** | displayed at 24–48px, sometimes larger | Small master's solid panel + full tail | `avatar-flying.svg`, `avatar.svg`, `social-avatar-800.png` |

### Wordmark (R4)

- `codeweekend`, lowercase, Bricolage Grotesque 800. It is re-instanced from the Google variable font at an **integer opsz of 48**, which avoids a silent float-opsz bug in the outlining tool. Tracking is -15/1000 em, with GPOS kerning applied.
- **Clean outlines.** The stock opsz-48 `e` is one self-intersecting contour: its crossbar is drawn through the bowl. Every glyph is boolean-unioned first (exact for lines and quadratics), so the `e` becomes an outer contour plus a reversed eye. Then the aperture is cut, then collinear nodes are merged and sub-3-unit micro-segments dropped. Result: 0 self-intersections in all 30 SVGs, and even-odd fills render pixel-identical to nonzero. The files are safe in Illustrator, Figma, Inkscape, cutters, embroidery software and icon-font tools.
- The e terminals are cut 30 units lower, which opens the apertures. **The k is stock**: the slit is gone.
- "ee", "we" and "nd" stay open at 14, 16 and 20px on Paper and on Night.
- One colour only: Ink on light, Paper on dark.

### Lockups (R5)

- **Horizontal.** The wordmark is set at 18u. Its x-height (9.5u) is centred on the panel axis, y = 10.5u. The gap from the right side vertex to the first ink of the "c" is 1.3 × stroke (4.68u). The lockup tail hangs below the kite.
  - **Large master** (`logo*.svg`, print, press, hand-placed layouts): the viewBox is cropped to the ink plus 1u on every side. Because the tail hangs, the box centre (y = 151) sits 4.6u below the x-height centre. When a slot centres the box automatically, offset it with `translate: 0 15%`.
  - **Small master** (`logo-small*.svg`, `logo-inline.svg`: nav, CMS headers, logo walls): the box is **symmetric about the panel axis**, which is also the x-height centre. Padding is 1u at the left, right and bottom, and the top is extended to match. Plain centring (`align-items: center`, a CMS header, a sponsor-wall cell) therefore puts the wordmark on the slot's centre line, with the kite hanging below it. No offsets or magic margins are needed.
- **Stacked.** The wordmark's ink width is 3.4 × the kite's width. The kite axis sits on the wordmark's ink centre. The gap from the chevron tips to the ascender line is 2 × stroke (7.2u). The tail curls over "we", which has no ascenders. Its ink clearance to the wordmark is 3.9u.
- **There is no tail-less lockup.**

---

## 2. Clear space

**Clear space is 2 × stroke = 7.2u on every side, measured from the visible body**, and for lockups from the body plus the wordmark. The tail may sit inside it (dashed boxes in `construction.png`). At a 36px body that is 10.3px. At a 48px body it is 13.7px.

## 3. Minimum sizes

| Use | Screen | Print |
|---|---|---|
| Horizontal lockup | body 20px (`logo-small.svg` CSS height 32.8px, 116px wide; the box includes its centring space) | body 5mm (lockup about 29mm wide) |
| Stacked lockup | body 48px (CSS height 79px) | body 12mm |
| Mark alone | body 20px (`mark-small.svg`); below that, use the favicon | body 5mm |
| Full-tail mark, avatar art | body 96px | body 25mm |
| Favicon | 16px (`favicon.svg`, `favicon.ico`) | not for print |

## 4. Nav: recommended sizes

Use the **Small master**: `logo-inline.svg` pasted inline, or `logo-small.svg` as an `<img>`. Its box is symmetric about the panel axis, so **plain vertical centring** puts the wordmark's x-height on the bar centre. You need no offsets. Measured with `align-items: center`: an x-height centre of 32.0px in a 64px bar at 1×, and 64.0px in a 128px bar at 2×.

| Bar | Body | CSS height × width | Ink rows | Tassel to bar bottom |
|---|---|---|---|---|
| **64px (recommended)** | 36px | **59.06 × 208.87px** | 18–60px | 3.9px (2.7u; the minimum is 1u = 1.4px) |
| 72px | 40px | 65.62 × 232.07px | 20–67px | 4.8px |
| 72px (same logo as 64) | 36px | 59.06 × 208.87px | 22–64px | 7.9px |

For any body B, the CSS height of `logo-small.svg` / `logo-inline.svg` is 1.6406 × B, and the width is 5.8019 × B. `logo.svg` (tight box) is 1.2193 × B high.

```html
<!-- header: paste logo-inline.svg inside the link. Keep the logo LTR in RTL mode. -->
<a class="brand" href="/" dir="ltr"><svg …logo-inline.svg…></svg></a>
```
```css
.site-nav { height: 64px; display: flex; align-items: center; }
.brand { line-height: 0; }
.brand svg { display: block; width: 208.87px; height: 59.06px; }
/* dark footer: recolour the same inline SVG */
.site-footer { --logo-mark: #FBF7EF; --logo-word: #FBF7EF; --logo-accent: #F4858A; } /* panel stays Saffron */
```
For the alumni footer, run "since 2014, formerly code{ }weekend" in Atkinson Hyperlegible Mono beside the logo for six months.

`logo-inline.svg` colour hooks (with the light defaults) are `--logo-mark` (chevrons and stitches, #2347B4), `--logo-panel` (#F5A71E), `--logo-accent` (tassel, #B4223B) and `--logo-word` (#1B2034). Checked in Chrome in a 64px header and footer with the CSS above.

**Other auto-centred slots** (CMS headers, sponsor walls, partner cards). Up to a 47px body, which means a lockup up to about 270px wide, use `logo-small*.svg`: it centres correctly as it is. Above that, `logo.svg` is a tight crop. Either place it by its x-height, or add `translate: 0 15%` so that its panel axis lands on the slot's centre line.

## 5. Favicon and app icons (R6)

```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#FBF7EF">
```
```json
"icons": [
  { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
  { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" },
  { "src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
]
```

These files live in `static/` and are served from the site root; `static/site.webmanifest` lists the app icons. The design master set also has `mask-icon.svg` (one colour, for legacy Safari pinned tabs) and `favicon-16/32/48.png` (the ICO frames as PNGs). They are not shipped in this repo, and the site does not need them.

The SVG is the icon modern browsers (Chrome, Edge, Firefox) show at every DPR. The ICO serves Safari, legacy browsers and Windows shortcuts. Keep `sizes="32x32"` on the ICO link, so that Chrome does not prefer the ICO over the SVG.

*Alternative (pixel-exact at 1× and 2×):* drop the SVG link and serve `favicon.ico` with `sizes="16x16 32x32 48x48"`. Browsers then show the hand-pixelled 16 frame at 1× and the 32 frame at 2×. At 1.25–1.75× they downsample the 32 frame, which is softer than the native SVG render. The default above favours the SVG, because 125% and 150% are the Windows laptop defaults.

| File | Drawing |
|---|---|
| `favicon.svg` | **Vector, master angles, no rendering hints.** A 32-unit Night tile, radius 6 (3px at 16). The kite follows the master construction: height 28 units with the apex at y = 2; 108°/90°/72° angles; a Lapis-200 ring of 3.6u (15% of the width); 2-unit spine gaps on x = 15–17, whole pixels at 32 and 64px. The Saffron panel is solid, at 0.38 of the kite (opened slightly from 0.34 for 16–24px), with its side vertices on the master panel axis 1.78u below the shoulder. No tail. Browsers rasterise it natively at every DPR, so it stays mirror-symmetric: 0 pixels off by more than 10% at 16, 18, 20, 24, 28, 30 and 32 device px. **What each DPR shows:** at 2× the bracket kite with crisp 2px spine gaps (the same drawing as the ICO 32 frame); at 1.25–1.75× the same kite, anti-aliased evenly; at 1× the kite with a soft 1px spine. Use the ICO-only alternative above if the 1× tab must be pixel-exact |
| `favicon.ico` | Three hand-pixelled frames with no anti-aliasing inside the tile, on the master angles. **32 and 48:** the vector drawing thresholded at 50% coverage, then hand-cleaned. Upper edges step 1,2,1,2,1,1,2,1 (36°) and lower edges 1,1,1,0 (54°). The shoulder is at 34% of the ink height. The ring is 4–5px perpendicular (15%). The kite-shaped core is 38% of the width, with its widest row just below the shoulder. 2px spine gaps run on x = 15–16 (32) and x = 23–24 (48). **16:** drawn by hand (thresholding gives a cross-shaped core), with 36°/54° steps, a 3px upper and 2px lower ring (equal perpendicular weight), a 2-4-6-4-2 Saffron diamond whose widest row sits on the shoulder, a solid tip, and no spine gap (R6) |
| `apple-touch-icon.png` 180 · `icon-192.png` · `icon-512.png` | Opaque Night ground. Large master with the lockup tail, reverse colours. The ink box is centred with 17.8% padding top and bottom (23% at the sides). The spine sits at 50.0% of the width |
| `icon-maskable-512.png` | Full-bleed Night. **The body axis is on x = 256**, as in `icon-512.png`, with the spine at 50.0%. The height is chosen so that kite and tail fit the smallest centred circle, scaled to a 36% radius inside the 40% safe zone. The body is 58.9% of the side |
| `avatar-flying.svg` / `social-avatar-800.png` | **The default avatar.** Rotated 8° clockwise, with the rotation baked into the coordinates. Full tail, Night ground, Paper chevrons, Pomegranate-300 tassel, and the **Small master's solid Saffron panel**. Avatars display at 24–48px (body 14–27px), where the Large master's split turns into a brown streak. The body is 57% of the height. The art fits inside the inscribed circle with an 8.9% margin, and survives a 40px circle crop. Both avatars live in `static/brand/` |
| `avatar.svg` | The upright alternate (for example, for the GitHub org). Solid panel. **The body axis is on x = 200**, as in `mark-square.svg` and the app icons. The body is 57%, with a 7.2% circle margin |

## 6. Colour values per variant (R9: unchanged from the foundation)

| Variant (file suffix) | Ground | Body: chevrons + stitches | Panel | Tassel | Wordmark |
|---|---|---|---|---|---|
| light (none) | Paper `#FBF7EF` or white | Lapis-600 `#2347B4` | Saffron-400 `#F5A71E` | Pomegranate-600 `#B4223B` | Ink `#1B2034` |
| `-reverse` | Night `#0E1630`, Lapis-900 `#0B1C4B` or Lapis-600 `#2347B4` | Paper `#FBF7EF` | Saffron-400 `#F5A71E` | Pomegranate-300 `#F4858A` | Paper `#FBF7EF` |
| `-mono-ink` (`mark-mono`, `mark-small-mono`, `mark-full-mono`) | any light ground | Ink `#1B2034` | Ink | Ink | Ink |
| `-mono-white` | any dark ground or photo | White `#FFFFFF` | White | White | White |
| favicon tile | Night `#0E1630` | ring Lapis-200 `#C8D9FF` | core Saffron-400 `#F5A71E` | — | — |

Contrast: Lapis-600 on Paper is 7.47:1, Ink on Paper 15.08:1, Paper on Night 16.71:1, and Lapis-200 on Night 12.61:1.

## 7. Do and don't

| Do | Don't |
|---|---|
| Use the Small master for any body of 20–47px, and the Large master from 48px. Avatars always use the solid panel | Use a media query to switch masters, or scale the Large master's split panel below 48px |
| Keep the tail in every lockup, curling left | Remove the tail from a lockup, hang it straight down, or draw it as a ribbon, bow or curly string |
| Centre `logo-small*` / `logo-inline` plainly: their box is symmetric about the panel axis | Centre the tight `logo.svg` box in a bar or slot without offsetting it (`translate: 0 15%`). The hanging tail makes that box bottom-heavy |
| Use the reverse files on Night, Lapis-900 or Lapis-600 | Put a Lapis body on Night (2.24:1) |
| Put the logo on Paper, white, Night or the Lapis grounds | Place the logo on a saffron field, or stack Lapis and Saffron as two equal fields |
| Recolour only through the published variants or the `--logo-*` variables | Use green anywhere; build a black, red and green trio; add gradients, glows, shadows or outlines |
| Keep it LTR (`dir="ltr"`) on RTL pages | Mirror, rotate (except the baked avatar), skew or re-space the wordmark |
| Sub-brands: the lockup plus an Atkinson Mono descriptor, for example `DEMO DAY 2026` | Build `demo{◆}day`-style constructions, or put a person, flyer or hands with the kite |
| Present the kite as a made object (craft) | Use "girls fly kites now" slogans or any *Kite Runner* reference |

**Story and continuity.**
- The launch line is "code{ }weekend is now codeweekend: same community, since 2014."
- For six months the footer carries "since 2014, formerly code{ }weekend" in Atkinson Hyperlegible Mono.
- `{ }` lives on as a glyph in the kilim border band and in code-comment eyebrows.

## 8. File index

**Where the files live**

| Folder | Contents | Public URL |
|---|---|---|
| `static/brand/` | The public logo kit: every SVG below, the avatars, `social-avatar-800.png` and the PNG exports | `https://codeweekend.net/brand/<file>`, listed on the [Brand & press kit page](https://codeweekend.net/brand/) |
| `static/` | `favicon.svg`, `favicon.ico`, the app icons and `site.webmanifest` | site root |
| `brand/logo/` | This spec, `logo-inline.svg` (for pasting into templates), `sheet.png`, `construction.png` | not published |

The build script lives in `brand/logo/src/` (`build.py` with `geom.py` for geometry and the outlined wordmark, `outline.py` for the glyph union, `favgrid.py` for the hand-pixelled favicon maps, `construct.py`, `qa.py`, and the opsz-48 Bricolage Grotesque instance in `fonts/`, SIL Open Font License). Shared render helpers are in `brand/tools/`. Run `python3 brand/logo/src/build.py --svg` (SVGs) or without flags (SVGs, PNGs, ICO, sheets); output lands in `brand/logo/`, then copy production files into `static/` and `static/brand/`. If the drawing must change, regenerate the whole set so every file stays in sync; do not hand-edit one file.

| File | What it is |
|---|---|
| `logo.svg` · `logo-reverse.svg` · `logo-mono-ink.svg` · `logo-mono-white.svg` | Horizontal lockup, Large master (body ≥ 48px). viewBox −10 −2.8 1464.1 307.7 |
| `logo-small.svg` · `logo-small-reverse.svg` · `logo-small-mono-ink.svg` · `logo-small-mono-white.svg` | Horizontal lockup, Small master (nav, CMS headers, logo walls; body 20–47px). viewBox −10 −102 1464.1 414: symmetric about the panel axis y = 105, with 1u at the left, right and bottom |
| `logo-inline.svg` (in `brand/logo/`) | The Small-master lockup for pasting inline, in the same centred box as `logo-small.svg`. Fills use `var(--logo-*, default)`. Includes `role="img"` and `aria-label` |
| `logo-stacked.svg` · `-reverse` · `-mono-ink` · `-mono-white` | Stacked lockup for square, social and OG use. viewBox −10 −2.8 836 415.6 |
| `mark.svg` · `mark-reverse.svg` · `mark-mono.svg` · `mark-mono-white.svg` | Symbol, Large master and lockup tail. The viewBox is tight to body + tail + 1u (260 × 307.7), so it is **not square** (R7) |
| `mark-small.svg` · `-reverse` · `-mono` · `-mono-white` | Symbol, Small master (body 20–47px) |
| `mark-full.svg` · `mark-full-reverse.svg` · `mark-full-mono.svg` | Symbol with the full tail, for hero, print and stickers (body ≥ 96px) |
| `mark-square.svg` · `mark-square-reverse.svg` | Square slot. The body is 64% of the height, with its centre 46% from the top. Lockup tail |
| `avatar-flying.svg` · `avatar.svg` | Social avatars (default and upright alternate). Solid panel |
| `favicon.svg` · `favicon.ico` (in `static/`) | Favicon set: a vector tile (32-unit viewBox) and the hand-pixelled 16/32/48 frames |
| `apple-touch-icon.png` · `icon-192.png` · `icon-512.png` · `icon-maskable-512.png` (in `static/`) | App icons, listed in `static/site.webmanifest` |
| `social-avatar-800.png` | `avatar-flying.svg` at 800 × 800 |
| `logo-1200.png` · `logo-reverse-1200.png` · `logo-stacked-1200.png` · `logo-stacked-reverse-1200.png` · `mark-512.png` · `mark-reverse-512.png` | Transparent PNG exports for people who cannot use SVG. Rendered at exactly these pixel sizes from `logo`, `logo-reverse`, `logo-stacked`, `logo-stacked-reverse`, `mark-square` and `mark-square-reverse` (colours verified exact) |
| `sheet.png` · `construction.png` (in `brand/logo/`) | Contact sheet, and grid and geometry |

Every SVG has outlined paths only, a viewBox with no width or height, `<title>CodeWeekend</title>` with `role="img"` and `aria-label="CodeWeekend"`, and 1-decimal coordinates. None has `<style>`, `<text>`, filters, rasters, transforms or `shape-rendering` hints. No contour self-intersects or overlaps another, so even-odd and nonzero fills are identical. The build's QA step checks these hygiene rules on every run.

## 9. Acceptance tests

| # | Test | Result |
|---|---|---|
| 1 | Misread test with fresh judges | **Not yet run.** The board is ready in the design workspace (mono mark with the lockup tail and the Small master at 80px and 28px, beside the badge, crypto, nib and gem archetypes). It needs a fresh three-person panel. The designer cannot be that panel |
| 2 | Nav at 1× and 2× | Pass, with plain centring and no offsets. The ink spans 18.1–60.1px of 64 at 1× (36–119 of 128 at 2×), and nothing crosses the bar. The x-height centre is off by 0.00px at 1× and at 2× (limit ±1px) |
| 3 | Favicon on paper, white, light tab, dark tab and Night | Pass. `favicon-16.png` (the ICO 16 frame): 0 non-exact interior pixels on all five grounds. It reads as a kite with a gold diamond, not a plus or a keyhole. `favicon.svg` is vector by design (section 10, item 8): 0 mirror failures (> 10%) at 16, 18, 20, 24, 28, 30 and 32 device px. The old crispEdges file failed 5–21 pixels by up to 231 levels at 18–30px |
| 4 | Tail survival at 48–64px | Pass. At 48px: stitches 4.2 × 3.8px, tassel 5.7px, gaps 1.9px. At 64px: 5.6 × 5.1px, tassel 7.6px |
| 5 | Mono at 24, 48 and 160px | Pass (visual check). The spine split shows from 48px |
| 6 | 40px circle avatar | Pass. The whole kite and tail stay inside the circle (8.9% margin for flying, 7.2% for upright; R8 asks ≥ 6%). The solid panel stays clean saffron at 24–48px: in the panel, the dark/brown share is 7/4/3% at 32/40/48px, against 60/50/34% with the split |
| 7 | Valid XML, R10 checks, contact sheet, judges' renders | Pass. All 30 SVGs parse and pass R10, with 0 self-intersections. All 13 wordmark files render pixel-identically under even-odd and nonzero fills. The app icons' spines sit at 50.0%. `sheet.png` and `construction.png` are regenerated. Eleven judge pages are rerun |

## 10. Deviations from the refinement brief, and why

1. **The tail gaps are true clearances.** Taken literally (origin 0.8u below the tips, gaps measured along the centreline), stitch 1's long side passes **0.135u** under the left chevron tip: 0.19px at a 36px body and 0.26px at 48px. The stitch fuses with the tip and plugs the spine gap. The 54°→72° turn also closes the inner corner of the first gap to 0.66u.
   - The origin stays on x = 12u, but it slides down until stitch 1 clears the tips by 0.8u, and every later gap is a true 1.0u.
   - As a result, the lockup tail adds 5.6u below the tips instead of 5.0u. It reaches x 3.4u (Large) and 2.4u (Small) instead of ≥ 3.5u, which is still inside the body's footprint, so no lockup gets wider.
   - The nav tail ends at 60.1px instead of about 58px, still inside the bar.
2. **The Small master's stitches are 2.2u long, not 2.0u.** At a 36px body, 2.0u is 2.85px, which misses R3's own goal of "every element ≥ 3px". 2.2u is 3.14px.
3. **Stacked tail clearance.** The 2 × stroke gap to the ascender line is kept, so the tail bottom is 1.6u above that line. Only x-height letters ("we") sit under the tail, and the true ink clearance is 3.9u. Keeping a 2u distance to the ascender line would have needed a 2.1 × stroke gap.
4. **`mark.svg` is not square.** R7 asks for a tight, non-square viewBox. The kit's file list said "square viewBox". `mark-square.svg` covers square slots.
5. **The favicon ICO has a 48px frame.** R6 defines the 16 and 32 drawings. The kit asked for 16/32/48, so 48 is drawn in the same way (4px ring, 2px gaps).
6. **Naming.** The mono lockups are `logo-mono-ink.svg` and `logo-mono-white.svg`, as the kit list asks, instead of `logo-mono.svg`. The maskable icon ships under both names.
7. **The full tail starts 1.0u clear of the tips** (the designer's drawing started at the bottom vertex, which is 1.04u). Its gaps are true 1.4u clearances, so it is 0.5u longer than the concept. The avatar still clears the circle by 8.9%.

**v1.1, after QA**

8. **`favicon.svg` is vector, not R6's crispEdges 16-grid.**
   - Chrome, Edge and Firefox pick the SVG over the ICO, so they rasterised the 16-grid at every DPR. At 1.25–1.75× each crispEdges edge snapped on its own, so the glyph went lopsided and the core turned into a plus (5–21 mirror failures, up to 231 levels, at 18–30 device px). At 2× retina tabs only ever showed the doubled 16 drawing, which reads as a lightbulb.
   - The SVG is now the master kite itself: true 36°/54° edges, open spine gaps, no rendering hint. It is symmetric at every DPR, and at 2× it matches the 32 frame.
   - The cost: at exactly 1× its 1px spine is anti-aliased (soft). Section 5 gives an ICO-only alternative for teams that want 1× tabs to be pixel-exact.
9. **The 16 frame is redrawn, not the CD's verbatim map.**
   - The old 16, 32 and 48 frames used 45° steps, a shoulder at about 43%, an 8% ring and a 50% rhombus core. That made them a different symbol from the logo: a gem in a thin frame.
   - All three frames now use the master angles. The 32 and 48 frames come straight from the vector drawing.
   - The 16 frame keeps R6's rules (no spine gap, a 2-4-6-4-2 diamond, nothing under the core). Its 5-row diamond needs the rows, so its shoulder sits at 42% of the height.
10. **The nav-lockup boxes are not tight at the top.** `logo-small*` and `logo-inline` extend their top padding so the box is symmetric about the x-height centre. Default centring (flex, CMS headers, logo walls) then aligns the wordmark with the text beside it, which the old `margin-top: 16.62px` recipe did only by hand. The Large-master lockups stay tight, as R5 asks, because they are the print and layout masters.
11. **The avatars use the solid panel.** R8 asked for the split panel. Avatars, however, display at 24–48px, inside the Small master's range, and there the 1u split read as a brown streak (34–60% of panel pixels dark at 32–48px).
12. **Axis-centred placements.** `avatar.svg` and `icon-maskable-512.png` put the body axis on the canvas centre, like `mark-square.svg` and the other app icons, instead of centring the minimum enclosing circle. That rule had pushed the body 7.8% right (avatar) and to 53.2% (maskable) to balance the left-curling tail.
