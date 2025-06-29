from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from ui.ui_main import MainUI
from image_tools import compress_and_resize_image
from config.settings import APP_VERSION
import sys
import os

class App(MainUI):
    def __init__(self):
        super().__init__()
        self.setup_menu_bar()
        self.select_button.clicked.connect(self.select_image)
        self.quality_slider.valueChanged.connect(
            lambda val: self.quality_label.setText(f"Quality: {val}")
        )
        self.process_button.clicked.connect(self.process_image)

    def setup_menu_bar(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help Menu
        help_menu = menu_bar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        QMessageBox.about(
            self,
            "About PixelForge",
            f"<b>PixelForge {APP_VERSION}</b><br><br>"
            "A simple and powerful image compression and resizing tool.<br>"
            "Supports PNG, JPEG, and WebP formats.<br><br>"
            "Developed with PySide6.<br>"
            "© 2024 PixelForge Contributors"
        )


    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.webp)")
        if file_path:
            self.image_path = file_path
            self.label.setText(os.path.basename(file_path))

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.webp)")
        if file_path:
            self.image_path = file_path
            self.label.setText(os.path.basename(file_path))

            # Load and scale preview
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview_label.setPixmap(scaled_pixmap)


    def process_image(self):
        if not self.image_path:
            QMessageBox.warning(self, "No Image", "Please select an image first.")
            return

        from config import DEFAULT_OUTPUT_DIR
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)

        try:
            format_selected = self.format_box.currentText().upper()
            quality = self.quality_slider.value()
            width = int(self.width_input.text()) if self.width_input.text().isdigit() else None
            height = int(self.height_input.text()) if self.height_input.text().isdigit() else None
            keep_aspect = self.aspect_check.isChecked()

            output_path = os.path.join(
                DEFAULT_OUTPUT_DIR,
                f"{os.path.splitext(os.path.basename(self.image_path))[0]}_processed.{format_selected.lower()}"
            )

            success, message = compress_and_resize_image(
                self.image_path, output_path, quality, width, height, keep_aspect, format_selected
            )

            if success:
                QMessageBox.information(self, "Success", message)
            else:
                QMessageBox.critical(self, "Error", message)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/PixelForge.ico"))
    window = App()
    window.show()
    sys.exit(app.exec())
