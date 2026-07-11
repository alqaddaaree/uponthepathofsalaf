import yaml
from pathlib import Path

POSTS_DIR = Path('src/content/posts')

for yaml_file in POSTS_DIR.glob('*.yaml'):
    data = yaml.safe_load(yaml_file.read_text(encoding='utf-8'))
    if 'quotedAuthor' in data:
        del data['quotedAuthor']
    if 'edited' in data:
        del data['edited']
    yaml_file.write_text(
        yaml.dump(data, allow_unicode=True, sort_keys=False),
        encoding='utf-8'
    )
    print(f'Cleaned {yaml_file.name}')
