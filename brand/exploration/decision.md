# CodeWeekend logo: decision

2026-10-03 · Creative director

**Inputs:**
- the logo brief and [`../foundation.md`](../foundation.md) (section 7)
- each designer's rationale and self-critique
- the three judging lenses (strategy, craft, distinctiveness) and their test renders
- the contact sheets in this folder (`concept-*.png`), which I looked at myself
- my own prototypes

The repo keeps the outcome: this decision, the presentation board [`shortlist.png`](shortlist.png) and the five concept sheets. The working files (concept sources, judging renders, prototypes) stay in the design workspace.

> **Read with the production spec.** The refinement brief below was the input to production. Where the shipped kit differs (the vector favicon, the nav-lockup boxes, the solid-panel avatars), [`../logo/SPEC.md`](../logo/SPEC.md) section 10 explains why, and the SPEC wins.

## Decision

**Gudiparan, the Bracket Kite, becomes the CodeWeekend logo**, once the refinement brief below is carried out.

This agrees with the panel: the kite has the highest mean (7.17) and no fatal flags, and I do not overrule it. I do reorder the two runners-up (see "Why not the other two"):

| My rank | Concept | Panel mean |
|---|---|---|
| 1 | Bracket Kite | 7.17 |
| 2 | Kilim Commit Grid | 5.33 |
| 3 | Girih Braces | 5.67 (one fatal flag) |

---

## The shortlist

### 1. Gudiparan · the Bracket Kite. Panel mean 7.17

Concept sheet: [`concept-bracket-kite.png`](concept-bracket-kite.png)

| Strategy | Craft | Distinctiveness | Fatal flags |
|---|---|---|---|
| 7 | 7 | 7.5 | 0 |

**Idea.** Two heavy code chevrons, `<` and `>`, built on the girih angles (108°, 90° and 72°), outline an Afghan fighter kite. A saffron panel inside is the light. A gap at the top and bottom vertices is both the bracket break and the kite's bamboo spine. A stitched tail gives lift. In one line: code, craft and lift in one shape, with no person shown.

**Strengths**
- It is the only concept that carries the brand idea, "lift, made by hand", and not only "code".
- The story retells in one line: "two code brackets make an Afghan kite". Kites fly on Fridays, the Afghan weekend.
- It is the only mark that is a specific object rather than a programming glyph, so it can be owned.
- It anchors the foundation's whole imagery system: the hero sky, the Her Kite tiles, the OG card, the Demo Day kite wall and the kite-lattice pattern.
- Its motion is natural: rise, and sway on the string.
- Craft: the best-composed lockup in the set. The stroke is exactly 3.6u, the paths use 1-decimal precision, and the wordmark is a good opsz-48 cut with opened e apertures. The reverse on Night is strong.
- There is no flag, religious or conflict reading.

**Weaknesses**
- The kite reading depends on the tail, and the most-seen instances have none: the nav, stacked and mono lockups. Without the tail it reads as a gem, crest, esports badge, pen nib or map pin.
- In mono it is a solid diamond inside a diamond, which is close to the gem and crypto archetypes.
- Favicon:
  - Its diagonal edges go soft at 16px, and the 4×5px core smears into a plus.
  - At 24px the spine gap is a 1.5px slit that looks like a rendering error.
  - It relies on an SVG media query that ICO and PNG converters ignore.
- The tail dashes break up into grey dust below 64px.
- `mark.svg` uses a square viewBox that includes the tail, so the kite body fills only 60% of it.
- The k slit is invisible below 40px and reads as a stencil "l<" at large sizes.
- Cultural notes:
  - Kite fighting is traditionally a boys' and men's rooftop game.
  - Western press will reach for *The Kite Runner*.
  - A kite can feel slightly childlike to employers.
- Alumni lose the `{ }` they have known since 2014.

### 2. Girih Braces · `code{◆}weekend`. Panel mean 5.67

Concept sheet: [`concept-girih-braces.png`](concept-girih-braces.png)

| Strategy | Craft | Distinctiveness | Fatal flags |
|---|---|---|---|
| 6 | 8 | 3 | 1 |

**Idea.** The community's `{ }`, rebuilt as Herati strapwork in girih angles, with one saffron girih tile between the braces: "the work, held by the community".

