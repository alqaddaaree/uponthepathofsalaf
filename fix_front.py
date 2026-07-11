import re
from pathlib import Path

POSTS_DIR = Path('src/content/posts')

for yaml_file in POSTS_DIR.glob('*.yaml'):
    name = yaml_file.name
    # Replace all "allah" variants (case-insensitive) with "Allah"
    new_name = re.sub(r'(?i)allah', 'Allah', name)

    if new_name != name:
        new_path = yaml_file.parent / new_name
        if new_path.exists():
            print(f'⚠ Skipping {name} – {new_name} already exists')
        else:
            yaml_file.rename(new_path)
            print(f'✓ {name} → {new_name}')
