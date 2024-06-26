from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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

class EditProfileDialog(QDialog):
    def __init__(self, conn, username, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.username = username
        self.setWindowTitle(f'Edit Profile: {username}')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.other_names_label = QLabel('Other Names:')
        self.other_names_input = QLineEdit()
        self.email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        self.phone_label = QLabel('Phone Number:')
        self.phone_input = QLineEdit()
        self.postal_code_label = QLabel('Postal Code:')
        self.postal_code_input = QLineEdit()

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_profile)

        self.layout.addWidget(self.other_names_label)
        self.layout.addWidget(self.other_names_input)
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.phone_label)
        self.layout.addWidget(self.phone_input)
        self.layout.addWidget(self.postal_code_label)
        self.layout.addWidget(self.postal_code_input)
        self.layout.addWidget(self.save_button)

        self.load_user_profile()

    def load_user_profile(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT other_names, email, phone_number, postal_code FROM user WHERE username=?", (self.username,))
        user = cursor.fetchone()

        if user:
            self.other_names_input.setText(user[0] if user[0] else '')
            self.email_input.setText(user[1] if user[1] else '')
            self.phone_input.setText(user[2] if user[2] else '')
            self.postal_code_input.setText(user[3] if user[3] else '')

    def save_profile(self):
        other_names = self.other_names_input.text()
        email = self.email_input.text()
        phone_number = self.phone_input.text()
        postal_code = self.postal_code_input.text()

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE user 
                SET other_names=?, email=?, phone_number=?, postal_code=? 
                WHERE username=?
            """, (other_names, email, phone_number, postal_code, self.username))
            self.conn.commit()
            QMessageBox.information(self, 'Success', 'User profile updated successfully')
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.warning(self, 'Error', f'Failed to update user profile: {str(e)}')
