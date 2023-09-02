from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFrame,
    QDialog,
    QDesktopWidget,
    QSpacerItem,
    QSizePolicy,
)

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
