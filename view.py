import sys
import os
import json
import time
import base64
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
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
)
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QIcon, QFont, QPixmap
from management import DatabaseManager
from main_window import MainWindow

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


class UserInterfaceGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("qualsys")
        self.setGeometry(500, 200, 450, 450)
        self.database_manager = DatabaseManager()
        self.center()
        self.init_ui()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(self.current_dir, "logo.png")
        self.setWindowIcon(QIcon(icon_path))

    def init_ui(self):
        self.login_page()
        self.load_credentials()

    def login_page(self):
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

    def center(self):
        available_geometry = QApplication.primaryScreen().availableGeometry()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(available_geometry.center())
        self.move(frame_geometry.topLeft())

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
        self.main_window = MainWindow()

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


def main():
    app = QApplication(sys.argv)
    window = UserInterfaceGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
