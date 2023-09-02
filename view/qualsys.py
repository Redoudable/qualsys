
import os
import time
import base64
from PySide2.QtWidgets import (
    QFrame,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
    QCheckBox,
    QSizePolicy,
    QSpacerItem,
    QAction,
    QStackedWidget
)
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QIcon, QFont


from .sub_window import SubWindow


class PasswordEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEchoMode(QLineEdit.Password)

        # Çalışma dizini
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        self.toggle_icon = QAction(self)
        self.toggle_icon.setIcon(QIcon(os.path.join(self.current_dir, "invisible.png")))
        self.toggle_icon.triggered.connect(self.toggle_password_visibility)
        self.addAction(self.toggle_icon, QLineEdit.TrailingPosition)

    def toggle_password_visibility(self):
        if self.echoMode() == QLineEdit.Password:
            self.setEchoMode(QLineEdit.Normal)
            self.toggle_icon.setIcon(QIcon(os.path.join(self.current_dir, "visible.png")))  # type: ignore
        else:
            self.setEchoMode(QLineEdit.Password)
            self.toggle_icon.setIcon(QIcon(os.path.join(self.current_dir, "invisible.png")))  # type: ignore


class Qualsys(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("qualsys")
        self.setGeometry(500, 200, 450, 450)
        self.setWindowIcon(QIcon(r"view\resources\logo.png"))
        
        self._initUI()

    def _initUI(self):
        self._pageStack = QStackedWidget(self)
        self.loginPage = Login(self._pageStack)
        self.mainPage = Main(self._pageStack)
        
        self._pageStack.addWidget(self.loginPage)
        self._pageStack.addWidget(self.mainPage)
        
        LAYOUT = QHBoxLayout(self)
        LAYOUT.addWidget(self._pageStack)
        
    def checkbox_state_changed(self, state):
        if state == Qt.Checked:
            self.load_credentials()
        else:
            self.clear_credentials()

    def load_credentials(self):
        try:
            with open("credentials.json", "r") as file:
                lines = file.readlines()
                if lines:
                    last_line = lines[-1].strip()
                    if last_line:
                        username, encrypted_password = last_line.split(",")
                        password = base64.b64decode(
                            encrypted_password.encode()
                        ).decode()
                        self.username_input.setText(username)
                        self.password_input.setText(password)
                        self.remember_checkbox.setChecked(True)
        except FileNotFoundError:
            print("credentials.json not found.")
        except Exception as e:
            print("Error loading credentials:", e)

    def create_credentials_file(self):
        try:
            with open("credentials.json", "w") as file:
                pass
        except Exception as e:
            print("Error creating credentials file:", e)

    def save_credentials(self):
        try:
            username = self.username_input.text()
            password = self.password_input.text()

            with open("credentials.json", "a") as file:
                encrypted_password = base64.b64encode(password.encode()).decode()
                credentials = f"{username},{encrypted_password}\n"
                file.write(credentials)
        except Exception as e:
            print("Error saving credentials:", e)

    def clear_credentials(self):
        self.username_input.clear()
        self.password_input.clear()
        if not self.remember_checkbox.isChecked():
            try:
                os.remove("credentials.json")
            except FileNotFoundError:
                pass

    def login(self):
        connection = self.database_manager.get_connection()
        if connection is not None:
            cursor = connection.cursor()
            username = self.username_input.text()
            password = self.password_input.text()
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, password),
            )
            user_data = cursor.fetchone()
            connection.close()
            if user_data:
                self.result_label.setText("Login successful")
                self.successful_login()
            else:
                self.result_label.setText("Login failed. Try again.")
                self.username_input.clear()
                self.password_input.clear()

    def successful_login(self):
        self.result_label.setText("Login successful")
        self.repaint()
        time.sleep(2)
        self.hide()
        self.main_window = Main()

        # QTimer kullanarak ana ekranı bir süre sonra göster
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_main_window)
        self.timer.start(1000)  # 1000 milisaniye (1 saniye) bekleyecek

        # Beni Hatırla işaretli ise kullanıcı adı ve parolayı credentials.txt dosyasına kaydet
        if self.remember_checkbox.isChecked():
            self.save_credentials()

    def show_main_window(self):
        self.main_window.show()
        self.timer.stop()  # Timer'ı durdur
        self.load_credentials()  # Kaydedilen kullanıcı adı ve şifreyi doldur


