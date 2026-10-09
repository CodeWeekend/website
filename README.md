# CodeWeekend

The website for [CodeWeekend](https://codeweekend.net) — an inclusive community of developers, founded in Kabul in 2014, now incorporated as a non-profit society in British Columbia, Canada. The 2026 program is a 12-week Web & AI Development Bootcamp for women and girls in Afghanistan.

Built with Hugo. Hosted on GitHub. Deployed via Coolify.

## Stack

- **[Hugo](https://gohugo.io/)** static site generator (extended, v0.140.0)
- **Markdown** for all content (no CMS)
- **Custom theme** in `layouts/` — no external theme dependency
- **Google Translate** widget for Dari (دری) and Pashto (پښتو), with automatic RTL switching
- **Caddy** in production (HTTP/2, gzip, zstd, security headers)
- **GitHub Actions** for CI (build check, accessibility audit, Lighthouse)
- **Coolify** for self-hosted deployment

## Brand

The site applies the **Weekend W** identity (brand kit v1.1). Start with [`brand/START-HERE.txt`](brand/START-HERE.txt) and the nine-page guide [`brand/codeweekend-brand-guide.pdf`](brand/codeweekend-brand-guide.pdf).

- **Colour:** `assets/css/main.css` uses the `--cw-*` tokens from [`brand/tokens.css`](brand/tokens.css) — Cream canvas, Ink text, Vermilion for the W and graphic highlights (never text on Cream), Rust primary buttons, Rust Dark underlined links.
- **Type:** Manrope (800 headlines, 400–500 body, 18 px / 1.6), Atkinson Hyperlegible Mono 500 for short labels, Vazirmatn for Dari and Pashto — all from Google Fonts.
- **Logo:** `layouts/partials/logo.html` inlines `static/brand/logo-primary.svg`; the footer shows the reverse version. Logo masters, icons and the social banner live in `static/brand/`, `static/` and `static/images/og-default.jpg`.
- **Imagery:** face-free W field hero (`static/images/hero-*.svg`) and story tiles (`static/images/tiles/`), used as decorative images with empty alt text.

## Quick start

```bash
# Install Hugo extended
brew install hugo                # macOS
# or download v0.140.0 extended from https://github.com/gohugoio/hugo/releases

# Run dev server
hugo server -D

# Open http://localhost:1313
```

## Authoring

Everything is Markdown with YAML front matter.

```bash
# A new student story
hugo new stories/farzana.md

# A new news/blog post
hugo new blog/2026-05-cohort-9-launch.md

# A new program (rare)
hugo new programs/data-engineering.md
```

Set `draft: false` when ready and push to `main`. Coolify auto-deploys.

### Featured story

The homepage hero pulls from the most recent story marked `featured: true` in its front matter. Currently this is Mahdia Khamoosh from the 2026 cohort. To change:

1. In the previously-featured story, set `featured: false`
2. In the new featured story, set `featured: true`
3. Commit and push.

### Homepage data

Most homepage data is in `data/`:

- **`stats.yaml`** — the four stat numbers in the impact band
- **`partners.yaml`** — partner / funder names with style variants
- **`promise.yaml`** — the four CodeWeekend Promise items
- **`howitworks.yaml`** — the three-step program flow
- **`team.yaml`** — team member info (used on /about/team/)

These don't require touching templates.

## Forms

The site has no backend. All forms are external (Tally, Airtable, Google Forms, etc.) and embedded via shortcodes:

```markdown
{{< tally id="abc123" title="Apply for the 2026 cohort" >}}
{{< airtable id="shrXXX" title="Mentor application" >}}
```

The application, mentor, and hiring CTAs use working internal pages by default:

```toml
applyFormUrl = "/get-involved/apply/"
mentorFormUrl = "/get-involved/mentor/"
hireFormUrl = "/get-involved/hire/"
```

Each page currently provides an email pathway. Replace a URL with a verified external form only after testing its privacy notice, success state, and mobile behavior.

## Translation (Dari & Pashto)

The site ships in English. The utility bar (top right) has **EN · دری · پښتو**.

Clicking دری or پښتو:

1. Sets a `googtrans` cookie pointing Google Translate at Dari (`fa`) or Pashto (`ps`)
2. Sets `<html dir="rtl">` immediately (no flash) via an inline early-load script in `<head>`
3. Loads the Google Translate widget offscreen, which translates all visible text on next load
4. The `assets/css/rtl.css` overrides handle CTA arrows (→ becomes ←), the featured-quote curly mark, and switch all type (Manrope and Atkinson Hyperlegible Mono) to Vazirmatn at 18 px / 1.8, without letter-spacing, for proper Dari/Pashto rendering

The Weekend W logo and code stay LTR in isolated elements even in RTL mode (brand rule), but the rest of the page chrome flips correctly.

When you have native Dari/Pashto translators on the team, migrate to [Hugo's native multilingual support](https://gohugo.io/content-management/multilingual/) for higher-quality translations.

## Project structure

```
codeweekend-site/
├── hugo.toml                  # site config, menus, params
├── archetypes/                # front-matter templates for new content
├── assets/css/                # main.css + rtl.css (Hugo Pipes minifies + fingerprints)
├── assets/js/                 # main.js
├── content/                   # all Markdown content
│   ├── _index.md
│   ├── about/
│   │   ├── _index.md
│   │   └── team.md
│   ├── programs/
│   │   ├── _index.md
│   │   ├── web-and-ai.md      # 2026 cohort: women & girls in Afghanistan
│   │   └── full-stack.md      # historical 6-month program
│   ├── stories/               # real graduates (real names, placeholder avatars)
│   │   ├── mahdia.md          # FEATURED: 2026 cohort
│   │   ├── pourya.md
│   │   ├── mustafa.md
│   │   └── mehreen.md
│   ├── get-involved/
│   │   ├── _index.md
│   │   ├── donate.md
│   │   ├── mentor.md
│   │   └── hire.md
│   ├── contact/_index.md
│   └── blog/                  # real news posts ported from codeweekend.net
│       ├── becoming-nonprofit.md
│       ├── codeweekend-updates-2022.md
│       └── codeweekend-bootcamp-2021.md
├── data/                      # YAML data for homepage blocks
├── layouts/                   # Hugo templates
│   ├── _default/              # baseof, single, list, 404
│   ├── partials/
│   │   ├── head.html
│   │   ├── nav.html
│   │   ├── util-bar.html
│   │   ├── footer.html
│   │   ├── translate.html
│   │   ├── logo.html
│   │   ├── program-card.html
│   │   ├── story-card.html
│   │   ├── blog-card.html
│   │   └── blocks/            # homepage section blocks
│   ├── shortcodes/
│   ├── programs/{single,list}.html
│   ├── stories/{single,list}.html
│   └── blog/{single,list}.html
├── static/
│   ├── images/
│   │   ├── hero-landscape.svg # Weekend W field hero (kit artwork)
│   │   ├── hero-square.svg
│   │   ├── tiles/*.svg        # kit story tiles and W patterns
│   │   └── og-default.jpg     # kit social banner (1200 × 630)
│   ├── brand/                 # logo masters and avatar from the brand kit
│   ├── favicon.svg            # plus favicon.ico, app icons and site.webmanifest
│   └── robots.txt
├── .github/workflows/ci.yml
├── Dockerfile                 # multi-stage: Hugo build → Caddy serve
├── Caddyfile                  # production server config
├── lighthouserc.json          # Lighthouse CI thresholds
└── README.md
```

## Deployment to Coolify

1. **Push to GitHub** (this repo is at github.com/rapiditeration/codeweekend).
2. **In Coolify**, create a new resource:
   - Type: **Application**
   - Source: this GitHub repo
   - Build pack: **Dockerfile**
   - Port: **80**
3. **Add the custom domain** (`codeweekend.net`) in Coolify's Domains tab. Coolify provisions a Let's Encrypt cert automatically.
4. **Enable auto-deploy on push to main.** Coolify creates a webhook on the GitHub repo.
5. (Optional) Enable **preview deployments** for PR branches.

## Local Docker test

```bash
docker build -t codeweekend .
docker run --rm -p 8080:80 codeweekend
# Visit http://localhost:8080
```

## Performance & accessibility targets

- LCP < 2.0s
- INP < 200ms
- CLS < 0.1
- Lighthouse Performance: 95+
- Lighthouse Accessibility: 100
- Total page weight < 1MB

`lighthouserc.json` enforces these in CI.

## Things to replace before "launch" feels right

The site builds and runs as-is. Some content is placeholder until real assets are gathered:

- **Story images** use the brand kit's decorative tiles (`static/images/tiles/`) — sanitised project imagery can replace them later _with consent_, with alt text describing the work
- **Application workflow** — replace the email-based interest pathway with a verified form before the next cohort opens
- **Stats** in `data/stats.yaml` — currently shows real-looking numbers (10+ years, 280+ applications, 50 in 2026 cohort, 30 LNF scholarships); update as the program grows
- **Donate flow** — currently routes to email; wire up direct online giving when ready

## Content provenance

The content in this site was migrated from the previous codeweekend.net site (April 2026). Real elements:

- **Founder, history, mission** — directly from the About page
- **Team members** — from the About page (Jamshid Hashimi, Abida Nabizada, Shaheen Naikpay, Hamid Afghan, Mustafa Ehsan Alokozay, Azizullah Saeidi)
- **Student testimonials** — from the homepage and Case Studies (Pourya Amire, Mustafa Mohammadi, Mehreen Najm)
- **2026 cohort details** — from the July 2026 announcement post (Mahdia Khamoosh, the program structure, Linda Norgrove Foundation, the BC nonprofit incorporation)
- **News posts** — three full posts from the previous site (2026 announcement, 2022 year-in-review, 2021 bootcamp launch)
- **Partners** — Linda Norgrove Foundation, Hackajob, Scrimba, RapidIteration

## License

Code is MIT-licensed. The CodeWeekend brand, logo, and content are © CodeWeekend.
