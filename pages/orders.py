import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class AddOrderDialog(QDialog):
    def __init__(self, parent=None):
        super(AddOrderDialog, self).__init__(parent)
        self.setWindowTitle("Add Order")
        self.resize(600, 250)

        layout = QFormLayout(self)

        self.product_label = QLabel("Product:")
        self.product_input = QLineEdit(self)
        layout.addRow(self.product_label, self.product_input)

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit(self)
        layout.addRow(self.quantity_label, self.quantity_input)

        self.date_label = QLabel("Date of Order:")
        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        layout.addRow(self.date_label, self.date_input)

        self.category_label = QLabel("Order Category:")
        self.category_input = QComboBox(self)
        layout.addRow(self.category_label, self.category_input)

        self.ordered_by_label = QLabel("Ordered by:")
        self.ordered_by_input = QLineEdit(self)
        layout.addRow(self.ordered_by_label, self.ordered_by_input)

        self.add_button = QPushButton("Add Order")
        self.add_button.clicked.connect(self.add_order)
        layout.addRow(self.add_button)

        self.load_categories()

    def load_categories(self):
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category_name FROM order_categories")
        categories = cursor.fetchall()
        for category in categories:
            self.category_input.addItem(category[0])
        conn.close()

    def add_order(self):
        product = self.product_input.text()
        quantity = self.quantity_input.text()
        date_of_order = self.date_input.date().toString(Qt.ISODate)
        category = self.category_input.currentText()
        ordered_by = self.ordered_by_input.text()

        if not product or not quantity or not date_of_order or not category or not ordered_by:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields")
            return

        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("""
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
        cursor.execute("""
            INSERT INTO orders_history (category, product, quantity, date_of_order, ordered_by)
            VALUES (?, ?, ?, ?, ?)
        """, (category, product, quantity, date_of_order, ordered_by))
        conn.commit()
        conn.close()

        self.accept()

class AddCategoryDialog(QDialog):
    def __init__(self, parent=None):
        super(AddCategoryDialog, self).__init__(parent)
        self.setWindowTitle("Add Order Category")
        self.resize(400, 100)

        layout = QFormLayout(self)

        self.category_name_label = QLabel("Category Name:")
        self.category_name_input = QLineEdit(self)
        layout.addRow(self.category_name_label, self.category_name_input)

        self.add_button = QPushButton("Add Category")
        self.add_button.clicked.connect(self.add_category)
        layout.addRow(self.add_button)

    def add_category(self):
        category_name = self.category_name_input.text()

        if not category_name:
            QMessageBox.warning(self, "Input Error", "Please fill in the category name")
            return

        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_categories (
                id INTEGER PRIMARY KEY,
                category_name TEXT
            )
        """)
        cursor.execute("INSERT INTO order_categories (category_name) VALUES (?)", (category_name,))
        conn.commit()
        conn.close()

        self.accept()