**Strengths**
- The best continuity: alumni will see "code{ }weekend, grown up".
- The most instantly legible as "coding" to donors and employers.
- No misreading risk.
- The best small-size craft in the set. The brace shanks are vertical and land on whole pixels, so the 16px favicon reads crisply as `{◆}` on every tab background. The master, favicon and avatar are one drawing.
- Mono holds, and the SVGs are lean.

**Weaknesses**
- Fatal flag from the Distinctiveness lens: at every size that matters, its silhouette cannot be told apart from typed `{◆}`. It refines the generic brace mark that the brief explicitly asks us to replace.
- The Herati craft (flared arms, half-tile nub) is invisible below about 48px.
- The lift idea is absent, and nothing in it speaks to Afghan women and girls.
- The braces are lighter than the letters, and the tile reads as a 6px spark in the nav.
- The lockup is long (7.3:1) and has no stacked version.

### 3. Kilim Gul · the Commit Grid. Panel mean 5.33

Concept sheet: [`concept-kilim-commit-grid.png`](concept-kilim-commit-grid.png)

| Strategy | Craft | Distinctiveness | Fatal flags |
|---|---|---|---|
| 5 | 5 | 6 | 0 |

**Idea.** A 7×7 stepped-diamond kilim gul that is also a contribution graph, with one saffron centre cell for "this weekend's commit". The wordmark is locked to the same grid.

**Strengths**
- The most audience-specific craft reference. Weaving is historically Afghan women's work: "from the loom to the code".
- "Commit" is a credible signal to employers.
- The cell is the most generative atom in the set: it gives the best pattern (a real kilim lattice), data graphics (one cell per graduate), progress bars and weave-in motion.
- The 16px favicon is the only pixel-perfect asset submitted, and the SVG hygiene is exemplary.

**Weaknesses**
- Seen alone, the mark is a pixel diamond, sparkle, 8-bit gem or loading glyph. Recall goes to the genre, not to CodeWeekend.
- The inner ring and centre form a plus or cross, which is a real risk under the no-religious-symbols rule.
- A gold-centred diamond of squares sits near the crypto-exchange archetype.
- It only scales cleanly when pixel-snapped: it smears at 16, 24 and 30px on fractional-DPR phones.
- Weaving is also one of the few kinds of work still allowed to Afghan women, so press can frame "loom to code" as confinement.
- It does not express lift.

---

## Why the Bracket Kite

1. **It is the only mark that carries the brand.** The foundation's idea is "lift, made by hand", and every imagery system already built on it uses kites:
   - the hero sky over the Hindu Kush
   - the Her Kite portraits that replace faces
   - the Demo Day kite wall where 30 graduates become 30 kites
   - the OG card

   The logo is the seed of that system. Any other mark leaves the centre of the system empty, or forces a second symbol.
2. **It is ownable.** It is a specific Afghan object, not a programming glyph or a UI convention. The `< >` reading is a reveal rather than a requirement: "Look closer. The kite is two code brackets." Non-developers get a kite. Developers get a kite and a wink.
3. **Its weaknesses can be fixed in the drawing; the others' cannot.** The kite's problems are all about execution:
   - where the tail appears
   - favicon hinting
   - mono
   - one glyph edit

   I prototyped the two biggest fixes, a tail in every lockup and a spine through the panel. They work: the kite reads as a kite in the nav, in mono and in the avatar. The Girih Braces' flaw (it *is* the trope) and the Kilim mark's flaw (it is generic on its own) are conceptual, and no amount of refinement removes them.
4. **On the craft score.** The craft lens rated Girih Braces 8 against the kite's 7, and I take that seriously. But the craft gaps close in a week of refinement, and the brief's central request, "ownable, warm, credible, specific to CodeWeekend", does not.

**How we handle the cultural notes.**
- We present the gudiparan as a *made object*: craft, patience, parts joined by hand. We do not present it as a re-enactment of the rooftop game. Ownership is shown through the Her Kite tiles, where each graduate's kite is her own. We never write slogans such as "girls fly kites now", which drift toward saviour framing.
- *The Kite Runner* stays banned in copy (foundation section 6).
- Against "childlike": crisp girih geometry, Lapis dominance, a heavy grotesque wordmark, and tails drawn only as straight stitched dashes. Never ribbons, bows or curly strings.

## Why not the other two

