import abc
import time

# Decoratore per la misurazione del tempo di creazione
def measure_time(func):
    def wrapper(*args, **kwargs):
        inizio = time.perf_counter()
        result = func(*args, **kwargs)
        fine = time.perf_counter()
        totale = fine - inizio
        print(f"Tempo creazione lavoratore: {totale:.6f} secondi")
        return result
    return wrapper

# Uso la metaclasse perchè in python tutte le classi sono create da metaclassi ma quella di default è type,
# a me serve una metaclasse che indichi il fatto che la mia classe sarà astratta che non può essere istanziata
# Inoltre in questo file utilizzo il desing pattern abstract factory
class PeopleFactory(metaclass=abc.ABCMeta):
    """Factory astratta per la creazione di oggetti worker"""

    @abc.abstractmethod
    def create_worker(self, name, age, username, password, type, salary):
        """Creazione degli oggetti worker, definita astratta"""
        pass


class WorkerFactory(PeopleFactory):
    """Concreta creazione della factory worker"""
    @measure_time
    def create_worker(self, name, age, username, password, type, salary):
        if type == "Employee":
            return Employee(name, age, username, password, salary)
        elif type == "Operator":
            return Operator(name, age, username, password, salary)
        else:
            raise ValueError("Invalid employee type")


class BossFactory(PeopleFactory):
    """Concreta creazione della factory boss"""
    @measure_time
    def create_worker(self, name, age, username, password, type, salary):
        return Boss(name, age, username, password, salary)


class People(metaclass=abc.ABCMeta):
    """Classe astratta degli oggetti worker"""

    def __init__(self, name, age, username, password, salary):
        self.name = name
        self.age = age
        self.username = username
        self.password = password
        self.salary = salary

    @abc.abstractmethod
    def get_type(self):
        pass

    def set_salary(self, salary):
        self.salary = salary


class Employee(People):
    """Classe concreta degli oggetti employee"""

    def __init__(self, name, age, username, password, salary):
        super().__init__(name, age, username, password, salary)

    def get_type(self):
        return "Employee"


class Operator(People):
    """Classe concreta degli oggetti operator"""

    def __init__(self, name, age, username, password, salary):
        super().__init__(name, age, username, password, salary)

    def get_type(self):
        return "Operator"


class Boss(People):
    """Classe concreta degli oggetti boss"""

    def __init__(self, name, age, username, password, salary):
        super().__init__(name, age, username, password, salary)

    def get_type(self):
        return "Boss"







