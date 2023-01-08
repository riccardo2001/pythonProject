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
    def __init__(self, company, worker_factory, username):
        super().__init__()

        # Setto varibili
        self.company = company
        self.worker_factory = worker_factory
        self.username = username

        # Setto finestra
        self.setWindowTitle("Loggato come Boss")
        layout = QGridLayout()

        # Setto i bottoni
        boss = BossSpecBtn("Boss View")
        boss.clicked.connect(self.viewBoss)
        employee = BossSpecBtn("Employee View")
        employee.clicked.connect(self.viewEmployee)
        operator = BossSpecBtn("Operator View")
        operator.clicked.connect(self.viewOperator)
        boss_label = BossLabel("Welcome Boss!")
        boss_label.setAlignment(Qt.Qt.AlignCenter)

        # Setto i widget
        self.setLayout(layout)
        layout.addWidget(boss_label)
        layout.addWidget(boss)
        layout.addWidget(employee)
        layout.addWidget(operator)

        #Setto schermo intero
        self.setStyleSheet("background-image: url(img.png);")
        self.showMaximized()


    def viewBoss(self):
        self.w = SottoWindowBoss(self.company, self.worker_factory)
        self.w.show()

    def viewEmployee(self):
        self.w = WindowEmployee(self.username)
        self.w.show()

    def viewOperator(self):
        self.w = WindowOperator(self.username)
        self.w.show()


