# $ expense-tracker add --description "Lunch" --amount 20
# # Expense added successfully (ID: 1)
#
# $ expense-tracker add --description "Dinner" --amount 10
# # Expense added successfully (ID: 2)
#
# $ expense-tracker list
# # ID  Date       Description  Amount
# # 1   2024-08-06  Lunch        $20
# # 2   2024-08-06  Dinner       $10
#
# $ expense-tracker summary
# # Total expenses: $30
#
# $ expense-tracker delete --id 2
# # Expense deleted successfully
#
# $ expense-tracker summary
# # Total expenses: $20
#
# $ expense-tracker summary --month 8
# # Total expenses for August: $20

# Here are some additional features that you can add to the application:
# - Add expense categories and allow users to filter expenses by category.
# - Allow users to set a budget for each month and show a warning when the user exceeds the budget.
# - Allow users to export expenses to a CSV file.

import json
from os import path

from datetime import datetime
from tabulate import tabulate

class ExpenseTracker:
    def __init__(self):
        if path.exists("data.json"):
            with open("data.json", "r") as f:
                self.data = json.load(f)
        else:
            self.data = []
            with open("data.json", "w") as f:
                json.dump(self.data, f, indent=4)

    def update_expense(self, expense_id: int, description: str | None = None, expense: int | None = None):
        if not self.data:
            print("No data found to update")

        total_user = len(list(filter(lambda x: x["id"] == expense_id, self.data)))

        if total_user == 0:
            print(f"No expense found to update with id {expense_id}")

        else:
            self.data = list(
                map(
                    lambda x:
                    x
                    if x["id"] != expense_id
                    else
                        {
                            "id": x["id"],
                            "description": description if description is not None else x["description"],
                            "expense": expense if expense is not None else x["expense"],
                            "date": x["date"]
                        }
                    , self.data
                )
            )

            with open("data.json", "w") as f:
                json.dump(self.data, f, indent=4)

            print("Expense updated successfully")

    def add_expense(self, description: str, expense: float):
        if self.data == []:
            self.data.append({"id": 0, "description": description, "expense": expense, "date": str(datetime.date(datetime.now()).isoformat())})

        else:
            self.data.append({"id": self.data[-1]["id"] + 1, "description": description, "expense": expense, "date": str(datetime.date(datetime.now()).isoformat())})

        print("Expense added successfully")
        with open("data.json", "w") as f:
            json.dump(self.data, f, indent=4)

    def delete_expense(self, expense_id: int):

        old_len = len(self.data)
        self.data = list(filter(lambda x: x["id"] != expense_id, self.data))
        new_len = len(self.data)

        if old_len == new_len:
            print("Id not found")

        else:
            print("Expense deleted successfully")

            with open("data.json", "w") as f:
                json.dump(self.data, f, indent=4)

    def summary_expense(self, month: int | None = None):

        if month is None:
            total_expense = sum(list(map(lambda x: x["expense"], self.data)))
            print(f"Total expense: ${total_expense}")

        elif month not in range(1, 13):
            print(f"Month {month} is not valid [Between 1 and 12]")

        else:
            total_expense = sum(
                list(
                    map(
                        lambda x:
                            x["expense"]
                            if datetime.fromisoformat(x["date"]).month == month else 0
                        , self.data)))
            print(f"Total expense: ${total_expense}")


    def display_expenses(self):
        print(tabulate(self.data, headers="keys"))

if __name__ == '__main__':
    tracker = ExpenseTracker()
    tracker.add_expense(description="Test #1", expense=100)
    tracker.add_expense(description="Test #2", expense=200)
    tracker.add_expense(description="Test #3", expense=300)
    tracker.add_expense(description="Test #4", expense=400)
    tracker.add_expense(description="Test #5", expense=500)
    tracker.add_expense(description="Test #6", expense=600)
    tracker.add_expense(description="Test #7", expense=700)
    tracker.add_expense(description="Test #8", expense=800)
    tracker.add_expense(description="Test #9", expense=900)

    tracker.delete_expense(expense_id=1)
    tracker.delete_expense(expense_id=2)

    tracker.update_expense(expense_id=1, description="Test #1", expense=100)
    tracker.update_expense(expense_id=2, description="Test #2", expense=200)
    tracker.update_expense(expense_id=3, description="Test #3 (updated)", expense=300)
    tracker.update_expense(expense_id=4, description="Test #4 (updated)", expense=400)
    tracker.update_expense(expense_id=5, description="Test #5 (updated)")
    tracker.update_expense(expense_id=6, expense=900000)

    tracker.display_expenses()
    tracker.summary_expense()
    tracker.summary_expense(month=2)
    tracker.summary_expense(month=3)
    tracker.summary_expense(month=14)
    tracker.summary_expense(month=-15)