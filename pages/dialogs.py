from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sqlite3

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

        # Get all sales records
        sql_query = """
            SELECT id, item_id, item_name, price, quantity, date_of_sale
            FROM sales_history
            ORDER BY date_of_sale DESC
        """

        # Execute the query and load data into the table
        self.cursor.execute(sql_query)
        records = self.cursor.fetchall()

        if not records:
            self.history_table.setRowCount(1)
            no_data_item = QTableWidgetItem("No data to display")
            no_data_item.setForeground(QBrush(Qt.black))  # Set text color to black
            self.history_table.setItem(0, 0, no_data_item)
            self.history_table.setSpan(0, 0, 1, 6)  # Span across all columns
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


class TransactionsDialog(QDialog):
    def __init__(self, parent=None):
        super(TransactionsDialog, self).__init__(parent)
        self.setWindowTitle("Transactions")
        self.resize(1000, 600)  # Larger dialog size for better visibility

        self.layout = QVBoxLayout(self)

        # Create the table for transactions
        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Transaction Id", "Date and Time", "Cashier", "Product", "Quantity", "Amount"
        ])
        self.layout.addWidget(self.history_table)

        self.init_db()
        self.load_data()

    def init_db(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        # Ensure `sales_history` table has the correct columns (this should already be correct)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                cashier TEXT,
                total_amount REAL,
                items TEXT,
                payment_method TEXT,
                item_id TEXT,
                item_name TEXT,
                price REAL,
                quantity INTEGER,
                date_of_sale TEXT
            )
        """)
        self.conn.commit()

    def load_data(self):
        # Clear the table
        self.history_table.setRowCount(0)

        # Get valid transactions
        sql_query = """
            SELECT id, date_of_sale, cashier, item_name, quantity, price
            FROM sales_history
            ORDER BY date_of_sale DESC
        """

        # Execute the query and load data into the table
        self.cursor.execute(sql_query)
        records = self.cursor.fetchall()

        if not records:
            self.history_table.setRowCount(1)
            no_data_item = QTableWidgetItem("No data to display")
            no_data_item.setForeground(QBrush(Qt.black))  # Set text color to black
            self.history_table.setItem(0, 0, no_data_item)
            self.history_table.setSpan(0, 0, 1, 6)  # Span across all columns
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
        self.setWindowTitle("Activities on Stocks and Products History")
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
        
        self.conn.commit()

    def load_data(self):
        # Clear the table
        self.history_table.setRowCount(0)

        # Get the filter option
        filter_option = self.filter_combo.currentText()

        # Generate SQL query based on filter option
        if filter_option == "Today":
            sql_query = f"SELECT product_id, name, category, description, date FROM stocks_history WHERE date(date) = date('now') ORDER BY date DESC"
        elif filter_option == "This Week":
            sql_query = f"SELECT product_id, name, category, description, date FROM stocks_history WHERE date(date) >= date('now', 'weekday 0', '-7 days') ORDER BY date DESC"
        elif filter_option == "This Month":
            sql_query = f"SELECT product_id, name, category, description, date FROM stocks_history WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now') ORDER BY date DESC"
        else:
            sql_query = f"SELECT product_id, name, category, description, date FROM stocks_history ORDER BY date DESC"

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



class InventoryHistoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Categories in POS')
        self.setGeometry(100, 100, 600, 400)  # Increased size of the dialog

        # Layout for the dialog
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Table to display category names
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(1)
        self.table_widget.setHorizontalHeaderLabels(['Category Name'])
        self.table_widget.horizontalHeader().setStyleSheet('color: #333333;')  # Dark text for the header
        self.table_widget.setStyleSheet('color: #333333;')  # Dark text for the table rows
        layout.addWidget(self.table_widget)

        # Fetch and display categories
        self.fetch_and_display_categories()

    def fetch_and_display_categories(self):
        # Connect to the database
        connection = sqlite3.connect('products.db')
        cursor = connection.cursor()
        
        # Query to get category names
        cursor.execute('SELECT name FROM categories')
        categories = cursor.fetchall()

        # Populate the table with category names
        self.table_widget.setRowCount(len(categories))
        for row_num, category in enumerate(categories):
            self.table_widget.setItem(row_num, 0, QTableWidgetItem(category[0]))

        connection.close()


class AlertsHistoryDialog(QDialog):
    def __init__(self, parent=None):
        super(AlertsHistoryDialog, self).__init__(parent)
        self.setWindowTitle("Alerts History")
        self.resize(800, 600)  # Adjusted size for better view

        self.layout = QVBoxLayout(self)

        # Create the table for alert history
        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(["Active Alerts", "Past Alerts"])
        self.layout.addWidget(self.history_table)

        self.init_db()
        self.load_data()

    def init_db(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        # Ensure `alerts_history` table has the correct columns
        
        self.conn.commit()

    def load_data(self):
        # Clear the table
        self.history_table.setRowCount(0)

        # Fetch active alerts
        self.cursor.execute("""
            SELECT description, date, additional_info FROM alerts_history 
            WHERE date >= date('now', 'start of day') ORDER BY date DESC
        """)
        active_alerts = self.cursor.fetchall()

        # Fetch past alerts
        self.cursor.execute("""
            SELECT description, date, additional_info FROM alerts_history 
            WHERE date < date('now', 'start of day') ORDER BY date DESC
        """)
        past_alerts = self.cursor.fetchall()

        # Populate the table with active and past alerts
        max_rows = max(len(active_alerts), len(past_alerts))
        self.history_table.setRowCount(max_rows)

        for row in range(max_rows):
            if row < len(active_alerts):
                description, date, additional_info = active_alerts[row]
                self.history_table.setItem(row, 0, QTableWidgetItem(description))
                self.history_table.setItem(row, 0, QTableWidgetItem(date))
                self.history_table.setItem(row, 0, QTableWidgetItem(additional_info))
            if row < len(past_alerts):
                description, date, additional_info = past_alerts[row]
                self.history_table.setItem(row, 1, QTableWidgetItem(description))
                self.history_table.setItem(row, 1, QTableWidgetItem(date))
                self.history_table.setItem(row, 1, QTableWidgetItem(additional_info))

        # Adjust column widths
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        for i in range(self.history_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
# =========================================SHOWING ALERTS =========================================
# usign self ensures you are calling an instance method
class AlertPopup(QDialog):
    def __init__(self, product, low_alert_level, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Low Stock Alert for {product}")
        self.setGeometry(0, 0, 300, 60)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowCloseButtonHint)
        self.setStyleSheet("""
            QDialog {
                background-color: #FFC107;
                border-radius: 15px;
                padding: 10px;
                border: 2px solid #FF9800;
            }
            QLabel {
                color: #000000;
                font-weight: bold;
            }
        """)
        self.initUI(product, low_alert_level)

    def initUI(self, product, low_alert_level):
        layout = QVBoxLayout(self)
        message = f"Product: {product} - Stock Alert: {low_alert_level}"
        alert_label = QLabel(message, self)
        alert_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(alert_label)
        self.setLayout(layout)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor("#FFC107")))
        path = QPainterPath()
        path.moveTo(self.width() - 20, 0)
        path.lineTo(self.width() - 0, 0)
        path.lineTo(self.width() - 10, 10)
        path.closeSubpath()
        painter.drawPath(path)

class AlertManager:
    def __init__(self):
        self.show_alerts()

    def show_alerts(self):
        connection = sqlite3.connect('products.db')
        cursor = connection.cursor()
        cursor.execute("SELECT name, low_alert_level, stock FROM products")
        products = cursor.fetchall()
        connection.close()
        for name, low_alert_level, stock in products:
            if stock <= low_alert_level:
                self.add_alert(name, low_alert_level)

    def add_alert(self, product, low_alert_level):
        alert_popup = AlertPopup(product, low_alert_level)
        screen_geometry = QApplication.primaryScreen().geometry()
        x_position = (screen_geometry.width() - alert_popup.width()) // 2 + 20
        # x_position = 50
        y_position = 32
        alert_popup.move(x_position, y_position)
        alert_popup.exec_()
        


class SalesHistoryDialog(QDialog):
    def __init__(self, parent=None):
        super(SalesHistoryDialog, self).__init__(parent)
        self.setWindowTitle("Sales History")
        self.resize(1000, 600)  # Larger dialog size

        self.layout = QVBoxLayout(self)

        # Create the table for sales history
        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Sale ID", "Item ID", "Item Name", "Price", "Quantity", "Date of Sale"
        ])
        self.layout.addWidget(self.history_table)

        self.init_db()
        self.load_data()

    def init_db(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        # Ensure `sales_history` table has the correct columns
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                cashier TEXT,
                total_amount REAL,
                items TEXT,
                payment_method TEXT,
                item_id TEXT,
                item_name TEXT,
                price REAL,
                quantity INTEGER,
                date_of_sale TEXT
            )
        """)
        self.conn.commit()

    def load_data(self):
        # Clear the table
        self.history_table.setRowCount(0)

        # Get all sales records
        sql_query = """
            SELECT id, item_id, item_name, price, quantity, date_of_sale
            FROM sales_history
            ORDER BY date_of_sale DESC
        """

        # Execute the query and load data into the table
        self.cursor.execute(sql_query)
        records = self.cursor.fetchall()

        if not records:
            self.history_table.setRowCount(1)
            no_data_item = QTableWidgetItem("No data to display")
            no_data_item.setForeground(QBrush(Qt.black))  # Set text color to black
            self.history_table.setItem(0, 0, no_data_item)
            self.history_table.setSpan(0, 0, 1, 6)  # Span across all columns
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
