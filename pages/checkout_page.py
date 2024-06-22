from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
from datetime import datetime
import os

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

        # Print Receipt Button
        self.print_receipt_button = QPushButton('Print Receipt')
        self.layout.addWidget(self.print_receipt_button)

        # Finish Sale Button
        self.finish_sale_button = QPushButton('Finish Sale')
        self.layout.addWidget(self.finish_sale_button)

        self.setLayout(self.layout)

        # Connect buttons to functions
        self.search_button.clicked.connect(self.search_item)
        self.clear_search_button.clicked.connect(self.load_all_items)
        self.scan_button.clicked.connect(self.scan_item)
        self.all_items_list.itemClicked.connect(self.select_item)
        self.cash_button.clicked.connect(self.process_payment)
        self.mpesa_button.clicked.connect(self.process_payment)
        self.print_receipt_button.clicked.connect(self.print_receipt)
        self.finish_sale_button.clicked.connect(self.finish_sale)

        # Load all items
        self.load_all_items()

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
        item_text = item.text().split(' - ')
        item_id = item_text[0]
        item_name = item_text[1]
        item_price = item_text[2].strip('$')
        self.add_item((item_id, item_name, item_price, 1))

    def add_item(self, item):
        row_position = self.item_table.rowCount()
        self.item_table.insertRow(row_position)
        for i, value in enumerate(item[:-1]):
            self.item_table.setItem(row_position, i, QTableWidgetItem(str(value)))
        # Add quantity spinner
        quantity_spinner = QSpinBox()
        quantity_spinner.setValue(item[-1])
        quantity_spinner.setMinimum(1)
        quantity_spinner.valueChanged.connect(self.update_total)
        self.item_table.setCellWidget(row_position, 3, quantity_spinner)
        # Add remove button
        remove_button = QPushButton('Remove')
        remove_button.clicked.connect(self.remove_item)
        self.item_table.setCellWidget(row_position, 4, remove_button)
        self.update_total()

    def remove_item(self):
        button = self.sender()
        index = self.item_table.indexAt(button.pos())
        self.item_table.removeRow(index.row())
        self.update_total()

    def update_total(self):
        total = 0.0
        for row in range(self.item_table.rowCount()):
            price = float(self.item_table.item(row, 2).text())
            quantity = self.item_table.cellWidget(row, 3).value()
            total += price * quantity
        self.total_label.setText(f'Total: ${total:.2f}')

    def apply_discount(self):
        discount_code = self.discount_input.text()
        # Implement discount logic based on the code
        # For now, we will just print the code
        print(f'Discount code applied: {discount_code}')
        # Update the total accordingly

    def process_payment(self):
        payment_method = self.sender().text()
        total = self.total_label.text().split('$')[1]
        receipt = f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        cashier_name = "Cashier Name"  # Replace with actual cashier name
        receipt += f"Cashier: {cashier_name}\n"
        receipt += f"Payment Method: {payment_method}\nTotal Amount: ${total}\n"
        items = []

        for row in range(self.item_table.rowCount()):
            item_id = self.item_table.item(row, 0).text()
            item_name = self.item_table.item(row, 1).text()
            item_price = self.item_table.item(row, 2).text()
            quantity = self.item_table.cellWidget(row, 3).value()
            receipt += f"{item_id} | {item_name} | ${item_price} | Qty: {quantity}\n"
            items.append({
                "item_id": item_id,
                "item_name": item_name,
                "item_price": item_price,
                "quantity": quantity
            })

        self.receipt_area.setText(receipt)
        self.store_sale(receipt, cashier_name, total, items, payment_method)

    def store_sale(self, receipt, cashier, total_amount, items, payment_method):
        items_str = "; ".join([f"{item['item_id']} ({item['quantity']})" for item in items])
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''INSERT INTO sales_history (date, cashier, total_amount, items, payment_method) 
                               VALUES (?, ?, ?, ?, ?)''', (date, cashier, total_amount, items_str, payment_method))
        self.conn.commit()

    def finish_sale(self):
        self.item_table.setRowCount(0)
        self.total_label.setText('Total: $0.00')
        self.discount_input.clear()
        self.receipt_area.clear()
        self.load_all_items()

    def print_receipt(self):
        receipt_text = self.receipt_area.toPlainText()
        if not os.path.exists('receipts'):
            os.makedirs('receipts')
        filename = datetime.now().strftime('receipts/%Y-%m-%d_%H-%M-%S.txt')
        with open(filename, 'w') as f:
            f.write(receipt_text)
        QMessageBox.information(self, "Receipt Printed", f"Receipt saved as {filename}")



