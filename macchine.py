# Semplice classe per la creazione degli oggetti per gli operatori
class Car:
    def __init__(self, type, color, quantity, optional):
        self.type = type
        self.color = color
        self.quantity = quantity
        self.optional = optional

    def get_type(self):
        return self.type

    def get_color(self):
        return self.color

    def get_quantity(self):
        return self.quantity

    def get_optional(self):
        return self.optional