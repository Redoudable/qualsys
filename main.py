import sys
from PySide2.QtWidgets import QApplication
from view import UserInterfaceGUI
from management import DatabaseManager


def main():
    app = QApplication(sys.argv)
    ui = UserInterfaceGUI()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
