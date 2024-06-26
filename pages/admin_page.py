import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


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

        self.edit_user_button = QPushButton('Edit User')
        self.edit_user_button.clicked.connect(self.edit_user_dialog)

        self.delete_user_button = QPushButton('Delete User')
        self.delete_user_button.clicked.connect(self.delete_user_dialog)

        # Display user list (optional)
        self.user_list = QListWidget()
        self.update_user_list()

        self.layout.addWidget(self.create_user_button)
        self.layout.addWidget(self.edit_user_button)
        self.layout.addWidget(self.delete_user_button)
        self.layout.addWidget(self.user_list)

    def update_user_list(self):
        self.user_list.clear()
        self.cursor.execute("SELECT username FROM user")
        users = self.cursor.fetchall()
        for user in users:
            self.user_list.addItem(user[0])

    def create_user_dialog(self):
        dialog = CreateUserDialog(self.conn, parent=self)
        dialog.exec_()
        self.update_user_list()

    def edit_user_dialog(self):
        selected_item = self.user_list.currentItem()
        if selected_item:
            username = selected_item.text()
            dialog = EditUserDialog(self.conn, username, parent=self)
            dialog.exec_()
            self.update_user_list()

    def delete_user_dialog(self):
        selected_item = self.user_list.currentItem()
        if selected_item:
            username = selected_item.text()
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


# Dialog to create a new user
class CreateUserDialog(QDialog):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.setWindowTitle('Create User')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.create_button = QPushButton('Create')
        self.create_button.clicked.connect(self.create_user)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.create_button)

    def create_user(self):
        new_username = self.username_input.text()
        new_password = self.password_input.text()

        if not new_username or not new_password:
            QMessageBox.warning(self, 'Error', 'Username and Password cannot be empty')
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (new_username, new_password))
            self.conn.commit()
            QMessageBox.information(self, 'Success', 'User created successfully')
            self.accept()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Error', 'Username already exists')


# Dialog to edit an existing user
class EditUserDialog(QDialog):
    def __init__(self, conn, username, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.username = username
        self.setWindowTitle(f'Edit User: {username}')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.new_password_label = QLabel('New Password:')
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_label = QLabel('Confirm Password:')
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_user)

        self.layout.addWidget(self.new_password_label)
        self.layout.addWidget(self.new_password_input)
        self.layout.addWidget(self.confirm_password_label)
        self.layout.addWidget(self.confirm_password_input)
        self.layout.addWidget(self.save_button)

    def save_user(self):
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not new_password or not confirm_password:
            QMessageBox.warning(self, 'Error', 'Password fields cannot be empty')
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE user SET password=? WHERE username=?", (new_password, self.username))
            self.conn.commit()
            QMessageBox.information(self, 'Success', 'User credentials updated successfully')
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.warning(self, 'Error', f'Failed to update user "{self.username}": {str(e)}')

