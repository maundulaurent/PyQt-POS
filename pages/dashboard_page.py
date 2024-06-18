from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        self.setStyleSheet("""

            QWidget {
                background-color: #2b2b2b;
                color: #fff;
            }
            QLabel {
                font-size: 16px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTableWidget {
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 4px;
                border: 1px solid #ddd;
            }
            .sidebar {
                background-color: #333;
                color: white;
                padding: 15px;
            }
            .sidebar QPushButton {
                background-color: #555;
                color: white;
                margin-bottom: 10px;
            }
            .sidebar QPushButton:hover {
                background-color: #777;
            }
        """)

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)
        # self.sidebar.setStyleSheet("background-color: #2E2E2E;")
        self.sidebar.setStyleSheet("background-color: #4e5052; border-radius: 6px;")
        self.sidebar.setFixedWidth(250)
        self.main_layout.addWidget(self.sidebar)


        self.add_sidebar_button("Dashboard")
        self.add_sidebar_button("Products")
        self.add_sidebar_button("Category")
        self.add_sidebar_button("SubCategory")
        self.add_sidebar_button("Brands")
        self.add_sidebar_button("Order")
        self.add_sidebar_button("Transactions")
        self.add_sidebar_button("Invoices")
        self.add_sidebar_button("Sales")
        self.add_sidebar_button("Sales Summary")

        # Main content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)
        self.main_layout.addWidget(self.content_area)

        # Header Section
        header_layout = QHBoxLayout()
        self.content_layout.addLayout(header_layout)
        

        self.header = QLabel("Dashboard")
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        header_layout.addWidget(self.header)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setStyleSheet("""
            padding: 10px;
            width: 20px;
            border-radius: 5px;
            border: 1px solid #ddd;
            margin-left: 16px;
            margin-bottom: 20px;

        """)
        header_layout.addWidget(self.search_bar)


        

        # Quick actions section
        self.quick_actions_layout = QGridLayout()
        self.content_layout.addLayout(self.quick_actions_layout)

        self.new_sale_button = QPushButton("New Sale")
        self.add_product_button = QPushButton("Add Product")

        # Add widgets to the grid layout
        self.quick_actions_layout.addWidget(self.new_sale_button, 0, 0)  # Row 0, Column 0
        self.quick_actions_layout.addWidget(self.add_product_button, 0, 1, 1, 2)  # Row 0, Column 1, Span 1 row, 2 columns


        # Recent transactions section
        self.recent_transactions_label = QLabel("Recent Transactions")
        self.recent_transactions_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        self.content_layout.addWidget(self.recent_transactions_label)

        self.recent_transactions_table = QTableWidget()
        self.recent_transactions_table.setColumnCount(3)
        self.recent_transactions_table.setHorizontalHeaderLabels(["Transaction ID", "Date", "Amount"])
        self.recent_transactions_table.horizontalHeader().setStretchLastSection(True)
        self.recent_transactions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.content_layout.addWidget(self.recent_transactions_table)

        # Notifications section
        self.notifications_label = QLabel("Notifications")
        self.notifications_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        self.content_layout.addWidget(self.notifications_label)

        # self.notifications_card = self.create_card("Notifications", "No new notifications")
        # self.content_layout.addWidget(self.notifications_card)

        # Top selling products section
        self.top_selling_label = QLabel("Top Selling Products")
        self.top_selling_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 20px;")
        self.content_layout.addWidget(self.top_selling_label)

        self.top_selling_table = QTableWidget()
        self.top_selling_table.setColumnCount(2)
        self.top_selling_table.setHorizontalHeaderLabels(["Product", "Sales"])
        self.top_selling_table.horizontalHeader().setStretchLastSection(True)
        self.top_selling_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.content_layout.addWidget(self.top_selling_table)


    def add_sidebar_button(self, text):
        button = QPushButton(text)
        button.setStyleSheet("""
            text-align: left;
            padding: 8px 12px;
            margin: 0; 
            border: none;  
            font-size: 16px;        

        """)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sidebar_layout.addWidget(button)
        self.sidebar_layout.setSpacing(0)  # Adjust vertical spacing between buttons
        self.sidebar_layout.setAlignment(Qt.AlignTop)  # Align buttons at the top of the layout



