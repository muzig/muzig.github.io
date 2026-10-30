# X-style profile homepage — design

Date: 2026-10-30
Status: approved (mockup v3)

## Goal

Replace the current magazine-style homepage with a personal profile page that borrows the layout of the X web app (three columns, banner, avatar, tabs, timeline) but reads as a personal blog, not a social account. The UI is in English.

The approved mockup lives at `.superpowers/brainstorm/77860-1793344205/content/layout-v3.html` (git-ignored). Treat it as the visual reference.

## Scope

In scope:

- The homepage (`src/pages/index.astro`) rebuilt as the profile page.
- A new `/about/` page using the same layout.
- New metadata fields for the 30 legacy posts.

Out of scope:

- The 30 legacy article pages under `legacy-pages/`. Their HTML and URLs stay unchanged.
- AI reader comments. That is the next sub-project. This design only reserves space for it.
- The historical Hugo system.

## Data

### Post metadata

Extend each entry in `src/data/legacy-posts.json` with:

| Field | Source | Notes |
|---|---|---|
| `titleEn` | Translated by the assistant, reviewed by the user | Required |
| `excerptEn` | Translated from `description`, or written from the article when `description` is only a type label such as "Guide" | Required, one or two sentences |
| `readMinutes` | Computed once from the article body text in `legacy-pages/` | Chinese characters count at 400 per minute, Latin words at 200 per minute, rounded up, minimum 1 |
| `series` | Read from the matching Hugo source in `content/posts/*.md` front matter | Optional; English display name kept in `profile.json` |
| `topicEn` | Mapped from the existing `category` | Fixed map, see below |

Topic map: `AI Agent` → `Agent Engineering`, `AI 编程` → `AI Coding`, `Go` → `Go`, `工程系统` → `Engineering Systems`, `编程语言` → `Programming Languages`.

A one-off script `scripts/enrich-legacy-posts.mjs` computes `readMinutes`, `series` and `topicEn` and writes them into the JSON. Translations are written by hand into the same file. The script is idempotent and does not overwrite existing `titleEn`/`excerptEn` values.

Astro-collection posts (`src/content/blog/`) get matching optional schema fields (`titleEn`, `excerptEn`) so both sources render through the same card. Their reading time is computed at build time from the body.

### Profile data

`src/data/profile.json` holds everything that describes the author:

- `name`, `site`, `bio`, `role`, `location`, `since`
- `links`: GitHub, Zhihu, email, RSS
- `now`: one short paragraph
- `startHere`: list of post URLs (three by default)
- `series`: map from series key to English display name and order

Editing the bio, the Now box or the Start here list only touches this file.

## Page structure

`src/layouts/ProfileLayout.astro` renders the three columns and is used by both the homepage and `/about/`.

| Component | Responsibility |
|---|---|
| `NavRail.astro` | Left column: M logo, Writing / Series / Topics / Archive / About / RSS, Subscribe button, author chip |
| `ProfileHeader.astro` | Sticky top bar, banner, avatar, Subscribe and email buttons, name, bio, meta row, counts, Now box |
| `ProfileTabs.astro` | Latest / Start here / Series / About tab bar |
| `StartHere.astro` | Horizontal rail of highlighted posts |
| `EntryCard.astro` | One post in the timeline: kicker (date · topic · read time), serif title, excerpt, topic chips, share action, pinned marker |
| `Sidebar.astro` | Right column: search, About me, Series with part counts, Topics |

Counts in the header (essays, series, total reading time) are computed from the data, not hard-coded.

### Behaviour

- **Latest** shows all posts, newest first, with the featured post pinned on top.
- **Start here** and **Series** filter the same page client-side. Series groups posts by `series`.
- **About** links to `/about/`, which renders the bio and links at full length.
- **Topics** and **Archive** in the nav point at filtered views of the homepage (`/?topic=…`, `/?view=archive`) instead of new pages.
- Search keeps the current client-side filter over titles, excerpts and topics.
- There is no bookmark action. Share uses the Web Share API when available and falls back to copying the link.

### Reserved for AI comments

The entry card has an `aiReplies` slot and the sidebar has a "Who reads here" box. Both render only when real data exists. With no data, nothing is shown. No invented counts, likes, reposts or views appear anywhere.

## Visual rules

- Dimensions follow the X web app: left column 275px, centre 600px, right 350px, 15px base font.
- Dark theme by default; a light theme applies under `prefers-color-scheme: light`. Colours are CSS variables on `:root`.
- Breakpoints: at ≤1280px the nav collapses to icons; at ≤1000px the sidebar hides; at ≤700px only the centre column remains.
- Own branding only: the M mark, no X logo, name or verification badge.
- Homepage uses `lang="en"` and an English title and description. Article pages keep `zh-CN`.

## Error handling

- A legacy post missing `titleEn` or `excerptEn` fails the build with the post URL in the message, so untranslated entries cannot ship.
- A `startHere` URL that matches no post fails the build.
- Missing `readMinutes` hides the read-time part of the kicker instead of showing a wrong number.

## Verification

1. `npm run check` passes (type check, build, `scripts/check-built-site.mjs`).
2. Every post URL on the homepage resolves to a built page in `dist/`.
3. Screenshots at 1280px, 1000px and 390px match the mockup layout.
4. The user previews the built site over Tailscale before anything is pushed.