**Girih Braces (panel mean 5.67, my rank 3).**
- It carries the only fatal flag of the round, and the flag is against the brief itself: "it reads as generic tech template… should be replaced". At favicon, nav and avatar sizes it is typed `{◆}`.
- Its continuity is real, but continuity of a generic mark is exactly what we were asked to stop.
- I rank it below the kilim, against the panel's order. A fatal flag on the brief's main request outweighs a 0.34 difference in the mean.
- **What we keep:**
  - Its lesson that small sizes need vertical, whole-pixel construction. This is applied to the new favicon below.
  - The `{ }` itself, which lives on as a code glyph in the kilim border band and in the alumni transition line (R11).

**Kilim Commit Grid (panel mean 5.33, my rank 2).**
- The most authentic craft reference and the best pattern system. But as a logo the mark alone is a pixel diamond, and its distinctiveness depends on the system being present around it.
- It carries plus/cross and crypto misreads.
- It is fragile wherever pixel snapping is not guaranteed.
- **What we keep:** the commit-grid cell and the "running water" divider stay in the pattern kit (foundation section 6). They serve as one cell per graduate on the impact page, week 1–12 progress and section dividers. They are a supporting pattern, never a logo.

---

## Refinement brief: the Bracket Kite

**Units.** 1u is 1/24 of the kite's width, which is 10 units in the current files. y runs downward. The x origin is the left vertex.

**Body geometry stays as built:**

| Element | Value |
|---|---|
| Outer polygon | top (12, 0) · right (24, 8.72) · bottom (12, 25.24) · left (0, 8.72) |
| Stroke | 3.6u, mitred side vertices, flat spine cuts |
| Spine gap | 2u |
| Chevron tips | y = 23.86u |
| Saffron panel | (12, 7.54) · (16.08, 10.5) · (12, 16.12) · (7.92, 10.5) |

**Approved deviations** from the written direction, as the designer requested:
- opsz 48 (not 96)
- tracking -15/1000 em
- wordmark x-height centred on the panel axis (y = 10.5u)
- kite-to-wordmark gap of 1.3 × stroke

**Prototypes** (design workspace, not in this repo):
- a tail generator
- the mark, mono mark and lockup with the lockup tail and the spine split
- the nav fit test
- the 16px favicon proposal

### R1. Put the tail in every lockup (the main fix)

**Rule: the tail never hangs straight down.** In prototypes, a tail on the vertical axis read as "!", a pendant or a plumb-bob. A tail always curls off to the left at girih angles, like a kite in wind. Stitches are straight, flat-cut dashes in the body colour. The tassel is a 72°/108° rhombus.

There are three tail lengths, all on one curl:

| Variant | Where it is used | Geometry |
|---|---|---|
| **Lockup tail** (new default) | Horizontal and stacked lockups, `mark.svg`, any kite rendered at 24–95px body height | Stitch 1 starts 0.8u below the chevron tips on the spine axis (x = 12u). It is 2.2u wide × 2.0u long, angled 54° from vertical, down and to the left. Then a 1.0u gap. Stitch 2 is 2.2u × 2.0u at 72°. Then a 1.0u gap. The tassel is 3.0u long × 2.2u wide, with its long axis at 72°. The tail adds ≈5.0u below the tips (about 20% of body height) and stays at x ≥ 3.5u, so it never reaches the wordmark. |
| **Full tail** | Avatars, hero, print, stickers, OG card, any body ≥ 96px | Keep the designer's 18° → 36° → 54° curl, but thicken the stitches from 1.6u to **2.2u** (2.4u long, 1.4u gaps). End with the tassel along **72°**, not plumb. The full tail and the lockup tail are then visibly the same curl at two lengths. |
| **No tail** | Only the favicon tile (≤ 32px) and repeat patterns (kite lattice, Her Kite tiles) | No tail. `mark-notail.svg` leaves the public kit and stays as a pattern source only. |

- **Colour:** the tassel is Pomegranate-600 on light and Pomegranate-300 on dark. In mono, the tassel and stitches take the body colour.
- **Clear space:** 2 × stroke (7.2u), measured from the **body**. The tail may sit inside the clear space.

### R2. Run the spine through the panel

- Add a **1.0u vertical knockout on x = 12u** that splits the saffron panel into two halves. It continues the 2u top and bottom spine gaps as a thinner bamboo spar.
- In prototype, this turned the mono "diamond in a diamond" (the gem and crypto read) into a kite frame. In colour it reads as kite paper on either side of the spine.
- Apply it at **rendered body height ≥ 48px in every colourway, including mono**. Below 48px the split would be under 1.5px and smear, so the panel stays solid there.
- The split is vertical, so it does not conflict with the rule against stacking Lapis and Saffron horizontally.

