from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit


class BossLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("padding: 2px; font: bold italic Times New Roman 100px; color: teal;")


class BossSpecBtn(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("background-color: slategray; color: #FFFFFF; padding: 2px; font: bold 10px;  border-color: #2752B8;")


class BossBtn(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("background-color: snow; color: teal; padding: 2px; font: bold 10px;  border-color: #2752B8;")