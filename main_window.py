import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFrame, QDialog, QDesktopWidget, QSpacerItem, QSizePolicy


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ana Pencere")
        self.setGeometry(100, 100, 1800, 1000)
        self.center_on_screen()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background-color: #F0F0F0;")

        self.init_ui()

    def center_on_screen(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        window_geometry = self.geometry()

        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        self.move(x, y)

    def init_ui(self):
        layout = QVBoxLayout(self.central_widget)

        self.menu_button = QPushButton("Menü")
        self.menu_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 14px;
                background-color: #4285F4;
                color: white;
                border: none;
                border-radius: 5px;
                border: 1px solid #4E565A;
            }
            
            QPushButton:hover {
                background-color: #4E565A;
                border: 1px solid #4E565A;
                border-top: 2px solid #000000;
                border-left: 2px solid #000000;
                border-right: 2px solid #000000;
                border-bottom: 2px solid #000000;
                border-radius: 6px;
                padding: 9px;
            }
        """)
        self.menu_button.clicked.connect(self.toggle_menu)
        layout.addWidget(self.menu_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.menu_frame = QFrame(self.central_widget)
        layout.addWidget(self.menu_frame)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        self.setup_menu_frame()
        self.menu_frame.hide()
        self.menu_button.setFixedHeight(40)
        self.menu_button.setFixedWidth(100)
        
        self.max_menu_frame_width = 175
        self.menu_frame.setFixedWidth(self.max_menu_frame_width)
        self.max_menu_frame_height = 900
        self.menu_frame.setFixedHeight(self.max_menu_frame_height)
        self.menu_frame.setSizePolicy(
        QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        new_width = min(self.central_widget.width(), self.max_menu_frame_width)
        self.menu_frame.setFixedWidth(new_width)
        new_height = min(self.central_widget.height(), self.max_menu_frame_height)
        self.menu_frame.setFixedHeight(new_height)
        
    def setup_menu_frame(self):
        menu_layout = QVBoxLayout(self.menu_frame)
        self.menu_frame.setStyleSheet(
        "background-color: #D9DADA; border: 1px solid #5E5971; border-radius: 10px; padding: 10px;")
        button_layout = QVBoxLayout()
        
        self.central_layout = QVBoxLayout(self.central_widget)

        self.menu_frame.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Expanding)

        button1 = QPushButton("Alt Pencere 1")
        button1.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 14px;
                background-color: #4285F4;
                color: white;
                border: none;
                border-radius: 5px;
                border: 1px solid #4E565A;
            }
            
            QPushButton:hover {
                background-color: #4E565A;
                border: 1px solid #4E565A;
                border-top: 2px solid #000000;
                border-left: 2px solid #000000;
                border-right: 2px solid #000000;
                border-bottom: 2px solid #000000;
                border-radius: 6px;
                padding: 9px;
            }
        """)
        button1.clicked.connect(self.open_subwindow1)
        button1.setCursor(Qt.PointingHandCursor)  # Farenin üzerine geldiğinde işaretçi şeklini değiştir
        button1.setObjectName("subbutton")  # Butonun adını belirtiyoruz
        button1.setFixedHeight(40)
        button1.setFixedWidth(150)
        button_layout.addWidget(button1, alignment=Qt.AlignLeft)
        
        button2 = QPushButton("Alt Pencere 2")
        button2.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 14px;
                background-color: #4285F4;
                color: white;
                border: none;
                border-radius: 5px;
                border: 1px solid #4E565A;
            }
            
            QPushButton:hover {
                background-color: #4E565A;
                border: 1px solid #4E565A;
                border-top: 2px solid #000000;
                border-left: 2px solid #000000;
                border-right: 2px solid #000000;
                border-bottom: 2px solid #000000;
                border-radius: 6px;
                padding: 9px;
            }
        """)
        button2.clicked.connect(self.open_subwindow2)
        button2.setCursor(Qt.PointingHandCursor)  # Farenin üzerine geldiğinde işaretçi şeklini değiştir
        button2.setFixedHeight(40)
        button2.setFixedWidth(150)
        button_layout.addWidget(button2, alignment=Qt.AlignLeft)

        button3 = QPushButton("Alt Pencere 3")
        button3.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 14px;
                background-color: #4285F4;
                color: white;
                border: none;
                border-radius: 5px;
                border: 1px solid #4E565A;
            }
            
            QPushButton:hover {
                background-color: #4E565A;
                border: 1px solid #4E565A;
                border-top: 2px solid #000000;
                border-left: 2px solid #000000;
                border-right: 2px solid #000000;
                border-bottom: 2px solid #000000;
                border-radius: 6px;
                padding: 9px;
            }
        """)
        button3.clicked.connect(self.open_subwindow3)
        button3.setCursor(Qt.PointingHandCursor)  # Farenin üzerine geldiğinde işaretçi şeklini değiştir
        button3.setFixedHeight(40)
        button3.setFixedWidth(150)
        button_layout.addWidget(button3, alignment=Qt.AlignLeft)

        button4 = QPushButton("Alt Pencere 4")
        button4.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 14px;
                background-color: #4285F4;
                color: white;
                border: none;
                border-radius: 5px;
                border: 1px solid #4E565A;
            }
            
            QPushButton:hover {
                background-color: #4E565A;
                border: 1px solid #4E565A;
                border-top: 2px solid #000000;
                border-left: 2px solid #000000;
                border-right: 2px solid #000000;
                border-bottom: 2px solid #000000;
                border-radius: 6px;
                padding: 9px;
            }
        """)
        button4.clicked.connect(self.open_subwindow4)
        button4.setCursor(Qt.PointingHandCursor)  # Farenin üzerine geldiğinde işaretçi şeklini değiştir
        button4.setFixedHeight(40)
        button4.setFixedWidth(150)
        button_layout.addWidget(button4, alignment=Qt.AlignLeft)

        menu_layout.addLayout(button_layout)  # Yeni buton layout'unu ana menü layout'una ekliyoruz

    def show_content_frame(self):
        pass  # İçerik sayfasını burada gösterme

    def open_subwindow1(self):
        sub_window = SubWindow(self, "Alt Pencere 1")
        sub_window.show()

    def open_subwindow2(self):
        sub_window = SubWindow(self, "Alt Pencere 2")
        sub_window.show()

    def open_subwindow3(self):
        sub_window = SubWindow(self, "Alt Pencere 3")
        sub_window.show()

    def open_subwindow4(self):
        sub_window = SubWindow(self, "Alt Pencere 4")
        sub_window.show()

    def toggle_menu(self):
        if self.menu_frame.isHidden():
            self.menu_frame.show()
        else:
            self.menu_frame.hide()


class SubWindow(QDialog):
    def __init__(self, parent=None, title="Alt Pencere"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(0, 0, 1500, 1000)
        self.center_on_screen()

        layout = QVBoxLayout(self)
        label = QLabel(f"{title}: Bu alt pencere bir butona tıklanarak açıldı.")
        layout.addWidget(label)

    def center_on_screen(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        window_geometry = self.geometry()

        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        self.move(x, y)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
