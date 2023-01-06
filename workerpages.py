from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QTabWidget, QGridLayout, QCheckBox
from workercomponent import WorkerLine, WorkerLabel, WorkerBtn
from macchine import Car
from clienti import Investor
from workertablemodel import TableModelImpiegato, TableModelOperator, TableModelBoss
from bosscomponenet import BossBtn, BossLabel, BossSpecBtn
import json
import os
import pickle

class WindowBoss(QWidget):
    def __init__(self, company, employee_factory):
        super().__init__()
        self.company = company
        self.employee_factory = employee_factory
        self.setWindowTitle("Loggato come Boss")
        self.layout = QGridLayout()
        # Inizializzazione della nested list per la tabella

        self.boss = BossSpecBtn("Boss View")
        self.boss.clicked.connect(self.viewBoss)
        self.employee = BossSpecBtn("Employee View")
        self.employee.clicked.connect(self.viewEmployee)
        self.operator = BossSpecBtn("Operator View")
        self.operator.clicked.connect(self.viewOperator)
        self.boss_label = BossLabel("Welcome Boss!")
        self.boss_label.setAlignment(Qt.Qt.AlignCenter)

        #setto lo sfondo
        self.setLayout(self.layout)
        self.layout.addWidget(self.boss_label)
        self.layout.addWidget(self.boss)
        self.layout.addWidget(self.employee)
        self.layout.addWidget(self.operator)
        #Setto schermo intero
        self.setStyleSheet("background-image: url(img.png);")
        self.showMaximized()


    def viewBoss(self):
        self.w = SottoWindowBoss(self.company, self.employee_factory)
        self.w.show()

    def viewEmployee(self):
        self.w = WindowEmployee()
        self.w.show()

    def viewOperator(self):
        self.w = WindowOperator()
        self.w.show()


