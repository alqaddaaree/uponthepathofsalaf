#!/usr/bin/env python3
import re
from pathlib import Path
import yaml

POSTS_DIR = Path('')

for md_file in POSTS_DIR.glob('*.md'):
    content = md_file.read_text(encoding='utf-8')

    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        continue

    frontmatter_text, body = match.groups()
    frontmatter = yaml.safe_load(frontmatter_text)
    frontmatter['body'] = body.strip()

    yaml_file = md_file.with_suffix('.yaml')
    yaml_file.write_text(
        yaml.dump(frontmatter, allow_unicode=True, sort_keys=False),
        encoding='utf-8'
    )
    md_file.unlink()  # Remove .md file
    print(f'Converted: {md_file.name} → {yaml_file.name}')
