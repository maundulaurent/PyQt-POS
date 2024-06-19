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
                background-color: #4e5052;
                color: white;
                font-size: 14px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4CAF50;
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
        self.sidebar.setStyleSheet("background-color: #4e5052; border-radius: 6px;")
        self.sidebar.setFixedWidth(250)
        self.main_layout.addWidget(self.sidebar)

        # Adjust the margins and spacing here
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)  # Add some margin around the layout
        self.sidebar_layout.setSpacing(5)  # Adjust vertical spacing between buttons

        # Add sidebar buttons
        self.add_sidebar_button("Dashboard", "images/pyimg.png")
        self.add_sidebar_button("Products", "images/pyimg.png")
        self.add_sidebar_button("Category", "images/home.png")
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

        # before quick actions
        before_quick = QHBoxLayout()
        self.setLayout(before_quick)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)
        card.setStyleSheet("""
            #card {
                background-color: #2b2b2b;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                min-width: 200px;
                max-width: 300px;
                height: 150px;
            }
        """)

        # card title
        title_label = QLabel("Recently Sold")
        title_label.setStyleSheet("font-size:16px; color: #A8A8A8;")
        card_layout.addWidget(title_label)

        # sold items details

        recently_sold = QLabel("New Americano Perfume")
        recently_sold.setStyleSheet("font-size: 12px; color: #ffffff ")
        card_layout.addWidget(recently_sold)

        self.content_layout.addWidget(card, alignment=Qt.AlignTop)

        # Quick actions section
        self.quick_actions_layout = QGridLayout()
        self.content_layout.addLayout(self.quick_actions_layout)

        self.new_sale_button = QLabel("New Sale")
        self.new_sale_button.setAlignment(Qt.AlignCenter)
        self.new_sale_button.setStyleSheet("""
            background: #4e5052;
            border-radius: 6px;
            font-weight:bold;
            font-size: 20px;
        """)
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

    def add_sidebar_button(self, text, icon_path=None):
        button = QPushButton()
        button_layout = QHBoxLayout()
        button.setLayout(button_layout)

        if icon_path:
            icon_label = QLabel()
            pixmap = QPixmap(icon_path)
            pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            button_layout.addWidget(icon_label, alignment=Qt.AlignLeft)  # Align icon to the left

        text_label = QLabel(text)
        button_layout.addWidget(text_label, alignment=Qt.AlignLeft)  # Align text to the left

        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)  # Adjust spacing between icon and text

        button.setStyleSheet("""
            text-align: left;
            padding: 8px 12px;
            margin: 0; 
            border: none;  
            font-size: 16px;        
        """)

        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sidebar_layout.addWidget(button)
        self.sidebar_layout.setAlignment(Qt.AlignTop)  # Align buttons at the top of the layout
