#!/usr/bin/env python3
import re
import yaml
from pathlib import Path

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)  # replace non-alnum with hyphens
    text = text.strip('-')
    return text

POSTS_DIR = Path('src/content/posts')

for yaml_file in POSTS_DIR.glob('*.yaml'):
    data = yaml.safe_load(yaml_file.read_text(encoding='utf-8'))
    title = data.get('title', 'untitled')
    slug = slugify(title)

    # Avoid overwriting if slug already exists
    new_path = yaml_file.parent / f'{slug}.yaml'
    if new_path.exists() and new_path != yaml_file:
        print(f'Warning: {new_path} already exists. Skipping {yaml_file}.')
        continue

    yaml_file.rename(new_path)
    print(f'Renamed {yaml_file.name} → {new_path.name}')
