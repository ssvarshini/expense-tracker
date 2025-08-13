class Expense:
    def __init__(self, name, category, amount, date):
        self.name = name
        self.category = category
        self.amount = amount
        self.date = date

    def __repr__(self):
        return f"Expense: {self.name}, {self.category}, ${self.amount}, {self.date}"