class SottoWindowBoss(QWidget):
    def __init__(self, company, worker_factory):
        super().__init__()

        # Setto variabili
        self.company = company
        self.worker_factory = worker_factory
        self.setWindowTitle("Loggato come Boss")

        # Se c'è data la carico senno me la ricalcolo da company che viene passato come parametro
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

        # Aggiungo il trigger di quando la tabella viene toccata
        self.table.setEditTriggers(QtWidgets.QTableView.DoubleClicked | QtWidgets.QTableView.EditKeyPressed)
        self.table.setModel(self.model)

        # Inizializzo i tab
        tabs = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()

        # Aggiungo i tab
        tabs.addTab(tab1, "Dipendenti")
        tabs.addTab(tab2, "Operazioni")

        # Creao tab1-2 e aggiungo table
        tab1.layout = QVBoxLayout()
        tab1.layout.addWidget(self.table)
        tab1.setLayout(tab1.layout)
        user_label = BossLabel("Welcome Boss")
        tab2.layout = QGridLayout()

        # Sort
        key_label = WorkerLabel("Sorted by Col: ")
        self.key_text = WorkerLine("")
        button1 = BossBtn("Sort")
        button1.clicked.connect(self.ordina)
        self.reverse = QCheckBox("REVERSE")
        # Find
        word_label = WorkerLabel("Search word: ")
        self.word_text = WorkerLine("")
        button2 = BossBtn("Find")
        button2.clicked.connect(self.cerca)

        # Delete
        delete_label = WorkerLabel("Worker Username: ")
        self.delete_text = WorkerLine("")
        button3 = BossBtn("Fire")
        button3.clicked.connect(self.fire)

        # Cambia paga
        salary_label = WorkerLabel("New Salary: ")
        self.namesal_text = WorkerLine("Username")
        self.salary_text = WorkerLine("Salary")
        button4 = BossBtn("Done")
        button4.clicked.connect(self.salary)

        # Aggiungi dipendente
        type_label = WorkerLabel("Insert values: ")
        self.name = WorkerLine("Name")
        self.age = WorkerLine("Age")
        self.username = WorkerLine("Username")
        self.password = WorkerLine("Password")
        self.type = WorkerLine("Type")
        self.salary = WorkerLine("Salary")
        button5 = BossBtn("Insert")
        button5.clicked.connect(self.insert)

        # Aggiungo i componenti a tab2
        tab2.layout.addWidget(key_label, 0, 1)
        tab2.layout.addWidget(self.key_text, 0, 2)
        tab2.layout.addWidget(button1, 0, 3)
        tab2.layout.addWidget(self.reverse, 0, 4)
        tab2.layout.addWidget(word_label, 1, 1)
        tab2.layout.addWidget(self.word_text, 1, 2)
        tab2.layout.addWidget(button2, 1, 3)
        tab2.layout.addWidget(type_label, 2, 1)
        tab2.layout.addWidget(self.name, 2, 2)
        tab2.layout.addWidget(self.age, 2, 3)
        tab2.layout.addWidget(self.username, 2, 4)
        tab2.layout.addWidget(self.password, 2, 5)
        tab2.layout.addWidget(self.type, 2, 6)
        tab2.layout.addWidget(self.salary, 2, 7)
        tab2.layout.addWidget(button5, 2, 8)
        tab2.layout.addWidget(delete_label, 3, 1)
        tab2.layout.addWidget(self.delete_text, 3, 2)
        tab2.layout.addWidget(button3, 3, 3)
        tab2.layout.addWidget(salary_label, 4, 1)
        tab2.layout.addWidget(self.namesal_text, 4, 2)
        tab2.layout.addWidget(self.salary_text, 4, 3)
        tab2.layout.addWidget(button4, 4, 4)
        tab2.setLayout(tab2.layout)

        # Logout
        logout = BossBtn("Logout")
        logout.clicked.connect(self.close)

        # Save
        save = BossBtn("Save")
        save.clicked.connect(self.savefun)

        # Imposto il layout per la finestra principale e gli aggiungo i widget
        layout = QGridLayout()
        layout.addWidget(user_label, 0, 1)
        layout.addWidget(tabs, 1, 1, 1, 10)
        layout.addWidget(save, 0, 9)
        layout.addWidget(logout, 0, 10)
        self.setStyleSheet("background-color: silver; background-repeat: no-repeat; background-position: center")
        self.setLayout(layout)

    # Funzione per il salvataggio di data_boss
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
                self.model = TableModelBoss(sorted(self.data_boss, key=lambda i: i[int(self.key_text.text())-1],reverse=self.reverse.isChecked()))
                self.key_text.setText("")
                self.table.setModel(self.model)
                self.savefun()
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
                    msg.setText("Elemento trovato nella/e posizione/i: {} \n Dipendente: {}".format(out, self.data_boss[out[0][0]-1]))
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
                out = [(ind, ind2) for ind, i in enumerate(self.data_boss)
                       for ind2, y in enumerate(i) if self.username.text() in str(y)]
                if not out:
                    # Operazione per aggiornare la tabella
                    self.data_boss.append([self.username.text(), int(self.age.text()), self.type.text(), int(self.salary.text())])
                    self.model = TableModelBoss(self.data_boss)
                    self.table.setModel(self.model)
                    self.company.add_worker(self.worker_factory.create_worker(self.name.text(), int(self.age.text()), self.username.text(), self.password.text(), self.type.text(), int(self.salary.text())))
                    self.serialize_obj()
                    self.savefun()
                    self.name.setText("Name")
                    self.age.setText("Age")
                    self.username.setText("Username")
                    self.password.setText("Password")
                    self.type.setText("Type")
                    self.salary.setText("Salary")
                else:
                    error_dialog = QMessageBox.warning(self, "Error", "Utente già presente", QMessageBox.Ok)

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
                    # Operazioni di aggiornamento e visualizzazione nuova tabella
                    self.data_boss[out[0][0]][3] = int(self.salary_text.text())
                    self.model = TableModelBoss(self.data_boss)
                    self.table.setModel(self.model)
                    self.company.setworker_salary(self.salary_text.text(), self.namesal_text.text())
                    self.namesal_text.setText("Username")
                    self.salary_text.setText("Salary")
                    self.serialize_obj()
                    self.savefun()
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
                       for ind2, y in enumerate(i) if self.delete_text.text() == str(y)]

                if out:
                    # Operazioni di aggiornamento e visualizzazione nuova tabella
                    del(self.data_boss[out[0][0]])
                    self.model = TableModelBoss(self.data_boss)
                    self.table.setModel(self.model)
                    self.company.delworker(self.delete_text.text())
                    self.delete_text.setText("")
                    self.savefun()
                    self.serialize_obj()
                else:
                    msg = QMessageBox()
                    msg.setText("Elemento non trovato(il nome utente cercato deve essere identico a quello in tabella)")
                    msg.exec_()
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    # Questa funzione serve per salvare l'oggetto company
    def serialize_obj(self):
        try:
            # apriamo un file in modalità scrittura binaria
            with open("company.pickle", "wb") as f:
                # serializziamo l'oggetto e lo scriviamo sul file
                pickle.dump(self.company, f)
        except:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)


