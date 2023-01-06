# Semplice classe per la creazione degli oggetti per gli impiegati
class Investor:
    def __init__(self, business_name, investment, n_order):
        self.business_name = business_name
        self.investment = investment
        self.n_order = n_order

    def get_name(self):
        return self.business_name

    def get_investment(self):
        return self.investment

    def get_n_order(self):
        return self.n_order