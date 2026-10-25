import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTabWidget, QWidget,
    QVBoxLayout, QFormLayout
)

PATTERN_USERNAME = r"^[A-Za-z0-9]{4,20}$"
PATTERN_EMAIL = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
PATTERN_PASSWORD = (
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)"
    r"(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)

registered_users = {"admin": "Admin@147"}


class LoginTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()

        self.user_input = QLineEdit()
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.check_login)

        layout.addRow("Username:", self.user_input)
        layout.addRow("Password:", self.pass_input)
        layout.addRow(login_btn)
        self.setLayout(layout)

    def check_login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text()
        msg = QMessageBox(self)

        if not re.fullmatch(PATTERN_PASSWORD, password):
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Weak Password")
            msg.setText(
                "Password must be at least 8 characters long.\n"
                "It must contain at least 1 lowercase letter, "
                "1 uppercase letter, 1 digit, and 1 special "
                "character (@$!%*?&)."
            )
        elif (username in registered_users
              and registered_users[username] == password):
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Login Successful!")
            msg.setWindowTitle("Success")
        else:
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Invalid Username or Password")
            msg.setWindowTitle("Error")

        msg.exec()


class RegisterTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()

        self.reg_user = QLineEdit()
        self.reg_email = QLineEdit()
        self.reg_pass = QLineEdit()
        self.reg_pass.setEchoMode(QLineEdit.Password)
        self.reg_confirm = QLineEdit()
        self.reg_confirm.setEchoMode(QLineEdit.Password)

        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.handle_register)

        layout.addRow("Username:", self.reg_user)
        layout.addRow("Email:", self.reg_email)
        layout.addRow("Password:", self.reg_pass)
        layout.addRow("Confirm Password:", self.reg_confirm)
        layout.addRow(register_btn)
        self.setLayout(layout)

    def handle_register(self):
        username = self.reg_user.text().strip()
        email = self.reg_email.text().strip()
        password = self.reg_pass.text()
        confirm = self.reg_confirm.text()
        msg = QMessageBox(self)

        if not re.fullmatch(PATTERN_USERNAME, username):
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Invalid Username")
            msg.setText(
                "Username must be 4–20 alphanumeric characters "
                "(no spaces or special characters)."
            )
            msg.exec()
            return

        if username in registered_users:
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Username Taken")
            msg.setText(
                f"'{username}' is already registered. "
                "Please choose another username."
            )
            msg.exec()
            return

        if not re.fullmatch(PATTERN_EMAIL, email):
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Invalid Email")
            msg.setText(
                "Please enter a valid email address "
                "(e.g. user@example.com)."
            )
            msg.exec()
            return

        if not re.fullmatch(PATTERN_PASSWORD, password):
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Weak Password")
            msg.setText(
                "Password must be at least 8 characters and "
                "include 1 uppercase, 1 lowercase, 1 digit, "
                "and 1 special character (@$!%*?&)."
            )
            msg.exec()
            return

        if password != confirm:
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Mismatch")
            msg.setText("Passwords do not match.")
            msg.exec()
            return

        registered_users[username] = password
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Registration Successful")
        msg.setText(
            f"User '{username}' registered successfully!\n"
            f"Email: {email}\n\n"
            "You can now log in using the Login tab."
        )
        msg.exec()

        # Clear fields after successful registration
        self.reg_user.clear()
        self.reg_email.clear()
        self.reg_pass.clear()
        self.reg_confirm.clear()



app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Login & Registration Forms")
window.setGeometry(720, 720, 420, 320)

tabs = QTabWidget()
tabs.addTab(LoginTab(), "Login")
tabs.addTab(RegisterTab(), "Register")

window.setCentralWidget(tabs)
window.show()

sys.exit(app.exec_())