### R3. Two size masters, no media queries

| Master | Used for | Drawing |
|---|---|---|
| **Large** | Body ≥ 48px | Stroke 3.6u · spine split (R2) · lockup or full tail |
| **Small** | Body 20–47px: the nav lockup, 32–40px thumbnails, email signatures | Stroke 3.6u · solid panel · lockup tail with stitches widened to **2.6u** and the tassel lengthened to **3.6u**, so every tail element is ≥ 3px at a 36px body |

The favicon is a third, hand-pixelled drawing (R6).

### R4. Wordmark

- Keep these: Bricolage Grotesque 800, opsz 48, tracking -15/1000 em with GPOS kerning, one colour (Ink on light, Paper on dark), and the opened e apertures (terminal cut moved 30 units).
- **Remove the k slit and restore the stock opsz-48 k.** The slit cannot be seen below 40px, reads as a stencil "l<" at display sizes, and gives no legibility gain. The mark already carries the spine.
- Re-instance from the variable font with an **integer** opsz. `text2path.py` passes a float, which Google rejects silently.
- Check that "ee", "we" and "nd" stay open at 14, 16 and 20px font size, on Paper and on Night.

### R5. Lockups

**Horizontal (primary)**
- Keep the designer's composition: wordmark at 18u, x-height centred on y = 10.5u, gap 1.3 × stroke from the right side vertex.
- Add the lockup tail.
- **In the 64px nav:** use the Small master with a 36px body, and put the panel axis on the bar centre (y = 32px). The tail then ends at about 58px, inside the bar, as verified in the nav fit test.
- Ship `logo.svg` with a viewBox cropped to body + tail + wordmark. Document the CSS height that gives a 36px body.

**Stacked**
- The kite (with the lockup tail) is centred above the wordmark.
- The gap is 2 × stroke (7.2u) from the chevron tips to the wordmark's ascender line. The 5.0u tail curls into the empty space above "co" and keeps at least 2u of clearance.

**Every lockup** comes in light, reverse (Night, and Lapis-900 or Lapis-600) and mono. Mono keeps the tail and, at Large, the spine split. **There is no tail-less lockup.**

### R6. Favicon set

**Delete the `<style>` media query.** Ship separate, purpose-drawn files.

**`favicon.svg` (the 16-grid master)** is hand-pixelled and built from `shape-rendering="crispEdges"` rect runs. It sits on a Night tile with a 3px radius.
- The ring is a 45° stepped rhombus, **2px horizontal** (about 1.4px perpendicular). It is lighter than the current ring.
- The core is a **2-4-6-4-2 pixel diamond** in Saffron-400, with a 1px Night gap inside the ring.
- There are no spine gaps and no tail.
- The browser draws it at 16 CSS px, and it doubles cleanly at 2× DPR.
- Pixel map (L = Lapis-200 `#C8D9FF`, S = Saffron-400, N = Night).

```
   0123456789012345
 0 NNNNNNNNNNNNNNNN
 1 NNNNNNNLLNNNNNNN
 2 NNNNNNLLLLNNNNNN
 3 NNNNNLLNNLLNNNNN
 4 NNNNLLNSSNLLNNNN
 5 NNNLLNSSSSNLLNNN
 6 NNLLNSSSSSSNLLNN
 7 NNLLNNSSSSNNLLNN
 8 NNNLLNNSSNNLLNNN
 9 NNNNLLNNNNLLNNNN
10 NNNNLLNNNNLLNNNN
11 NNNNNLLNNLLNNNNN
12 NNNNNNLNNLNNNNNN
13 NNNNNNLLLLNNNNNN
14 NNNNNNNLLNNNNNNN
15 NNNNNNNNNNNNNNNN
```

**Do not add any 1–2px stem, tail or tassel pixel under the core.** In testing it turned the core into a keyhole.

**Other files in the set**

| File | Specification |
|---|---|
| `favicon.ico` | Contains the 16px drawing above plus a **32-grid redraw**. In the redraw the ring is 3px, the spine gaps are exactly 2px on whole pixels (x = 15–16), the core is solid, and there are no 1.5px slits. Spine gaps appear from a 32px tile upward, never at 24px. |
| `apple-touch-icon.png` (180) | Night ground, Large master with the lockup tail |
| `icon-192.png`, `icon-512.png` | Same as the apple-touch icon |
| `icon-512-maskable.png` | Same, with the kite and tail inside the central 80% safe zone |
| `mask-icon.svg` | One-colour version |

