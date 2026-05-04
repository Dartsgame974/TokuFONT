import sys
import json
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QListWidget, QPushButton, QLabel, 
                             QLineEdit, QTextEdit, QComboBox, QFileDialog, 
                             QMessageBox, QFormLayout, QGroupBox, QInputDialog)
from PyQt5.QtCore import Qt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS_JSON = os.path.join(BASE_DIR, 'fonts.json')
FRANCHISES_JSON = os.path.join(BASE_DIR, 'franchises.json')
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
FONTS_DIR = os.path.join(BASE_DIR, 'font')

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(FONTS_DIR, exist_ok=True)

class FontManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TokuFONT Manager")
        self.resize(900, 700)
        
        self.fonts_data = []
        self.franchises_data = []
        self.current_font_index = -1

        self.load_data()
        self.init_ui()

    def load_data(self):
        if os.path.exists(FONTS_JSON):
            with open(FONTS_JSON, 'r', encoding='utf-8') as f:
                self.fonts_data = json.load(f)
        else:
            self.fonts_data = []

        if os.path.exists(FRANCHISES_JSON):
            with open(FRANCHISES_JSON, 'r', encoding='utf-8') as f:
                self.franchises_data = json.load(f)
        else:
            self.franchises_data = []

    def save_data(self):
        with open(FONTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.fonts_data, f, indent=2, ensure_ascii=False)
        QMessageBox.information(self, "Success", "fonts.json saved successfully!")

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Left panel (List)
        left_panel = QVBoxLayout()
        self.font_list = QListWidget()
        self.font_list.currentRowChanged.connect(self.on_font_selected)
        for font in self.fonts_data:
            self.font_list.addItem(font.get('title', 'Unknown'))
        
        btn_add_new = QPushButton("Add New Font")
        btn_add_new.clicked.connect(self.add_new_font)
        
        btn_save_all = QPushButton("Save All to JSON")
        btn_save_all.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 10px;")
        btn_save_all.clicked.connect(self.save_data)

        left_panel.addWidget(QLabel("<b>Existing Fonts:</b>"))
        left_panel.addWidget(self.font_list)
        left_panel.addWidget(btn_add_new)
        left_panel.addWidget(btn_save_all)

        main_layout.addLayout(left_panel, 1)

        # Right panel (Form)
        right_panel = QVBoxLayout()
        form_layout = QFormLayout()

        self.id_input = QLineEdit()
        self.title_input = QLineEdit()
        
        self.season_combo = QComboBox()
        self.populate_seasons()

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(80)

        self.author_input = QLineEdit()
        self.author_url_input = QLineEdit()
        self.official_url_input = QLineEdit()

        form_layout.addRow("ID (slug):", self.id_input)
        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Season:", self.season_combo)
        form_layout.addRow("Description:", self.desc_input)
        form_layout.addRow("Author:", self.author_input)
        form_layout.addRow("Author URL:", self.author_url_input)
        form_layout.addRow("Official URL:", self.official_url_input)

        # Main Thumbnail
        self.main_thumb_path = QLineEdit()
        btn_main_thumb = QPushButton("Browse Image")
        btn_main_thumb.clicked.connect(self.browse_main_thumb)
        thumb_layout = QHBoxLayout()
        thumb_layout.addWidget(self.main_thumb_path)
        thumb_layout.addWidget(btn_main_thumb)
        form_layout.addRow("Main Thumbnail:", thumb_layout)

        right_panel.addLayout(form_layout)

        # Carousel Thumbnails
        carousel_group = QGroupBox("Carousel Thumbnails")
        carousel_layout = QVBoxLayout()
        self.carousel_list = QListWidget()
        self.carousel_list.setMaximumHeight(80)
        btn_add_carousel = QPushButton("Add Image")
        btn_add_carousel.clicked.connect(self.add_carousel_thumb)
        carousel_layout.addWidget(self.carousel_list)
        carousel_layout.addWidget(btn_add_carousel)
        carousel_group.setLayout(carousel_layout)
        right_panel.addWidget(carousel_group)

        # Downloads
        dl_group = QGroupBox("Downloads")
        dl_layout = QVBoxLayout()
        self.dl_list = QListWidget()
        self.dl_list.setMaximumHeight(100)
        btn_add_dl = QPushButton("Add Download File")
        btn_add_dl.clicked.connect(self.add_download)
        dl_layout.addWidget(self.dl_list)
        dl_layout.addWidget(btn_add_dl)
        dl_group.setLayout(dl_layout)
        right_panel.addWidget(dl_group)

        # Save Button for current font
        btn_save_font = QPushButton("Apply Changes to Selected Font")
        btn_save_font.clicked.connect(self.apply_current_font)
        right_panel.addWidget(btn_save_font)

        main_layout.addLayout(right_panel, 2)
        
        self.clear_form()

    def populate_seasons(self):
        self.season_combo.clear()
        for franchise in self.franchises_data:
            for series in franchise.get('series', []):
                self.season_combo.addItem(f"{franchise['name']} - {series['name']}", series['code'])

    def add_new_font(self):
        self.current_font_index = -1
        self.font_list.clearSelection()
        self.clear_form()
        self.id_input.setFocus()

    def clear_form(self):
        self.id_input.clear()
        self.title_input.clear()
        self.desc_input.clear()
        self.author_input.clear()
        self.author_url_input.clear()
        self.official_url_input.clear()
        self.main_thumb_path.clear()
        self.carousel_list.clear()
        self.dl_list.clear()

    def on_font_selected(self, index):
        if index < 0 or index >= len(self.fonts_data):
            return
        self.current_font_index = index
        font = self.fonts_data[index]
        
        self.id_input.setText(font.get('id', ''))
        self.title_input.setText(font.get('title', ''))
        
        code = font.get('season_code', '')
        idx = self.season_combo.findData(code)
        if idx >= 0:
            self.season_combo.setCurrentIndex(idx)
            
        self.desc_input.setPlainText(font.get('description', ''))
        self.author_input.setText(font.get('author', ''))
        self.author_url_input.setText(font.get('author_url', ''))
        self.official_url_input.setText(font.get('official_source_url', ''))
        self.main_thumb_path.setText(font.get('main_thumbnail', ''))
        
        self.carousel_list.clear()
        for thumb in font.get('thumbnails', []):
            self.carousel_list.addItem(thumb)
            
        self.dl_list.clear()
        for dl in font.get('downloads', []):
            self.dl_list.addItem(f"{dl['name']} | {dl['file']}")

    def copy_file_to_project(self, file_path, target_dir, prefix_path):
        if not file_path or not os.path.exists(file_path):
            return ""
        
        # If it's already in our project, just return the relative path
        if BASE_DIR in os.path.abspath(file_path):
            rel = os.path.relpath(file_path, BASE_DIR)
            return rel.replace("\\", "/")
            
        filename = os.path.basename(file_path)
        dest_path = os.path.join(target_dir, filename)
        
        # Auto-rename if exists to prevent overwrite
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(target_dir, f"{base}_{counter}{ext}")
            counter += 1
            
        shutil.copy2(file_path, dest_path)
        rel_path = f"{prefix_path}/{os.path.basename(dest_path)}"
        return rel_path

    def browse_main_thumb(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Main Thumbnail", "", "Images (*.png *.jpg *.jpeg *.webp)")
        if file:
            rel_path = self.copy_file_to_project(file, IMAGES_DIR, "images")
            self.main_thumb_path.setText(rel_path)

    def add_carousel_thumb(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Carousel Image", "", "Images (*.png *.jpg *.jpeg *.webp)")
        if file:
            rel_path = self.copy_file_to_project(file, IMAGES_DIR, "images")
            self.carousel_list.addItem(rel_path)

    def add_download(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Font File", "", "Fonts (*.ttf *.otf *.woff *.woff2)")
        if file:
            name, ok = QInputDialog.getText(self, "Download Name", "Enter the display name for this download (e.g. 'Windows V2'):")
            if ok and name:
                rel_path = self.copy_file_to_project(file, FONTS_DIR, "font")
                self.dl_list.addItem(f"{name} | {rel_path}")

    def apply_current_font(self):
        if not self.id_input.text() or not self.title_input.text():
            QMessageBox.warning(self, "Error", "ID and Title are required!")
            return

        font_data = {
            "id": self.id_input.text().strip(),
            "title": self.title_input.text().strip(),
            "season_code": self.season_combo.currentData(),
            "description": self.desc_input.toPlainText().strip(),
            "author": self.author_input.text().strip(),
            "author_url": self.author_url_input.text().strip(),
            "official_source_url": self.official_url_input.text().strip(),
            "main_thumbnail": self.main_thumb_path.text().strip(),
            "thumbnails": [self.carousel_list.item(i).text() for i in range(self.carousel_list.count())],
            "downloads": []
        }

        for i in range(self.dl_list.count()):
            text = self.dl_list.item(i).text()
            if " | " in text:
                name, path = text.split(" | ", 1)
                font_data["downloads"].append({"name": name, "file": path})

        import zipfile
        if len(font_data["downloads"]) > 1:
            zips_dir = os.path.join(BASE_DIR, 'zips')
            os.makedirs(zips_dir, exist_ok=True)
            zip_filename = f"{font_data['id']}.zip"
            zip_path = os.path.join(zips_dir, zip_filename)
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for dl in font_data["downloads"]:
                    file_path = os.path.join(BASE_DIR, dl['file'])
                    if os.path.exists(file_path):
                        zipf.write(file_path, arcname=os.path.basename(file_path))
            font_data["zip_file"] = f"zips/{zip_filename}"

        if self.current_font_index == -1:
            self.fonts_data.append(font_data)
            self.font_list.addItem(font_data['title'])
            self.current_font_index = len(self.fonts_data) - 1
            self.font_list.setCurrentRow(self.current_font_index)
            QMessageBox.information(self, "Added", "New font added to the list. Don't forget to 'Save All'.")
        else:
            self.fonts_data[self.current_font_index] = font_data
            self.font_list.item(self.current_font_index).setText(font_data['title'])
            QMessageBox.information(self, "Updated", "Font updated. Don't forget to 'Save All'.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FontManager()
    window.show()
    sys.exit(app.exec_())
