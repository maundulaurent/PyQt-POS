import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



# Admin Page
class LoginPage(QWidget):
    def __init__(self, switch_to_admin_page, switch_to_dashboard_page):
        super().__init__()
        self.switch_to_admin_page = switch_to_admin_page
        self.switch_to_dashboard_page = switch_to_dashboard_page

        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        self.init_db()
        self.init_ui()

        # Database Initialization
    def init_db(self):
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()
        
        # Create user table if it does not exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username TEXT NOT NULL UNIQUE, 
                        password TEXT NOT NULL,
                        role TEXT NOT NULL DEFAULT 'user')''')
        
        # Check if there's any admin user, if not create the default admin
        self.cursor.execute("SELECT COUNT(*) FROM user WHERE role='admin'")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO user (username, password, role) VALUES ('admin', 'admin', 'admin')")
        
        self.conn.commit()

    def init_ui(self):      
        self.setWindowTitle("POS LoginPage")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.user_authenticate)

        self.admin_login = QPushButton('or Login as Admin')
        self.admin_login.clicked.connect(self.admin_authenticate)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.admin_login)

    def admin_authenticate(self):
        self.cursor.execute("SELECT COUNT(*) FROM user WHERE role='admin'")
        if self.cursor.fetchone()[0] > 0:
            dialog = AdminLoginDialog(self.conn, self.switch_to_admin_page)
            dialog.exec_()
        else:
            dialog = AdminSetupDialog(self.conn)
            dialog.exec_()
    def user_authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        self.cursor.execute("SELECT * FROM user WHERE username=? AND password=? AND role='user'", (username, password))
        result = self.cursor.fetchone()

        if result:

            # QMessageBox.information(self, 'Success', 'User login successful')
            self.switch_to_dashboard_page()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials')
        # QMessageBox.information(self, 'User Login', 'User authentication Coming')



# Admin Setup Dialog
class AdminSetupDialog(QDialog):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.setWindowTitle('Admin Setup')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.new_username_label = QLabel('New Username:')
        self.new_username_input = QLineEdit()
        self.new_password_label = QLabel('New Password:')
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_label = QLabel('Confirm Password:')
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.save_button = QPushButton('Login')
        self.save_button.clicked.connect(self.save_new_admin)

        self.layout.addWidget(self.new_username_label)
        self.layout.addWidget(self.new_username_input)
        self.layout.addWidget(self.new_password_label)
        self.layout.addWidget(self.new_password_input)
        self.layout.addWidget(self.confirm_password_label)
        self.layout.addWidget(self.confirm_password_input)
        self.layout.addWidget(self.save_button)

    def save_new_admin(self):
        new_username = self.new_username_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not new_username or not new_password or not confirm_password:
            QMessageBox.warning(self, 'Error', 'Fields cannot be empty')
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
            return

        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('UPDATE user SET username=?, password=? WHERE role="admin"', (new_username, new_password))
            self.conn.commit()
            QMessageBox.information(self, 'Success', 'Admin credentials updated successfully')
            self.accept()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Error', 'Username already exists')

# Admin Login Dialog
class AdminLoginDialog(QDialog):


    def __init__(self, conn, switch_to_admin_page):
        super().__init__()
        
        self.conn = conn
        self.switch_to_admin_page = switch_to_admin_page
        self.setWindowTitle('Admin Login')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.authenticate)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username=? AND password=? AND role='admin'", (username, password))
        result = cursor.fetchone()

        if result:
            # QMessageBox.information(self, 'Success', 'Admin login successful')
            self.accept()
            self.switch_to_admin_page()
            # Open admin page or perform other actions
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials')