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
        # self.cursor.execute('''ALTER TABLE products ADD COLUMN low_alert_level INTEGER DEFAULT 0;''')

       
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
        self.btn_all_products.clicked.connect(self.show_all_products)
        self.toolbar_layout.addWidget(self.btn_all_products)

        self.btn_add_product = QPushButton("Add New Product")
        self.btn_add_product.clicked.connect(self.add_new_product)
        self.toolbar_layout.addWidget(self.btn_add_product)


        self.edit_product_btn = QPushButton("Edit Product")
        self.edit_product_btn.clicked.connect(self.edit_product)
        self.toolbar_layout.addWidget(self.edit_product_btn)

        self.delete_product_btn = QPushButton("Delete Product")
        self.delete_product_btn.clicked.connect(self.delete_product)
        self.toolbar_layout.addWidget(self.delete_product_btn)

          # Add search input field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("search product")
        self.search_input.setFixedWidth(140)
        self.toolbar_layout.addWidget(self.search_input)

        self.btn_search = QPushButton("Search")
        self.btn_search.clicked.connect(self.search_products)
        self.toolbar_layout.addWidget(self.btn_search)


        # Product list
        self.product_list_layout = QVBoxLayout()
        self.content_layout.addLayout(self.product_list_layout)

        self.product_list_layout.addWidget(QLabel("All Products In PeterPOS Database"))

        # Initialize table to display products
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(6)
        self.product_table.setHorizontalHeaderLabels(["Product Name", "Product ID", "Product Category", "Stock Level", "Price per Product", "Low Alert Level"])
        self.product_list_layout.addWidget(self.product_table)

        # Buttons for product operations
        self.product_buttons_layout = QHBoxLayout()
        self.product_list_layout.addLayout(self.product_buttons_layout)

        self.add_stock_button = QPushButton("Add stock to Product")
        self.add_stock_button.clicked.connect(self.add_stock_to_product)
        self.product_buttons_layout.addWidget(self.add_stock_button)



        # Stock alerts
        self.stock_alerts_layout = QVBoxLayout()
        self.content_layout.addLayout(self.stock_alerts_layout)

        self.stock_alerts_layout.addWidget(QLabel("Stock Alerts/Notifications"))
        self.stock_alerts = QLabel("No alerts.")
        self.stock_alerts_layout.addWidget(self.stock_alerts)

        # Load products initially
        self.load_products()

   
        # self.show()

        

    def add_new_product(self):
        dialog = AddProductDialog(self)
        dialog.resize(400, 300)
        if dialog.exec_():  # User clicked OK
            self.load_products()
            QMessageBox.information(self, "Product Added", "Product successfully added.")
        dialog.deleteLater()

    def load_products(self):
        self.product_table.clearContents()
        self.cursor.execute("SELECT name, id, category_id, stock, price, low_alert_level FROM products")
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
                self.product_table.setItem(i, 5, QTableWidgetItem(str(product[5])))  # Product Price

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

    def add_stock_to_product(self):
        selected_rows = self.product_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Select Product", "Please select a product to add stock to.")
            return

        row = selected_rows[0].row()
        product_id = self.product_table.item(row, 1).text()

        dialog = AddStockDialog(self, product_id=product_id)
        if dialog.exec_():  # User clicked OK
            QMessageBox.information(self, "Stock Added", "Stock successfully added.")
            self.load_products()  # Refresh the products table
        dialog.deleteLater()

    def show_all_products(self):
        self.load_products()


    def search_products(self):
        search_text = self.search_input.text().strip().lower()

        if not search_text:
            QMessageBox.warning(self, "Empty Search Query", "Please enter a search query.")
            return

        self.product_table.clearContents()
        self.cursor.execute("SELECT name, id, category_id, stock, price, low_alert_level FROM products WHERE lower(name) LIKE ? OR id LIKE ?", ('%' + search_text + '%', '%' + search_text + '%'))
        products = self.cursor.fetchall()

        if not products:
            self.product_table.setRowCount(1)
            self.product_table.setItem(0, 0, QTableWidgetItem("No Items matching your search."))
            self.product_table.setSpan(0, 0, 1, 5)  # Span across all columns
        else:
            self.product_table.setRowCount(len(products))
            for i, product in enumerate(products):
                self.product_table.setItem(i, 0, QTableWidgetItem(product[0]))  # Product Name
                self.product_table.setItem(i, 1, QTableWidgetItem(product[1]))  # Product ID
                self.product_table.setItem(i, 2, QTableWidgetItem(str(product[2])))  # Category ID
                self.product_table.setItem(i, 3, QTableWidgetItem(str(product[3])))  # Stock Level
                self.product_table.setItem(i, 4, QTableWidgetItem(str(product[4])))  # Product Price
                self.product_table.setItem(i, 5, QTableWidgetItem(str(product[5])))  # Product Alert

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
        self.resize(400,300)
        layout = QVBoxLayout(self)

        self.product_name_input = QLineEdit()
        layout.addWidget(QLabel("Product Name:"))
        layout.addWidget(self.product_name_input)

        self.product_price_input = QLineEdit()
        layout.addWidget(QLabel("Product Price:Ksh"))
        layout.addWidget(self.product_price_input)

        # Fetch categories dynamically from the database
        self.product_category_input = QComboBox()
        self.populate_categories()
        layout.addWidget(QLabel("Product Category:"))
        layout.addWidget(self.product_category_input)

        self.stock_level_input = QLineEdit()
        self.stock_level_input.setValidator(QIntValidator(1, 999999))
        layout.addWidget(QLabel("Initial Stock Level:"))
        layout.addWidget(self.stock_level_input)

        self.low_alert_level_input = QLineEdit()
        self.low_alert_level_input.setValidator(QIntValidator(1, 999999))
        layout.addWidget(QLabel("Set Low Stock Alert Level"))
        layout.addWidget(self.low_alert_level_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept_and_validate)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if product_id:
            # Populate dialog fields with existing product data for editing
            parent.cursor.execute("SELECT name, price, category_id, stock, low_alert_level FROM products WHERE id=?", (product_id,))
            product_data = parent.cursor.fetchone()
            self.product_name_input.setText(product_data[0])
            self.product_price_input.setText(str(product_data[1]))
            self.product_category_input.setCurrentIndex(self.product_category_input.findText(str(product_data[2])))
            self.stock_level_input.setText(str(product_data[3]))
            self.low_alert_level_input.setText(str(product_data[4]))#populate that

    def accept_and_validate(self):
        product_name = self.product_name_input.text().strip()
        product_price = self.product_price_input.text().strip()
        product_category = self.product_category_input.currentText()
        stock_level = self.stock_level_input.text().strip()
        low_alert_level = self.low_alert_level_input.text().strip()

              # Check if category is empty
        if product_category == "" and product_name != "" and product_price != "" and low_alert_level != "":
            QMessageBox.warning(self, "Missing Category Field", "Please select a product category. If none, create a new one in inventory management.")
        elif product_name == "" or product_price == "" or low_alert_level == "":
            QMessageBox.warning(self, "Incomplete Information", "Please fill in all fields.")

        else:
            parent = self.parent()
            if self.product_id is None:
                # Generate a unique product ID (example using current timestamp)
                product_id = str(int(time.time()))  # Example of generating ID
                # Insert the new product into the database
                parent.cursor.execute("INSERT INTO products (id, name, price, category_id, stock, low_alert_level) VALUES (?, ?, ?, ?, ?, ?)",
                                      (product_id, product_name, product_price, product_category, stock_level, low_alert_level))
                parent.conn.commit()

                parent.log_stock_activity("Added", product_name, product_category, product_id)
            else:
                # Update existing product in the database
                parent.cursor.execute("UPDATE products SET name=?, price=?, category_id=?, stock=?, low_alert_level=? WHERE id=?",
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

        # Retrieve the prroduct name for the title
        if product_id:
            parent.cursor.execute("SELECT name, price, category_id, stock, low_alert_level FROM products WHERE id=?", (product_id,))
            product_data = parent.cursor.fetchone()
            product_name = product_data[0]
            self.setWindowTitle(f"Edit {product_name}'s Product Details")
        else:
            self.setWindowTitle("Edit Products's Details")
        self.resize(400,300)

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
        self.stock_level_input.setReadOnly(True)
        layout.addWidget(QLabel("Stock Level:(To add, go to add stock)"))
        layout.addWidget(self.stock_level_input)

        self.low_alert_level_input = QLineEdit()
        self.low_alert_level_input.setValidator(QIntValidator(1, 999999))
        layout.addWidget(QLabel("Low Alert Level:"))
        layout.addWidget(self.low_alert_level_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept_and_validate)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if product_id:
            parent.cursor.execute("SELECT name, price, category_id, stock, low_alert_level FROM products WHERE id=?", (product_id,))
            product_data = parent.cursor.fetchone()
            self.product_name_input.setText(product_data[0])
            self.product_price_input.setText(str(product_data[1]))
            self.product_category_input.setCurrentIndex(self.product_category_input.findText(str(product_data[2])))
            self.stock_level_input.setText(str(product_data[3]))
            self.low_alert_level_input.setText(str(product_data[4]))

    def accept_and_validate(self):
        product_name = self.product_name_input.text().strip()
        product_price = self.product_price_input.text().strip()
        product_category = self.product_category_input.currentText()
        stock_level = self.stock_level_input.text().strip()
        low_alert_level = self.low_alert_level_input.text().strip()

        if product_name == "" or product_price == "" or product_category == "":
            QMessageBox.warning(self, "Incomplete Information", "Please fill in all fields.")
        else:
            parent = self.parent()
            parent.cursor.execute("UPDATE products SET name=?, price=?, category_id=?, stock=?, low_alert_level=? WHERE id=?",
                                  (product_name, product_price, product_category, stock_level, low_alert_level, self.product_id))
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


class AddStockDialog(QDialog):
    def __init__(self, parent=None, product_id=None):
        super().__init__(parent)
        self.product_id = product_id  # Store product_id for updating stock
        self.setWindowTitle("Add Stock to Product")
        self.resize(300, 150)

        layout = QVBoxLayout(self)

        # Fetch product details from the database
        parent.cursor.execute("SELECT name, stock FROM products WHERE id=?", (self.product_id,))
        product_data = parent.cursor.fetchone()
        if not product_data:
            QMessageBox.warning(self, "Error", "Product not found.")
            self.reject()
            return

        product_name, current_stock = product_data

        self.current_stock_label = QLabel(f"Current Stock Level for '{product_name}': {current_stock}")
        layout.addWidget(self.current_stock_label)

        self.add_stock_input = QLineEdit()
        self.add_stock_input.setPlaceholderText("Enter number of units to add")
        self.add_stock_input.setValidator(QIntValidator(1, 10000, self))  # Integer input only
        layout.addWidget(QLabel("Units to Add:"))
        layout.addWidget(self.add_stock_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept_and_validate)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept_and_validate(self):
        units_to_add = self.add_stock_input.text().strip()

        if not units_to_add:
            QMessageBox.warning(self, "Incomplete Information", "Please enter the number of units to add.")
        else:
            units_to_add = int(units_to_add)
            parent = self.parent()
            parent.cursor.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (units_to_add, self.product_id))
            parent.conn.commit()

            product_name = parent.product_table.item(parent.product_table.currentRow(), 0).text()
            product_category = parent.product_table.item(parent.product_table.currentRow(), 2).text()

            parent.log_stock_activity("Added Stock", product_name, product_category, self.product_id)
            parent.load_products()

            QMessageBox.information(self, "Stock Added", f"Added {units_to_add} units to '{product_name}'.")
            self.accept()
