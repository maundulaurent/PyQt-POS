import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class InventoryManagementPage(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize database connection
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()

        # Initialize UI
        self.init_ui()

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
        self.heading_text.addWidget(QPushButton("Inventory Management Page"))
        self.content_layout.addLayout(self.heading_text)

# Toolbar
        self.toolbar_layout = QHBoxLayout()
        self.content_layout.addLayout(self.toolbar_layout)

        # Toolbar buttons
        self.btn_all_products = QPushButton("All Products")
        # self.btn_all_products.clicked.connect(self.show_all_products)
        self.toolbar_layout.addWidget(self.btn_all_products)

        self.btn_categories = QPushButton("Categories")
        self.btn_categories.clicked.connect(self.show_categories)
        self.toolbar_layout.addWidget(self.btn_categories)

        self.btn_add_product = QPushButton("Add New Product")
        self.btn_add_product.clicked.connect(self.add_new_product)
        self.toolbar_layout.addWidget(self.btn_add_product)

        self.btn_search = QPushButton("Search")
        # self.btn_search.clicked.connect(self.search_products)
        self.toolbar_layout.addWidget(self.btn_search)

        self.btn_filter = QPushButton("Filter Products")
        # self.btn_filter.clicked.connect(self.filter_products)
        self.toolbar_layout.addWidget(self.btn_filter)

        self.btn_export = QPushButton("Export")
        # self.btn_export.clicked.connect(self.export_data)
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

        self.product_buttons_layout.addWidget(QPushButton("Edit Products"))
        self.product_buttons_layout.addWidget(QPushButton("Delete Product"))

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
        self.setGeometry(100, 100, 800, 600)
        self.show()

    def load_products(self):
        self.product_table.clearContents()
        self.cursor.execute("SELECT name, id, category_id, stock FROM products")
        products = self.cursor.fetchall()
        
        self.product_table.setRowCount(len(products))
        for i, product in enumerate(products):
            self.product_table.setItem(i, 0, QTableWidgetItem(product[0]))  # Product Name
            self.product_table.setItem(i, 1, QTableWidgetItem(product[1]))  # Product ID
            self.product_table.setItem(i, 2, QTableWidgetItem(str(product[2])))  # Category ID (you may want to fetch category name)
            self.product_table.setItem(i, 3, QTableWidgetItem(str(product[3])))  # Stock Level

        self.product_table.resizeColumnsToContents()

    def add_new_product(self):
        dialog = AddProductDialog(self)
        if dialog.exec_():  # User clicked OK
            product_name = dialog.product_name_input.text()
            product_id = dialog.product_id_input.text()
            product_category = dialog.product_category_input.currentText()
            stock_level = dialog.stock_level_input.text()

            # Check if the product already exists
            self.cursor.execute("SELECT id FROM products WHERE name=?", (product_name,))
            existing_product = self.cursor.fetchone()

            if existing_product:
                QMessageBox.warning(self, "Duplicate Product", "Product already exists.")
            else:
                # Insert the new product into the database
                self.cursor.execute("INSERT INTO products (id, name, category_id, stock) VALUES (?, ?, ?, ?)",
                                    (product_id, product_name, product_category, stock_level))
                self.conn.commit()

                # Update the product list in your application
                self.load_products()

                QMessageBox.information(self, "Product Added", "Product successfully added.")

        dialog.deleteLater()

    def load_categories(self):
        # Method to load categories from the database
        self.cursor.execute("SELECT id, name FROM categories")
        categories = self.cursor.fetchall()
        # return categories

         # Create a dialog to display categories
        dialog = ShowCategoriesDialog(categories, parent=self)
        dialog.exec_()
        
    def show_categories(self):
        # Fetch existing categories from the database
        self.cursor.execute("SELECT id, name FROM categories")
        categories = self.cursor.fetchall()

        # Create a dialog to display categories
        dialog = ShowCategoriesDialog(categories, parent=self)
        dialog.exec_()



class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Product")

        layout = QVBoxLayout(self)

        self.product_name_input = QLineEdit()
        layout.addWidget(QLabel("Product Name:"))
        layout.addWidget(self.product_name_input)

        self.product_id_input = QLineEdit()
        layout.addWidget(QLabel("Product ID:"))
        layout.addWidget(self.product_id_input)

        # Fetch categories dynamically from the database
        self.product_category_input = QComboBox()
        self.populate_categories()
        layout.addWidget(QLabel("Product Category:"))
        layout.addWidget(self.product_category_input)

        self.stock_level_input = QLineEdit()
        layout.addWidget(QLabel("Stock Level:"))
        layout.addWidget(self.stock_level_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def populate_categories(self):
        # Fetch categories from the database and populate the dropdown
        parent = self.parent()
        parent.cursor.execute("SELECT id, name FROM categories")
        categories = parent.cursor.fetchall()
        for category_id, category_name in categories:
            self.product_category_input.addItem(f"{category_name} ({category_id})")


class ShowCategoriesDialog(QDialog):
    def __init__(self, categories, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Categories")
        self.categories = categories

        layout = QVBoxLayout(self)

        # Display categories in a table
        self.category_table = QTableWidget()
        self.category_table.setColumnCount(2)
        self.category_table.setHorizontalHeaderLabels(["Category ID", "Category Name"])
        self.category_table.setRowCount(len(self.categories))

        for i, (category_id, category_name) in enumerate(self.categories):
            self.category_table.setItem(i, 0, QTableWidgetItem(str(category_id)))
            self.category_table.setItem(i, 1, QTableWidgetItem(category_name))

        layout.addWidget(self.category_table)

        # Buttons to manage categories
        button_layout = QHBoxLayout()

        add_button = QPushButton("Add Category")
        add_button.clicked.connect(self.add_category)
        button_layout.addWidget(add_button)

        edit_button = QPushButton("Edit Category")
        edit_button.clicked.connect(self.edit_category)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete Category")
        delete_button.clicked.connect(self.delete_category)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

    def add_category(self):
        # Dialog to add a new category
        dialog = AddEditCategoryDialog(self)
        if dialog.exec_():
            category_name = dialog.category_name_input.text()

            # Check if the category already exists
            existing_category = [category for category in self.categories if category[1] == category_name]
            if existing_category:
                QMessageBox.warning(self, "Duplicate Category", "Category already exists.")
            else:
                # Insert the new category into the database
                self.parent().cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
                self.parent().conn.commit()

                # Update the categories list and table
                self.parent().load_categories()

                QMessageBox.information(self, "Category Added", "Category successfully added.")

    def edit_category(self):
        # Get the selected category from the table
        selected_rows = self.category_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Select Category", "Please select a category to edit.")
            return

        row = selected_rows[0].row()
        category_id = self.category_table.item(row, 0).text()
        category_name = self.category_table.item(row, 1).text()

        # Dialog to edit the selected category
        dialog = AddEditCategoryDialog(self, category_name)
        if dialog.exec_():
            new_category_name = dialog.category_name_input.text()

            # Check if the new category name already exists (excluding the current category)
            existing_category = [category for category in self.categories if category[1] == new_category_name and category[0] != int(category_id)]
            if existing_category:
                QMessageBox.warning(self, "Duplicate Category", "Category already exists.")
            else:
                # Update the category in the database
                self.parent().cursor.execute("UPDATE categories SET name=? WHERE id=?", (new_category_name, category_id))
                self.parent().conn.commit()

                # Update the categories list and table
                self.parent().load_categories()

                QMessageBox.information(self, "Category Updated", "Category successfully updated.")

    def delete_category(self):
        # Get the selected category from the table
        selected_rows = self.category_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Select Category", "Please select a category to delete.")
            return

        row = selected_rows[0].row()
        category_id = self.category_table.item(row, 0).text()

        # Confirmation dialog for deleting the category
        confirm = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to delete this category?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            # Delete the category from the database
            self.parent().cursor.execute("DELETE FROM categories WHERE id=?", (category_id,))
            self.parent().conn.commit()

            # Update the categories list and table
            self.parent().load_categories()

            QMessageBox.information(self, "Category Deleted", "Category successfully deleted.")


class AddEditCategoryDialog(QDialog):
    def __init__(self, parent=None, initial_category_name=""):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Category")

        layout = QVBoxLayout(self)

        self.category_name_input = QLineEdit(initial_category_name)
        layout.addWidget(QLabel("Category Name:"))
        layout.addWidget(self.category_name_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

