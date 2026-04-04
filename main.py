from dataclasses import dataclass

@dataclass
class ExpenseTracker:
    amount: int

def add_expense(expense: ExpenseTracker):
    ...