class CompleteOrderDialog(QDialog):
    def __init__(self, order, parent=None):
        super(CompleteOrderDialog, self).__init__(parent)
        self.setWindowTitle("Complete Order")
        self.resize(600, 400)

        layout = QFormLayout(self)

        self.order = order

        self.category_label = QLabel("Order Category:")
        self.category_input = QLineEdit(order[0])
        self.category_input.setReadOnly(True)
        layout.addRow(self.category_label, self.category_input)

        self.product_label = QLabel("Product:")
        self.product_input = QLineEdit(order[1])
        self.product_input.setReadOnly(True)
        layout.addRow(self.product_label, self.product_input)

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit(str(order[2]))
        self.quantity_input.setReadOnly(True)
        layout.addRow(self.quantity_label, self.quantity_input)

        self.date_label = QLabel("Date of Order:")
        self.date_input = QLineEdit(order[3])
        self.date_input.setReadOnly(True)
        layout.addRow(self.date_label, self.date_input)

        self.ordered_by_label = QLabel("Ordered by:")
        self.ordered_by_input = QLineEdit(order[4])
        self.ordered_by_input.setReadOnly(True)
        layout.addRow(self.ordered_by_label, self.ordered_by_input)

        self.mode_of_payment_label = QLabel("Mode of Payment:")
        self.mode_of_payment_input = QLineEdit(self)
        layout.addRow(self.mode_of_payment_label, self.mode_of_payment_input)

        self.who_paid_label = QLabel("Who Paid:")
        self.who_paid_input = QLineEdit(self)
        layout.addRow(self.who_paid_label, self.who_paid_input)

        self.amount_received_label = QLabel("Amount Received:")
        self.amount_received_input = QLineEdit(self)
        layout.addRow(self.amount_received_label, self.amount_received_input)

        self.confirmed_by_label = QLabel("Confirmed By:")
        self.confirmed_by_input = QLineEdit(self)
        layout.addRow(self.confirmed_by_label, self.confirmed_by_input)

        self.complete_button = QPushButton("Complete Order")
        self.complete_button.clicked.connect(self.complete_order)
        layout.addRow(self.complete_button)

    def complete_order(self):
        mode_of_payment = self.mode_of_payment_input.text()
        who_paid = self.who_paid_input.text()
        amount_received = self.amount_received_input.text()
        confirmed_by = self.confirmed_by_input.text()

        if not mode_of_payment or not who_paid or not amount_received or not confirmed_by:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields")
            return

        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE orders_history
            SET order_completed_on = ?,
                mode_of_payment = ?,
                who_paid = ?,
                amount_received = ?,
                confirmed_by = ?
            WHERE category = ? AND product = ? AND date_of_order = ?
        """, (QDate.currentDate().toString(Qt.ISODate), mode_of_payment, who_paid, amount_received, confirmed_by, self.order[0], self.order[1], self.order[3]))
        conn.commit()
        conn.close()

        self.accept()



class EditOrderDialog(QDialog):
    def __init__(self, order_data, parent=None):
        super(EditOrderDialog, self).__init__(parent)
        self.setWindowTitle("Edit Order")
        self.resize(600, 250)

        self.order_data = order_data

        layout = QFormLayout(self)

        self.product_label = QLabel("Product:")
        self.product_input = QLineEdit(order_data[1])
        layout.addRow(self.product_label, self.product_input)

        self.quantity_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit(order_data[2])
        layout.addRow(self.quantity_label, self.quantity_input)

        self.date_label = QLabel("Date of Order:")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.fromString(order_data[3], Qt.ISODate))
        self.date_input.setCalendarPopup(True)
        layout.addRow(self.date_label, self.date_input)

        self.category_label = QLabel("Order Category:")
        self.category_input = QComboBox(self)
        self.load_categories()
        self.category_input.setCurrentText(order_data[0])
        layout.addRow(self.category_label, self.category_input)

        self.ordered_by_label = QLabel("Ordered by:")
        self.ordered_by_input = QLineEdit(order_data[4])
        layout.addRow(self.ordered_by_label, self.ordered_by_input)

        self.update_button = QPushButton("Update Order")
        self.update_button.clicked.connect(self.update_order)
        layout.addRow(self.update_button)

    def load_categories(self):
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category_name FROM order_categories")
        categories = cursor.fetchall()
        for category in categories:
            self.category_input.addItem(category[0])
        conn.close()

    def update_order(self):
        product = self.product_input.text()
        quantity = self.quantity_input.text()
        date_of_order = self.date_input.date().toString(Qt.ISODate)
        category = self.category_input.currentText()
        ordered_by = self.ordered_by_input.text()

        if not product or not quantity or not date_of_order or not category or not ordered_by:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields")
            return

        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE orders_history
            SET product = ?, quantity = ?, date_of_order = ?, category = ?, ordered_by = ?
            WHERE product = ? AND category = ? AND date_of_order = ?
        """, (product, quantity, date_of_order, category, ordered_by, self.order_data[1], self.order_data[0], self.order_data[3]))
        conn.commit()
        conn.close()

        self.accept()




class OrdersPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Add the table for active orders
        self.active_orders_label = QLabel("Active Orders:")
        left_layout.addWidget(self.active_orders_label)
        self.active_orders_table = QTableWidget()
        self.active_orders_table.setColumnCount(5)
        self.active_orders_table.setHorizontalHeaderLabels(["Order Category", "Product", "Quantity/Units", "Date of Order", "Ordered by"])
        left_layout.addWidget(self.active_orders_table)

        # Add the table for completed orders
        self.completed_orders_label = QLabel("Completed Orders:")
        right_layout.addWidget(self.completed_orders_label)
        self.completed_orders_table = QTableWidget()
        self.completed_orders_table.setColumnCount(10)
        self.completed_orders_table.setHorizontalHeaderLabels(["Order Category", "Product", "Quantity/Units", "Date of Order", "Ordered by", "Order Completed On", "Mode of Payment", "Who Paid", "Amount Received", "Confirmed By"])
        right_layout.addWidget(self.completed_orders_table)

        # Add buttons to the left layout
        buttons_layout = QHBoxLayout()
        self.add_order_button = QPushButton("Add Order")
        self.add_order_button.clicked.connect(self.show_add_order_dialog)
        buttons_layout.addWidget(self.add_order_button)

        self.edit_order_button = QPushButton("Edit Order")
        self.edit_order_button.clicked.connect(self.show_edit_order_dialog)
        buttons_layout.addWidget(self.edit_order_button)


        self.add_order_category_button = QPushButton("Add Order Category")
        self.add_order_category_button.clicked.connect(self.show_add_category_dialog)
        buttons_layout.addWidget(self.add_order_category_button)

        self.complete_order_button = QPushButton("Complete an Order")
        self.complete_order_button.clicked.connect(self.show_complete_order_dialog)
        buttons_layout.addWidget(self.complete_order_button)
        
        left_layout.addLayout(buttons_layout)

        # Spacer to prevent the layouts from touching the bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Add spacer to the        # Add spacer to the bottom of each layout
        left_layout.addItem(spacer)
        right_layout.addItem(spacer)

        # Set maximum height for the tables to cover halfway down the page
        self.active_orders_table.setMaximumHeight(300)  # Adjust this value as needed
        self.completed_orders_table.setMaximumHeight(300)  # Adjust this value as needed

        self.layout.addLayout(left_layout)
        self.layout.addLayout(right_layout)

        self.load_orders()

    def load_orders(self):
        self.active_orders_table.setRowCount(0)
        self.completed_orders_table.setRowCount(0)

        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("""
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

        cursor.execute("SELECT * FROM orders_history WHERE order_completed_on IS NULL ORDER BY date_of_order DESC")
        active_orders = cursor.fetchall()
        for order in active_orders:
            row_position = self.active_orders_table.rowCount()
            self.active_orders_table.insertRow(row_position)
            self.active_orders_table.setItem(row_position, 0, QTableWidgetItem(order[0]))  # Category
            self.active_orders_table.setItem(row_position, 1, QTableWidgetItem(order[1]))  # Product
            self.active_orders_table.setItem(row_position, 2, QTableWidgetItem(str(order[2])))  # Quantity
            self.active_orders_table.setItem(row_position, 3, QTableWidgetItem(order[3]))  # Date of Order
            self.active_orders_table.setItem(row_position, 4, QTableWidgetItem(order[4]))  # Ordered by

        cursor.execute("SELECT * FROM orders_history WHERE order_completed_on IS NOT NULL ORDER BY order_completed_on DESC")
        completed_orders = cursor.fetchall()
        for order in completed_orders:
            row_position = self.completed_orders_table.rowCount()
            self.completed_orders_table.insertRow(row_position)
            self.completed_orders_table.setItem(row_position, 0, QTableWidgetItem(order[0]))  # Category
            self.completed_orders_table.setItem(row_position, 1, QTableWidgetItem(order[1]))  # Product
            self.completed_orders_table.setItem(row_position, 2, QTableWidgetItem(str(order[2])))  # Quantity
            self.completed_orders_table.setItem(row_position, 3, QTableWidgetItem(order[3]))  # Date of Order
            self.completed_orders_table.setItem(row_position, 4, QTableWidgetItem(order[4]))  # Ordered by
            self.completed_orders_table.setItem(row_position, 5, QTableWidgetItem(order[5]))  # Order Completed On
            self.completed_orders_table.setItem(row_position, 6, QTableWidgetItem(order[6]))  # Mode of Payment
            self.completed_orders_table.setItem(row_position, 7, QTableWidgetItem(order[7]))  # Who Paid
            self.completed_orders_table.setItem(row_position, 8, QTableWidgetItem(str(order[8])))  # Amount Received
            self.completed_orders_table.setItem(row_position, 9, QTableWidgetItem(order[9]))  # Confirmed By

        conn.close()

    def show_add_order_dialog(self):
        dialog = AddOrderDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_orders()

    def show_edit_order_dialog(self):
        selected_row = self.active_orders_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select an order to edit.")
            return
        
        order_data = []
        for column in range(5):
            item = self.active_orders_table.item(selected_row, column)
            order_data.append(item.text() if item else "")
        
        dialog = EditOrderDialog(order_data, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_orders()


    def show_add_category_dialog(self):
        dialog = AddCategoryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Reload categories in the AddOrderDialog
            for index in range(self.add_order_category_button.count()):
                self.add_order_category_button.removeItem(index)
            self.load_orders()

    def show_complete_order_dialog(self):
        selected_row = self.active_orders_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select an order to complete")
            return

        order_category = self.active_orders_table.item(selected_row, 0).text()
        order_product = self.active_orders_table.item(selected_row, 1).text()
        order_quantity = self.active_orders_table.item(selected_row, 2).text()
        order_date = self.active_orders_table.item(selected_row, 3).text()
        order_ordered_by = self.active_orders_table.item(selected_row, 4).text()

        order = (order_category, order_product, order_quantity, order_date, order_ordered_by)

        dialog = CompleteOrderDialog(order, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_orders()

