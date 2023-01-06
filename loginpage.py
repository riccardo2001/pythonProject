from PyQt5.QtWidgets import QLabel, QLineEdit, QMessageBox, QWidget, QGridLayout
from workerpages import WindowEmployee, WindowBoss, WindowOperator
from loginComponent import LoginBtn, LoginLabel, LoginLine
import time

# Decoratore per misurare il login
def measure_time(func):
    def wrapper(widget):
        inizio = time.perf_counter()
        result = func(widget)
        fine = time.perf_counter()
        totale = fine - inizio
        print(f"Tempo Impiegato per il login: {totale:.6f} secondi")
        return result
    return wrapper


# Pagina di login
class LoginWindow(QWidget):
    def __init__(self, company, emp_op_factory):
        super().__init__()
        self.company = company
        self.emp_op_factory = emp_op_factory
        self.layout = QGridLayout(self)
        # Create the username label and line edit
        self.username_label = LoginLabel("Username: ")
        self.username_edit = LoginLine(self)

        # Create the password label and line edit
        self.password_label = LoginLabel("Password: ")
        self.password_edit = LoginLine(self)
        self.password_edit.setEchoMode(QLineEdit.Password)

        # Create the login button
        self.login_button = LoginBtn("Login")
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.username_label, 0, 1)
        self.layout.addWidget(self.username_edit, 0, 2)
        self.layout.addWidget(self.password_label, 1, 1)
        self.layout.addWidget(self.password_edit, 1, 2)
        self.layout.addWidget(self.login_button, 2, 1, 2, 2)

        self.setStyleSheet("background-color: darkslategray; background-repeat: no-repeat; background-position: center")

        self.setLayout(self.layout)
        self.setWindowTitle("Login")
        self.show()

    @measure_time
    def login(self):
        # Ottengo le credenziali
        username = self.username_edit.text()
        password = self.password_edit.text()
        # Verifico se le credenziali sono nella compagnia
        person = self.company.check_credentials(username, password)
        # Di seguito creo un visione diversa a seconda di chi si è loggato e chiudo la login window
        if person == "Boss":
            with open('username.txt', 'w') as f:
                f.write(username + '\n')
            self.w = WindowBoss(self.company, self.emp_op_factory)
            self.w.show()
            self.close()
        elif person == "Employee":
            with open('username.txt', 'w') as f:
                f.write(username + '\n')
            self.w = WindowEmployee()
            self.w.show()
            self.close()
        elif person == "Operator":
            with open('username.txt', 'w') as f:
                f.write(username + '\n')
            self.w = WindowOperator()
            self.w.show()
            self.close()
        else:
            # Se le credenziali mostro un messaggio di errore
            error_dialog = QMessageBox.warning(self, "Error", "Invalid username or password", QMessageBox.Ok)
