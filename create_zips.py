import os
import json
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_JSON = os.path.join(BASE_DIR, 'fonts.json')
ZIPS_DIR = os.path.join(BASE_DIR, 'zips')

os.makedirs(ZIPS_DIR, exist_ok=True)

with open(FONTS_JSON, 'r', encoding='utf-8') as f:
    fonts_data = json.load(f)

for font in fonts_data:
    downloads = font.get('downloads', [])
    if len(downloads) > 1:
        zip_filename = f"{font['id']}.zip"
        zip_path = os.path.join(ZIPS_DIR, zip_filename)
        
        # Create ZIP file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for dl in downloads:
                file_path = os.path.join(BASE_DIR, dl['file'])
                if os.path.exists(file_path):
                    # Add to zip with just the filename
                    zipf.write(file_path, arcname=os.path.basename(file_path))
                else:
                    print(f"Warning: File not found {file_path}")
        
        font['zip_file'] = f"zips/{zip_filename}"
        print(f"Created ZIP for {font['id']}")
    else:
        # If only 1 file, no need for zip. Ensure key is removed if it was there
        font.pop('zip_file', None)

with open(FONTS_JSON, 'w', encoding='utf-8') as f:
    json.dump(fonts_data, f, indent=2, ensure_ascii=False)

print("ZIP creation complete!")
