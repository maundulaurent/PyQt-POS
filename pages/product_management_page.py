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
        self.product_table.setColumnCount(4)
        self.product_table.setHorizontalHeaderLabels(["Product Name", "Product ID", "Product Category", "Stock Level"])
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

    def load_products(self):
        self.product_table.clearContents()
        self.cursor.execute("SELECT name, id, category_id, stock FROM products")
        products = self.cursor.fetchall()

        if not products:
            self.product_table.setRowCount(1)
            self.product_table.setItem(0, 0, QTableWidgetItem("No Items in your Repository, Please add to display"))
            self.product_table.setSpan(0, 0, 1, 4)  # Span across all columns
        else:
            self.product_table.setRowCount(len(products))
            for i, product in enumerate(products):
                self.product_table.setItem(i, 0, QTableWidgetItem(product[0]))  # Product Name
                self.product_table.setItem(i, 1, QTableWidgetItem(product[1]))  # Product ID
                self.product_table.setItem(i, 2, QTableWidgetItem(str(product[2])))  # Category ID
                self.product_table.setItem(i, 3, QTableWidgetItem(str(product[3])))  # Stock Level

        self.product_table.resizeColumnsToContents()
    def add_new_product(self):
        dialog = AddProductDialog(self)
        dialog.resize(400, 300)
        if dialog.exec_():  # User clicked OK
            product_name = dialog.product_name_input.text()
            product_category = dialog.product_category_input.currentText()
            stock_level = dialog.stock_level_input.text()

            try:
                # Generate a unique product ID (example using current timestamp)
                product_id = str(int(time.time()))  # Example of generating ID

                # Insert the new product into the database
                self.cursor.execute("INSERT INTO products (id, name, category_id, stock) VALUES (?, ?, ?, ?)",
                                    (product_id, product_name, product_category, stock_level))
                self.conn.commit()

                current_datetime = datetime.datetime.now()
                formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

                # Log the activity
                self.log_stock_activity("Added", product_name, product_category, product_id)

                # Update the product list in your application
                self.load_products()

                QMessageBox.information(self, "Product Added", "Product successfully added.")

            except sqlite3.IntegrityError as e:
                QMessageBox.warning(self, "Database Error", "Failed to add product. Please check if the product already exists.")

        dialog.deleteLater()


    def edit_product(self):
        selected_rows = self.product_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Select Product", "Please select a product to edit.")
            return

        row = selected_rows[0].row()
        product_id = self.product_table.item(row, 1).text()
        product_name = self.product_table.item(row, 0).text()
        product_category = self.product_table.item(row, 2).text()

        dialog = AddProductDialog(self, product_id=product_id)  # Pass product_id for editing
        dialog.setWindowTitle("Edit Product")

        if dialog.exec_():
            # Fetch the product name and category for logging
            new_product_name = dialog.product_name_input.text()
            new_product_category = dialog.product_category_input.currentText()

            # Log the activity in stocks_history
            self.log_stock_activity("Edited", new_product_name, new_product_category, product_id)

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

        confirm = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete the item:\n\n{product_name} (ID: {product_id})",
                                    QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
            self.conn.commit()

            # Log the activity in stocks_history
            self.log_stock_activity("Deleted", product_name, product_category,product_id)

            self.load_products()
            QMessageBox.information(self, "Product Deleted", "Product successfully deleted.")
    

    # Add search functionality in ProductManagementPage class
    def search_products(self):
        search_text, ok = QInputDialog.getText(self, "Search Products", "Enter product name:")
        if ok and search_text:
            self.cursor.execute("SELECT name, id, category_id, stock FROM products WHERE name LIKE ?", ('%' + search_text + '%',))
            products = self.cursor.fetchall()
            self.product_table.setRowCount(len(products))
            for i, product in enumerate(products):
                self.product_table.setItem(i, 0, QTableWidgetItem(product[0]))  # Product Name
                self.product_table.setItem(i, 1, QTableWidgetItem(product[1]))  # Product ID
                self.product_table.setItem(i, 2, QTableWidgetItem(str(product[2])))  # Category ID
                self.product_table.setItem(i, 3, QTableWidgetItem(str(product[3])))  # Stock Level
        elif ok and not search_text:
            QMessageBox.warning(self, "Empty Search", "Please enter a product name to search.")

    # Connect search button to search_products method in init_ui method

    def log_stock_activity(self, action, product_name, product_category, product_id):
        date = time.strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
        description = f"{action} product {product_name} (ID: {product_id})"
        
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

        self.cursor.execute("INSERT INTO stocks_history (product_id, name, category, description, date) VALUES (?, ?, ?, ?, ?)",
                            (product_id, product_name, product_category, description, date))
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
            else:
                # Update existing product in the database
                parent.cursor.execute("UPDATE products SET name=?, price=?, category_id=?, stock=? WHERE id=?",
                                      (product_name, product_price, product_category, stock_level, self.product_id))
                parent.conn.commit()

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

