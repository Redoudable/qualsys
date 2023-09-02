from PySide2.QtWidgets import QApplication

from core.management import DatabaseManager
from view import Qualsys


class MainController:
    def __init__(self, argv: list) -> None:
        self.app = QApplication(argv)
        self.manager = DatabaseManager()
        self.view = Qualsys()

    def run(self) -> int:
        self.view.show()
        
        return self.app.exec_()

    def list_documents(self):
        self.manager.list_documents()

    def insert_document(self, content, documentation_number, commits):
        self.manager.insert_document(content, documentation_number, commits)

    def delete_document(self, document_id):
        self.manager.delete_document(document_id)

    def update_document(self, document_id, new_content, new_commits):
        self.manager.update_document(document_id, new_content, new_commits)

    def insert_new_user(self, username, password, permission):
        self.manager.insert_new_user(username, password, permission)

    def delete_user(self, user_id):
        self.manager.delete_user(user_id)

    def list_users(self):
        self.manager.list_users()
