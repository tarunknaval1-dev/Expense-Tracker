import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("expenses.json")
BUDGET_FILE = Path("budget.json")


def load_expenses():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


def load_budget():
    if BUDGET_FILE.exists():
        with open(BUDGET_FILE, "r") as file:
            return json.load(file).get("monthly_budget", 0)
    return 0


def save_budget(budget):
    with open(BUDGET_FILE, "w") as file:
        json.dump({"monthly_budget": budget}, file, indent=4)


def add_expense(expenses):
    name = input("Enter expense name: ").strip()
    category = input("Enter category: ").strip()

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid amount.")
        return

    expense = {
        "name": name,
        "category": category or "Other",
        "amount": amount,
        "date": str(date.today())
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully!")


def view_expenses(expenses):
    if not expenses:
        print("\nNo expenses found.\n")
        return

    total = 0
    print("\n--- Your Expenses ---")

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. {expense['name']} | "
            f"{expense['category']} | "
            f"Rs. {expense['amount']:.2f} | "
            f"{expense['date']}"
        )
        total += expense["amount"]

    print(f"\nTotal expense: Rs. {total:.2f}\n")


def category_summary(expenses):
    if not expenses:
        print("\nNo expenses found.\n")
        return

    categories = {}

    for expense in expenses:
        category = expense["category"]
        categories[category] = categories.get(category, 0) + expense["amount"]

    print("\n--- Category-wise Spending ---")

    for category, total in categories.items():
        print(f"{category}: Rs. {total:.2f}")

    print()


def set_monthly_budget():
    try:
        budget = float(input("Enter your monthly budget: "))
        if budget <= 0:
            print("Budget must be greater than zero.")
            return

        save_budget(budget)
        print(f"Monthly budget set to Rs. {budget:.2f}")

    except ValueError:
        print("Please enter a valid amount.")


def budget_status(expenses):
    budget = load_budget()

    if budget == 0:
        print("\nNo monthly budget has been set yet.\n")
        return

    total_spent = sum(expense["amount"] for expense in expenses)
    remaining = budget - total_spent

    print("\n--- Monthly Budget Status ---")
    print(f"Budget: Rs. {budget:.2f}")
    print(f"Spent: Rs. {total_spent:.2f}")

    if remaining >= 0:
        print(f"Remaining: Rs. {remaining:.2f}")
    else:
        print(f"Over budget by: Rs. {abs(remaining):.2f}")

    print()


def delete_expense(expenses):
    view_expenses(expenses)

    if not expenses:
        return

    try:
        number = int(input("Enter expense number to delete: "))

        if number < 1 or number > len(expenses):
            print("Invalid expense number.")
            return

        removed = expenses.pop(number - 1)
        save_expenses(expenses)
        print(f"{removed['name']} deleted successfully!")

    except ValueError:
        print("Please enter a valid number.")


def main():
    expenses = load_expenses()

    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Category-wise Summary")
        print("4. Set Monthly Budget")
        print("5. View Budget Status")
        print("6. Delete Expense")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            category_summary(expenses)
        elif choice == "4":
            set_monthly_budget()
        elif choice == "5":
            budget_status(expenses)
        elif choice == "6":
            delete_expense(expenses)
        elif choice == "7":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()