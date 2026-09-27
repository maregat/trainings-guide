#!/usr/bin/env python3
"""
Update exercises.json: WebM → MP4 URLs
"""

import json
from pathlib import Path

with open('src/data/exercises.json') as f:
    data = json.load(f)

updated_count = 0
for ex_id, exercise in data['exercises'].items():
    if 'videoLink' in exercise and exercise['videoLink']:
        url = exercise['videoLink'].get('url', '')
        # Ersetze .webm mit .mp4
        if url and url.endswith('.webm'):
            new_url = url.replace('.webm', '.mp4')
            exercise['videoLink']['url'] = new_url
            print(f"✅ {exercise['name']:40s} → .mp4")
            updated_count += 1

with open('src/data/exercises.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✨ {updated_count} URLs aktualisiert!")
