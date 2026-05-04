import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

with open('f:/TokuFONT/franchises.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for franchise in data:
    franchise['code'] = slugify(franchise['name'])
    for series in franchise['series']:
        series['code'] = slugify(series['name'])

# Add Project RED
project_red = {
    "name": "Project RED",
    "icon": "/icons/series/default.png",
    "code": "project-red",
    "series": [
        {
            "name": "Super Space Sheriff Gavan Infinity",
            "icon": "/icons/series/default.png",
            "code": "super-space-sheriff-gavan-infinity"
        }
    ]
}

# Check if Project RED already exists
exists = False
for f in data:
    if f['name'] == 'Project RED':
        exists = True
        break

if not exists:
    data.append(project_red)

with open('f:/TokuFONT/franchises.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("JSON updated successfully.")
