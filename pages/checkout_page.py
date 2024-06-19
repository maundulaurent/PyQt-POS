from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import cv2
from pyzbar import pyzbar

class CheckoutPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Product List
        self.product_list = QTableWidget()
        self.product_list.setColumnCount(4)
        self.product_list.setHorizontalHeaderLabels(["Product ID", "Product Name", "Price", ""])
        self.layout.addWidget(self.product_list)

        # Cart
        self.cart = QTableWidget()
        self.cart.setColumnCount(5)
        self.cart.setHorizontalHeaderLabels(["Product ID", "Product Name", "Price", "Quantity", "Total"])
        self.layout.addWidget(self.cart)

        # Discount
        self.discount_label = QLabel("Discount (%):")
        self.discount_input = QLineEdit()
        self.discount_input.setValidator(QIntValidator(0, 100))
        self.layout.addWidget(self.discount_label)
        self.layout.addWidget(self.discount_input)

        # Checkout Button
        self.checkout_button = QPushButton("Checkout")
        self.checkout_button.clicked.connect(self.checkout)
        self.layout.addWidget(self.checkout_button)

        # Total
        self.total_label = QLabel("Total: $0.00")
        self.layout.addWidget(self.total_label)

        # Print Receipt Button
        self.print_receipt_button = QPushButton("Print Receipt")
        self.print_receipt_button.clicked.connect(self.print_receipt)
        self.layout.addWidget(self.print_receipt_button)

        # Scan Barcode Button
        self.scan_barcode_button = QPushButton("Scan Barcode")
        self.scan_barcode_button.clicked.connect(self.scan_barcode)
        self.layout.addWidget(self.scan_barcode_button)

        # Database Connection
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        # Load Products
        self.load_products()

        # Styles
        self.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
            }
            QPushButton {
                padding: 8px 12px;
                border-radius: 6px;
                background-color: #4e5052;
                color: white;
            }
            QLabel {
                font-size: 14px;
                margin-top: 10px;
            }
            QLineEdit {
                padding: 4px;
                border-radius: 6px;
                border: 1px solid #ccc;
                font-size: 14px;
            }
        """)

    def load_products(self):
        products = self.cursor.execute("SELECT id, name, price FROM products").fetchall()
        self.product_list.setRowCount(0)
        for row, product in enumerate(products):
            self.product_list.insertRow(row)
            for col, item in enumerate(product):
                self.product_list.setItem(row, col, QTableWidgetItem(str(item)))
            add_button = QPushButton("Add to Cart")
            add_button.clicked.connect(lambda ch, row=row: self.add_to_cart(row))
            self.product_list.setCellWidget(row, 3, add_button)

    def add_to_cart(self, row):
        product_id = self.product_list.item(row, 0).text()
        product_name = self.product_list.item(row, 1).text()
        product_price = float(self.product_list.item(row, 2).text())
        existing_row = self.find_in_cart(product_id)
        if existing_row is None:
            self.cart.insertRow(self.cart.rowCount())
            self.cart.setItem(self.cart.rowCount() - 1, 0, QTableWidgetItem(product_id))
            self.cart.setItem(self.cart.rowCount() - 1, 1, QTableWidgetItem(product_name))
            self.cart.setItem(self.cart.rowCount() - 1, 2, QTableWidgetItem(str(product_price)))
            self.cart.setItem(self.cart.rowCount() - 1, 3, QTableWidgetItem("1"))
            self.cart.setItem(self.cart.rowCount() - 1, 4, QTableWidgetItem(str(product_price)))
        else:
            current_quantity = int(self.cart.item(existing_row, 3).text())
            new_quantity = current_quantity + 1
            self.cart.setItem(existing_row, 3, QTableWidgetItem(str(new_quantity)))
            self.cart.setItem(existing_row, 4, QTableWidgetItem(str(product_price * new_quantity)))
        self.update_total()

    def find_in_cart(self, product_id):
        for row in range(self.cart.rowCount()):
            if self.cart.item(row, 0).text() == product_id:
                return row
        return None

    def update_total(self):
        total = 0.0
        for row in range(self.cart.rowCount()):
            total += float(self.cart.item(row, 4).text())
        discount = self.discount_input.text()
        if discount:
            total -= total * (int(discount) / 100)
        self.total_label.setText(f"Total: ${total:.2f}")

    def checkout(self):
        QMessageBox.information(self, "Checkout", "Transaction completed successfully!")
        self.cart.setRowCount(0)
        self.update_total()

    def print_receipt(self):
        receipt = "Receipt\n\n"
        receipt += "Product ID\tProduct Name\tPrice\tQuantity\tTotal\n"
        for row in range(self.cart.rowCount()):
            receipt += f"{self.cart.item(row, 0).text()}\t"
            receipt += f"{self.cart.item(row, 1).text()}\t"
            receipt += f"{self.cart.item(row, 2).text()}\t"
            receipt += f"{self.cart.item(row, 3).text()}\t"
            receipt += f"{self.cart.item(row, 4).text()}\n"
        receipt += f"\nTotal: {self.total_label.text()}"

        with open("receipt.txt", "w") as file:
            file.write(receipt)

        QMessageBox.information(self, "Receipt", "Receipt has been printed to 'receipt.txt'")

    def scan_barcode(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                self.process_barcode(barcode_data)
                cap.release()
                cv2.destroyAllWindows()
                return

            cv2.imshow('Barcode Scanner', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def process_barcode(self, barcode_data):
        product = self.cursor.execute("SELECT id, name, price FROM products WHERE id=?", (barcode_data,)).fetchone()
        if product:
            product_id, product_name, product_price = product
            row_position = self.product_list.rowCount()
            self.product_list.insertRow(row_position)
            self.product_list.setItem(row_position, 0, QTableWidgetItem(product_id))
            self.product_list.setItem(row_position, 1, QTableWidgetItem(product_name))
            self.product_list.setItem(row_position, 2, QTableWidgetItem(str(product_price)))
            add_button = QPushButton("Add to Cart")
            add_button.clicked.connect(lambda ch, row=row_position: self.add_to_cart(row))
            self.product_list.setCellWidget(row_position, 3, add_button)
        else:
            QMessageBox.warning(self, "Error", "Product not found")

