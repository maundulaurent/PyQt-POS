from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
from datetime import datetime
import os
import json


class CheckoutPage(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the database connection
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        # Layout setup
        self.layout = QVBoxLayout()

        # Search Bar
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Enter item ID or name')
        self.search_button = QPushButton('Search')
        self.clear_search_button = QPushButton('Clear Search')
        self.scan_button = QPushButton('Scan Item')
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.clear_search_button)
        self.search_layout.addWidget(self.scan_button)
        self.layout.addLayout(self.search_layout)

        # All Items List
        self.all_items_list = QListWidget()
        self.layout.addWidget(self.all_items_list)

        # Item List
        self.item_table = QTableWidget(0, 5)
        self.item_table.setHorizontalHeaderLabels(['Item ID', 'Item Name', 'Price', 'Quantity', 'Remove'])
        self.layout.addWidget(self.item_table)

        # Total Amount
        self.total_label = QLabel('Total: $0.00')
        self.layout.addWidget(self.total_label)

        # Discount Input
        self.discount_input = QLineEdit()
        self.discount_input.setPlaceholderText('Enter discount code')
        self.layout.addWidget(self.discount_input)

        # Payment Methods
        self.payment_methods = QHBoxLayout()
        self.cash_button = QPushButton('Cash')
        self.mpesa_button = QPushButton('Mpesa')
        self.payment_methods.addWidget(self.cash_button)
        self.payment_methods.addWidget(self.mpesa_button)
        self.layout.addLayout(self.payment_methods)

        # Receipt Area
        self.receipt_area = QTextEdit()
        self.receipt_area.setReadOnly(True)
        self.layout.addWidget(self.receipt_area)

        # CashOut Sale Button
        self.cashout_sale_button = QPushButton('CashOut Sale')
        self.layout.addWidget(self.cashout_sale_button)

        self.setLayout(self.layout)

        # Connect buttons to functions
        self.search_button.clicked.connect(self.search_item)
        self.clear_search_button.clicked.connect(self.load_all_items)
        self.scan_button.clicked.connect(self.scan_item)
        self.all_items_list.itemClicked.connect(self.select_item)
        self.cash_button.clicked.connect(self.process_cash_payment)
        self.mpesa_button.clicked.connect(self.show_mpesa_dialog)
        self.cashout_sale_button.clicked.connect(self.finish_sale)

        # Load all items
        self.load_all_items()
        self.init_db()

    def init_db(self):
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

    def load_all_items(self):
        self.all_items_list.clear()
        self.cursor.execute("SELECT id, name, price FROM products")
        items = self.cursor.fetchall()
        for item in items:
            item_text = f"{item[0]} - {item[1]} - ${item[2]}"
            self.all_items_list.addItem(item_text)

    def fetch_items_by_id_or_name(self, search_text):
        query = "SELECT id, name, price FROM products WHERE id LIKE ? OR name LIKE ?"
        search_text = f"%{search_text}%"
        self.cursor.execute(query, (search_text, search_text))
        return self.cursor.fetchall()

    def search_item(self):
        self.all_items_list.clear()
        search_text = self.search_input.text()
        items = self.fetch_items_by_id_or_name(search_text)

        if items:
            for item in items:
                item_text = f"{item[0]} - {item[1]} - ${item[2]}"
                self.all_items_list.addItem(item_text)
        else:
            QMessageBox.warning(self, "Item not found", "The item could not be found in the database.")

    def scan_item(self):
        # Implement the logic for scanning an item
        # For now, we'll simulate with a static item ID
        scanned_item_id = 'item1'
        self.search_input.setText(scanned_item_id)
        self.search_item()

    def select_item(self, item):
        item_id = item.text().split(' - ')[0]
        self.cursor.execute("SELECT id, name, price FROM products WHERE id = ?", (item_id,))
        product = self.cursor.fetchone()
        if product:
            item_id, item_name, item_price = product
            item_found = False
            for row in range(self.item_table.rowCount()):
                if self.item_table.item(row, 0).text() == item_id:
                    quantity_widget = self.item_table.cellWidget(row, 3)
                    quantity_widget.setValue(quantity_widget.value() + 1)  # Increase the quantity
                    item_found = True
                    break

            if not item_found:
                row_position = self.item_table.rowCount()
                self.item_table.insertRow(row_position)
                self.item_table.setItem(row_position, 0, QTableWidgetItem(item_id))
                self.item_table.setItem(row_position, 1, QTableWidgetItem(item_name))
                self.item_table.setItem(row_position, 2, QTableWidgetItem(f"${item_price}"))
                quantity_input = QSpinBox()
                quantity_input.setMinimum(1)
                quantity_input.setValue(1)
                self.item_table.setCellWidget(row_position, 3, quantity_input)
                remove_button = QPushButton('Remove')
                remove_button.clicked.connect(lambda _, row=row_position: self.remove_item(row))
                self.item_table.setCellWidget(row_position, 4, remove_button)
            self.update_total_amount()

    def remove_item(self, row):
        self.item_table.removeRow(row)
        self.update_total_amount()

    def update_total_amount(self):
        total_amount = 0.0
        for row in range(self.item_table.rowCount()):
            item_price = float(self.item_table.item(row, 2).text().replace('$', ''))
            item_quantity = self.item_table.cellWidget(row, 3).value()
            total_amount += item_price * item_quantity
        self.total_label.setText(f'Total: ${total_amount:.2f}')

    def process_cash_payment(self):
        if self.item_table.rowCount() == 0:
            QMessageBox.warning(self, "No Items", "There are no items to check out.")
            return
        
        self.prepare_receipt('Cash')

    def show_mpesa_dialog(self):
        if self.item_table.rowCount() == 0:
            QMessageBox.warning(self, "No Items", "There are no items to check out.")
            return

        total_amount = self.total_label.text().replace('Total: $', '')
        total_amount = float(total_amount)

        # Assuming MpesaDialog is defined elsewhere
        self.mpesa_dialog = MpesaDialog(total_amount)
        self.mpesa_dialog.exec_()
        if self.mpesa_dialog.result() == QDialog.Accepted:
            self.prepare_receipt('Mpesa')

    def prepare_receipt(self, payment_method):
        total_amount = self.total_label.text().replace('Total: $', '')
        total_amount = float(total_amount)
        cashier = 'Cashier Name'  # Replace with actual cashier name if available
        self.items = []

        for row in range(self.item_table.rowCount()):
            item_id = self.item_table.item(row, 0).text()
            item_name = self.item_table.item(row, 1).text()
            item_price = self.item_table.item(row, 2).text().replace('$', '')
            quantity = self.item_table.cellWidget(row, 3).value()
            self.items.append((item_id, item_name, float(item_price), quantity))

        receipt_text = f"Receipt\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt_text += f"Cashier: {cashier}\n"
        receipt_text += f"Payment Method: {payment_method}\n"
        receipt_text += f"Total Amount: ${total_amount:.2f}\n\n"
        receipt_text += "Items:\n"
        for item_id, item_name, item_price, quantity in self.items:
            receipt_text += f"{item_id} - {item_name} - ${item_price:.2f} x {quantity}\n"

        self.receipt_area.setText(receipt_text)
        self.payment_method = payment_method
        self.total_amount = total_amount

    def finish_sale(self):
        if not hasattr(self, 'payment_method'):
            QMessageBox.warning(self, "Payment Method", "Please select a payment method.")
            return

        # Store the sale details
        self.store_sale(self.payment_method)

        # Clear the cart and reset the page
        self.item_table.setRowCount(0)
        self.update_total_amount()
        self.receipt_area.clear()
        self.search_input.clear()
        self.discount_input.clear()
        self.payment_method = None

    def store_sale(self, payment_method):
        cashier = 'Cashier Name'  # Replace with actual cashier name if available

        # Insert sale details into the `sales_history` table
        for item_id, item_name, item_price, quantity in self.items:
            self.cursor.execute("""
                INSERT INTO sales_history (date, cashier, total_amount, items, payment_method, item_id, item_name, price, quantity, date_of_sale)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                cashier,
                self.total_amount,
                json.dumps(self.items),
                payment_method,
                item_id,
                item_name,
                item_price,
                quantity,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))

        self.conn.commit()
        self.generate_receipt_file()

    def generate_receipt_file(self):
        receipt_text = self.receipt_area.toPlainText()
        receipt_folder = 'receipts'
        if not os.path.exists(receipt_folder):
            os.makedirs(receipt_folder)

        receipt_filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        receipt_filepath = os.path.join(receipt_folder, receipt_filename)
        with open(receipt_filepath, 'w') as file:
            file.write(receipt_text)


class MpesaDialog(QDialog):
    def __init__(self, total_amount, parent=None):
        super().__init__(parent)
        self.total_amount = total_amount
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('MPESA Payment')
        self.setModal(True)
        self.setFixedSize(300, 150)

        # Layout
        self.layout = QVBoxLayout()
        
        # Total Amount Label
        self.total_label = QLabel(f"Total Amount: ${self.total_amount:.2f}")
        self.layout.addWidget(self.total_label)

        # MPESA Phone Number
        self.phone_number_label = QLabel('MPESA Phone Number:')
        self.phone_number_input = QLineEdit()
        self.phone_number_input.setPlaceholderText('Enter MPESA phone number')
        self.layout.addWidget(self.phone_number_label)
        self.layout.addWidget(self.phone_number_input)

        # MPESA PIN
        self.pin_label = QLabel('MPESA PIN:')
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText('Enter MPESA PIN')
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.pin_label)
        self.layout.addWidget(self.pin_input)

        # Submit Button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.process_mpesa)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def process_mpesa(self):
        phone_number = self.phone_number_input.text()
        pin = self.pin_input.text()

        # Simple validation
        if not phone_number or not pin:
            QMessageBox.warning(self, "Input Error", "Please enter both phone number and MPESA PIN.")
            return

        # You can add more sophisticated MPESA validation or processing here

        # For now, just accept the dialog
        self.accept()