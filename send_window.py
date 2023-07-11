from PySide2.QtWidgets import *
import sys

class EmailSend(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Email")
        self.resize(800, 400)
        self.send_layout = QGridLayout()
        self.file_added = None

        self.label_to = QLabel("To::")
        self.text_to = QLineEdit()
        self.label_subject = QLabel("Subject:")
        self.text_subject = QLineEdit()
        self.label_body = QLabel("Body:")
        self.text_body = QTextEdit()
        self.button_send = QPushButton("Send")
        self.button_attachment = QPushButton("Attachment")
        self.button_attachment.clicked.connect(self.add_attachment)
        self.button_clear = QPushButton("Clear")
        #self.button_emails = QPushButton()

        self.send_layout.addWidget(self.label_to, 0, 0)
        self.send_layout.addWidget(self.text_to, 0, 1)
        self.send_layout.addWidget(self.label_subject, 1, 0)
        self.send_layout.addWidget(self.text_subject, 1, 1)
        self.send_layout.addWidget(self.label_body, 2, 0)
        self.send_layout.addWidget(self.text_body, 2, 1)
        self.send_layout.addWidget(self.button_attachment, 3, 0)
        self.send_layout.addWidget(self.button_send, 3, 1)
        self.send_layout.addWidget(self.button_clear, 3, 2)

        self.setLayout(self.send_layout)

    def send_mail(self):
        send_to = self.text_to.text()
        send_subject = self.text_subject.text()
        send_body = self.text_body.text=()
        if self.file_added:
            None

    def add_attachment(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select file", "", "All files (*.*)")

        if file_path:
            self.file_added = file_path

    def clear_email(self):
        self.text_to.clear()
        self.text_body.clear()
        self.text_subject.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailSend()
    window.show()
    sys.exit(app.exec_())