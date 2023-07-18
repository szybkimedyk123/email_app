from PySide2.QtWidgets import *
import send_window
import imaplib
import time
import email
import os
import sys

class EmailReceive(QWidget):
    def __init__(self, user_email, user_password, user_imap_host, user_smtp_host, user_imap_port, user_smtp_port):
        super().__init__()

        self.setWindowTitle("Email")
        self.resize(800, 600)
        self.receive_layout = QGridLayout()
        self.user_email = user_email
        self.user_password = user_password
        self.user_imap_host = user_imap_host
        self.user_smtp_host = user_smtp_host
        self.user_imap_port = user_imap_port
        self.user_smtp_port = user_smtp_port

        self.list_emails = QListWidget()
        self.list_emails.itemClicked.connect(self.show_mail)
        self.text_emails = QTextEdit()
        self.text_emails.setReadOnly(True)
        self.from_emails = QLineEdit()
        self.from_emails.setReadOnly(True)
        self.subject_emails = QLineEdit()
        self.subject_emails.setReadOnly(True)
        self.text_display = QTextEdit()
        self.button_refresh = QPushButton("Refresh")
        self.button_refresh.clicked.connect(self.refresh_action)
        self.button_send_window = QPushButton("Back to send")
        self.button_send_window.clicked.connect(self.back_to_send_window)
        self.button_download_attachment = QPushButton("Download attachment")
        self.button_download_attachment.clicked.connect(self.download_attachment)

        self.receive_layout.addWidget(self.list_emails, 0, 0)
        self.receive_layout.addWidget(self.from_emails, 1, 0)
        self.receive_layout.addWidget(self.subject_emails, 2, 0)
        self.receive_layout.addWidget(self.text_emails, 3, 0)
        #self.receive_layout.addWidget(self.text_display, 2, 0)
        self.receive_layout.addWidget(self.button_refresh, 4, 0)
        self.receive_layout.addWidget(self.button_send_window, 4 ,1)
        self.receive_layout.addWidget(self.button_download_attachment, 4, 2)

        self.setLayout(self.receive_layout)

        self.load_emails()

    def refresh_action(self):
        None

    def download_attachment(self):
        None

    def load_emails(self):
        server = imaplib.IMAP4_SSL(self.user_imap_host, self.user_imap_port)

        server.login(self.user_email, self.user_password)
        server.select("inbox")
        status, messages = server.search(None, "ALL")
        email_list = []

        for num in messages[0].split():
            status, data = server.fetch(num, "(RFC822)")
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email)

            from_ = email_message["From"]
            subject = email_message["Subject"]
            date_str = self.get_date(email_message)
            if email_message.is_multipart():
                body = ""
                for part in email_message.get_payload():
                    if part.get_content_type() == 'text/plain':
                        body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
            else:
                body = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')

            item = QListWidgetItem()
            item.setText(f"From: {from_}\nSubject: {subject}\nDate: {date_str}")
            item.setData(32, body)
            email_list.append(item)
            for item in reversed(email_list):
                self.list_emails.insertItem(0, item)

        server.logout()

    def get_date(self, email_message):
        date_str = email_message.get("Delivery-Date") or email_message.get("Date")

        if date_str:
            try:
                date_tuple = email.utils.parsedate_tz(date_str)
                date_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(email.utils.mktime_tz(date_tuple)))
            except:
                date_str = "Unknown Date"
        else:
            date_str = "Unknown Date"

        return date_str

    def show_mail(self, item):
        email_info = item.text().split('\n')
        from_ = email_info[0][6:]
        subject = email_info[1][9:]
        self.from_emails.setText(from_)
        self.subject_emails.setText(subject)
        self.text_emails.setPlainText(item.data(32))

    def back_to_send_window(self):
        self.close()
        self.new_send_window = send_window.EmailSend(self.user_email, self.user_password, self.user_imap_host,
                                                             self.user_smtp_host, self.user_imap_port, self.user_smtp_port)
        self.new_send_window.show()