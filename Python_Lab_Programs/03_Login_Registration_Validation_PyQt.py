import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox

app = QApplication(sys.argv)
window = QMainWindow()

username = "admin"
password = "Admin@147"


def check_login():
    entered_user = qlineEdit.text()
    entered_pass = qlineEdit1.text()
    patternForPassword = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    msg = QMessageBox(window)

    if re.fullmatch(patternForPassword, entered_pass):
        if entered_user == username and entered_pass == password:
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
        msg.exec()
        return
    msg.exec()


window.setWindowTitle("Login Registration Forms")
window.setGeometry(720, 720, 600, 400)

qLabel = QLabel(window)
qLabel.setText("Username")
qLabel.setStyleSheet("color: rgb(255, 255, 255);")
qLabel.setGeometry(50, 50, 60, 30)
qLabel.show()

qlineEdit = QLineEdit(window)
qlineEdit.setText("")
qlineEdit.setStyleSheet("color: rgb(255, 255, 255);")
qlineEdit.setGeometry(150, 50, 80, 30)

qLabel = QLabel(window)
qLabel.setText("Password")
qLabel.setStyleSheet("color: rgb(255, 255, 255);")
qLabel.setGeometry(50, 100, 60, 30)
qLabel.show()

qlineEdit1 = QLineEdit(window)
qlineEdit1.setText("")
qlineEdit1.setStyleSheet("color: rgb(255, 255, 255);")
qlineEdit1.setGeometry(150, 100, 80, 30)

button = QPushButton(window)
button.setText("Login")
button.setStyleSheet("color: rgb(255, 255, 255);")
button.setGeometry(100, 150, 80, 30)

button.clicked.connect(check_login)

window.show()
sys.exit(app.exec_())
