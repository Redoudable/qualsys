import sys
from PySide2.QtCore import Qt  # Bu satırı ekledik
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFrame,
    QGridLayout,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Şık Ana Pencere")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background-color: #F0F0F0;")

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self.central_widget)

        self.menu_frame = QFrame(self.central_widget)
        self.content_frame = QFrame(self.central_widget)

        layout.addWidget(self.menu_frame, 0, 0)
        layout.addWidget(self.content_frame, 0, 1)

        self.show_menu_frame()

    def show_menu_frame(self):
        self.menu_frame.show()
        self.content_frame.hide()

        menu_layout = QVBoxLayout(self.menu_frame)

        menu_label = QLabel("Ana Menü")
        menu_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        menu_layout.addWidget(menu_label, alignment=Qt.AlignCenter)

        content_button = QPushButton("İçerik Sayfasına Git")
        content_button.setStyleSheet("padding: 10px; font-size: 14px;")
        content_button.clicked.connect(self.show_content_frame)
        menu_layout.addWidget(content_button, alignment=Qt.AlignCenter)

    def show_content_frame(self):
        self.menu_frame.hide()
        self.content_frame.show()

        content_layout = QVBoxLayout(self.content_frame)

        label = QLabel("İçerik Sayfası")
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        content_layout.addWidget(label, alignment=Qt.AlignCenter)

        back_button = QPushButton("Menüye Geri Dön")
        back_button.setStyleSheet("padding: 10px; font-size: 14px;")
        back_button.clicked.connect(self.show_menu_frame)
        content_layout.addWidget(back_button, alignment=Qt.AlignCenter)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
