# First Principles Journal

A minimal, typography-led technical journal for ML, LLM inference, and systems engineering. The site is built with Astro and Markdown content collections. Pages CMS provides the editing interface by committing content and images to GitHub; there is no separate content database or custom backend.

## Design and product decisions

- **One feed:** a featured investigation followed by the rest of the published notes. There is no separate portfolio, about page, search interface, or tag directory in v1.
- **Minimal surface, deep content:** the homepage uses only identity, one sentence, social links, and the work. Article pages lead with the claim and artifact without editorial labels or section banners.
- **Two external font families:** Inter for interface text and Newsreader for headings and long-form reading. Code uses the system monospace stack.
- **Content-first:** a new article is a Markdown file with typed frontmatter. Astro creates its route at `/posts/<slug>/` during the build.
- **Static output:** the public site has no runtime database or required browser JavaScript. The Markdown pipeline includes math rendering and Shiki code highlighting.
- **Honest claims:** article examples are drafts unless they have been verified. The published OLS article links to a small runnable implementation and states the scope and limitations of the tests.

## Requirements

- Node.js 20.11.1 or newer (Node 22 LTS is recommended).
- npm.
- Python 3.10+ and NumPy only if you want to run the included OLS example tests.

## Run locally

```bash
npm install
npm run dev
```

The header places a GitHub icon link beside the light/dark theme control. Both icons use `@lucide/astro`. Use npm for dependency installation; the project intentionally does not include a stale pnpm lockfile.

Astro prints the local development URL. Before publishing, run:

```bash
npm run check
npm run build
npm run test:ols
```

The `prebuild`/`predev` lifecycle syncs `examples/ols/ols.py` to `public/code/ols.py`, which is the source file linked from the example article. If you edit the Python source and want to refresh the public copy immediately, run `npm run sync:ols`.

To run the Python tests:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Publish a new post through Pages CMS

1. Push this project to a GitHub repository.
2. Open [Pages CMS](https://app.pagescms.org/) and sign in with GitHub.
3. Install/authorize the Pages CMS GitHub App for the account and repository that contains this project.
4. Open the repository. Pages CMS reads the root `.pages.yml` configuration.
5. Open **Articles** and create a new article. Add a title, summary, date, topic labels, thumbnail, article body, artifact URL, and repository URL if applicable.
6. Keep **Draft (hide from public site)** enabled while the article is in progress. Preview it locally with `npm run dev`. Uncheck the draft field only when its claims, code, images, and links are ready.
7. Save the entry in Pages CMS. It creates a Git commit with the Markdown and uploaded images. Your hosting provider rebuilds the public site from that commit.

Pages CMS is a hosted editing interface, not a local `/admin` route. You do not need to install or operate a CMS server. It edits the repository itself, so the complete content history remains in Git. See the [Pages CMS quick start](https://pagescms.org/docs/quick-start/) for authorization details.

### Article frontmatter

The CMS creates this shape automatically:

```yaml
---
title: "An investigation title"
summary: "A one-sentence statement of what was built or learned."
date: 2026-10-24
draft: true
featured: false
tags:
  - systems
thumbnail: "/images/posts/your-image.webp"
thumbnailAlt: "A concise description of the image."
artifactSummary: "What the reader is looking at and what it demonstrates."
artifactUrl: "/downloads/experiment.csv"
repoUrl: "https://github.com/your-account/your-repository"
caption: "A figure caption explaining what the evidence does and does not show."
---

Article text starts here.
```

`draft` defaults to `true` in Astro when omitted, so a new file is not accidentally published without an explicit decision. Set `featured: true` on the single article you want to lead the homepage. If no article is featured, the newest published article is selected automatically. The featured article is not repeated in the list below it.

The article layout creates compact jump links from actual level-two headings, without adding a separate navigation label. Useful common patterns are:

- Mathematical investigations: `The objective`, `The implementation`, `What broke / where it diverges`, `What I would test next`.
- Systems investigations: `The mental model`, `The experiment`, `What the measurements say`, `Failure modes`, `Next experiment`.

The template is intentionally flexible. Keep sections only when the work needs them; do not manufacture a derivation or benchmark to match a template.

## Configure the site identity

Edit **Site settings** in Pages CMS or `src/data/site.json` directly:

- `name`, `pitch`, and `description` control the identity and metadata.
- `github` controls the GitHub icon link beside the theme toggle. `linkedin`, `x`, and `email` control optional text links on the left side of the header. Empty values are not rendered.
- `personalSite` controls the personal-site link in the minimal footer.
- `repositoryUrl` is a fallback source-repository link used by articles that do not override `repoUrl`.
- The theme toggle switches between light and dark modes and remembers the preference in the browser.
- `siteUrl` must be the real canonical production origin, for example `https://notes.example.com`.

Set the same production URL as `PUBLIC_SITE_URL` in your hosting environment. Astro uses that value for canonical sitemap configuration. Do not leave `example.com` in production metadata.

## Deploy to Cloudflare Pages

This is a static Astro site. The project is configured with Astro's static output; no Cloudflare adapter or server runtime is necessary for the public pages.

1. Push the project to GitHub.
2. In Cloudflare, create a Pages project and connect the repository.
3. Use `npm run build` as the build command and `dist` as the build output directory.
4. Set `PUBLIC_SITE_URL` to the final HTTPS origin in the build environment.
5. Update `siteUrl` in `src/data/site.json` to that same origin, commit the change, and redeploy.
6. Attach your custom domain in Cloudflare Pages and follow its DNS instructions.

Each Pages CMS commit triggers the connected build. A failed build should prevent that content change from being deployed; fix the build error, then commit again.

## Content and media conventions

- Store posts in `src/content/posts/` as Markdown.
- Upload article thumbnails under `public/images/posts/` through Pages CMS.
- Use meaningful alt text. If an image is a conceptual illustration, say so in the caption; do not frame it as measured evidence.
- Prefer original plots, diagrams, code output, and experiment results over decorative artwork.
- Keep numerical claims reproducible. State the environment, data, metric, baseline, and tolerances behind benchmarks.
- Make limitations explicit. A documented boundary is better than an unsupported claim of completeness.
- Avoid enormous source-code dumps in the article. Show the relevant excerpt, link the full artifact, and explain the design decisions.

## Project structure

```text
.
├── .pages.yml                  # Pages CMS schema
├── astro.config.mjs            # Astro, math rendering, sitemap, syntax highlighting
├── src/
│   ├── components/             # Header, post cards, metadata
│   ├── content/posts/          # Published Markdown and unpublished drafts
│   ├── content.config.ts       # Typed article schema
│   ├── data/site.json          # Editable site identity and external links
│   ├── layouts/BaseLayout.astro
│   ├── pages/                  # Homepage, article route, 404
│   └── styles/global.css       # Design tokens and responsive styling
├── public/
│   ├── code/ols.py             # Synced, public artifact source
│   └── images/                 # Original SVG diagrams
├── examples/ols/ols.py         # Canonical small OLS implementation
├── tests/test_ols.py           # Unit tests for the example implementation
└── docs/                       # Additional project notes
```

## CMS and hosting costs

Pages CMS's hosted GitHub editor is the intended CMS. It does not add a database, API, or separate server to this project. Hosting depends on the provider and its current plan; verify current limits in the provider's dashboard before deployment. The code does not require a paid content service.
