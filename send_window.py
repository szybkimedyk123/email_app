from PySide2.QtWidgets import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import receive_window
import imaplib
import json
import sys

class EmailSend(QWidget):
    def __init__(self, user_email, user_password, user_imap_host, user_smtp_host ,user_imap_port, user_smtp_port):
        super().__init__()

        self.setWindowTitle("Email")
        self.resize(800, 400)
        self.send_layout = QGridLayout()
        self.file_added = None
        self.attachment_filename = None
        self.user_email = user_email
        self.user_password = user_password
        self.user_imap_host = user_imap_host
        self.user_smtp_host = user_smtp_host
        self.user_imap_port = user_imap_port
        self.user_smtp_port = user_smtp_port

        self.label_to = QLabel("To:")
        self.text_to = QLineEdit()
        self.label_subject = QLabel("Subject:")
        self.text_subject = QLineEdit()
        self.label_body = QLabel("Body:")
        self.text_body = QTextEdit()
        self.button_send = QPushButton("Send")
        self.button_send.clicked.connect(self.send_mail)
        self.button_attachment = QPushButton("Attachment")
        self.button_attachment.clicked.connect(self.add_attachment)
        #self.button_clear = QPushButton("Clear")
        self.button_emails = QPushButton("Emails")
        self.button_emails.clicked.connect(self.open_mails)

        self.send_layout.addWidget(self.label_to, 0, 0)
        self.send_layout.addWidget(self.text_to, 0, 1)
        self.send_layout.addWidget(self.label_subject, 1, 0)
        self.send_layout.addWidget(self.text_subject, 1, 1)
        self.send_layout.addWidget(self.label_body, 2, 0)
        self.send_layout.addWidget(self.text_body, 2, 1)
        self.send_layout.addWidget(self.button_attachment, 3, 0)
        self.send_layout.addWidget(self.button_send, 3, 1)
        self.send_layout.addWidget(self.button_emails, 3, 2)

        self.setLayout(self.send_layout)

    def send_mail(self):
        if self.text_to.text() == "":
            QMessageBox.warning(self, "Send failed", "Missing information")

        else:

            send_to = self.text_to.text()
            send_subject = self.text_subject.text()
            send_body = self.text_body.toPlainText()

            self.clear_email()

            message = MIMEMultipart()
            message['From'] = self.user_email
            message['To'] = send_to
            message['Subject'] = send_subject
            message.attach(MIMEText(send_body, "plain"))

            if self.file_added:
                attachment = MIMEApplication(self.file_added)
                attachment['Content-Disposition'] = f'attachment; filename="{self.attachment_filename}"'
                message.attach(attachment)

            try:
                server = smtplib.SMTP(self.user_smtp_host, self.user_smtp_port)
                server.starttls()
                server.login(self.user_email, self.user_password)
                server.send_message(message)
                server.quit()
                QMessageBox.information(self, "Sent", "Successfully sent")
                self.clear_email()
            except:
                QMessageBox.critical(self, "Error", "Sent failed")

    def open_mails(self):
        self.close()
        self.new_recive_window = receive_window.EmailReceive(self.user_email, self.user_password, self.user_imap_host, self.user_smtp_host,
                                                     self.user_imap_port, self.user_smtp_port)
        self.new_recive_window.show()

    def add_attachment(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select file", "", "All files (*.*)")

        if file_path:
            self.file_added = file_path
            self.attachment_filename = file_path.split("/")[-1]

    def clear_email(self):
        self.text_to.clear()
        self.text_body.clear()
        self.text_subject.clear()