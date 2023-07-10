from PySide2.QtWidgets import *
import sys

class LoginMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Email login")
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

        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.login)
        email_layout.addWidget(self.button_login)

        self.setLayout(email_layout)

    def login(self):
            user_email = self.text_email
            user_password = self.text_password


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginMenu()
    window.show()
    sys.exit(app.exec_())