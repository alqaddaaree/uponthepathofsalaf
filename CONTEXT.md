# The Salaf's Path — Project Overview

## Project Summary

A static website built with **Astro** that transforms a Telegram channel export (`result.json`) into a searchable, accessible digital library of Islamic content. The site serves 144+ posts containing quotes from scholars, hadith, tafsir, and Islamic knowledge — all rendered with proper Arabic/English RTL support.

---

## Table of Contents
1. [Tech Stack](#tech-stack)
2. [Project Structure](#project-structure)
3. [Content Management](#content-management)
4. [Development Workflow](#development-workflow)
5. [Key Features](#key-features)
6. [Component Architecture](#component-architecture)
7. [Search Implementation](#search-implementation)
8. [RTL & Multilingual Support](#rtl--multilingual-support)
9. [Deployment](#deployment)
10. [Known Issues & Considerations](#known-issues--considerations)

---

## Tech Stack

| Category | Technology |
|----------|------------|
| **Framework** | Astro 7.0.7 |
| **Language** | TypeScript + JavaScript |
| **Styling** | Custom CSS (no framework) |
| **CMS** | PageCMS (Git-based) |
| **Search** | Fuse.js (client-side, lazy-loaded) |
| **Deployment** | Vercel |
| **Version Control** | Git / GitHub |
| **Package Manager** | npm |

---

## Project Structure

```
uponthepathofthesalaf/
├── public/
│   ├── styles/
│   │   └── global.css          # All global styles
│   ├── logo.jpg                # Site logo
│   ├── favicon.png             # Generated favicon
│   ├── apple-touch-icon.png
│   ├── icon-*.png
│   └── manifest.json           # PWA manifest
├── src/
│   ├── content/
│   │   └── posts/              # Markdown posts (144+ files)
│   │       ├── 1.md
│   │       ├── 2.md
│   │       └── ...
│   ├── components/
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   ├── Hero.astro
│   │   ├── TopicCloud.astro
│   │   └── PostCard.astro
│   ├── layouts/
│   │   └── Layout.astro        # Base layout with meta/OG tags
│   ├── pages/
│   │   ├── index.astro         # Homepage with search
│   │   ├── topics/
│   │   │   ├── index.astro     # All topics grid
│   │   │   └── [...topic].astro # Topic detail page
│   │   ├── posts/
│   │   │   └── [...id].astro   # Single post detail
│   │   └── rss.xml.js          # RSS feed endpoint
│   ├── content.config.ts       # Astro content collection
│   └── styles/
│       └── global.css          # (moved to public/)
├── scripts/
│   └── generate-favicons.js    # Favicon generator
├── export/
│   └── export_to_md_fixed.py   # Python converter
├── .pages.yml                  # PageCMS configuration
├── astro.config.mjs
├── package.json
└── CONTRIBUTING.md             # Private guide
```

---

## Content Management

### Source Data
- **Input:** `result.json` — exported from Telegram channel via Telegram's data export
- **Content:** 213 messages → filtered to 144 relevant posts
- **Skipped:** Service messages, videos, images, empty content

### Conversion Process
```bash
python3 export/export_to_md_fixed.py
```

**What it does:**
1. Parses `result.json`
2. Extracts text from `text_entities` (handles bold, italic, blockquote, links)
3. Strips irrelevant content (videos, images, service messages)
4. Generates topics via keyword matching
5. Outputs Markdown files with YAML frontmatter

### Frontmatter Schema
```yaml
---
id: 284
title: "When distress becomes intense..."
date: "2026-07-05T10:54:52"
author: "عَلَىٰ نَهجِ السَّلَفِ  Upon the path of the Salaf"
quotedAuthor: "ʿAbbās"
topics: ["Knowledge", "Seerah", "Trials"]
type: "message"
edited: "2026-07-05T10:58:59"
---
```

### Content Collection (Astro)
```typescript
// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const postsCollection = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    id: z.number(),
    title: z.string(),
    date: z.string(),
    author: z.string().nullable().optional(),
    quotedAuthor: z.string().nullable().optional(),
    topics: z.array(z.string()).default([]),
    type: z.enum(['message', 'article', 'translation']).default('message'),
    edited: z.string().nullable().optional(),
    forwarded_from: z.string().nullable().optional(),
    has_audio: z.boolean().default(false),
    has_file: z.boolean().default(false),
  }),
});

export const collections = { posts: postsCollection };
```

### Writing New Posts (PageCMS)
- Writers use the PageCMS admin interface
- **Important:** Use **double newlines** (blank lines) between paragraphs
- Single newline = space (not a paragraph break)
- Topics are added as an array in frontmatter

---

## Development Workflow

### Install Dependencies
```bash
npm install
```

### Development Server
```bash
npm run dev
# http://localhost:4321
```

### Build for Production
```bash
npm run build
# Outputs to ./dist/
```

### Preview Production Build
```bash
npm run preview
```

### Generate Favicons
```bash
node scripts/generate-favicons.js
# Requires sharp: npm install sharp
```

### Convert New Telegram Export
```bash
# Place result.json in project root
python3 export/export_to_md_fixed.py
```

---

## Key Features

### 1. Homepage
- Hero section with search bar
- Topic cloud with counts
- Recent posts grid (7 posts, featured first)
- Client-side search with lazy-loaded index

### 2. Topics
- All topics grid with post counts
- Each topic shows filtered posts
- Automatic topic generation from frontmatter

### 3. Single Post
- Full content with formatting
- Breadcrumb navigation
- Related posts (based on shared topics)
- Tags for topics
- RTL-aware layout

### 4. Search
- Fuse.js client-side search
- Search index built at build time
- 200ms debounce
- Matches: title, excerpt, topics, author
- Results styled identically to posts

### 5. RSS Feed
- `/rss.xml` endpoint
- All posts included
- Standard RSS 2.0 format

### 6. SEO & Social
- Open Graph tags
- Twitter Cards (summary_large_image)
- Canonical URLs
- Description meta tags

---

## Component Architecture

### Header.astro
- Logo (image + text)
- Navigation: Home, Topics, Search button
- Sticky with gold bottom border

### Footer.astro
- Brand description
- Topics links
- External links (Telegram)
- Arabic calligraphy

### Hero.astro
- Gradient background with geometric pattern
- Bismillah, title, tagline
- Search form (submits to homepage search)
- Stats: total posts, topics, scholars

### TopicCloud.astro
- Shows top 12 topics with counts
- Active state for current topic
- Responsive pill buttons

### PostCard.astro
- Card with gold left accent bar
- Topic tag, date, title, excerpt
- Author attribution
- Featured variant (dark gradient background)
- **Important:** Styles are in `global.css` (shared with search results)

### Layout.astro
- Meta tags, OG tags, Twitter cards
- Favicon links
- Google Fonts (Amiri, Cinzel, Inter, Fira Code)
- Header + Footer wrapper
- `dir="auto"` on wrapper for RTL

---

## Search Implementation

### How It Works
1. **Build time:** Search index is generated from all posts in the frontmatter
2. **Client-side:** Index is passed via `define:vars` to the module script
3. **Lazy initialization:** Fuse.js is only initialized on first search
4. **Debounce:** 200ms delay before searching
5. **Results:** Rendered as cards matching PostCard styling

### Key Files
- `src/pages/index.astro` — search logic
- `src/utils/renderCard.ts` — shared card rendering
- `public/styles/global.css` — shared styles

### Search Index Structure
```typescript
{
  id: number,
  title: string,
  excerpt: string,      // Stripped of markdown, 200 chars
  topics: string[],
  author: string,
}
```

### Fuse.js Configuration
```javascript
new Fuse(searchIndex, {
  keys: ['title', 'excerpt', 'topics', 'author'],
  threshold: 0.3,
})
```

---

## RTL & Multilingual Support

### Font Strategy
| Text Type | Font |
|-----------|------|
| English body | Inter |
| Arabic body | Amiri (auto-fallback) |
| Titles (English) | Cinzel |
| Titles (Arabic) | Amiri (fallback) |
| Code blocks | Fira Code |

**Implementation:** Font stack handles auto-selection
```css
font-family: 'Inter', 'Amiri', sans-serif;
/* Inter lacks Arabic glyphs → browser falls back to Amiri */
```

### Direction Handling
- **Paragraphs:** Each `<p>` gets `dir="auto"` via Rehype plugin
- **Arabic paragraphs:** Automatically RTL
- **English paragraphs:** Automatically LTR
- **Mixed content:** Each line is a separate paragraph via double newlines

### Double Newline Rule
- **✅ Correct:**
  ```
  First paragraph.
  
  Second paragraph.
  ```
- **❌ Incorrect:**
  ```
  First paragraph.
  Second paragraph.
  ```

**Why:** Markdown requires blank lines between paragraphs. Single newlines become spaces.

---

## Deployment

### Vercel Deployment
```bash
npm run build
npx vercel --prod
```

### GitHub + Vercel (Auto-deploy)
1. Push to GitHub
2. Connect repo to Vercel
3. Automatic deployments on push to main

### Environment Variables
- `SITE` — Site URL (e.g., `https://uponthepathofsalaf.vercel.app`)

### Build Output
- `/dist/` — Static files
- Ready for any static hosting (Vercel, Netlify, Cloudflare Pages)

---

## Known Issues & Considerations

### 1. Search Index Weight
**Current:** Index is embedded in the HTML (baked at build time).  
**For 144 posts:** ~50KB HTML overhead. Acceptable.  
**For 1500+ posts:** Would be 400-600KB. Consider moving to `/search-index.json` lazy-load.

**Fix if needed:** Already implemented in `search-index.json.js` (commented out), can switch to fetch-based loading.

### 2. Card Markup Duplication
**Current:** PostCard styles are in `global.css` and used by both Astro component and search JS.  
**Risk:** If `PostCard.astro` changes its markup, search results will diverge.  
**Mitigation:** Comment in `PostCard.astro` reminds about the duplicate.

### 3. Double Newlines
**Current:** Writers must use double newlines in Markdown.  
**Risk:** New contributors may not know this.  
**Mitigation:** `CONTRIBUTING.md` explains this clearly.

### 4. Arabic Font Detection
**Current:** Font stack auto-detects Arabic via Unicode ranges.  
**Works:** Browsers automatically switch fonts when Arabic characters appear.

### 5. Markdown in Excerpts
**Current:** Excerpts strip markdown via `stripMarkdown()` function.  
**Works:** Both build-time and search index use the same function.

---

## Quick Reference

### Commands
| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `python3 export/export_to_md_fixed.py` | Convert Telegram JSON to Markdown |
| `node scripts/generate-favicons.js` | Generate favicons from logo.jpg |

### Key Environment Variables
| Variable | Purpose |
|----------|---------|
| `SITE` | Base URL for canonical and OG tags |

### Important Files for New Developers
1. `src/content.config.ts` — Content collection schema
2. `src/pages/index.astro` — Homepage with search
3. `src/layouts/Layout.astro` — Meta tags, fonts, global styles
4. `public/styles/global.css` — All global styles
5. `CONTRIBUTING.md` — Contributor guide

---

## Future Improvements

1. **Search:** Move index to `/search-index.json` for very large collections
2. **Pagination:** Add infinite scroll or pagination for posts
3. **Comments:** Consider adding comment system
4. **Analytics:** Add simple analytics (Plausible, Umami)
5. **Email Newsletter:** RSS feed is a good start, could add email subscription
6. **Audio Support:** Currently skipped, could support audio posts
7. **Image Optimization:** Use Astro's Image component for responsive images

---

## Credits & Acknowledgments

- **Content:** Telegram channel "Upon the Path of Salaf"
- **Scholars:** Ibn Uthaymeen, Al-Albani, Ibn al-Qayyim, Ibn Baz, Muqbil al-Wadi'i, and others
- **Translators:** Umm ʿAbdirraḥmān as-Sūdāniyyah, Umm Tamīm aṣ-Ṣūmāliyyah, Umm Muṣʿab al-Ghāniyyah al-Almāniyyah
- **Build:** Custom Astro implementation

---

*Generated: July 2026*