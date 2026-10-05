---
title: "Brand & press kit"
description: "The CodeWeekend logo, colours and typefaces, ready to download. For journalists, partners, and anyone writing about us or making something with us."
styles:
  - "css/brand-kit.css"

# Logo downloads. Every file lives in static/brand/ and is served from /brand/.
# `previews` sets the ground each preview sits on: paper, white or night.
downloads:
  - name: "Primary logo"
    use: "Our default logo. Use it on Paper, white or light photos."
    note: "Under about 270 px wide (headers, logo walls), use the small-size file: its tail is drawn heavier and it centres cleanly."
    previews:
      - { file: "logo.svg", ground: "paper" }
    files:
      - { label: "Full colour", file: "logo.svg" }
      - { label: "Full colour", file: "logo-1200.png" }
      - { label: "Small sizes", file: "logo-small.svg" }
  - name: "Reverse logo"
    use: "For Night, deep Lapis and dark photos."
    previews:
      - { file: "logo-reverse.svg", ground: "night" }
    files:
      - { label: "Reverse", file: "logo-reverse.svg" }
      - { label: "Reverse", file: "logo-reverse-1200.png" }
      - { label: "Small sizes", file: "logo-small-reverse.svg" }
  - name: "One colour"
    use: "For one-colour print, engraving, embroidery and stamps."
    previews:
      - { file: "logo-small-mono-ink.svg", ground: "white" }
      - { file: "logo-small-mono-white.svg", ground: "night" }
    files:
      - { label: "Ink", file: "logo-mono-ink.svg" }
      - { label: "White", file: "logo-mono-white.svg" }
  - name: "Stacked logo"
    use: "For square spaces: posters, social posts, stickers."
    previews:
      - { file: "logo-stacked.svg", ground: "paper" }
      - { file: "logo-stacked-reverse.svg", ground: "night" }
    files:
      - { label: "Full colour", file: "logo-stacked.svg" }
      - { label: "Reverse", file: "logo-stacked-reverse.svg" }
      - { label: "Full colour", file: "logo-stacked-1200.png" }
      - { label: "Reverse", file: "logo-stacked-reverse-1200.png" }
  - name: "Kite mark"
    use: "The kite on its own, when our name is already close by. Keep it at least 20 px tall."
    previews:
      - { file: "mark.svg", ground: "paper" }
      - { file: "mark-reverse.svg", ground: "night" }
    files:
      - { label: "Full colour", file: "mark.svg" }
      - { label: "Reverse", file: "mark-reverse.svg" }
      - { label: "Square", file: "mark-512.png" }
      - { label: "Square reverse", file: "mark-reverse-512.png" }
  - name: "Social avatar"
    use: "For profile pictures. The kite stays inside a circle crop."
    previews:
      - { file: "avatar-flying.svg", ground: "avatar" }
    files:
      - { label: "Avatar", file: "social-avatar-800.png" }
      - { label: "Avatar", file: "avatar-flying.svg" }
      - { label: "Upright", file: "avatar.svg" }

# Core palette. Tokens match assets/css/main.css; full ramps are in brand/foundation.md.
palette:
  - group: "Brand colours"
    colours:
      - { name: "Lapis", token: "--lapis-600", hex: "#2347B4", rgb: "35 71 180", role: "The brand colour: the logo, links and buttons." }
      - { name: "Saffron", token: "--saffron-400", hex: "#F5A71E", rgb: "245 167 30", role: "The light: the kite panel and one bright accent. Never text on Paper." }
      - { name: "Pomegranate", token: "--pomegranate-600", hex: "#B4223B", rgb: "180 34 59", role: "Celebration and urgency, used sparingly." }
      - { name: "Firuza", token: "--firuza-600", hex: "#116B82", rgb: "17 107 130", role: "Tile turquoise for tags and small details." }
  - group: "Neutrals"
    colours:
      - { name: "Paper", token: "--paper", hex: "#FBF7EF", rgb: "251 247 239", role: "The default background, like undyed wool." }
      - { name: "Sand", token: "--sand", hex: "#EADFCB", rgb: "234 223 203", role: "Bands, table stripes and pattern tints." }
      - { name: "Ink", token: "--ink", hex: "#1B2034", rgb: "27 32 52", role: "Body text and headings." }
      - { name: "Night", token: "--night", hex: "#0E1630", rgb: "14 22 48", role: "Dark sections, the footer and the avatar ground." }
---

### About CodeWeekend

Use this short description when you write about us. You can shorten it, but please keep the facts as they are.

> CodeWeekend is an inclusive community of developers. It was founded in Kabul in 2014 and is now a registered non-profit society in British Columbia, Canada. CodeWeekend runs free, fully live coding programs for Afghan learners. Its 2026 Web & AI Development Bootcamp is a 12-week program for women and girls in Afghanistan, taught live by working developers.

**One line:** CodeWeekend has taught free, live coding classes to Afghan learners since 2014.

### How to write our name

Write **CodeWeekend**: one word, with a capital C and a capital W. Please don't write "Code Weekend", "Codeweekend" or "code{&nbsp;}weekend". The lowercase *codeweekend* appears only inside the logo.
