#!/usr/bin/env python3
# export_to_md_fixed.py

import json
import os
import re
from datetime import datetime
from pathlib import Path
import yaml

# ============================================================
# EDIT THIS SECTION TO IMPROVE CATEGORIZATION
# ============================================================
TOPIC_KEYWORDS = {
    'Aqeedah': ['aqeedah', 'creed', 'tawheed', 'shirk', 'kufr', 'iman', 'faith'],
    'Tawheed': ['tawheed', 'la ilaha illallah', 'oneness'],
    'Fiqh': ['fiqh', 'ruling', 'fatwa', 'permissible', 'haram', 'halal'],
    'Hadith': ['hadith', 'sahih', 'bukhari', 'muslim', 'narrated'],
    'Tafsir': ['tafsir', 'surah', 'ayah', 'verse'],
    'Seerah': ['seerah', 'prophet', 'messenger'],
    "Du'a": ['dua', 'supplication', 'invoke'],
    'Patience': ['patience', 'sabr', 'steadfast'],
    'Trials': ['trial', 'fitnah', 'calamity', 'affliction'],
    'Knowledge': ['knowledge', 'ilm', 'learn', 'study'],
    'Marriage': ['marriage', 'wife', 'husband', 'spouse'],
    'Women': ['women', 'sister', 'female', 'niqab', 'hijab'],
    'Parents': ['parents', 'mother', 'father'],
    'Innovation': ['innovation', 'bidah'],
    'The Salaf': ['salaf', 'predecessors'],
    'Scholars': ['shaykh', 'uthaymin', 'albani', 'muqbil', 'bin baz'],
    'Ramadan': ['ramadan', 'fasting', 'iftar'],
    'Hajj': ['hajj', 'arafah', 'dhul hijjah'],
    'Manhaj': ['manhaj', 'methodology', 'salafi'],
    'Character': ['manners', 'character', 'haya', 'modesty'],
    'Repentance': ['repent', 'tawbah', 'forgiveness'],
    'Death': ['death', 'grave', 'akhirah', 'hereafter'],
    'Sincerity': ['sincerity', 'ikhlas', 'intention'],
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def has_arabic(text):
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
    return bool(arabic_pattern.search(text))

def generate_topics(text):
    topics = set()
    lower_text = text.lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in lower_text:
                topics.add(topic)
                break
    return sorted(list(topics))

def extract_text_from_entities(entities):
    if not entities:
        return ''
    text = ''
    for entity in entities:
        entity_type = entity.get('type', '')
        entity_text = entity.get('text', '')
        if entity_type == 'plain':
            text += entity_text
        elif entity_type == 'bold':
            text += f'**{entity_text}**'
        elif entity_type == 'italic':
            text += f'*{entity_text}*'
        elif entity_type == 'underline':
            text += f'_{entity_text}_'
        elif entity_type == 'blockquote':
            text += f'\n> {entity_text}\n'
        elif entity_type == 'text_link':
            text += f'[{entity_text}]({entity.get("href", "")})'
        elif entity_type == 'link':
            text += entity_text
        elif entity_type == 'hashtag':
            text += f'#{entity_text}'
        elif entity_type == 'mention':
            text += f'@{entity_text}'
        elif entity_type == 'code':
            text += f'`{entity_text}`'
        elif entity_type == 'custom_emoji':
            text += entity_text or ''
        else:
            text += entity_text or ''
    return text

def is_relevant_message(msg):
    if msg.get('type') == 'service':
        return False
    media_type = msg.get('media_type', '')
    if media_type in ['video_file', 'video', 'photo', 'sticker']:
        return False
    if msg.get('photo') or msg.get('video'):
        return False
    if not msg.get('text') and not msg.get('text_entities'):
        return False
    return True

def clean_text(text):
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def get_title(text):
    first_line = text.split('\n')[0].strip()
    first_line = re.sub(r'\*\*', '', first_line)
    first_line = re.sub(r'_', '', first_line)
    if len(first_line) > 80:
        return first_line[:80] + '...'
    return first_line or 'Untitled'

def extract_author(text):
    patterns = [
        r'Shaykh ([^\n,]+)',
        r'Sheikh ([^\n,]+)',
        r'Ibn ([^\n,]+)',
        r'Imām ([^\n,]+)',
        r'Imam ([^\n,]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

def clean_from_name(from_name):
    if not from_name:
        return 'Unknown'
    cleaned = re.sub(r'[^\w\s\u0600-\u06FF]', '', from_name)
    return cleaned.strip() or 'Unknown'

def process_paragraph(text):
    """
    Split text into separate paragraphs per line.
    Each non-empty line becomes its own paragraph.
    """
    lines = text.split('\n')
    # Strip each line, keep non-empty
    paragraphs = [line.strip() for line in lines if line.strip()]
    # Join with double newline to create separate <p> tags
    return '\n\n'.join(paragraphs)

# ============================================================
# MAIN CONVERSION FUNCTION
# ============================================================

def convert_json_to_markdown(json_path, output_dir):
    print('📖 Reading JSON...')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    messages = data.get('messages', [])
    print(f'📝 Found {len(messages)} messages')
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    converted = 0
    skipped = 0
    
    for msg in messages:
        if not is_relevant_message(msg):
            skipped += 1
            continue
        
        # Extract text
        text = ''
        if isinstance(msg.get('text'), str):
            text = msg['text']
        elif msg.get('text_entities'):
            text = extract_text_from_entities(msg['text_entities'])
        elif isinstance(msg.get('text'), list):
            parts = []
            for part in msg['text']:
                if isinstance(part, str):
                    parts.append(part)
                elif isinstance(part, dict):
                    parts.append(part.get('text', ''))
            text = ''.join(parts)
        
        text = clean_text(text)
        if len(text) < 10:
            skipped += 1
            continue
        
        # Process text to ensure each line is a separate paragraph
        text = process_paragraph(text)
        
        # Generate metadata
        topics = generate_topics(text)
        title = get_title(text)
        author = clean_from_name(msg.get('from'))
        quoted_author = extract_author(text)
        msg_id = msg.get('id')
        date = msg.get('date', datetime.now().isoformat())
        
        # Build frontmatter dict
        frontmatter = {
            'id': msg_id,
            'title': title,
            'date': date,
            'author': author,
            'quotedAuthor': quoted_author,
            'topics': topics,
            'type': 'message',
        }
        
        if msg.get('edited'):
            frontmatter['edited'] = msg['edited']
        if msg.get('forwarded_from'):
            frontmatter['forwarded_from'] = msg['forwarded_from']
        
        # Serialize frontmatter to YAML with all strings quoted
        yaml_str = yaml.dump(frontmatter, allow_unicode=True, default_style='"', sort_keys=False)
        
        # Build markdown content
        md_content = '---\n' + yaml_str + '---\n\n' + text
        
        # Write file
        output_file = Path(output_dir) / f'{msg_id}.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        converted += 1
    
    print(f'✅ Converted: {converted}')
    print(f'⏭️ Skipped: {skipped}')
    print(f'📁 Output: {output_dir}')

# ============================================================
# RUN
# ============================================================

if __name__ == '__main__':
    script_dir = Path(__file__).parent  # Go up to project root
    json_path = script_dir / 'result.json'
    output_dir = script_dir / 'src' / 'content' / 'posts'
    
    if not json_path.exists():
        print(f'❌ JSON not found at: {json_path}')
        print('💡 Place result.json in the project root')
        exit(1)
    
    # Remove old posts if they exist
    if output_dir.exists():
        import shutil
        backup_dir = script_dir / 'src' / 'content' / 'posts_backup'
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.move(str(output_dir), str(backup_dir))
        print(f'📦 Backed up old posts to {backup_dir}')
    
    convert_json_to_markdown(json_path, output_dir)
    print('\n✨ Done! Run `npm run dev` to see the site.')
