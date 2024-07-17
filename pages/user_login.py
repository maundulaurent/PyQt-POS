import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from uifiles.login_ui import Ui_Form
from pages.dialogs import AlertManager

class LoginPage(QWidget, Ui_Form):
    def __init__(self, switch_to_admin_page, switch_to_dashboard_page):
        super().__init__()
        self.switch_to_admin_page = switch_to_admin_page
        self.switch_to_dashboard_page = switch_to_dashboard_page

        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT COUNT(*) FROM user WHERE role='admin'")
        self.has_admin = self.cursor.fetchone()[0] > 0 

        # self.init_db()
        self.setupUi(self)  # Set up the UI from the generated code
        self.init_ui()

    # def init_db(self):
    #     self.conn = sqlite3.connect('products.db')
    #     self.cursor = self.conn.cursor()

        # self.cursor.execute("SELECT COUNT(*) FROM user WHERE role='admin'")
        # has_admin = self.cursor.fetchone()[0] > 0
        # self.conn.commit()

    def init_ui(self):
        self.pushButton.clicked.connect(self.user_authenticate)
        self.label_5.clicked.connect(self.admin_authenticate)

    def admin_authenticate(self):
        if not self.has_admin:  # Only check if no admin exists
            self.cursor.execute("SELECT COUNT(*) FROM user WHERE role='admin'")
            self.has_admin = self.cursor.fetchone()[0] > 0

        if self.has_admin:
            dialog = AdminLoginDialog(self.conn, self.switch_to_admin_page)
            if dialog.exec_() == QDialog.Accepted:
                pass
        else:
            dialog = AdminSetupDialog(self.conn)
            if dialog.exec_() == QDialog.Accepted:
                # Update has_admin after successful setup (optional)
                self.cursor.execute("SELECT COUNT(*) FROM user WHERE role='admin'")
                self.has_admin = self.cursor.fetchone()[0] > 0
                

    def user_authenticate(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        self.cursor.execute("SELECT * FROM user WHERE username=? AND password=? AND role='user'", (username, password))
        result = self.cursor.fetchone()
        if result:
            self.switch_to_dashboard_page()
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.show_alert_dialog()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials')

    def show_alert_dialog(self):
        alert_manager = AlertManager()
# Admin Setup Dialog
class AdminSetupDialog(QDialog):
    def __init__(self, conn):
        super().__init__()
        
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()


        self.resize(320,250)
        self.setWindowTitle('Initial setUp for SuperUser')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.new_username_label = QLabel('Username:')
        self.new_username_input = QLineEdit()
        self.new_password_label = QLabel(' Password:')
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_label = QLabel('Confirm Password:')
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.save_button = QPushButton('Create SuperUser')
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
            self.cursor.execute('INSERT INTO user (username, password, role) VALUES(?, ?, ?)',  (new_username, new_password, 'admin'))
            self.conn.commit()
            QMessageBox.information(self, 'Success', 'SuperUser created successfully')
            self.accept()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Error', 'Username already exists')

# Admin Login Dialog
class AdminLoginDialog(QDialog):
    def __init__(self, conn, switch_to_admin_page):
        super().__init__()

        self.resize(280, 200)

        self.conn = conn
        self.switch_to_admin_page = switch_to_admin_page
        self.setWindowTitle('Login as Superuser')

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

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Example switch functions
    def switch_to_admin_page():
        print("Switching to admin page...")

    def switch_to_dashboard_page():
        print("Switching to dashboard page...")

    login_page = LoginPage(switch_to_admin_page, switch_to_dashboard_page)
    login_page.show()

    sys.exit(app.exec_())
