from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem


# A page where users can add, edit, or delete products. This page can include fields for product
#  ID, name, price, category, and stock quantity.


class ProductManagementPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.product_list = QTableWidget()
        self.product_list.setColumnCount(3)
        self.product_list.setHorizontalHeaderLabels(["Product ID", "Product Name", "Price"])
        self.layout.addWidget(self.product_list)

        self.add_product_section = QHBoxLayout()
        self.layout.addLayout(self.add_product_section)

        self.product_id_input = QLineEdit()
        self.product_id_input.setPlaceholderText("Product ID")
        self.add_product_section.addWidget(self.product_id_input)

        self.product_name_input = QLineEdit()
        self.product_name_input.setPlaceholderText("Product Name")
        self.add_product_section.addWidget(self.product_name_input)

        self.product_price_input = QLineEdit()
        self.product_price_input.setPlaceholderText("Product Price")
        self.add_product_section.addWidget(self.product_price_input)

        self.add_product_button = QPushButton("Add Product")
        self.add_product_button.clicked.connect(self.add_product)
        self.add_product_section.addWidget(self.add_product_button)

    def add_product(self):
        product_id = self.product_id_input.text()
        product_name = self.product_name_input.text()
        product_price = self.product_price_input.text()

        if product_id and product_name and product_price:
            row_position = self.product_list.rowCount()
            self.product_list.insertRow(row_position)
            self.product_list.setItem(row_position, 0, QTableWidgetItem(product_id))
            self.product_list.setItem(row_position, 1, QTableWidgetItem(product_name))
            self.product_list.setItem(row_position, 2, QTableWidgetItem(product_price))

            self.product_id_input.clear()
            self.product_name_input.clear()
            self.product_price_input.clear()
