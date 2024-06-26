from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QAction, QLabel, QLineEdit, QToolBar, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap

from pages.user_login import LoginPage
from pages.welcome_page import WelcomePage
from pages.dashboard_page import DashboardPage
from pages.product_management_page import ProductManagementPage
from pages.checkout_page import CheckoutPage
from pages.inventory_management_page import InventoryManagementPage
from pages.settings_page import SettingsPage
from pages.admin_page import AdminPage
from pages.history import HistoryManager, HistoryWidget
from pages.orders import OrdersPage


class POSSystem(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Peter POS")
        
        

        self.setGeometry(100, 50, 800, 600)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.user_login = LoginPage(
            self.switch_to_admin_page,
            self.switch_to_dashboard_page
        )
        self.welcome_page = WelcomePage(
            self.switch_to_dashboard_page,
            self.switch_to_admin_page
            )
        self.dashboard_page = DashboardPage(
            self.show_products,
            self.show_inventory,
            self.show_orders,
            self.show_history,
        )
        self.product_management_page = ProductManagementPage()
        self.checkout_page = CheckoutPage()
        self.inventory_management_page = InventoryManagementPage()
        self.settings_page = SettingsPage()
        self.admin_page = AdminPage()
        self.history_page = HistoryManager()
        self.history_widget = HistoryWidget()
        self.orders_page = OrdersPage()

        self.central_widget.addWidget(self.user_login)#Stack this number one
        self.central_widget.addWidget(self.welcome_page)
        self.central_widget.addWidget(self.dashboard_page)
        self.central_widget.addWidget(self.product_management_page)
        self.central_widget.addWidget(self.checkout_page)
        self.central_widget.addWidget(self.inventory_management_page)
        self.central_widget.addWidget(self.settings_page)
        self.central_widget.addWidget(self.orders_page)
        self.central_widget.addWidget(self.admin_page)
        self.central_widget.addWidget(self.history_page)

        self.menu_bar = None  # Initialize menu bar as None initially
        self.create_menu_bar()
        self.central_widget.setCurrentWidget(self.user_login)  # Initially show login page
        self.menuBar().setVisible(False)  # Ensure menu bar is hidden initially

    def switch_to_dashboard_page(self, logged_in=True):
        self.central_widget.setCurrentWidget(self.dashboard_page)
        if logged_in:
            # Show menu bar only after successful login
            self.menuBar().setVisible(True)

    def switch_to_admin_page(self, logged_in=True):
        self.central_widget.setCurrentWidget(self.admin_page)
        if logged_in:
            # Show menu bar only after successful login
            self.menuBar().setVisible(True)

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("background-color: #000; color: #fff; padding: 8px;")

        navigate_menu = menu_bar.addMenu("Navigate")

        dashboard_action = QAction("Dashboard", self)
        dashboard_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.dashboard_page))
        navigate_menu.addAction(dashboard_action)

        product_management_action = QAction("Product Management", self)
        product_management_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.product_management_page))
        navigate_menu.addAction(product_management_action)

        checkout_action = QAction("Checkout", self)
        checkout_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.checkout_page))
        navigate_menu.addAction(checkout_action)

        inventory_management_action = QAction("Inventory Management", self)
        inventory_management_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.inventory_management_page))
        navigate_menu.addAction(inventory_management_action)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.settings_page))
        navigate_menu.addAction(settings_action)

        reports_action = QAction("Reports", self)
        reports_action.triggered.connect(lambda: self.central_widget.setCurrentWidget(self.reports_page))
        navigate_menu.addAction(reports_action)

        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        account_menu = menu_bar.addMenu("Account")
        logout_action = QAction("Signout", self)
        logout_action.triggered.connect(self.handle_logout)
        account_menu.addAction(logout_action)

    def handle_logout(self):
        self.central_widget.setCurrentWidget(self.user_login)
        # Get the actual menu bar object using menuBar()
        menu_bar = self.menuBar()
        if menu_bar is not None:  # Check if menu bar is created
            menu_bar.setVisible(False)  # Hide the menu bar

 
    def show_about_dialog(self):
        about_dialog = QLabel("This is a POS system For Managing a business.")
        about_dialog.setWindowTitle("About")
        about_dialog.setGeometry(100, 100, 200, 100)
        about_dialog.show()



# Dashboard Links
    def show_products(self):
        self.central_widget.setCurrentWidget(self.product_management_page)

    def show_inventory(self):
        self.central_widget.setCurrentWidget(self.inventory_management_page)
    def show_orders(self):
        self.central_widget.setCurrentWidget(self.orders_page)
    def show_history(self):
        self.central_widget.setCurrentWidget(self.history_page)