class WindowOperator(QWidget):
    def __init__(self, nome_utente):
        super().__init__()
        self.data_operatore = []
        username = nome_utente

        # Se c'è già la lista data_operatore la carico senno me la creao
        if os.path.exists('data_operatore.txt'):
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

        # Do il benvenuto
        user_label = WorkerLabel("Welcome " + username)
        self.setWindowTitle("Loggato come Operatore")

        # Creazione tabella
        self.table = QtWidgets.QTableView()

        # Setup table
        self.model = TableModelOperator(self.data_operatore)

        # Aggiusto l'ultima colonna senno devo allargarla tutte le volte
        self.table.resizeColumnToContents(3)

        # Do la possibilità di regolare la dimensione delle colonne
        self.table.adjustSize()

        # Aggiungo il trigger di quando la tabella viene toccata
        self.table.setEditTriggers(QtWidgets.QTableView.DoubleClicked | QtWidgets.QTableView.EditKeyPressed)
        self.table.setModel(self.model)

        # Inizializzo la visualizzazione tab
        tabs = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()

        # Aggiungo i tab
        tabs.addTab(tab1, "Tabella Commissioni")
        tabs.addTab(tab2, "Operazioni")

        # Creao il primo tab
        tab1.layout = QVBoxLayout()
        tab1.layout.addWidget(self.table)
        tab1.setLayout(tab1.layout)

        # Creo il secondo tab
        tab2.layout = QGridLayout()

        # Sort
        key_label = WorkerLabel("Sorted by Col: ")
        self.key_text = WorkerLine("")
        button1 = WorkerBtn("Sort")
        button1.clicked.connect(self.ordina)
        self.reverse = QCheckBox("REVERSE")

        # Find
        word_label = WorkerLabel("Search word: ")
        self.word_text = WorkerLine("")
        button2 = WorkerBtn("Find")
        button2.clicked.connect(self.cerca)

        # Delete
        delete_label = WorkerLabel("Delete word: ")
        self.delete_text = WorkerLine("")
        button3 = WorkerBtn("Remove")
        button3.clicked.connect(self.elimina)
        self.box = QCheckBox("ALL LINE")

        # Insert
        type_label = WorkerLabel("Insert values: ")
        self.type_text = WorkerLine("Type")
        self.color_text = WorkerLine("Color")
        self.number_text = WorkerLine("Number")
        self.optionals_text = WorkerLine("Optionals")
        button4 = WorkerBtn("Insert")
        button4.clicked.connect(self.insert)

        # Sum ordini
        sum_label = WorkerLabel("Sum Orders: ")
        button5 = WorkerBtn("Done")
        button5.clicked.connect(self.sum_ordini)

        # Aggiungo al tab i widget regolandoli nel gridlayout
        tab2.layout.addWidget(key_label, 0, 1)
        tab2.layout.addWidget(self.key_text, 0, 2)
        tab2.layout.addWidget(button1, 0, 3)
        tab2.layout.addWidget(self.reverse, 0, 4)
        tab2.layout.addWidget(word_label, 1, 1)
        tab2.layout.addWidget(self.word_text, 1, 2)
        tab2.layout.addWidget(button2, 1, 3)
        tab2.layout.addWidget(type_label, 2, 1)
        tab2.layout.addWidget(self.type_text, 2, 2)
        tab2.layout.addWidget(self.color_text, 2, 3)
        tab2.layout.addWidget(self.number_text, 2, 4)
        tab2.layout.addWidget(self.optionals_text, 2, 5)
        tab2.layout.addWidget(button4, 2, 6)
        tab2.layout.addWidget(delete_label, 3, 1)
        tab2.layout.addWidget(self.delete_text, 3, 2)
        tab2.layout.addWidget(button3, 3, 3)
        tab2.layout.addWidget(self.box, 3, 4)
        tab2.layout.addWidget(sum_label, 4, 1)
        tab2.layout.addWidget(button5, 4, 3)
        tab2.setLayout(tab2.layout)

        # Setto lo sfondo
        self.setStyleSheet("background-color: powderblue; background-repeat: no-repeat; background-position: center")

        # Logout
        logout = WorkerBtn("Logout")
        logout.clicked.connect(self.close)

        # Save
        save = WorkerBtn("Save")
        save.clicked.connect(self.savefun)

        # Imposto il layout per la finestra principale e gli aggiungo i widget
        layout = QGridLayout()
        layout.addWidget(user_label, 0, 1)
        layout.addWidget(tabs, 1, 1, 1, 10)
        layout.addWidget(save, 0, 9)
        layout.addWidget(logout, 0, 10)
        self.setLayout(layout)

    def ordina(self):
        if self.key_text.text():
            try:
                # Operazione per aggiornare la tabella
                self.model = TableModelOperator(sorted(self.data_operatore, key=lambda i: i[int(self.key_text.text())-1], reverse=self.reverse.isChecked()))
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
                    msg.setText("Elemento trovato nella/e posizione/i: {} \n Macchina: {}".format(out, self.data_operatore[out[0][0]-1]))
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
                out = ([[ind, ind2] for ind, i in enumerate(self.data_operatore)
                        for ind2, y in enumerate(i) if self.type_text.text() == str(y)])
                if not out:
                    if self.optionals_text.text():
                        self.data_operatore.append([self.type_text.text(), self.color_text.text(), int(self.number_text.text()), self.optionals_text.text()])
                    else:
                        self.data_operatore.append([self.type_text.text(), self.color_text.text(), self.number_text.text(), " "])
                    self.type_text.setText("Type")
                    self.color_text.setText("Color")
                    self.number_text.setText("Number")
                    self.optionals_text.setText("Optionals")
                else:
                    error_dialog = QMessageBox.warning(self, "Error", "Tipo già presente", QMessageBox.Ok)



                # Operazione per aggiornare la tabella
                self.model = TableModelOperator(self.data_operatore)
                self.table.setModel(self.model)
            except:
                error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)
        else:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid insert", QMessageBox.Ok)

    def sum_ordini(self):
        try:
            msg = QMessageBox()
            sum_order = lambda data: sum(int(orders[2]) for orders in data)
            result = sum_order(self.data_operatore)
            msg.setText("La somma degli ordini è: {}".format(result))
            msg.exec_()
        except:
            error_dialog = QMessageBox.warning(self, "Error", "An error occured", QMessageBox.Ok)

    # Funzione per il salvataggio di data_operatore
    def savefun(self):
        try:
            # Apro il file
            with open('data_operatore.txt', 'w') as f:
                # Convert list to JSON string and write to file
                f.write(json.dumps(self.data_operatore))
        except:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid save", QMessageBox.Ok)


