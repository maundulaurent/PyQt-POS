from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QLabel, QPushButton


# This is the main page where sales transactions occur. It typically includes a product list,
#  the ability to add products to the cart, apply discounts, and complete transactions.

class CheckoutPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.product_list = QTableWidget()
        self.product_list.setColumnCount(3)
        self.product_list.setHorizontalHeaderLabels(["Product ID", "Product Name", "Price"])
        self.layout.addWidget(self.product_list)

        self.checkout_button = QPushButton("Checkout")
        self.layout.addWidget(self.checkout_button)

        self.total_label = QLabel("Total: $0.00")
        self.layout.addWidget(self.total_label)
