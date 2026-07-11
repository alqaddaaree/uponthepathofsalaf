#!/usr/bin/env python3
import re
from pathlib import Path

POSTS_DIR = Path('')

for md_file in POSTS_DIR.glob('*.md'):
    content = md_file.read_text(encoding='utf-8')

    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        continue

    frontmatter, body = match.groups()

    # Remove YAML type tags: !!int, !!null, etc.
    frontmatter = re.sub(r'!!\w+\s+', '', frontmatter)

    # If a value is literally "null" (quoted), replace with empty string or remove
    frontmatter = re.sub(r':\s*"null"', ': ""', frontmatter)

    # Write back
    cleaned = f'---\n{frontmatter}\n---\n{body}'
    md_file.write_text(cleaned, encoding='utf-8')
    print(f'Fixed: {md_file.name}')
