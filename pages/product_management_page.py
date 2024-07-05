from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import time
import datetime


class ProductManagementPage(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize database connection
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        # Initialize UI
        self.init_ui()
        self.init_db()

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
        
        # Create a new table for stock history without UNIQUE constraint on product_id
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stocks_history_new
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id TEXT, name TEXT, category TEXT, description TEXT, date TEXT)''')

        # Copy data from old table to new table
        self.cursor.execute('''INSERT INTO stocks_history_new (product_id, name, category, description, date)
                            SELECT product_id, name, category, description, date FROM stocks_history''')

        # Drop the old table
        self.cursor.execute('DROP TABLE IF EXISTS stocks_history')

        # Rename the new table to the old table's name
        self.cursor.execute('ALTER TABLE stocks_history_new RENAME TO stocks_history')

        self.conn.commit()
        self.load_products()

    def init_ui(self):
        # Main layout
        self.main_layout = QHBoxLayout(self)

        # Navigation menu
        self.nav_layout = QVBoxLayout()
        self.nav_menu = QWidget()
        self.nav_menu.setFixedWidth(200)
        self.nav_menu.setLayout(self.nav_layout)
        self.nav_menu.setStyleSheet("""
            background-color: #4e5052;
            border-radius: 5px;
        """)
        self.main_layout.addWidget(self.nav_menu, 1)

        # Navigation items
        nav_items = ["Dashboard", "Inventory", "Stocks", "New Sale"]
        nav_label = QLabel("Navigation Menu")
        nav_label.setStyleSheet("color: white; padding: 20px;")
        self.nav_layout.addWidget(nav_label)
        for item in nav_items:
            button = QPushButton(item)
            button.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: #34495E;
                    border: none;
                    text-align: left;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #1ABC9C;
                }
            """)
            self.nav_layout.addWidget(button)

        # Content layout
        self.content_layout = QVBoxLayout()
        self.main_layout.addLayout(self.content_layout)

        # Heading text
        self.heading_text = QHBoxLayout()
        self.heading_text.addWidget(QPushButton("Product Sales and Management"))
        self.content_layout.addLayout(self.heading_text)

        # Toolbar
        self.toolbar_layout = QHBoxLayout()
        self.content_layout.addLayout(self.toolbar_layout)

        # Toolbar buttons
        self.btn_all_products = QPushButton("All Products")
        # self.btn_all_products.clicked.connect(self.show_all_products)
        self.toolbar_layout.addWidget(self.btn_all_products)

        self.btn_add_product = QPushButton("Add New Product")
        self.btn_add_product.clicked.connect(self.add_new_product)
        self.toolbar_layout.addWidget(self.btn_add_product)

        self.btn_search = QPushButton("Search")
        self.toolbar_layout.addWidget(self.btn_search)

        self.btn_filter = QPushButton("Filter Products")
        self.toolbar_layout.addWidget(self.btn_filter)

        self.btn_export = QPushButton("Export")
        self.toolbar_layout.addWidget(self.btn_export)

        # Product list
        self.product_list_layout = QVBoxLayout()
        self.content_layout.addLayout(self.product_list_layout)

        self.product_list_layout.addWidget(QLabel("All Products"))

        # Initialize table to display products
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(5)
        self.product_table.setHorizontalHeaderLabels(["Product Name", "Product ID", "Product Category", "Stock Level", "Price per Product"])
        self.product_list_layout.addWidget(self.product_table)

        # Buttons for product operations
        self.product_buttons_layout = QHBoxLayout()
        self.product_list_layout.addLayout(self.product_buttons_layout)

        self.add_product_button = QPushButton("Add a New Product")
        self.add_product_button.clicked.connect(self.add_new_product)
        self.product_buttons_layout.addWidget(self.add_product_button)

        self.edit_product_btn = QPushButton("Edit Product")
        self.edit_product_btn.clicked.connect(self.edit_product)
        self.product_buttons_layout.addWidget(self.edit_product_btn)

        self.delete_product_btn = QPushButton("Delete Product")
        self.delete_product_btn.clicked.connect(self.delete_product)
        self.product_buttons_layout.addWidget(self.delete_product_btn)

        # Stock alerts
        self.stock_alerts_layout = QVBoxLayout()
        self.content_layout.addLayout(self.stock_alerts_layout)

        self.stock_alerts_layout.addWidget(QLabel("Stock Alerts/Notifications"))
        self.stock_alerts = QLabel("No alerts.")
        self.stock_alerts_layout.addWidget(self.stock_alerts)

        # Load products initially
        self.load_products()

        # Set up main window
        self.setWindowTitle("Inventory Management")
        # self.setGeometry(100, 100, 800, 600)
        self.show()

        self.btn_search.clicked.connect(self.search_products)

    def add_new_product(self):
        dialog = AddProductDialog(self)
        dialog.resize(400, 300)
        if dialog.exec_():  # User clicked OK
            self.load_products()
            QMessageBox.information(self, "Product Added", "Product successfully added.")
        dialog.deleteLater()

    def load_products(self):
        self.product_table.clearContents()
        self.cursor.execute("SELECT name, id, category_id, stock, price FROM products")
        products = self.cursor.fetchall()

        if not products:
            self.product_table.setRowCount(1)
            self.product_table.setItem(0, 0, QTableWidgetItem("No Items in your Repository, Please add items to display"))
            self.product_table.setSpan(0, 0, 1, 5)  # Span across all columns
        else:
            self.product_table.setRowCount(len(products))
            for i, product in enumerate(products):
                self.product_table.setItem(i, 0, QTableWidgetItem(product[0]))  # Product Name
                self.product_table.setItem(i, 1, QTableWidgetItem(product[1]))  # Product ID
                self.product_table.setItem(i, 2, QTableWidgetItem(str(product[2])))  # Category ID
                self.product_table.setItem(i, 3, QTableWidgetItem(str(product[3])))  # Stock Level
                self.product_table.setItem(i, 4, QTableWidgetItem(str(product[4])))  # Product Price

        self.product_table.resizeColumnsToContents()

    def edit_product(self):
        selected_rows = self.product_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Select Product", "Please select a product to edit.")
            return

        row = selected_rows[0].row()
        product_id = self.product_table.item(row, 1).text()
        
        dialog = EditProductDialog(self, product_id=product_id)
        if dialog.exec_():
            self.load_products()
            QMessageBox.information(self, "Product Updated", "Product successfully updated.")


    def delete_product(self):
        selected_rows = self.product_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Select Product", "Please select a product to delete.")
            return

        row = selected_rows[0].row()
        product_id = self.product_table.item(row, 1).text()
        product_name = self.product_table.item(row, 0).text()
        product_category = self.product_table.item(row, 2).text()

        reply = QMessageBox.question(self, "Delete Product",
                                     f"Are you sure you want to delete the product '{product_name}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.conn.commit()

            # Log the activity in stocks_history
            self.log_stock_activity("Deleted", product_name, product_category, product_id)

            self.load_products()
            QMessageBox.information(self, "Product Deleted", "Product successfully deleted.")

    def search_products(self):
        search_text = self.btn_search.text().strip().lower()

        if not search_text:
            QMessageBox.warning(self, "Empty Search Query", "Please enter a search query.")
            return

        self.product_table.clearContents()
        self.cursor.execute("SELECT name, id, category_id, stock, price FROM products WHERE lower(name) LIKE ? OR id LIKE ?", ('%' + search_text + '%', '%' + search_text + '%'))
        products = self.cursor.fetchall()

        if not products:
            self.product_table.setRowCount(1)
            self.product_table.setItem(0, 0, QTableWidgetItem("No Items matching your search."))
            self.product_table.setSpan(0, 0, 1, 4)  # Span across all columns
        else:
            self.product_table.setRowCount(len(products))
            for i, product in enumerate(products):
                self.product_table.setItem(i, 0, QTableWidgetItem(product[0]))  # Product Name
                self.product_table.setItem(i, 1, QTableWidgetItem(product[1]))  # Product ID
                self.product_table.setItem(i, 2, QTableWidgetItem(str(product[2])))  # Category ID
                self.product_table.setItem(i, 3, QTableWidgetItem(str(product[3])))  # Stock Level
                self.product_table.setItem(i, 4, QTableWidgetItem(str(product[4])))  # Product Price

        self.product_table.resizeColumnsToContents()

    def log_stock_activity(self, action, product_name, product_category, product_id):
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO stocks_history (product_id, name, category, description, date) VALUES (?, ?, ?, ?, ?)",
                            (product_id, product_name, product_category, action, current_datetime))
        self.conn.commit()




    




# Update AddProductDialog class
class AddProductDialog(QDialog):
    def __init__(self, parent=None, product_id=None):
        super().__init__(parent)
        self.product_id = product_id  # Store product_id for editing
        self.setWindowTitle("Add New Product" if product_id is None else "Edit Product")

        layout = QVBoxLayout(self)

        self.product_name_input = QLineEdit()
        layout.addWidget(QLabel("Product Name:"))
        layout.addWidget(self.product_name_input)

        self.product_price_input = QLineEdit()
        layout.addWidget(QLabel("Product Price:"))
        layout.addWidget(self.product_price_input)

        # Fetch categories dynamically from the database
        self.product_category_input = QComboBox()
        self.populate_categories()
        layout.addWidget(QLabel("Product Category:"))
        layout.addWidget(self.product_category_input)

        self.stock_level_input = QLineEdit()
        layout.addWidget(QLabel("Stock Level:"))
        layout.addWidget(self.stock_level_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept_and_validate)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if product_id:
            # Populate dialog fields with existing product data for editing
            parent.cursor.execute("SELECT name, price, category_id, stock FROM products WHERE id=?", (product_id,))
            product_data = parent.cursor.fetchone()
            self.product_name_input.setText(product_data[0])
            self.product_price_input.setText(str(product_data[1]))
            self.product_category_input.setCurrentIndex(self.product_category_input.findText(str(product_data[2])))
            self.stock_level_input.setText(str(product_data[3]))

    def accept_and_validate(self):
        product_name = self.product_name_input.text().strip()
        product_price = self.product_price_input.text().strip()
        product_category = self.product_category_input.currentText()
        stock_level = self.stock_level_input.text().strip()

        if product_name == "" or product_price == "" or product_category == "":
            QMessageBox.warning(self, "Incomplete Information", "Please fill in all fields.")
        else:
            parent = self.parent()
            if self.product_id is None:
                # Generate a unique product ID (example using current timestamp)
                product_id = str(int(time.time()))  # Example of generating ID
                # Insert the new product into the database
                parent.cursor.execute("INSERT INTO products (id, name, price, category_id, stock) VALUES (?, ?, ?, ?, ?)",
                                      (product_id, product_name, product_price, product_category, stock_level))
                parent.conn.commit()

                parent.log_stock_activity("Added", product_name, product_category, product_id)
            else:
                # Update existing product in the database
                parent.cursor.execute("UPDATE products SET name=?, price=?, category_id=?, stock=? WHERE id=?",
                                      (product_name, product_price, product_category, stock_level, self.product_id))
                parent.conn.commit()

                parent.log_stock_activity("Edited", product_name, product_category, self.product_id)

            # Update the product list in your application
            parent.load_products()

            QMessageBox.information(self, "Product Added" if self.product_id is None else "Product Updated",
                                    "Product successfully added." if self.product_id is None else "Product successfully updated.")
            self.accept()

    def populate_categories(self):
        # Fetch categories from the database and populate the dropdown
        parent = self.parent()
        parent.cursor.execute("SELECT id, name FROM categories")
        categories = parent.cursor.fetchall()
        for category_id, category_name in categories:
            self.product_category_input.addItem(f"{category_name} ({category_id})")


class EditProductDialog(QDialog):
    def __init__(self, parent=None, product_id=None):
        super().__init__(parent)
        self.product_id = product_id
        self.setWindowTitle("Edit Product")

        layout = QVBoxLayout(self)

        self.product_name_input = QLineEdit()
        layout.addWidget(QLabel("Product Name:"))
        layout.addWidget(self.product_name_input)

        self.product_price_input = QLineEdit()
        layout.addWidget(QLabel("Product Price:"))
        layout.addWidget(self.product_price_input)

        self.product_category_input = QComboBox()
        self.populate_categories()
        layout.addWidget(QLabel("Product Category:"))
        layout.addWidget(self.product_category_input)

        self.stock_level_input = QLineEdit()
        layout.addWidget(QLabel("Stock Level:"))
        layout.addWidget(self.stock_level_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept_and_validate)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if product_id:
            parent.cursor.execute("SELECT name, price, category_id, stock FROM products WHERE id=?", (product_id,))
            product_data = parent.cursor.fetchone()
            self.product_name_input.setText(product_data[0])
            self.product_price_input.setText(str(product_data[1]))
            self.product_category_input.setCurrentIndex(self.product_category_input.findText(str(product_data[2])))
            self.stock_level_input.setText(str(product_data[3]))

    def accept_and_validate(self):
        product_name = self.product_name_input.text().strip()
        product_price = self.product_price_input.text().strip()
        product_category = self.product_category_input.currentText()
        stock_level = self.stock_level_input.text().strip()

        if product_name == "" or product_price == "" or product_category == "":
            QMessageBox.warning(self, "Incomplete Information", "Please fill in all fields.")
        else:
            parent = self.parent()
            parent.cursor.execute("UPDATE products SET name=?, price=?, category_id=?, stock=? WHERE id=?",
                                  (product_name, product_price, product_category, stock_level, self.product_id))
            parent.conn.commit()

            parent.log_stock_activity("Edited", product_name, product_category, self.product_id)
            parent.load_products()

            QMessageBox.information(self, "Product Updated", "Product successfully updated.")
            self.accept()

    def populate_categories(self):
        parent = self.parent()
        parent.cursor.execute("SELECT id, name FROM categories")
        categories = parent.cursor.fetchall()
        for category_id, category_name in categories:
            self.product_category_input.addItem(f"{category_name} ({category_id})")
