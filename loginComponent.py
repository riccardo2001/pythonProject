from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit

# Classe per l'abbellimento dei componenti di login

class LoginBtn(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("background-color: slategray; color: #FFFFFF ; padding: 2px ; font: bold 10px ;  border-color: #2752B8;")


class LoginLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("border: 2px solid slategray; border-radius: 4px; padding: 2px; font: bold 10px ; color: #FFFFFF ;")


class LoginLine(QLineEdit):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("border: 2px solid slategray; border-radius: 4px; padding: 2px; font: bold 10px ; color: #FFFFFF ;")