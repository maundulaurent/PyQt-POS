from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3

class ProductManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_db()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Category Management Bar
        self.category_bar = QWidget()
        self.category_layout = QHBoxLayout()
        self.category_bar.setLayout(self.category_layout)
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Add Category", "Delete Category", "Edit Category"])
        self.category_combo.currentTextChanged.connect(self.manage_category)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All"])
        self.filter_combo.currentTextChanged.connect(self.filter_products)

        self.category_layout.addWidget(QLabel("Category: "))
        self.category_layout.addWidget(self.category_combo)
        self.category_layout.addStretch()
        self.category_layout.addWidget(QLabel("Filter: "))
        self.category_layout.addWidget(self.filter_combo)
        self.main_layout.addWidget(self.category_bar)

        # Product Management Area
        self.product_management_area = QWidget()
        self.product_layout = QVBoxLayout()
        self.product_management_area.setLayout(self.product_layout)
        self.main_layout.addWidget(self.product_management_area)

        # Form for product details
        self.product_form = QFormLayout()

        self.product_name = QLineEdit()
        self.product_name.setPlaceholderText("Required")
        self.product_price = QLineEdit()
        self.product_price.setValidator(QIntValidator())
        self.product_price.setPlaceholderText("Required")
        self.product_category = QComboBox()
        self.product_stock = QLabel()

        self.product_form.addRow("Product Name:", self.product_name)
        self.product_form.addRow("Price:", self.product_price)
        self.product_form.addRow("Category:", self.product_category)
        self.product_form.addRow("Stock Quantity:", self.product_stock)

        self.product_layout.addLayout(self.product_form)

        # Buttons for add, edit, and delete
        self.buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Product")
        self.edit_button = QPushButton("Edit Product")
        self.delete_button = QPushButton("Delete Product")

        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.edit_button)
        self.buttons_layout.addWidget(self.delete_button)
        self.product_layout.addLayout(self.buttons_layout)

        # Product Table
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(5)
        self.product_table.setHorizontalHeaderLabels(["Product ID", "Name", "Price", "Category", "Stock"])
        self.product_layout.addWidget(self.product_table)

        # Connect buttons to functions
        self.add_button.clicked.connect(self.add_product)
        self.edit_button.clicked.connect(self.edit_product)
        self.delete_button.clicked.connect(self.delete_product)

        # Styles
        self.setStyleSheet("""
            QComboBox, QLineEdit, QLabel, QPushButton {
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 12px;
                border-radius: 6px;
                background-color: #4e5052;
                color: white;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
            }
            QLabel {
                margin-top: 10px;
            }
        """)

    def init_db(self):
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories
                               (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products
                               (id TEXT PRIMARY KEY, name TEXT, price INTEGER, category_id INTEGER, stock INTEGER,
                                FOREIGN KEY (category_id) REFERENCES categories (id))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales_history
                       (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, cashier TEXT, total_amount REAL, items TEXT, payment_method TEXT)''')
        self.conn.commit()
        self.load_categories()
        self.load_products()

    def load_categories(self):
        self.product_category.clear()
        self.filter_combo.clear()
        self.filter_combo.addItem("All")
        categories = self.cursor.execute("SELECT * FROM categories").fetchall()
        for category in categories:
            self.product_category.addItem(category[1], category[0])
            self.filter_combo.addItem(category[1])

    def load_products(self):
        self.product_table.setRowCount(0)
        for row, form in enumerate(self.cursor.execute("SELECT * FROM products")):
            self.product_table.insertRow(row)
            for col, item in enumerate(form):
                self.product_table.setItem(row, col, QTableWidgetItem(str(item)))

    def add_product(self):
        if not self.validate_form():
            return

        product_name = self.product_name.text()
        product_price = int(self.product_price.text())
        category_id = self.product_category.currentData()
        product_id = f"{category_id}_{self.cursor.execute('SELECT COUNT(*) FROM products').fetchone()[0] + 1}"
        product_stock = 0

        self.cursor.execute("INSERT INTO products (id, name, price, category_id, stock) VALUES (?, ?, ?, ?, ?)",
                            (product_id, product_name, product_price, category_id, product_stock))
        self.conn.commit()
        self.load_products()
        self.reset_form()

    def edit_product(self):
        current_row = self.product_table.currentRow()
        if current_row >= 0:
            product_id = self.product_table.item(current_row, 0).text()
            if not self.validate_form():
                return

            product_name = self.product_name.text()
            product_price = int(self.product_price.text())
            category_id = self.product_category.currentData()

            self.cursor.execute("UPDATE products SET name=?, price=?, category_id=? WHERE id=?",
                                (product_name, product_price, category_id, product_id))
            self.conn.commit()
            self.load_products()
            self.reset_form()

    def delete_product(self):
        current_row = self.product_table.currentRow()
        if current_row >= 0:
            product_id = self.product_table.item(current_row, 0).text()
            self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
            self.conn.commit()
            self.load_products()

    def filter_products(self):
        category = self.filter_combo.currentText()
        for row in range(self.product_table.rowCount()):
            item = self.product_table.item(row, 3)
            if category == "All" or item.text() == category:
                self.product_table.showRow(row)
            else:
                self.product_table.hideRow(row)

    def manage_category(self):
        category_action = self.category_combo.currentText()
        if category_action == "Add Category":
            self.add_category()
        elif category_action == "Delete Category":
            self.delete_category()
        elif category_action == "Edit Category":
            self.edit_category()

    def add_category(self):
        text, ok = QInputDialog.getText(self, 'Add Category', 'Enter category name:')
        if ok and text:
            self.cursor.execute("INSERT INTO categories (name) VALUES (?)", (text,))
            self.conn.commit()
            self.load_categories()

    def delete_category(self):
        categories = [self.product_category.itemText(i) for i in range(self.product_category.count())]
        text, ok = QInputDialog.getItem(self, 'Delete Category', 'Select category to delete:', categories, editable=False)
        if ok and text:
            self.cursor.execute("DELETE FROM categories WHERE name=?", (text,))
            self.conn.commit()
            self.load_categories()

    def edit_category(self):
        categories = [self.product_category.itemText(i) for i in range(self.product_category.count())]
        old_text, ok = QInputDialog.getItem(self, 'Edit Category', 'Select category to edit:', categories, editable=False)
        if ok and old_text:
            new_text, ok = QInputDialog.getText(self, 'Edit Category', 'Enter new category name:')
            if ok and new_text:
                self.cursor.execute("UPDATE categories SET name=? WHERE name=?", (new_text, old_text))
                self.conn.commit()
                self.load_categories()

    def validate_form(self):
        if not self.product_name.text() or not self.product_price.text():
            QMessageBox.warning(self, "Input Error", "Please fill all required fields.")
            return False
        return True

    def reset_form(self):
        self.product_name.clear()
        self.product_price.clear()