### R7. `mark.svg` viewBox

- `mark.svg` is the Large master with the lockup tail. Its viewBox is tight to body + tail + 1u. It is **not square**, so the body fills the box.
- Add `mark-full.svg` (full tail) and its reverse, for hero and print.
- Add `mark-square.svg` for square slots: body at 64% of the height, body centre 46% from the top, tail inside.

### R8. Avatar

- The **default social avatar is the flying variant**: 8° clockwise, full tail, Night ground, Paper chevrons, saffron panel with the spine split, Pomegranate-300 tassel, body at 56–58% of the height. Bake the rotation into the paths; do not use `transform`.
- It must survive a circle crop: everything inside the inscribed circle with at least 6% margin. Test it as a 40px circle thumbnail.
- The upright avatar is the alternate, for example for the GitHub org.

### R9. Colour

No change from foundation section 7:

| Ground | Body | Panel | Tassel |
|---|---|---|---|
| Paper or white | Lapis-600 | Saffron-400 | Pomegranate-600 |
| Night, Lapis-900 or Lapis-600 | Paper | Saffron-400 | Pomegranate-300 |

- Never put a Lapis body on Night (2.24:1).
- Never place the logo on a saffron field.
- No green, ever.

### R10. File hygiene

Every SVG must meet all of these:
- a viewBox, with no fixed width or height
- a `<title>` and an `aria-label="CodeWeekend"`
- 1-decimal coordinates
- no `<style>`, `<text>`, filters, rasters or transforms
- `dir="ltr"` wherever it is inlined

Rebuild everything from one script so the masters stay in sync.

### R11. Story and usage guardrails (for the guidelines page)

- **One-line story:** "Two code brackets, `<` and `>`, make an Afghan kite. Learners build it; the community holds the string."
- Never draw a flyer or hands. Never draw the tail as a ribbon, bow or curly string. Never reference *The Kite Runner*.
- **Alumni continuity:**
  - Launch post: "code{ }weekend is now codeweekend: same community, since 2014."
  - For six months the footer reads: "codeweekend · since 2014, formerly code{ }weekend". It is set in Atkinson Mono.
  - `{ }` stays in the system as a glyph in the kilim border band and in code-comment eyebrows.
- **Sub-brands:** the horizontal lockup plus an Atkinson Mono descriptor, for example `DEMO DAY 2026`. No `demo{◆}day` constructions.

### Acceptance tests (all must pass before the logo is final)

1. **Misread test.** Rerun the strategy lens's misread board: the one-colour mark and lockup at 80px and 28px, beside the badge, crypto-diamond, nib and gem archetypes. A fresh panel of three must name "kite" first, unprompted, for the mark with the lockup tail.
2. **Nav test.** In the 64px bar at 1× and 2×, with a 36px body, nothing crosses the bar edges. The centre of the wordmark x-height is within ±1px of the bar centre.
3. **Favicon test.** At 16px and 1× on paper, white, light tab-bar, dark tab-bar and Night, there are no anti-aliased pixels inside the tile. It reads as a diamond with a gold diamond, not a plus and not a keyhole.
4. **Tail survival.** In the 48px and 64px marks at 1×, every stitch is at least 2px wide and the tassel is at least 4px long.
5. **Mono.** At 24, 48 and 160px the mono mark reads as a kite, with the spine visible from 48px.
6. **Avatar.** The 40px circle crop keeps the whole kite and tail.
7. **Files.** Valid XML and the R10 checks pass. Rerun the standard contact sheet and the three judges' test renders on the refined files.

### Deliverables

| Group | Files |
|---|---|
| Mark | `mark.svg`, `mark-reverse.svg`, `mark-mono.svg`, `mark-full.svg`, `mark-full-reverse.svg`, `mark-square.svg` |
| Horizontal lockup | `logo.svg`, `logo-reverse.svg`, `logo-mono.svg` |
| Stacked lockup | `logo-stacked.svg`, `logo-stacked-reverse.svg`, `logo-stacked-mono.svg` |
| Avatar | `avatar-flying.svg`, `avatar.svg` |
| Favicon and app icons | `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `icon-512-maskable.png`, `mask-icon.svg` |
| Build and sheet | the build script, and the refreshed `sheet.png` |

Also update foundation section 7.1 to match:
- tail rules (R1)
- spine split (R2)
- size masters (R3)
- k restored (R4)
- favicon set (R6)
