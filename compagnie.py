# Classe per racchiudere le due factory attraverso due liste
class Company:
    def __init__(self):
        # Use the factory to create the Employee objects
        self.workers = []
        self.bosses = []

    def add_worker(self, worker):
        self.workers.append(worker)

    def add_boss(self, boss):
        self.bosses.append(boss)

    def check_credentials(self, username, password):
        """Controllo le credenziali"""
        for worker in self.workers:
            if worker.username == username and worker.password == password:
                return worker.get_type()
        for boss in self.bosses:
            if boss.username == username and boss.password == password:
                return boss.get_type()
        return False

    def get_workers(self):
        return self.workers

    def get_boss(self):
        return self.bosses

    def get_all(self):
        return self.bosses + self.workers

    def setworker_salary(self, salary, username):
        for worker in self.workers:
            if worker.username == username:
                worker.set_salary(salary)

    def delworker(self, username):
        for worker in self.workers:
            if worker.username == username:
                self.workers.remove(worker)
