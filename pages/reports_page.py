import sys

from PyQt5.QtWidgets import *

class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


        self.reports_label = QLabel("Current Reports")
        self.layout.addWidget(self.reports_label)

# A page to generate and view various reports such as sales reports, inventory reports, and financial summaries.