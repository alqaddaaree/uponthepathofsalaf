#!/usr/bin/env python3
"""
Migrate topics from free-text names to a dedicated topics collection.

Steps:
1. Extract all unique topic names from posts.
2. For each, create a topic file (src/content/topics/{slug}.yaml).
3. Update all posts: replace topic names with slugs.
4. Output a mapping for reference.
"""

import yaml
import re
from pathlib import Path
from collections import Counter

# Paths
POSTS_DIR = Path('src/content/posts')
TOPICS_DIR = Path('src/content/topics')

# Create topics directory if it doesn't exist
TOPICS_DIR.mkdir(parents=True, exist_ok=True)

# --- Step 1: Extract unique topics and their counts ---
def extract_topics():
    """Read all posts and collect topic names with counts."""
    topic_counter = Counter()
    for yaml_file in POSTS_DIR.glob('*.yaml'):
        try:
            data = yaml.safe_load(yaml_file.read_text(encoding='utf-8'))
            for topic in data.get('topics', []):
                if topic:  # skip empty
                    topic_counter[topic] += 1
        except Exception as e:
            print(f"⚠️ Error reading {yaml_file}: {e}")
    return topic_counter

topic_counter = extract_topics()
if not topic_counter:
    print("❌ No topics found. Aborting.")
    exit(1)

print(f"📊 Found {len(topic_counter)} unique topics:")
for topic, count in topic_counter.most_common():
    print(f"   {count:3} | {topic}")

# --- Step 2: Create topic files ---
def slugify(name):
    """Convert a topic name to a URL-friendly slug."""
    # Lowercase, replace spaces and underscores with hyphens
    slug = re.sub(r'[\s_]+', '-', name.lower())
    # Remove any non-alphanumeric characters except hyphens and apostrophes
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    return slug or 'untitled'

# Mapping: old topic name → slug
topic_slug_map = {}

for topic_name, count in topic_counter.items():
    slug = slugify(topic_name)
    # Ensure unique slug (if collision, add a numeric suffix)
    original_slug = slug
    suffix = 1
    while (TOPICS_DIR / f'{slug}.yaml').exists() or slug in topic_slug_map.values():
        slug = f"{original_slug}-{suffix}"
        suffix += 1
    topic_slug_map[topic_name] = slug

    # Create topic file
    topic_data = {
        'name': topic_name,
        'slug': slug,
        'description': f"Lessons and content related to {topic_name}.",
        'order': 999 - count  # Higher count → lower order (appears first)
    }
    topic_file = TOPICS_DIR / f'{slug}.yaml'
    topic_file.write_text(
        yaml.dump(topic_data, allow_unicode=True, sort_keys=False),
        encoding='utf-8'
    )
    print(f"✅ Created topic file: {topic_file}")

# --- Step 3: Update posts to use slugs ---
print("\n🔄 Updating posts...")
updated_count = 0
for yaml_file in POSTS_DIR.glob('*.yaml'):
    content = yaml_file.read_text(encoding='utf-8')
    data = yaml.safe_load(content)
    old_topics = data.get('topics', [])
    if not old_topics:
        continue
    # Replace names with slugs
    new_topics = []
    for t in old_topics:
        slug = topic_slug_map.get(t)
        if slug:
            new_topics.append(slug)
        else:
            # Fallback: generate slug on the fly (should not happen)
            new_topics.append(slugify(t))
    # Remove duplicates and sort
    new_topics = sorted(set(new_topics))
    data['topics'] = new_topics

    # Write back
    yaml_file.write_text(
        yaml.dump(data, allow_unicode=True, sort_keys=False),
        encoding='utf-8'
    )
    updated_count += 1
    print(f"   Updated {yaml_file.name}")

print(f"\n✅ Updated {updated_count} post files.")

# --- Step 4: Save mapping for reference ---
mapping_file = Path('topic_mapping.txt')
with open(mapping_file, 'w', encoding='utf-8') as f:
    f.write("Old Topic Name → Slug\n")
    f.write("=" * 40 + "\n")
    for old, slug in sorted(topic_slug_map.items()):
        f.write(f"{old} → {slug}\n")
print(f"📄 Mapping saved to {mapping_file}")

print("\n🎉 Migration complete.")
print("Next steps:")
print("1. Update .pages.yml: change 'topics' field to type 'relation' pointing to 'topics' collection.")
print("2. Update src/pages/topics/index.astro and src/pages/topics/[...topic].astro to use the topics collection.")
print("3. Restart dev server and test.")
