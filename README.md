# CodeWeekend

The website for [CodeWeekend](https://codeweekend.net) — an inclusive community of developers, founded in Kabul in 2014, now incorporated as a non-profit society in British Columbia, Canada. The 2025 program is a 12-week Web & AI Development Bootcamp for women and girls in Afghanistan.

Built with Hugo. Hosted on GitHub. Deployed via Coolify.

## Stack

- **[Hugo](https://gohugo.io/)** static site generator (extended, v0.140.0)
- **Markdown** for all content (no CMS)
- **Custom theme** in `layouts/` — no external theme dependency
- **Google Translate** widget for Dari (دری) and Pashto (پښتو), with automatic RTL switching
- **Caddy** in production (HTTP/2, gzip, zstd, security headers)
- **GitHub Actions** for CI (build check, accessibility audit, Lighthouse)
- **Coolify** for self-hosted deployment

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

The homepage hero pulls from the most recent story marked `featured: true` in its front matter. Currently this is Mahdia Khamoosh from the 2025 cohort. To change:

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

Replace the placeholder URLs in `hugo.toml` under `[params]`:

```toml
applyFormUrl = "https://tally.so/r/REPLACE_ME_APPLY"
mentorFormUrl = "https://tally.so/r/REPLACE_ME_MENTOR"
hireFormUrl = "https://tally.so/r/REPLACE_ME_HIRE"
newsletterFormUrl = "https://tally.so/r/REPLACE_ME_NEWSLETTER"
```

## Translation (Dari & Pashto)

The site ships in English. The utility bar (top right) has **EN · دری · پښتو**.

Clicking دری or پښتو:

1. Sets a `googtrans` cookie pointing Google Translate at Dari (`fa`) or Pashto (`ps`)
2. Sets `<html dir="rtl">` immediately (no flash) via an inline early-load script in `<head>`
3. Loads the Google Translate widget offscreen, which translates all visible text on next load
4. The `assets/css/rtl.css` overrides handle CTA arrows (→ becomes ←), the featured-quote curly mark, and switches Latin fonts to Vazirmatn for proper Persian/Arabic rendering

The bracket wordmark logo stays LTR even in RTL mode (brand integrity), but the rest of the page chrome flips correctly.

When you have native Dari/Pashto translators on the team, migrate to [Hugo's native multilingual support](https://gohugo.io/content-management/multilingual/) for higher-quality translations.

## Project structure

```
codeweekend-site/
├── hugo.toml                  # site config, menus, params
├── archetypes/                # front-matter templates for new content
├── assets/css/                # main.css + rtl.css (Hugo Pipes minifies + fingerprints)
├── assets/js/                 # main.js + translate.js
├── content/                   # all Markdown content
│   ├── _index.md
│   ├── about/
│   │   ├── _index.md
│   │   └── team.md
│   ├── programs/
│   │   ├── _index.md
│   │   ├── web-and-ai.md      # 2025 cohort: women & girls in Afghanistan
│   │   └── full-stack.md      # historical 6-month program
│   ├── stories/               # real graduates (real names, placeholder avatars)
│   │   ├── mahdia.md          # FEATURED: 2025 cohort
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
│   │   ├── hero.svg           # editorial illustration with code window
│   │   └── stories/*.svg      # initials-based avatar placeholders
│   ├── favicon.svg
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

- **Student photos** in `static/images/stories/` are SVG initials avatars — replace with real graduate photos _with consent_
- **Form URLs** in `hugo.toml` — replace with real Tally/Airtable IDs
- **Hero image** (`static/images/hero.svg`) is a stylized illustration — could be replaced with a real photo of a cohort, with consent
- **Stats** in `data/stats.yaml` — currently shows real-looking numbers (10+ years, 280+ applications, 50 in 2025 cohort, 30 LNF scholarships); update as the program grows
- **Donate flow** — currently routes to email; wire up direct online giving when ready

## Content provenance

The content in this site was migrated from the previous codeweekend.net site (April 2026). Real elements:

- **Founder, history, mission** — directly from the About page
- **Team members** — from the About page (Jamshid Hashimi, Abida Nabizada, Shaheen Naikpay, Hamid Afghan, Mustafa Ehsan Alokozay, Azizullah Saeidi)
- **Student testimonials** — from the homepage and Case Studies (Pourya Amire, Mustafa Mohammadi, Mehreen Najm)
- **2025 cohort details** — from the August 2025 announcement post (Mahdia Khamoosh, the program structure, Linda Norgrove Foundation, the BC nonprofit incorporation)
- **News posts** — three full posts from the previous site (2025 announcement, 2022 year-in-review, 2021 bootcamp launch)
- **Partners** — Linda Norgrove Foundation, Hackajob, Scrimba, RapidIteration

## License

Code is MIT-licensed. The CodeWeekend brand, logo, and content are © CodeWeekend.
