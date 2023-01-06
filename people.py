import abc
import time


def measure_time(func):
    def wrapper(*args, **kwargs):
        inizio = time.perf_counter()
        result = func(*args, **kwargs)
        fine = time.perf_counter()
        totale = fine - inizio
        print(f"Tempo creazione lavoratore: {totale:.6f} secondi")
        return result
    return wrapper


class WorkerFactory(metaclass=abc.ABCMeta):
    """Abstract factory for creating Worker objects."""

    @abc.abstractmethod
    def create_worker(self, name, age, username, password, type, salary):
        """Create an Employee object."""
        pass


class EmployeeFactory(WorkerFactory):
    """Concrete factory for creating Employee and Operator objects."""
    @measure_time
    def create_worker(self, name, age, username, password, type, salary):
        if type == "Employee":
            return Employee(name, age, username, password, salary)
        elif type == "Operator":
            return Operator(name, age, username, password, salary)
        else:
            raise ValueError("Invalid employee type")


class BossFactory(WorkerFactory):
    """Concrete factory for creating Boss objects."""
    @measure_time
    def create_worker(self, name, age, username, password, type, salary):
        return Boss(name, age, username, password, salary)


class Worker(metaclass=abc.ABCMeta):
    """Abstract base class for Worker objects."""

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


class Employee(Worker):
    """Concrete class for Employee objects."""

    def __init__(self, name, age, username, password, salary):
        super().__init__(name, age, username, password, salary)

    def get_type(self):
        return "Employee"


class Operator(Worker):
    """Concrete class for Operator objects."""

    def __init__(self, name, age, username, password, salary):
        super().__init__(name, age, username, password, salary)

    def get_type(self):
        return "Operator"


class Boss(Worker):
    """Concrete class for Boss objects."""

    def __init__(self, name, age, username, password, salary):
        super().__init__(name, age, username, password, salary)

    def get_type(self):
        return "Boss"







