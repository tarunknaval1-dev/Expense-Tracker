import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("expenses.json")


def load_expenses():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense(expenses):
    name = input("Enter expense name: ").strip()
    category = input("Enter category: ").strip()

    try:
        amount = float(input("Enter amount: "))
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
        amount = expense["amount"]

        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    print("\n--- Category-wise Spending ---")

    for category, total in categories.items():
        print(f"{category}: Rs. {total:.2f}")

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
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            category_summary(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()