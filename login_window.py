from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
import imaplib
import send_window
import receive_window
import json
import sys

class LoginMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Email login")
        self.setWindowIcon(QIcon("images/image_email.png"))
        self.resize(400, 400)
        email_layout = QVBoxLayout()

        email_input = QHBoxLayout()
        self.label_email = QLabel("Email:")
        self.text_email = QLineEdit()
        email_input.addWidget(self.label_email)
        email_input.addWidget(self.text_email)
        email_layout.addLayout(email_input)

        password_input = QHBoxLayout()
        self.label_password = QLabel("Password:")
        self.text_password = QLineEdit()
        self.text_password.setEchoMode(QLineEdit.Password)
        password_input.addWidget(self.label_password)
        password_input.addWidget(self.text_password)
        email_layout.addLayout(password_input)
        self.radio_advance = QGridLayout()
        self.popular_sites = QComboBox()
        self.popular_sites.addItem("None")

        with open('email_servers.json') as file:
            self.data = json.load(file)

        addresses = [item['name'] for item in self.data['address']]
        self.popular_sites.addItems(addresses)

        self.address_data = {item['name']: item for item in self.data['address']}

        self.popular_sites.currentIndexChanged.connect(self.update_data)

        self.radio_advance.addWidget(self.popular_sites, 0, 1, 1, 2)
        self.add_button = QPushButton("Add site")
        self.add_button.clicked.connect(self.add_sites)
        self.radio_advance.addWidget(self.add_button, 0, 0)
        email_layout.addLayout(self.radio_advance)

        self.label_site_name = QLabel("Site:")
        self.text_site_name = QLineEdit()
        self.label_imap_host = QLabel("IMAP Host:")
        self.text_imap_host = QLineEdit()
        self.label_smtp_host = QLabel("SMTP Host:")
        self.text_smtp_host = QLineEdit()
        self.label_imap_port = QLabel("IMAP Port:")
        self.text_imap_port = QLineEdit()
        self.label_smtp_port = QLabel("SMTP Port:")
        self.text_smtp_port = QLineEdit()

        self.radio_advance.addWidget(self.label_site_name, 1, 0)
        self.radio_advance.addWidget(self.text_site_name, 1, 1)
        self.radio_advance.addWidget(self.label_imap_host, 2, 0)
        self.radio_advance.addWidget(self.text_imap_host, 2, 1)
        self.radio_advance.addWidget(self.label_smtp_host, 3, 0)
        self.radio_advance.addWidget(self.text_smtp_host, 3, 1)
        self.radio_advance.addWidget(self.label_imap_port, 4, 0)
        self.radio_advance.addWidget(self.text_imap_port, 4, 1)
        self.radio_advance.addWidget(self.label_smtp_port, 5, 0)
        self.radio_advance.addWidget(self.text_smtp_port, 5, 1)

        buttons_group = QHBoxLayout()
        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.login_action)
        buttons_group.addWidget(self.button_login)
        self.button_clear = QPushButton("Clear")
        self.button_clear.clicked.connect(self.clear)
        buttons_group.addWidget(self.button_clear)
        email_layout.addLayout(buttons_group)

        self.setLayout(email_layout)

    def login_action(self):
        if self.text_email.text() == "" or self.text_password.text() == "" or self.text_smtp_host.text() == "" \
            or self.text_smtp_port.text() == "" or self.text_imap_host.text() == "" or self.text_imap_port.text() == "":
            QMessageBox.warning(self, "Log in failed", "Missing information")
        else:
            user_email = self.text_email.text()
            user_password = self.text_password.text()
            user_imap_host = self.text_imap_host.text()
            user_smtp_host = self.text_smtp_host.text()
            user_imap_port = self.text_imap_port.text()
            user_smtp_port = self.text_smtp_port.text()

            server = imaplib.IMAP4_SSL(user_imap_host, user_imap_port)

            try:
                server.login(user_email, user_password)
                server.select("INBOX")
                status, messages = server.search(None, "ALL")

                if status == 'OK':
                    self.close()
                    self.new_send_window = send_window.EmailSend(user_email, user_password, user_imap_host, user_smtp_host ,user_imap_port, user_smtp_port)
                    self.new_send_window.show()

            except imaplib.IMAP4.error:
                QMessageBox.information(self, "Log in failed", "Incorrect email or password")

    def clear(self):
        self.popular_sites.setCurrentIndex(0)
        self.text_email.clear()
        self.text_password.clear()
        self.text_imap_host.clear()
        self.text_imap_port.clear()
        self.text_smtp_host.clear()
        self.text_smtp_port.clear()
        self.text_site_name.setVisible(True)
        self.label_site_name.setVisible(True)


    def update_data(self, index):
        selected_value = self.popular_sites.currentText()

        if selected_value == "None":
            self.text_imap_host.setReadOnly(False)
            self.text_imap_host.setText("")
            self.text_smtp_host.setReadOnly(False)
            self.text_smtp_host.setText("")
            self.text_imap_port.setReadOnly(False)
            self.text_imap_port.setText("")
            self.text_smtp_port.setReadOnly(False)
            self.text_smtp_port.setText("")
            self.text_site_name.setVisible(True)
            self.label_site_name.setVisible(True)

        else:
            selected_address = self.address_data.get(selected_value)

            if selected_address:

                self.text_site_name.setVisible(False)
                self.text_site_name.clear()
                self.label_site_name.setVisible(False)
                imap_host = selected_address['imap_host']
                smtp_host = selected_address['smtp_host']
                imap_port = selected_address['imap_port']
                smtp_port = selected_address['smtp_port']
                self.text_imap_host.setText(imap_host)
                self.text_imap_host.setReadOnly(True)
                self.text_smtp_host.setText(smtp_host)
                self.text_smtp_host.setReadOnly(True)
                self.text_imap_port.setText(imap_port)
                self.text_imap_port.setReadOnly(True)
                self.text_smtp_port.setText(smtp_port)
                self.text_smtp_port.setReadOnly(True)

    def add_sites(self):
        user_site_name = self.text_site_name.text()
        is_site = self.popular_sites.findText(user_site_name)
        if is_site != -1:
            QMessageBox.warning(self, "This page is added", "Cannot add an existing page")
        else:
            user_imap_host = self.text_imap_host.text()
            user_smtp_host = self.text_smtp_host.text()
            user_imap_port = self.text_imap_port.text()
            user_smtp_port = self.text_smtp_port.text()
            new_site = {
                "name": user_site_name,
                "imap_host": user_imap_host,
                "smtp_host": user_smtp_host,
                "imap_port": user_imap_port,
                "smtp_port": user_smtp_port
            }
            self.data["address"].append(new_site)
            with open("email_servers.json", "w") as file:
                json.dump(self.data, file, indent=2)

            self.popular_sites.addItem(user_site_name)
            self.address_data[new_site['name']] = new_site
            print(self.address_data)
            QMessageBox.information(self, "Success", "Added new site correctly")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginMenu()
    window.show()
    sys.exit(app.exec_())