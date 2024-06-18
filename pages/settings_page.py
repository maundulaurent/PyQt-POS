from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.settings_label = QLabel("Settings")
        self.layout.addWidget(self.settings_label)