class WindowEmployee(QWidget):
    def __init__(self, nome_user):
        super().__init__()
        self.data_impiegato = []
        username = nome_user
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

        user_label = WorkerLabel("Welcome " + username)
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

        # Aggiungo il trigger di quando la tabella viene toccata
        self.table.setEditTriggers(QtWidgets.QTableView.DoubleClicked | QtWidgets.QTableView.EditKeyPressed)

        # Inizializzo la visualizzazione tab
        tabs = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()

        # Aggiungo i tab
        tabs.addTab(tab1, "Tabella Investitori")
        tabs.addTab(tab2, "Operazioni")

        # Creao il primo tab
        tab1.layout = QVBoxLayout()
        tab1.layout.addWidget(self.table)
        tab1.setLayout(tab1.layout)

        # Creo il secondo tab
        tab2.layout = QGridLayout()

        # Sort
        key_label = WorkerLabel("Sorted by Col: ")
        self.key_text = WorkerLine("")
        button1 = WorkerBtn("Sort")
        button1.clicked.connect(self.ordina)

        # Find
        word_label = WorkerLabel("Search word: ")
        self.word_text = WorkerLine("")
        button2 = WorkerBtn("Find")
        button2.clicked.connect(self.cerca)
        self.reverse = QCheckBox("REVERSE")

        # Delete
        delete_label = WorkerLabel("Delete word: ")
        self.delete_text = WorkerLine("")
        button3 = WorkerBtn("Remove")
        button3.clicked.connect(self.elimina)
        self.box = QCheckBox("ALL LINE")

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
        tab2.layout.addWidget(key_label, 0, 1)
        tab2.layout.addWidget(self.key_text, 0, 2)
        tab2.layout.addWidget(button1, 0, 3)
        tab2.layout.addWidget(self.reverse, 0, 4)
        tab2.layout.addWidget(word_label, 1, 1)
        tab2.layout.addWidget(self.word_text, 1, 2)
        tab2.layout.addWidget(button2, 1, 3)
        tab2.layout.addWidget(type_label, 2, 1)
        tab2.layout.addWidget(self.name_text, 2, 2)
        tab2.layout.addWidget(self.investment_text, 2, 3)
        tab2.layout.addWidget(self.orders_text, 2, 4)
        tab2.layout.addWidget(button4, 2, 6)
        tab2.layout.addWidget(delete_label, 3, 1)
        tab2.layout.addWidget(self.delete_text, 3, 2)
        tab2.layout.addWidget(button3, 3, 3)
        tab2.layout.addWidget(self.box, 3, 4)
        tab2.layout.addWidget(money_label, 4, 1)
        tab2.layout.addWidget(money, 4, 3)
        tab2.setLayout(tab2.layout)

        # Setto lo sfondo
        self.setStyleSheet("background-color: blanchedalmond; background-repeat: no-repeat; background-position: center")
        # Logout
        logout = WorkerBtn("Logout")
        logout.clicked.connect(self.close)

        # Save
        save = WorkerBtn("Save")
        save.clicked.connect(self.savefun)

        # Imposto il layout per la finestra principale e gli aggiungo i widget
        layout = QGridLayout()
        layout.addWidget(user_label, 0, 1)
        layout.addWidget(tabs, 1, 1, 1, 10)
        layout.addWidget(save, 0, 9)
        layout.addWidget(logout, 0, 10)
        self.setLayout(layout)

    def ordina(self):
        if self.key_text.text():
            try:
                print(self.key_text.text())
                print(self.data_impiegato[0])
                print(self.data_impiegato[1])
                print(self.data_impiegato[2])
                # Operazione per aggiornare la tabella, uso lmbda evitando l'uso di item getter che mi aggiunge un nuovo modulo
                self.model = TableModelImpiegato(sorted(self.data_impiegato, key=lambda i: i[int(self.key_text.text())-1], reverse=self.reverse.isChecked()))
                self.key_text.setText("")
                self.table.setModel(self.model)
            except Exception as e:
                print(e)
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
                    msg.setText("Elemento trovato nella/e posizione/i: {} \n Cliente: {}".format(out, self.data_impiegato[out[0][0]-1]))
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
                out = [(ind, ind2) for ind, i in enumerate(self.data_impiegato)
                       for ind2, y in enumerate(i) if self.name_text.text() == str(y)]
                if not out:
                    self.data_impiegato.append([self.name_text.text(), int(self.investment_text.text()), int(self.orders_text.text())])
                    # Operazione per aggiornare la tabella
                    self.model = TableModelImpiegato(self.data_impiegato)
                    self.table.setModel(self.model)
                    self.name_text.setText("Buisness_name")
                    self.investment_text.setText("Investment")
                    self.orders_text.setText("N_Orders")
                else:
                    error_dialog = QMessageBox.warning(self, "Error", "Cliente già presente", QMessageBox.Ok)

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

    # Faccio la somma degli investimenti
    def income(self):
        try:
            msg = QMessageBox()
            sum_investment = lambda data: sum(int(investment[1]) for investment in data)
            result = sum_investment(self.data_impiegato)
            msg.setText("La somma degli investment è: {}".format(result))
            msg.exec_()
        except:
            error_dialog = QMessageBox.warning(self, "Error", "An error occured", QMessageBox.Ok)

    # Funzione per il salvataggio di data_impiegato
    def savefun(self):
        try:
            # Apro il file
            with open('data_impiegato.txt', 'w') as f:
                # Convert list to JSON string and write to file
                f.write(json.dumps(self.data_impiegato))
        except:
            error_dialog = QMessageBox.warning(self, "Error", "Invalid save", QMessageBox.Ok)