# Contributor Guide 📝

## Writing New Posts

All content is written in Markdown. Each post is a file in `src/content/posts/`.

### File Naming

Each post file should be named with a unique numeric ID, e.g. `123.md`.

### Frontmatter

Every post must include frontmatter with the following fields:

```yaml
---
id: 123
title: "Post Title"
date: "2026-07-11T12:00:00"
author: "Author Name"
topics: ["Topic1", "Topic2"]
type: message
---
```

### Paragraphs (⚠️ Important!)

**Use double newlines (blank lines) between paragraphs.**

A single newline will **not** create a new paragraph — it will be treated as a space.

#### ✅ Correct:

```
First paragraph.

Second paragraph.
```

#### ❌ Incorrect:

```
First paragraph.
Second paragraph.
```

### Example Post

```markdown
---
id: 125
title: "Patience in Times of Trial"
date: "2026-07-11T12:00:00"
author: "Ibn al-Qayyim"
topics: ["Patience", "Trials"]
type: message
---

**Ibn al-Qayyim said:**

“Patience is half of faith.”

Indeed, the one who is patient will be rewarded without measure.

*{وَمَنْ يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ}*

“And whoever puts his trust in Allah, He will suffice him.”
```

### Topics / Tags

Add topics as an array in the frontmatter. Existing topics will appear in the topic cloud automatically.

### Images

Place images in `public/images/` and reference them as `/images/your-image.jpg`.

### Publishing

To publish, commit your changes and push to GitHub. The site will automatically rebuild.

If using PageCMS, you can edit and publish directly from the admin interface.

### Need Help?

Reach out to the channel admins or open an issue on the GitHub repository.