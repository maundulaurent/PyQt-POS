from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
from datetime import datetime
import os
import json
import requests



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
        # self.mpesa_button.clicked.connect(self.process_payment)
        self.mpesa_button.clicked.connect(self.show_mpesa_dialog)
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

    def show_mpesa_dialog(self):
        total = self.total_label.text().split('$')[1]
        self.mpesa_dialog = MpesaDialog(total)
        self.mpesa_dialog.exec_()


class MpesaDialog(QDialog):
    def __init__(self, total_amount):
        super().__init__()
        self.setWindowTitle('Mpesa Payment')
        self.layout = QVBoxLayout()

        self.total_amount = total_amount

        self.phone_label = QLabel('Enter Customer Phone Number:')
        self.layout.addWidget(self.phone_label)

        self.phone_input = QLineEdit()
        self.layout.addWidget(self.phone_input)

        self.amount_label = QLabel(f'Amount to be paid: ${self.total_amount}')
        self.layout.addWidget(self.amount_label)

        self.pay_button = QPushButton('Pay')
        self.layout.addWidget(self.pay_button)

        self.setLayout(self.layout)
        self.pay_button.clicked.connect(self.process_payment)

    def process_payment(self):
        phone_number = self.phone_input.text()
        if not phone_number:
            QMessageBox.warning(self, "Input Error", "Please enter the customer phone number.")
            return
                # Format the phone number
        phone_number = self.format_phone_number(phone_number)
        if not phone_number:
            QMessageBox.warning(self, "Input Error", "Please enter a valid phone number in the format 07XXXXXXXX.")
            return

        # Call the MPESA STK Push function
        self.mpesa_stk_push(phone_number, self.total_amount)
    def format_phone_number(self, phone_number):
        # Remove any leading + or non-numeric characters
        phone_number = ''.join(filter(str.isdigit, phone_number))
        
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif not phone_number.startswith('254'):
            return None  # Invalid phone number format
        
        return phone_number
    
    def mpesa_stk_push(self, phone_number, amount):
        # Implement the STK push logic here
        consumer_key = ''
        consumer_secret = ''
        short_code = ''
        lipa_na_mpesa_online_passkey = '#'
        business_short_code = '174379'
        callback_url = ''

        
        try:
            # Get the access token
            access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
            response = requests.get(access_token_url, auth=(consumer_key, consumer_secret))
            access_token = json.loads(response.text)['access_token']

            # Ensure amount is a valid number
            try:
                amount = float(amount)
                amount = int(amount)  # Ensure amount is an integer
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Invalid amount format.")
                return

            # Make the STK push request
            api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = f"{short_code}{lipa_na_mpesa_online_passkey}{timestamp}"

            payload = {
                'BusinessShortCode': short_code,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': amount,
                'PartyA': phone_number,
                'PartyB': business_short_code,
                'PhoneNumber': phone_number,
                'CallBackURL': callback_url,
                'AccountReference': 'POS System',
                'TransactionDesc': 'Payment for items'
            }

            response = requests.post(api_url, headers=headers, json=payload)
            response_data = response.json()
            if 'ResponseCode' in response_data:
                if response_data['ResponseCode'] == '0':
                    QMessageBox.information(self, "Payment", f"STK Push to {phone_number} for ${amount} initiated.")
                else:
                    QMessageBox.warning(self, "Payment Error", f"Failed to initiate STK Push: {response_data['errorMessage']}")
            else:
                QMessageBox.warning(self, "Payment Error", f"Unexpected response: {response_data}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

        self.accept()