import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.email = "admin@admin.com"
        self.password = "Admin@147"

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login Registration Form")
        self.setGeometry(720, 200, 600, 400)  # Adjusted Y coordinate so it fits your screen

        self.qLabelEmail = QLabel("Email", self)
        self.qLabelEmail.setGeometry(50, 50, 100, 30)

        self.qlineEdit = QLineEdit(self)
        self.qlineEdit.setGeometry(150, 50, 120, 30)

        self.qLabelPass = QLabel("Password", self)
        self.qLabelPass.setGeometry(50, 100, 100, 30)

        self.qlineEdit1 = QLineEdit(self)
        self.qlineEdit1.setEchoMode(QLineEdit.EchoMode.Password)  # Masks the password text
        self.qlineEdit1.setGeometry(150, 100, 120, 30)

        self.button = QPushButton("Login", self)
        self.button.setGeometry(100, 150, 80, 30)
        self.button.clicked.connect(self.check_login)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def check_login(self):
        entered_user = self.qlineEdit.text()
        entered_pass = self.qlineEdit1.text()
        patternForPassword = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        validEmail = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        msg = QMessageBox(self)

        if re.fullmatch(validEmail, entered_user):
            if re.fullmatch(patternForPassword, entered_pass):
                if entered_user == self.email and entered_pass == self.password:
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setText("Login Successful!")
                    msg.setWindowTitle("Success")
                else:
                    msg.setIcon(QMessageBox.Icon.Critical)
                    msg.setText("Invalid Username or Password")
                    msg.setWindowTitle("Error")
            else:
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Weak Password")
                msg.setText(
                    "Password must be at least 8 characters long.\n"
                    "It must contain at least 1 lowercase letter, 1 uppercase letter, "
                    "1 digit, and 1 special character (@$!%*?&)."
                )
                msg.exec_()
                return
        else:
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Invalid Email")
            msg.setText("Invalid Email Format")

        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
