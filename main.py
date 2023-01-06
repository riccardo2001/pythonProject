import sys
from PyQt5.QtWidgets import QApplication
from compagnie import Company
from people import Emp_OP_Factory, BossFactory
from loginpage import LoginWindow
import pickle
import os

if __name__ == "__main__":
    # Creo le due factory
    employee_factory = Emp_OP_Factory()
    boss_factory = BossFactory()

    # Creo la compagnia
    company = Company()

    # Aggiungo alla compagnia i lavoratori
    company.add_worker(employee_factory.create_worker("John", 30, "jo", "pa", "Employee", 1500))
    company.add_worker(employee_factory.create_worker("Jane", 25, "jane123", "password2", "Employee", 1500))
    company.add_worker(employee_factory.create_worker("Mike", 35, "mike123", "password3", "Operator", 1500))
    company.add_worker(employee_factory.create_worker("Bob", 35, "bob123", "password3", "Operator", 1500))
    company.add_worker(employee_factory.create_worker("Alice", 28, "alice123", "password4", "Operator", 1500))
    company.add_worker(employee_factory.create_worker("Charlie", 40, "charlie123", "password5", "Operator", 1500))
    company.add_boss(boss_factory.create_worker("Eve", 45, "eve123", "password5", "Boss", 30000))


    # Se sono state applicate modifiche alla compagnia questo file esisterà e verrà caricato
    # pickle usato per la serializzazione
    if os.path.exists('company.pickle'):
        with open('company.pickle', 'rb') as f:
            company = pickle.load(f)

    app = QApplication(sys.argv)
    window = LoginWindow(company, employee_factory)
    sys.exit(app.exec())





