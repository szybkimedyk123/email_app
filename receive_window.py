from PySide2.QtWidgets import *
import send_window
import sys

class EmailReceive(QWidget):
    def __init__(self, user_email, user_password, user_imap_host, user_smtp_host ,user_imap_port, user_smtp_port):
        super().__init__()

        self.setWindowTitle("Email")
        self.resize(800, 400)
        self.receive_layout = QGridLayout()
        self.user_email = user_email
        self.user_password = user_password
        self.user_imap_host = user_imap_host
        self.user_smtp_host = user_smtp_host
        self.user_imap_port = user_imap_port
        self.user_smtp_port = user_smtp_port

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

    def back_to_send_window(self):
        self.close()
        self.new_send_window = send_window.EmailSend(self.user_email, self.user_password, self.user_imap_host,
                                                             self.user_smtp_host, self.user_imap_port, self.user_smtp_port)
        self.new_send_window.show()