class SottoWindowBoss(QWidget):
    def __init__(self, company, employee_factory):
        super().__init__()
        self.company = company
        self.employee_factory = employee_factory
        self.setWindowTitle("Loggato come Boss")
        if os.path.exists('data_boss.txt'):
            # Open file for reading
            with open('data_boss.txt', 'r') as f:
                # Read JSON string from file and parse it
                self.data_boss = json.loads(f.read())
        else:
            self.data_boss = [[worker.username, worker.age, worker.get_type(), worker.salary] for worker in self.company.get_workers()]
        # Creazione tabella
        self.table = QtWidgets.QTableView()
        # Aggiusto l'ultima colonna senno devo allargarla tutte le volte
        self.table.resizeColumnToContents(0)
        self.table.resizeColumnToContents(1)
        self.table.resizeColumnToContents(2)
        self.table.resizeColumnToContents(3)
        # Setup table
        self.model = TableModelBoss(self.data_boss)
        # Do la possibilità di regolare la dimensione delle colonne
        self.table.adjustSize()
        # Do la possibilità di modifica delle colonne
        self.table.setEditTriggers(QtWidgets.QTableView.DoubleClicked | QtWidgets.QTableView.EditKeyPressed)
        self.table.setModel(self.model)

        # Inizializzo la visualizzazione tab
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Aggiungo i tab
        self.tabs.addTab(self.tab1, "Dipendenti")
        self.tabs.addTab(self.tab2, "Operazioni")

        # Creao il primo tab
        self.tab1.layout = QVBoxLayout()
        self.tab1.layout.addWidget(self.table)
        self.tab1.setLayout(self.tab1.layout)
        self.user_label = BossLabel("Welcome Boss")

        # Creo il secondo tab
        self.tab2.layout = QGridLayout()
        # Sort
        self.key_label = WorkerLabel("Sorted by Col: ")
        self.key_text = WorkerLine(self)
        self.button1 = BossBtn("Sort")
        self.button1.clicked.connect(self.ordina)
        # Find
        self.word_label = WorkerLabel("Search word: ")
        self.word_text = WorkerLine(self)
        self.button2 = BossBtn("Find")
        self.button2.clicked.connect(self.cerca)
        # Delete
        delete_label = WorkerLabel("Worker name: ")
        self.delete_text = WorkerLine(self)
        self.button3 = BossBtn("Fire")
        self.button3.clicked.connect(self.fire)
        # Cambia paga
        self.salary_label = WorkerLabel("New Salary: ")
        self.namesal_text = WorkerLine("Username")
        self.salary_text = WorkerLine("Salary")
        self.button4 = BossBtn("Done")
        self.button4.clicked.connect(self.salary)
        # Aggiungi dipendente
        type_label = WorkerLabel("Insert values: ")
        self.name = WorkerLine("Name")
        self.age = WorkerLine("Age")
        self.username = WorkerLine("Username")
        self.password = WorkerLine("Password")
        self.type = WorkerLine("Type")
        self.salary = WorkerLine("Salary")
        self.button5 = BossBtn("Insert")
        self.button5.clicked.connect(self.insert)

        self.tab2.layout.addWidget(self.key_label, 0, 1)
        self.tab2.layout.addWidget(self.key_text, 0, 2)
        self.tab2.layout.addWidget(self.button1, 0, 3)
        self.tab2.layout.addWidget(self.word_label, 1, 1)
        self.tab2.layout.addWidget(self.word_text, 1, 2)
        self.tab2.layout.addWidget(self.button2, 1, 3)
        self.tab2.layout.addWidget(type_label, 2, 1)
        self.tab2.layout.addWidget(self.name, 2, 2)
        self.tab2.layout.addWidget(self.age, 2, 3)
        self.tab2.layout.addWidget(self.username, 2, 4)
        self.tab2.layout.addWidget(self.password, 2, 5)
        self.tab2.layout.addWidget(self.type, 2, 6)
        self.tab2.layout.addWidget(self.salary, 2, 7)
        self.tab2.layout.addWidget(self.button5, 2, 8)
        self.tab2.layout.addWidget(delete_label, 3, 1)
        self.tab2.layout.addWidget(self.delete_text, 3, 2)
        self.tab2.layout.addWidget(self.button3, 3, 3)
        self.tab2.layout.addWidget(self.salary_label, 4, 1)
        self.tab2.layout.addWidget(self.namesal_text, 4, 2)
        self.tab2.layout.addWidget(self.salary_text, 4, 3)
        self.tab2.layout.addWidget(self.button4, 4, 4)
        self.tab2.setLayout(self.tab2.layout)


        # Logout
        self.logout = BossBtn("Logout")
        self.logout.clicked.connect(self.close)
        # Save
        self.save = BossBtn("Save")
        self.save.clicked.connect(self.savefun)


        # Imposto il layout per la finestra principale e gli aggiungo i widget
        self.layout = QGridLayout()
        self.layout.addWidget(self.user_label, 0, 1)
        self.layout.addWidget(self.tabs, 1, 1, 1, 10)
        self.layout.addWidget(self.save, 0, 9)
        self.layout.addWidget(self.logout, 0, 10)
        self.setStyleSheet("background-color: silver; background-repeat: no-repeat; background-position: center")
        self.setLayout(self.layout)

    def savefun(self):
        try:
            # Open file for writing
            with open('data_boss.txt', 'w') as f:
                # Convert list to JSON string and write to file
                f.write(json.dumps(self.data_boss))
        except:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid save", QMessageBox.Ok)

    def ordina(self):
        if self.key_text.text():
            try:
                # Operazione per aggiornare la tabella
                self.model = TableModelOperator(sorted(self.data_boss, key=lambda i: i[int(self.key_text.text())-1]))
                self.key_text.setText("")
                self.table.setModel(self.model)
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)
        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    def cerca(self):
        if self.word_text.text():
            try:
                out = [(ind, ind2) for ind, i in enumerate(self.data_boss)
                       for ind2, y in enumerate(i) if self.word_text.text() in str(y)]
                # Aggiungo 1 agli indici per renderlo leggibile in tabella
                out = [(x + 1, y + 1) for x, y in out]
                self.word_text.setText("")
                if out:
                    msg = QMessageBox()
                    msg.setText("Elemento trovato nella/e posizione/i: {}".format(out))
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setText("Elemento non trovato")
                    msg.exec_()
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)
        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    def insert(self):
        if self.name.text() and self.age.text() and self.username.text() and self.password.text() and (self.type.text() == "Operator" or self.type.text() == "Employee") and self.salary.text():
            try:
                self.data_boss.append([self.name.text(), self.age.text(), self.type.text(), self.salary.text()])
                # Operazione per aggiornare la tabella
                self.model = TableModelOperator(self.data_boss)
                self.table.setModel(self.model)
                self.company.add_worker(self.employee_factory.create_worker(self.name.text(), self.age.text(), self.username.text(), self.password.text(), self.type.text(), self.salary.text()))
                self.name.setText("Name")
                self.age.setText("Age")
                self.username.setText("Username")
                self.password.setText("Password")
                self.type.setText("Type")
                self.salary.setText("Salary")
                self.serialize_obj()
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)
        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    def salary(self):
        if self.salary_text.text() and self.namesal_text.text():
            try:
                out = [(ind, ind2) for ind, i in enumerate(self.data_boss)
                       for ind2, y in enumerate(i) if self.namesal_text.text() in str(y)]

                if out:
                    self.data_boss[out[0][0]][3] = self.salary_text.text()
                    self.model = TableModelOperator(self.data_boss)
                    self.table.setModel(self.model)
                    self.company.setworker_salary(self.salary_text.text(), self.namesal_text.text())
                    self.namesal_text.setText("")
                    self.salary_text.setText("")
                    self.serialize_obj()
                else:
                    msg = QMessageBox()
                    msg.setText("Elemento non trovato")
                    msg.exec_()
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)


    def fire(self):
        if self.delete_text.text():
            try:
                out = [(ind, ind2) for ind, i in enumerate(self.data_boss)
                       for ind2, y in enumerate(i) if self.delete_text.text() in str(y)]

                if out:
                    del(self.data_boss[out[0][0]])
                    self.model = TableModelOperator(self.data_boss)
                    self.table.setModel(self.model)
                    self.company.delworker(self.delete_text.text())
                    self.delete_text.setText("")
                    self.savefun()
                    self.serialize_obj()
                else:
                    msg = QMessageBox()
                    msg.setText("Elemento non trovato")
                    msg.exec_()
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    def serialize_obj(self):
        # apriamo un file in modalità scrittura binaria
        with open("company.pickle", "wb") as f:
            # serializziamo l'oggetto e lo scriviamo sul file
            pickle.dump(self.company, f)


