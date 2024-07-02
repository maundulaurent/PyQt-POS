import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class AddOrderDialog(QDialog):
    def __init__(self, parent=None):
        super(AddOrderDialog, self).__init__(parent)
        self.setWindowTitle("Add Order")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        self.order_type_label = QLabel("Order Type:")
        layout.addWidget(self.order_type_label)
        self.order_type_input = QLineEdit(self)
        layout.addWidget(self.order_type_input)

        self.product_label = QLabel("Product:")
        layout.addWidget(self.product_label)
        self.product_input = QLineEdit(self)
        layout.addWidget(self.product_input)

        self.quantity_label = QLabel("Quantity:")
        layout.addWidget(self.quantity_label)
        self.quantity_input = QLineEdit(self)
        layout.addWidget(self.quantity_input)

        self.date_label = QLabel("Date of Order:")
        layout.addWidget(self.date_label)
        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        layout.addWidget(self.date_input)

        self.payment_label = QLabel("Method of Payment:")
        layout.addWidget(self.payment_label)
        self.payment_input = QLineEdit(self)
        layout.addWidget(self.payment_input)

        self.add_button = QPushButton("Add Order")
        self.add_button.clicked.connect(self.add_order)
        layout.addWidget(self.add_button)

    def add_order(self):
        order_type = self.order_type_input.text()
        product = self.product_input.text()
        quantity = self.quantity_input.text()
        date_of_order = self.date_input.date().toString(Qt.ISODate)
        method_of_payment = self.payment_input.text()

        if not order_type or not product or not quantity or not date_of_order:
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields")
            return

        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("""
            
            CREATE TABLE IF NOT EXISTS orders_history (
                id INTEGER PRIMARY KEY,
                order_type TEXT,
                product TEXT,
                quantity INTEGER,
                date_of_order TEXT,
                method_of_payment TEXT,
                status TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO orders_history (order_type, product, quantity, date_of_order, method_of_payment, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order_type, product, quantity, date_of_order, method_of_payment, "Active"))
        conn.commit()
        conn.close()

        self.accept()


class OrdersPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.reports_label = QLabel("Current Orders")
        self.layout.addWidget(self.reports_label)

        self.active_orders_label = QLabel("Active Orders:")
        self.layout.addWidget(self.active_orders_label)
        self.active_orders_list = QListWidget()
        self.layout.addWidget(self.active_orders_list)

        self.completed_orders_label = QLabel("Completed Orders:")
        self.layout.addWidget(self.completed_orders_label)
        self.completed_orders_list = QListWidget()
        self.layout.addWidget(self.completed_orders_list)

        self.add_order_button = QPushButton("Add Order")
        self.add_order_button.clicked.connect(self.show_add_order_dialog)
        self.layout.addWidget(self.add_order_button)

        self.load_orders()

    def load_orders(self):
        self.active_orders_list.clear()
        self.completed_orders_list.clear()

        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders_history (
                id INTEGER PRIMARY KEY,
                order_type TEXT,
                product TEXT,
                quantity INTEGER,
                date_of_order TEXT,
                method_of_payment TEXT,
                status TEXT
            )
        """)
        cursor.execute("SELECT * FROM orders_history WHERE status = 'Active'")
        active_orders = cursor.fetchall()
        for order in active_orders:
            item = QListWidgetItem(f"{order[1]}: {order[2]} - {order[3]} units on {order[4]}")
            self.active_orders_list.addItem(item)

        cursor.execute("SELECT * FROM orders_history WHERE status = 'Completed'")
        completed_orders = cursor.fetchall()
        for order in completed_orders:
            item = QListWidgetItem(f"{order[1]}: {order[2]} - {order[3]} units on {order[4]}")
            self.completed_orders_list.addItem(item)

        conn.close()

    def show_add_order_dialog(self):
        dialog = AddOrderDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_orders()


