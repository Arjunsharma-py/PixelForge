# ui_main.py

from PySide6.QtWidgets import (
    QLabel, QPushButton, QComboBox, QSlider, QHBoxLayout,
    QVBoxLayout, QWidget, QCheckBox, QLineEdit, QMainWindow
)
from PySide6.QtCore import Qt
from config.settings import APP_TITLE, WINDOW_SIZE, SUPPORTED_FORMATS

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setFixedSize(*WINDOW_SIZE)

        self.image_path = None

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # UI Elements
        self.preview_label = QLabel("Image Preview")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setFixedHeight(180)
        self.preview_label.setStyleSheet("border: 1px solid #ccc;")

        self.label = QLabel("No image selected")
        self.label.setAlignment(Qt.AlignCenter)

        self.select_button = QPushButton("Select Image")

        self.format_box = QComboBox()
        self.format_box.addItems([fmt.lower() for fmt in SUPPORTED_FORMATS])

        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(75)

        self.quality_label = QLabel("Quality: 75")

        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Width")

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Height")

        self.aspect_check = QCheckBox("Maintain Aspect Ratio")

        self.process_button = QPushButton("Compress & Save")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.insertWidget(1, self.preview_label)
        layout.addWidget(self.select_button)

        layout.addWidget(QLabel("Output Format:"))
        layout.addWidget(self.format_box)

        layout.addWidget(self.quality_label)
        layout.addWidget(self.quality_slider)

        size_layout = QHBoxLayout()
        size_layout.addWidget(self.width_input)
        size_layout.addWidget(self.height_input)
        layout.addLayout(size_layout)
        layout.addWidget(self.aspect_check)

        layout.addWidget(self.process_button)

        central_widget.setLayout(layout)