class Login(QFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setContentsMargins(70, 200, 70, 150)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # type: ignore

        self.username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setFixedWidth(200)
        font = QFont("GeoSlab703 Md BT", 15)
        self.username_input.setPlaceholderText("Username")
        font = QFont("GeoSlab703 Md BT", 10)
        self.username_label.setFont(font)
        self.username_input.setFont(font)
        self.username_label.setBuddy(self.username_input)
        self.username_input.setStyleSheet(
            """
    QLineEdit {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 5px;
        background-color: white;
        color: #4E565A;
    }

    QLineEdit:focus {
        border: 2px solid #97A59A;
    }
"""
        )
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        self.username_input.setMaxLength(20)

        self.password_label = QLabel("Password")
        self.password_input = PasswordEdit()
        self.password_input.setFixedWidth(200)
        font = QFont("GeoSlab703 Md BT", 15)
        self.password_input.setPlaceholderText("Password")
        font = QFont("GeoSlab703 Md BT", 10)
        self.password_label.setFont(font)
        self.password_input.setFont(font)
        self.password_label.setBuddy(self.password_input)
        self.password_input.setStyleSheet(
            """
    QLineEdit {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 5px;
        background-color: white;
        color: #4E565A;
    }

    QLineEdit:focus {
        border: 2px solid #97A59A;
    }
"""
        )
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.remember_checkbox = QCheckBox("Beni Hatırla")
        self.remember_checkbox.stateChanged.connect(self.checkbox_state_changed)
        font = QFont("GeoSlab703 Md BT", 10)
        self.remember_checkbox.setFont(font)
        self.remember_checkbox.setStyleSheet(
            """
    QCheckBox {
        color: #333;
    }

    QCheckBox::indicator {
        width: 20px;
        height: 20px;
    }

    QCheckBox::indicator:unchecked {
        border: 2px solid #4E565A;
        border-radius: 6px;
    }

    QCheckBox::indicator:checked {
        background-color: None;
        border-radius: 6px;
        image: url(check.png);
    }
"""
        )
        layout.addWidget(self.remember_checkbox)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        font = QFont("GeoSlab703 Md BT", 15)
        self.login_button.setFont(font)
        self.login_button.setStyleSheet(
            """
    QPushButton {
        background-color: #97A59A;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }

    QPushButton:hover {
        background-color: #4E565A;
    }
"""
        )
        layout.addWidget(self.login_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        spacer_item = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer_item)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.version_label = QLabel("ver 0.1")
        self.statusBar().addWidget(self.version_label, 1)

class Main(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
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
        self.menu_button.setStyleSheet(
            """
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
        """
        )
        self.menu_button.clicked.connect(self.toggle_menu)
        layout.addWidget(self.menu_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        self.menu_frame = QFrame(self.central_widget)
        layout.addWidget(self.menu_frame)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        self.setup_menu_frame()
        self.menu_frame.hide()
        self.menu_button.setFixedHeight(40)
        self.menu_button.setFixedWidth(200)

        self.max_menu_frame_width = 200
        self.menu_frame.setFixedWidth(self.max_menu_frame_width)
        self.max_menu_frame_height = 900
        self.menu_frame.setFixedHeight(self.max_menu_frame_height)
        self.menu_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        new_width = min(self.central_widget.width(), self.max_menu_frame_width)
        self.menu_frame.setFixedWidth(new_width)
        new_height = min(self.central_widget.height(), self.max_menu_frame_height)
        self.menu_frame.setFixedHeight(new_height)

    def setup_menu_frame(self):
        menu_layout = QVBoxLayout(self.menu_frame)
        self.menu_frame.setStyleSheet(
            "background-color: #D9DADA; border: 1px solid #5E5971; border-radius: 10px; padding: 10px;"
        )
        button_layout = QVBoxLayout()

        self.central_layout = QVBoxLayout(self.central_widget)

        self.menu_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        button1 = QPushButton("Alt Pencere 1")
        button1.setStyleSheet(
            """
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
        """
        )
        button1.clicked.connect(self.open_subwindow1)
        button1.setCursor(
            Qt.PointingHandCursor
        )  # Farenin üzerine geldiğinde işaretçi şeklini değiştir
        button1.setObjectName("subbutton")  # Butonun adını belirtiyoruz
        button1.setFixedHeight(40)
        button1.setFixedWidth(150)
        button_layout.addWidget(button1, alignment=Qt.AlignLeft)

        button2 = QPushButton("Alt Pencere 2")
        button2.setStyleSheet(
            """
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
        """
        )
        button2.clicked.connect(self.open_subwindow2)
        button2.setCursor(
            Qt.PointingHandCursor
        )  # Farenin üzerine geldiğinde işaretçi şeklini değiştir
        button2.setFixedHeight(40)
        button2.setFixedWidth(150)
        button_layout.addWidget(button2, alignment=Qt.AlignLeft)

        button3 = QPushButton("Alt Pencere 3")
        button3.setStyleSheet(
            """
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
        """
        )
        button3.clicked.connect(self.open_subwindow3)
        button3.setCursor(
            Qt.PointingHandCursor
        )  # Farenin üzerine geldiğinde işaretçi şeklini değiştir
        button3.setFixedHeight(40)
        button3.setFixedWidth(150)
        button_layout.addWidget(button3, alignment=Qt.AlignLeft)

        button4 = QPushButton("Alt Pencere 4")
        button4.setStyleSheet(
            """
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
        """
        )
        button4.clicked.connect(self.open_subwindow4)
        button4.setCursor(
            Qt.PointingHandCursor
        )  # Farenin üzerine geldiğinde işaretçi şeklini değiştir
        button4.setFixedHeight(40)
        button4.setFixedWidth(150)
        button_layout.addWidget(button4, alignment=Qt.AlignLeft)

        menu_layout.addLayout(
            button_layout
        )  # Yeni buton layout'unu ana menü layout'una ekliyoruz

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

