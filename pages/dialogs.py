from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sqlite3
import sys

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


# ################################################
                # HISTORY PAGE DIALOGS#

class BaseHistoryDialog(QDialog):
    def __init__(self, table_name, title, parent=None):
        super(BaseHistoryDialog, self).__init__(parent)
        self.table_name = table_name
        self.setWindowTitle(title)
        self.resize(850, 400)

        self.layout = QVBoxLayout(self)
        
        self.filter_combo = QComboBox(self)
        self.filter_combo.addItems(["Today", "This Week", "This Month", "All Transactions"])
        self.filter_combo.currentIndexChanged.connect(self.load_data)
        self.layout.addWidget(self.filter_combo)

        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["ID", "Description", "Date", "Additional Info"])
        self.layout.addWidget(self.history_table)

        self.init_db()
        self.load_data()

    def init_db(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        # Check if table exists, and create it if not
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY,
                description TEXT,
                date TEXT,
                additional_info TEXT
            )
        """)
        self.conn.commit()

    def load_data(self):
        # Clear the table
        self.history_table.setRowCount(0)

        # Get the filter option
        filter_option = self.filter_combo.currentText()

        # Generate SQL query based on filter option
        if filter_option == "Today":
            sql_query = f"SELECT * FROM {self.table_name} WHERE date(date) = date('now')"
        elif filter_option == "This Week":
            sql_query = f"SELECT * FROM {self.table_name} WHERE date(date) >= date('now', 'weekday 0', '-7 days')"
        elif filter_option == "This Month":
            sql_query = f"SELECT * FROM {self.table_name} WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')"
        else:
            sql_query = f"SELECT * FROM {self.table_name}"

        # Execute the query and load data into the table
        self.cursor.execute(sql_query)
        records = self.cursor.fetchall()

        if not records:
            self.history_table.setRowCount(1)
            no_data_item = QTableWidgetItem("No data to display")
            no_data_item.setForeground(QBrush(Qt.black))  # Set text color to black
            self.history_table.setItem(0, 0, no_data_item)
        else:
            self.history_table.setRowCount(len(records))
            for row_index, row_data in enumerate(records):
                for column_index, column_data in enumerate(row_data):
                    self.history_table.setItem(row_index, column_index, QTableWidgetItem(str(column_data)))


class TransactionsDialog(BaseHistoryDialog):
    def __init__(self, parent=None):
        super(TransactionsDialog, self).__init__("transactions", "Transactions", parent)


class AccountsHistoryDialog(BaseHistoryDialog):
    def __init__(self, parent=None):
        super(AccountsHistoryDialog, self).__init__("accounts_history", "Accounts History", parent)

class OrdersHistoryDialog(QDialog):
    def __init__(self, parent=None):
        super(OrdersHistoryDialog, self).__init__(parent)
        self.setWindowTitle("Orders History")
        self.resize(900, 500)

        self.layout = QVBoxLayout(self)

        # Add a combo box for filter options (though we'll display all records now)
        self.filter_combo = QComboBox(self)
        self.filter_combo.addItems(["All Orders"])  # Only "All Orders" option
        self.filter_combo.setDisabled(True)  # Disable the filter combo box
        self.layout.addWidget(self.filter_combo)

        # Create the table for order history
        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(10)
        self.history_table.setHorizontalHeaderLabels([
            "Order Category", "Product", "Quantity", "Date of Order",
            "Ordered By", "Order Completed On", "Mode of Payment", "Who Paid",
            "Amount Received", "Confirmed By"
        ])
        self.layout.addWidget(self.history_table)

        self.init_db()
        self.load_data()

    def init_db(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        # Ensure `orders_history` table has the correct columns
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders_history (
                category TEXT,
                product TEXT,
                quantity TEXT,
                date_of_order TEXT,
                ordered_by TEXT,
                order_completed_on TEXT,
                mode_of_payment TEXT,
                who_paid TEXT,
                amount_received REAL,
                confirmed_by TEXT
            )
        """)
        self.conn.commit()

    def load_data(self):
        # Clear the table
        self.history_table.setRowCount(0)

        # Get all orders
        sql_query = """
            SELECT category, product, quantity, date_of_order, ordered_by, 
                   order_completed_on, mode_of_payment, who_paid, amount_received, confirmed_by
            FROM orders_history
            ORDER BY date_of_order DESC
        """

        # Execute the query and load data into the table
        self.cursor.execute(sql_query)
        records = self.cursor.fetchall()

        if not records:
            self.history_table.setRowCount(1)
            no_data_item = QTableWidgetItem("No data to display")
            no_data_item.setForeground(QBrush(Qt.black))  # Set text color to black
            self.history_table.setItem(0, 0, no_data_item)
            self.history_table.setSpan(0, 0, 1, 10)  # Span across all columns
        else:
            self.history_table.setRowCount(len(records))
            for row_index, row_data in enumerate(records):
                for column_index, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    item.setForeground(QBrush(Qt.black))  # Set text color to black
                    self.history_table.setItem(row_index, column_index, item)

        # Adjust column widths
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        for i in range(self.history_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

class StocksHistoryDialog(QDialog):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.table_name = table_name
        self.setWindowTitle("Activites on Stocks and Products History")
        self.resize(850, 400)

        self.layout = QVBoxLayout(self)
        
        self.filter_combo = QComboBox(self)
        self.filter_combo.addItems(["Today", "This Week", "This Month", "All Activities"])
        self.filter_combo.currentIndexChanged.connect(self.load_data)
        self.layout.addWidget(self.filter_combo)

        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Product ID", "Product Name", "Category", "Description", "Date"])
        self.layout.addWidget(self.history_table)

        self.init_db()
        self.load_data()

    def init_db(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        # Check if table exists, and create it if not
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS stocks_history (
                product_id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                description TEXT,
                date TEXT
            )
        """)
        self.conn.commit()

    def load_data(self):
        # Clear the table
        self.history_table.setRowCount(0)

        # Get the filter option
        filter_option = self.filter_combo.currentText()

        # Generate SQL query based on filter option
        if filter_option == "Today":
            sql_query = f"SELECT * FROM stocks_history WHERE date(date) = date('now') ORDER BY date DESC"
        elif filter_option == "This Week":
            sql_query = f"SELECT * FROM stocks_history WHERE date(date) >= date('now', 'weekday 0', '-7 days') ORDER BY date DESC"
        elif filter_option == "This Month":
            sql_query = f"SELECT * FROM stocks_history WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now') ORDER BY date DESC"
        else:
            sql_query = f"SELECT * FROM stocks_history ORDER BY date DESC"

        # Execute the query and load data into the table
        self.cursor.execute(sql_query)
        records = self.cursor.fetchall()

        if not records:
            self.history_table.setRowCount(1)
            no_data_item = QTableWidgetItem("No data to display")
            no_data_item.setForeground(QBrush(Qt.black))  # Set text color to black
            self.history_table.setItem(0, 0, no_data_item)
            self.history_table.setSpan(0, 0, 1, 5)  # Span across all columns
        else:
            self.history_table.setRowCount(len(records))
            for row_index, row_data in enumerate(records):
                for column_index, column_data in enumerate(row_data):
                    self.history_table.setItem(row_index, column_index, QTableWidgetItem(str(column_data)))

        # Adjust column widths
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        for i in range(self.history_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)


class InventoryHistoryDialog(BaseHistoryDialog):
    def __init__(self, parent=None):
        super(InventoryHistoryDialog, self).__init__("inventory_history", "Inventory History", parent)


class AlertsHistoryDialog(BaseHistoryDialog):
    def __init__(self, parent=None):
        super(AlertsHistoryDialog, self).__init__("alerts_history", "Alerts History", parent)


class SalesHistoryDialog(BaseHistoryDialog):
    def __init__(self, parent=None):
        super(SalesHistoryDialog, self).__init__("sales_history", "Sales History", parent)

