from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class WelcomePage(QWidget):
    def __init__(self, switch_page):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.welcome_label = QLabel("~|~Init Technologies~|~")
        self.layout.addWidget(self.welcome_label)

        self.login_admin = QPushButton("Login as Admin")
        # Add the Login Button Functionality Here
        self.layout.addWidget(self.login_admin)

        self.login_user = QPushButton("Login as Guest")
        # Add fuunc here
        self.layout.addWidget(self.login_user)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(switch_page)
        self.layout.addWidget(self.start_button)
