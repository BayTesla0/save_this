import sys
import os
import yt_dlp
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QFileDialog, QMessageBox, 
                             QComboBox, QHBoxLayout)

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.last_save_path = os.path.expanduser('~')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube İçerik İndirici')
        self.setGeometry(300, 300, 500, 300)

        layout = QVBoxLayout()

        # URL Girişi
        url_layout = QHBoxLayout()
        self.url_label = QLabel('YouTube URL:')
        self.url_input = QLineEdit()
        url_layout.addWidget(self.url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # İçerik Tipi Seçimi
        content_layout = QHBoxLayout()
        self.content_label = QLabel('İçerik Tipi:')
        self.content_type = QComboBox()
        self.content_type.addItems([
            'Tek Video', 
            'Kanal Videoları', 
            'Kanal Shortları', 
            'Oynatma Listesi'
        ])
        content_layout.addWidget(self.content_label)
        content_layout.addWidget(self.content_type)
        layout.addLayout(content_layout)

        # Kaydetme Konumu Seçimi
        path_layout = QHBoxLayout()
        self.path_label = QLabel(f'Kaydetme Konumu: {self.last_save_path}')
        self.path_button = QPushButton('Kaydetme Konumu Seç')
        self.path_button.clicked.connect(self.select_save_path)
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_button)
        layout.addLayout(path_layout)

        # İndirme Butonu
        self.download_button = QPushButton('İndir')
        self.download_button.clicked.connect(self.download_content)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def select_save_path(self):
        path = QFileDialog.getExistingDirectory(self, 'Kaydetme Konumu Seç', self.last_save_path)
        if path:
            self.last_save_path = path
            self.path_label.setText(f'Kaydetme Konumu: {path}')

    def download_content(self):
        url = self.url_input.text()
        content_type = self.content_type.currentText()
        
        if not url:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir URL girin.')
            return

        # Ortak indirme ayarları
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': f'{self.last_save_path}/%(title)s.%(ext)s',
        }

        # İçerik tipine göre farklı ayarlar
        if content_type == 'Tek Video':
            ydl_opts['nooverwrites'] = True
        elif content_type == 'Kanal Videoları':
            ydl_opts.update({
                'playlist_items': '1-100',  # İlk 100 video
            })
        elif content_type == 'Kanal Shortları':
            ydl_opts.update({
                # Shorts için match_filter fonksiyon olarak tanımlanmalı
                'match_filter': lambda info: 'duration' in info and info['duration'] < 60 or None,
                'playlist_items': '1-200',  # İlk 200 short
            })
        elif content_type == 'Oynatma Listesi':
            ydl_opts['nooverwrites'] = True

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            QMessageBox.information(self, 'Başarılı', f'{content_type} başarıyla indirildi!')
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'İndirme sırasında hata oluştu: {str(e)}')

def main():
    app = QApplication(sys.argv)
    ex = YouTubeDownloader()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
