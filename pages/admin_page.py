import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pages.dialogs import CreateUserDialog, EditUserDialog, EditProfileDialog

# Admin Page
class AdminPage(QWidget):
    def __init__(self):
        super().__init__()

        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Admin Page")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create buttons for user management
        self.create_user_button = QPushButton('Create User')
        self.create_user_button.clicked.connect(self.create_user_dialog)

        self.edit_profile_button = QPushButton('Edit Profile')
        self.edit_profile_button.clicked.connect(self.edit_profile_dialog)

        # Display user list (optional)
        self.user_list = QListWidget()
        self.update_user_list()

        self.layout.addWidget(self.create_user_button)
        self.layout.addWidget(self.edit_profile_button)
        self.layout.addWidget(self.user_list)

    def update_user_list(self):
        self.user_list.clear()
        self.cursor.execute("SELECT username FROM user")
        users = self.cursor.fetchall()
        for user in users:
            user_widget = self.create_user_widget(user[0])
            list_item = QListWidgetItem(self.user_list)
            list_item.setSizeHint(user_widget.sizeHint())
            self.user_list.addItem(list_item)
            self.user_list.setItemWidget(list_item, user_widget)

    def create_user_widget(self, username):
        widget = QWidget()
        layout = QHBoxLayout()

        user_label = QLabel(username)
        edit_button = QPushButton('Edit')
        edit_button.clicked.connect(lambda: self.edit_user_dialog(username))
        delete_button = QPushButton('Delete')
        delete_button.clicked.connect(lambda: self.delete_user_dialog(username))

        layout.addWidget(user_label)
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        widget.setLayout(layout)

        return widget

    def create_user_dialog(self):
        dialog = CreateUserDialog(self.conn, parent=self)
        dialog.exec_()
        self.update_user_list()

    def edit_user_dialog(self, username):
        dialog = EditUserDialog(self.conn, username, parent=self)
        dialog.exec_()
        self.update_user_list()

    def delete_user_dialog(self, username):
        reply = QMessageBox.question(self, 'Delete User', f'Are you sure you want to delete user "{username}"?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.delete_user(username)
            self.update_user_list()

    def delete_user(self, username):
        try:
            self.cursor.execute("DELETE FROM user WHERE username=?", (username,))
            self.conn.commit()
            QMessageBox.information(self, 'Success', f'User "{username}" deleted successfully')
        except sqlite3.Error as e:
            QMessageBox.warning(self, 'Error', f'Failed to delete user "{username}": {str(e)}')

    def edit_profile_dialog(self):
        selected_item = self.user_list.currentItem()
        if selected_item:
            username = self.user_list.itemWidget(selected_item).layout().itemAt(0).widget().text()
            dialog = EditProfileDialog(self.conn, username, parent=self)
            dialog.exec_()
            self.update_user_list()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = AdminPage()
    window.show()
    sys.exit(app.exec_())
