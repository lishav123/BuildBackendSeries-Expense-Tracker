import json
import argparse
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

    def update_expense(self, expense_id: int, description: str | None = None, expense: float | None = None,
                       category: str | None = None):
        if not self.data:
            print("No data found to update")
            return

        total_user = len(list(filter(lambda x: x["id"] == expense_id, self.data)))

        if total_user == 0:
            print(f"No expense found to update with id {expense_id}")
        else:
            self.data = list(
                map(
                    lambda x:
                    x if x["id"] != expense_id else
                    {
                        "id": x["id"],
                        "description": description if description is not None else x["description"],
                        "expense": expense if expense is not None else x["expense"],
                        "date": x["date"],
                        "category": category if category is not None else x["category"]
                    }
                    , self.data
                )
            )

            with open("data.json", "w") as f:
                json.dump(self.data, f, indent=4)
            print("Expense updated successfully")

    def add_expense(self, description: str, expense: float, category: str = "General"):
        if not self.data:
            new_id = 1
        else:
            new_id = self.data[-1]["id"] + 1

        self.data.append({
            "id": new_id,
            "description": description,
            "expense": expense,
            "date": str(datetime.date(datetime.now()).isoformat()),
            "category": category.lower()
        })

        print(f"Expense added successfully (ID: {new_id})")
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

    def summary_expense(self, month: int | None = None, category: str | None = None):
        if month is None:
            total_expense = sum(list(map(lambda x: x["expense"], self.data))) if category is None else sum(
                list(map(lambda x: x["expense"], list(filter(lambda x: x["category"] == category, self.data)))))
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
                        , self.data))) if category is None else sum(
                list(
                    map(
                        lambda x:
                        x["expense"]
                        if datetime.fromisoformat(x["date"]).month == month else 0
                        , list(filter(lambda x: x["category"] == category, self.data)))))
            print(f"Total expense: ${total_expense}")
            return total_expense

    def display_expenses(self, month: int | None = None, category: str | None = None):
        if month is None and category is None:
            print(tabulate(self.data, headers="keys"))
        if month is None and category is not None:
            print(tabulate(list(filter(lambda x: x['category'] == category, self.data)), headers="keys"))
        if month is not None and category is None:
            if month in range(1, 13):
                print(tabulate(list(filter(lambda x: datetime.fromisoformat(x['date']).month == month, self.data)),
                               headers="keys"))
            else:
                print("Invalid month")
        if month is not None and category is not None:
            if month in range(1, 13):
                print(tabulate(list(
                    filter(lambda x: datetime.fromisoformat(x['date']).month == month and x['category'] == category,
                           self.data)), headers="keys"))
            else:
                print("Invalid month")

    def export_csv(self):
        import pandas as pd
        pd.DataFrame(self.data).to_csv("data.csv", index=False)
        print("Data exported to data.csv successfully")


# ==========================================
# CLI ARGPARSE SETUP
# ==========================================
def main():
    tracker = ExpenseTracker()

    parser = argparse.ArgumentParser(description="A simple CLI Expense Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- ADD COMMAND ---
    parser_add = subparsers.add_parser("add", help="Add a new expense")
    parser_add.add_argument("--description", required=True, type=str, help="Description of the expense")
    # Note: dest="expense" maps the user's --amount directly to your class method's 'expense' parameter
    parser_add.add_argument("--amount", required=True, type=float, dest="expense", help="Amount of the expense")
    parser_add.add_argument("--category", type=str, default="General", help="Category of the expense")
    # Bind this subparser to the add_expense method
    parser_add.set_defaults(func=lambda args: tracker.add_expense(args.description, args.expense, args.category))

    # --- LIST COMMAND ---
    parser_list = subparsers.add_parser("list", help="List all expenses")
    parser_list.add_argument("--month", type=int, help="Filter by month (1-12)")
    parser_list.add_argument("--category", type=str, help="Filter by category")
    parser_list.set_defaults(func=lambda args: tracker.display_expenses(args.month, args.category))

    # --- SUMMARY COMMAND ---
    parser_summary = subparsers.add_parser("summary", help="Show expense summary")
    parser_summary.add_argument("--month", type=int, help="Filter summary by month (1-12)")
    parser_summary.add_argument("--category", type=str, help="Filter summary by category")
    parser_summary.set_defaults(func=lambda args: tracker.summary_expense(args.month, args.category))

    # --- DELETE COMMAND ---
    parser_delete = subparsers.add_parser("delete", help="Delete an expense")
    parser_delete.add_argument("--id", required=True, type=int, dest="expense_id", help="ID of the expense to delete")
    parser_delete.set_defaults(func=lambda args: tracker.delete_expense(args.expense_id))

    # --- UPDATE COMMAND ---
    parser_update = subparsers.add_parser("update", help="Update an existing expense")
    parser_update.add_argument("--id", required=True, type=int, dest="expense_id", help="ID of the expense to update")
    parser_update.add_argument("--description", type=str, help="New description")
    parser_update.add_argument("--amount", type=float, dest="expense", help="New amount")
    parser_update.add_argument("--category", type=str, help="New category")
    parser_update.set_defaults(
        func=lambda args: tracker.update_expense(args.expense_id, args.description, args.expense, args.category))

    # --- EXPORT COMMAND ---
    parser_export = subparsers.add_parser("export", help="Export expenses to a CSV file")
    parser_export.set_defaults(func=lambda args: tracker.export_csv())

    # Parse the arguments and trigger the appropriate function
    args = parser.parse_args()

    # args.func executes the lambda function we set in set_defaults()
    args.func(args)


if __name__ == '__main__':
    main()