from PySide2.QtWidgets import *
import sys

class EmailReceive(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Email")
        self.resize(800, 400)
        self.receive_layout = QGridLayout()

        self.list_emails = QListWidget()
        self.text_emails = QTextEdit()
        self.text_emails.setReadOnly(True)
        self.text_display = QTextEdit()
        self.button_refresh = QPushButton('Refresh')

        self.receive_layout.addWidget(self.list_emails, 0, 0)
        self.receive_layout.addWidget(self.text_emails, 1, 0)
        self.receive_layout.addWidget(self.text_display, 2, 0)
        self.receive_layout.addWidget(self.button_refresh, 3, 0)

        self.setLayout(self.receive_layout)

    def refresh_action(self):
        None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailReceive()
    window.show()
    sys.exit(app.exec_())