class WindowOperator(QWidget):
    def __init__(self):
        super().__init__()
        self.data_operatore = []
        with open('username.txt', 'r') as f:
            username = f.read()
        if os.path.exists('data_operatore.txt'):
            # Open file for reading
            with open('data_operatore.txt', 'r') as f:
                # Read JSON string from file and parse it
                self.data_operatore = json.loads(f.read())
        else:
            # Inizializzazione della nested list per la tabella
            self.data_operatore.extend(
                [[car.type, car.color, car.quantity, ", ".join(car.optional)] for car in
                 [Car("Sedan", "blue", 5, ["leather seats", "sunroof"]),
                  Car("SUV", "red", 2, ["4WD", "tow package"]),
                  Car("Truck", "silver", 1, ["extended cab", "bed liner", "leather seats"]),
                  Car("Hatchback", "green", 3, ["sport suspension", "rearview camera"]),
                  Car("Coupe", "black", 4, ["turbocharged engine", "sport wheels"])]])

        self.user_label = WorkerLabel("Welcome " + username)
        self.setWindowTitle("Loggato come Operatore")
        # Creazione tabella
        self.table = QtWidgets.QTableView()
        # Setup table
        self.model = TableModelOperator(self.data_operatore)
        # Aggiusto l'ultima colonna senno devo allargarla tutte le volte
        self.table.resizeColumnToContents(3)
        # Do la possibilità di regolare la dimensione delle colonne
        self.table.adjustSize()
        # Do la possibilità di modifica delle colonne
        self.table.setEditTriggers(QtWidgets.QTableView.DoubleClicked | QtWidgets.QTableView.EditKeyPressed)
        self.table.setModel(self.model)
        # Inizializzo la visualizzazione tab
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Aggiungo i tab
        self.tabs.addTab(self.tab1, "Tabella Commissioni")
        self.tabs.addTab(self.tab2, "Operazioni")

        # Creao il primo tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.table)
        self.tab1.setLayout(self.tab1.layout)

        # Creo il secondo tab
        self.tab2.layout = QGridLayout(self)
        # Sort
        key_label = WorkerLabel("Sorted by Col: ")
        self.key_text = WorkerLine(self)
        button1 = WorkerBtn("Sort")
        button1.clicked.connect(self.ordina)
        # Find
        word_label = WorkerLabel("Search word: ")
        self.word_text = WorkerLine(self)
        button2 = WorkerBtn("Find")
        button2.clicked.connect(self.cerca)
        # Delete
        delete_label = WorkerLabel("Delete word: ")
        self.delete_text = WorkerLine(self)
        button3 = WorkerBtn("Remove")
        button3.clicked.connect(self.elimina)
        self.box = QCheckBox("ALL LINE", self)
        # Insert
        type_label = WorkerLabel("Insert values: ")
        self.type_text = WorkerLine("Type")
        self.color_text = WorkerLine("Color")
        self.number_text = WorkerLine("Number")
        self.optionals_text = WorkerLine("Optionals")
        button4 = WorkerBtn("Insert")
        button4.clicked.connect(self.insert)
        # Aggiungo al tab i widget regolandoli nel gridlayout
        self.tab2.layout.addWidget(key_label, 0, 1)
        self.tab2.layout.addWidget(self.key_text, 0, 2)
        self.tab2.layout.addWidget(button1, 0, 3)
        self.tab2.layout.addWidget(word_label, 1, 1)
        self.tab2.layout.addWidget(self.word_text, 1, 2)
        self.tab2.layout.addWidget(button2, 1, 3)
        self.tab2.layout.addWidget(type_label, 2, 1)
        self.tab2.layout.addWidget(self.type_text, 2, 2)
        self.tab2.layout.addWidget(self.color_text, 2, 3)
        self.tab2.layout.addWidget(self.number_text, 2, 4)
        self.tab2.layout.addWidget(self.optionals_text, 2, 5)
        self.tab2.layout.addWidget(button4, 2, 6)
        self.tab2.layout.addWidget(delete_label, 3, 1)
        self.tab2.layout.addWidget(self.delete_text, 3, 2)
        self.tab2.layout.addWidget(button3, 3, 3)
        self.tab2.layout.addWidget(self.box, 3, 4)
        self.tab2.setLayout(self.tab2.layout)
        # Setto lo sfondo
        self.setStyleSheet("background-color: powderblue; background-repeat: no-repeat; background-position: center")
        # Logout
        self.logout = WorkerBtn("Logout")
        self.logout.clicked.connect(self.close)
        # Save
        self.save = WorkerBtn("Save")
        self.save.clicked.connect(self.savefun)
        # Imposto il layout per la finestra principale e gli aggiungo i widget
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.user_label, 0, 1)
        self.layout.addWidget(self.tabs, 1, 1, 1, 10)
        self.layout.addWidget(self.save, 0, 9)
        self.layout.addWidget(self.logout, 0, 10)
        self.setLayout(self.layout)

    def ordina(self):
        if self.key_text.text():
            try:
                # Operazione per aggiornare la tabella
                self.model = TableModelOperator(sorted(self.data_operatore, key=lambda i: i[int(self.key_text.text())-1]))
                self.key_text.setText("")
                self.table.setModel(self.model)
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)
        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    def cerca(self):
        if self.word_text.text():
            try:
                out = [(ind, ind2) for ind, i in enumerate(self.data_operatore)
                       for ind2, y in enumerate(i) if self.word_text.text() in str(y)]
                # Aggiungo 1 agli indici per renderlo leggibile in tabella

                out = [(x + 1, y + 1) for x, y in out]
                self.word_text.setText("")
                if out:
                    msg = QMessageBox()
                    msg.setText("Elemento trovato nella/e posizione/i: {}".format(out))
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setText("Elemento non trovato")
                    msg.exec_()
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)
        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    def elimina(self):
        if self.delete_text.text():
            try:
                out = ([[ind, ind2] for ind, i in enumerate(self.data_operatore)
                        for ind2, y in enumerate(i) if self.delete_text.text() in str(y)])
                self.delete_text.setText("")
                if out:
                    for x, y in out:
                        if self.box.isChecked():
                            del(self.data_operatore[int(x)])
                        else:
                            self.data_operatore[int(x)][int(y)] = " "
                    # Operazione per aggiornare la tabella
                    self.model = TableModelOperator(self.data_operatore)
                    self.table.setModel(self.model)
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)
        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)


    # Insert dove guardo se nessuno è none allora appendo il nuovo oggetto in più ho il controllo sugli optional che possono esserci oppure no
    def insert(self):
        if self.type_text.text() and self.color_text.text() and self.number_text.text():
            try:
                if self.optionals_text.text():
                    self.data_operatore.append([self.type_text.text(), self.color_text.text(), self.number_text.text(), self.optionals_text.text()])
                else:
                    self.data_operatore.append([self.type_text.text(), self.color_text.text(), self.number_text.text(), " "])
                self.type_text.setText("Type")
                self.color_text.setText("Color")
                self.number_text.setText("Number")
                self.optionals_text.setText("Optionals")
                # Operazione per aggiornare la tabella
                self.model = TableModelOperator(self.data_operatore)
                self.table.setModel(self.model)
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)
        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    def savefun(self):
        try:
            # Open file for writing
            with open('data_operatore.txt', 'w') as f:
                # Convert list to JSON string and write to file
                f.write(json.dumps(self.data_operatore))
        except:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid save", QMessageBox.Ok)


class WindowEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.data_impiegato = []
        with open('username.txt', 'r') as f:
            username = f.read()

        if os.path.exists('data_impiegato.txt'):
            # Open file for reading
            with open('data_impiegato.txt', 'r') as f:
                # Read JSON string from file and parse it
                self.data_impiegato = json.loads(f.read())
        else:
            # Inizializzazione
            self.data_impiegato.extend(
                [[investor.business_name, investor.investment, investor.n_order] for investor in
                 [Investor("Ferrari", 1000, 1),
                  Investor("Honda", 2000, 2),
                  Investor("Bugatti", 1500, 3),
                  Investor("Lamborghini", 2500, 4),
                  Investor("Fiat", 3000, 5)]])

        self.user_label = WorkerLabel("Welcome " + username)
        self.setWindowTitle("Loggato come Impiegato")
        # Creazione tabella
        self.table = QtWidgets.QTableView()
        # Setup table
        self.model = TableModelImpiegato(self.data_impiegato)
        self.table.setModel(self.model)
        # Aggiusto l'ultima colonna senno devo allargarla tutte le volte
        self.table.resizeColumnToContents(0)
        self.table.resizeColumnToContents(2)
        # Do la possibilità di regolare la dimensione delle colonne
        self.table.adjustSize()
        # Do la possibilità di modifica delle colonne
        self.table.setEditTriggers(QtWidgets.QTableView.DoubleClicked | QtWidgets.QTableView.EditKeyPressed)
        # Inizializzo la visualizzazione tab
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Aggiungo i tab
        self.tabs.addTab(self.tab1, "Tabella Investitori")
        self.tabs.addTab(self.tab2, "Operazioni")

        # Creao il primo tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.table)
        self.tab1.setLayout(self.tab1.layout)

        # Creo il secondo tab
        self.tab2.layout = QGridLayout(self)
        # Sort
        key_label = WorkerLabel("Sorted by Col: ")
        self.key_text = WorkerLine(self)
        button1 = WorkerBtn("Sort")
        button1.clicked.connect(self.ordina)
        # Find
        word_label = WorkerLabel("Search word: ")
        self.word_text = WorkerLine(self)
        button2 = WorkerBtn("Find")
        button2.clicked.connect(self.cerca)
        # Delete
        delete_label = WorkerLabel("Delete word: ")
        self.delete_text = WorkerLine(self)
        button3 = WorkerBtn("Remove")
        button3.clicked.connect(self.elimina)
        self.box = QCheckBox("ALL LINE", self)
        # Insert
        type_label = WorkerLabel("Insert values: ")
        self.name_text = WorkerLine("Buisness_name")
        self.investment_text = WorkerLine("Investment")
        self.orders_text = WorkerLine("N_Orders")
        button4 = WorkerBtn("Insert")
        button4.clicked.connect(self.insert)
        # Somma soldi
        money_label = WorkerLabel("Income sum: ")
        money = WorkerBtn("Find")
        money.clicked.connect(self.income)
        # Aggiungo al tab i widget regolandoli nel gridlayout
        self.tab2.layout.addWidget(key_label, 0, 1)
        self.tab2.layout.addWidget(self.key_text, 0, 2)
        self.tab2.layout.addWidget(button1, 0, 3)
        self.tab2.layout.addWidget(word_label, 1, 1)
        self.tab2.layout.addWidget(self.word_text, 1, 2)
        self.tab2.layout.addWidget(button2, 1, 3)
        self.tab2.layout.addWidget(type_label, 2, 1)
        self.tab2.layout.addWidget(self.name_text, 2, 2)
        self.tab2.layout.addWidget(self.investment_text, 2, 3)
        self.tab2.layout.addWidget(self.orders_text, 2, 4)
        self.tab2.layout.addWidget(button4, 2, 6)
        self.tab2.layout.addWidget(delete_label, 3, 1)
        self.tab2.layout.addWidget(self.delete_text, 3, 2)
        self.tab2.layout.addWidget(button3, 3, 3)
        self.tab2.layout.addWidget(self.box, 3, 4)
        self.tab2.layout.addWidget(money_label, 4, 1)
        self.tab2.layout.addWidget(money, 4, 3)
        self.tab2.setLayout(self.tab2.layout)
        # Setto lo sfondo
        self.setStyleSheet("background-color: blanchedalmond	; background-repeat: no-repeat; background-position: center")
        # Logout
        self.logout = WorkerBtn("Logout")
        self.logout.clicked.connect(self.close)
        # Save
        self.save = WorkerBtn("Save")
        self.save.clicked.connect(self.savefun)
        # Imposto il layout per la finestra principale e gli aggiungo i widget
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.user_label, 0, 1)
        self.layout.addWidget(self.tabs, 1, 1, 1, 10)
        self.layout.addWidget(self.save, 0, 9)
        self.layout.addWidget(self.logout, 0, 10)
        self.setLayout(self.layout)

    def ordina(self):
        if self.key_text.text():
            try:
                # Operazione per aggiornare la tabella, uso lmbda evitando l'uso di item getter che mi aggiunge un nuovo modulo
                self.model = TableModelImpiegato(sorted(self.data_impiegato, key=lambda i: i[int(self.key_text.text())-1]))
                self.key_text.setText("")
                self.table.setModel(self.model)
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    def cerca(self):
        if self.word_text.text():
            try:
                out = [(ind, ind2) for ind, i in enumerate(self.data_impiegato)
                       for ind2, y in enumerate(i) if self.word_text.text() in str(y)]
                # Aggiungo 1 agli indici per renderlo leggibile in tabella
                out = [(x + 1, y + 1) for x, y in out]
                self.word_text.setText("")
                if out:
                    msg = QMessageBox()
                    msg.setText("Elemento trovato nella/e posizione/i: {}".format(out))
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setText("Elemento non trovato")
                    msg.exec_()
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    # Insert dove guardo se nessuno è none allora appendo il nuovo oggetto in più ho il controllo sugli optional che possono esserci oppure no
    def insert(self):
        if self.name_text.text() and self.investment_text.text() and self.orders_text.text():
            try:
                self.data_impiegato.append([self.name_text.text(), self.investment_text.text(), self.orders_text.text()])
                self.name_text.setText("Buisness_name")
                self.investment_text.setText("Investment")
                self.orders_text.setText("N_Orders")
                # Operazione per aggiornare la tabella
                self.model = TableModelImpiegato(self.data_impiegato)
                self.table.setModel(self.model)
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    def elimina(self):
        if self.delete_text.text():
            try:
                out = ([[ind, ind2] for ind, i in enumerate(self.data_impiegato)
                        for ind2, y in enumerate(i) if self.delete_text.text() in str(y)])
                self.delete_text.setText("")
                if out:
                    for x, y in out:
                        if self.box.isChecked():
                            del(self.data_impiegato[int(x)])
                        else:
                            self.data_impiegato[int(x)][int(y)] = " "
                    # Operazione per aggiornare la tabella
                    self.model = TableModelImpiegato(self.data_impiegato)
                    self.table.setModel(self.model)
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    def income(self):
        try:
            msg = QMessageBox()
            sum_investment = lambda data: sum(int(investment[1]) for investment in data)
            result = sum_investment(self.data_impiegato)
            msg.setText("La somma degli investment è: {}".format(result))
            msg.exec_()
        except:
            error_dialog = QMessageBox.warning(self, "Error", "An error occured", QMessageBox.Ok)


    def savefun(self):
        try:
            # Open file for writing
            with open('data_impiegato.txt', 'w') as f:
                # Convert list to JSON string and write to file
                f.write(json.dumps(self.data_impiegato))
        except:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid save", QMessageBox.Ok)

