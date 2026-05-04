import os
import shutil
import json

SOURCE_DIR = r"C:\Users\DartsgameKL\Documents\FONT BY AFDRYAN-20260504T102352Z-3-001\FONT BY AFDRYAN"
TARGET_DIR = r"f:\TokuFONT"
IMAGES_DIR = os.path.join(TARGET_DIR, "images")
FONTS_DIR = os.path.join(TARGET_DIR, "font")

mapping = {
    "BOON BOOM": {
        "id": "boonboomfont",
        "title": "BoonBoomFont Bakuage Sentai BoonBoomGer",
        "season_code": "bakuage-sentai-boonboomger",
        "description": "Custom font for Bakuage Sentai Boonboomger.",
        "url": "https://www.deviantart.com/afdryan/art/BoonBoomFont-Bakuage-Sentai-BoonBoomGer-1019264121"
    },
    "GAVV GRANUTE": {
        "id": "granute-script",
        "title": "Granute Script Font Kamen Rider Gavv",
        "season_code": "kamen-rider-gavv",
        "description": "Custom font for Kamen Rider Gavv.",
        "url": "https://www.deviantart.com/afdryan/art/Granute-Script-Font-Kamen-Rider-Gavv-1098882692"
    },
    "KINGOHGER": {
        "id": "kingohger-script",
        "title": "Ohsama Sentai King-Ohger Chikyuu Script Font",
        "season_code": "ohsama-sentai-king-ohger",
        "description": "Custom font for Ohsama Sentai King-Ohger.",
        "url": "https://www.deviantart.com/afdryan/art/Ohsama-Sentai-King-Ohger-Chikyuu-Script-Font-1040352932"
    },
    "Kamen rider GOTCHARD": {
        "id": "ride-chemy",
        "title": "Ride Chemy Card Font Kamen Rider Gotchard",
        "season_code": "kamen-rider-gotchard",
        "description": "Custom font for Kamen Rider Gotchard.",
        "url": "https://www.deviantart.com/afdryan/art/Ride-Chemy-Card-Font-Kamen-Rider-Gotchard-974191385"
    },
    "kamen rider BLADE": {
        "id": "rouze-card",
        "title": "Rouze Card Font Kamen Rider Blade",
        "season_code": "kamen-rider-blade",
        "description": "Custom font for Kamen Rider Blade.",
        "url": "https://www.deviantart.com/afdryan/art/Rouze-Card-Font-Kamen-Rider-Blade-1019861688"
    },
    "kamen rider SABER": {
        "id": "saber-font",
        "title": "Kamen Rider Saber Font",
        "season_code": "kamen-rider-saber",
        "description": "Custom font for Kamen Rider Saber.",
        "url": "https://www.deviantart.com/afdryan/art/Kamen-Rider-Saber-Font-Download-Link-on-Descript-847390935"
    }
}

fonts_json_path = os.path.join(TARGET_DIR, "fonts.json")
with open(fonts_json_path, 'r', encoding='utf-8') as f:
    fonts_data = json.load(f)

AUTHOR_NAME = "AFDRYAN"
AUTHOR_URL = "https://www.deviantart.com/afdryan"

for dir_name, meta in mapping.items():
    full_path = os.path.join(SOURCE_DIR, dir_name)
    if not os.path.exists(full_path):
        print(f"Skipping {dir_name}, path does not exist.")
        continue
    
    images = []
    font_files = []
    
    for root, _, files in os.walk(full_path):
        for file in files:
            ext = file.lower().split('.')[-1]
            src_file = os.path.join(root, file)
            
            if ext in ['png', 'jpg', 'jpeg', 'webp']:
                dst_file = os.path.join(IMAGES_DIR, file)
                if not os.path.exists(dst_file):
                    shutil.copy2(src_file, dst_file)
                images.append(f"images/{file}")
            elif ext in ['ttf', 'otf', 'woff', 'woff2']:
                dst_file = os.path.join(FONTS_DIR, file)
                if not os.path.exists(dst_file):
                    shutil.copy2(src_file, dst_file)
                font_files.append({"name": os.path.splitext(file)[0], "file": f"font/{file}"})
                
    if not images and not font_files:
        continue
        
    main_thumbnail = images[0] if images else ""
    
    new_entry = {
        "id": meta["id"],
        "title": meta["title"],
        "season_code": meta["season_code"],
        "description": meta["description"],
        "author": AUTHOR_NAME,
        "author_url": AUTHOR_URL,
        "official_source_url": meta["url"],
        "main_thumbnail": main_thumbnail,
        "thumbnails": images,
        "downloads": font_files
    }
    
    # Update if exists, else append
    existing = next((item for item in fonts_data if item["id"] == meta["id"]), None)
    if existing:
        idx = fonts_data.index(existing)
        fonts_data[idx] = new_entry
    else:
        fonts_data.append(new_entry)

with open(fonts_json_path, 'w', encoding='utf-8') as f:
    json.dump(fonts_data, f, indent=2, ensure_ascii=False)

print("Import complete!")
