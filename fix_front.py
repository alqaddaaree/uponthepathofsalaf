#!/usr/bin/env python3
import yaml
from pathlib import Path

TOPICS_DIR = Path('src/content/topics')
POSTS_DIR = Path('src/content/posts')

print("🔍 Checking topics...")
for yaml_file in TOPICS_DIR.glob('*.yaml'):
    try:
        data = yaml.safe_load(yaml_file.read_text(encoding='utf-8'))
        if not data:
            print(f"❌ {yaml_file}: Empty or invalid YAML")
            continue
        if 'name' not in data:
            print(f"❌ {yaml_file}: Missing 'name' field")
        if 'slug' not in data:
            print(f"❌ {yaml_file}: Missing 'slug' field")
        # Check for extra fields that might cause issues
    except Exception as e:
        print(f"❌ {yaml_file}: YAML parsing error: {e}")

print("\n🔍 Checking posts for invalid topics...")
for yaml_file in POSTS_DIR.glob('*.yaml'):
    try:
        data = yaml.safe_load(yaml_file.read_text(encoding='utf-8'))
        # Just check if it loads
    except Exception as e:
        print(f"❌ {yaml_file}: YAML parsing error: {e}")
