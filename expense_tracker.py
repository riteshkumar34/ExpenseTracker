import calendar
from expense import Expense
from datetime import datetime

def main():
    expense_file_path = "expenses.csv"

    while True:
        print("Running Expense Tracker!")

        budget = float(input("Enter your monthly budget: "))

        # Clear file when restarting
        with open(expense_file_path, 'w') as f:
            f.write("")  # Empty file
        
        expense = get_user_expense()  
        save_expense_to_file(expense, expense_file_path)  
        
        summarize_expenses(expense_file_path, budget)  # Pass budget
        
        restart = input("Do you want to restart? (yes/no): ").strip().lower()
        if restart != 'yes':
            break

def get_user_expense():
    print("Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    print(f"You have entered {expense_name}, {expense_amount}")

    expense_categories = ['Food', 'Home', 'Work', 'Fun', 'Misc']

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i+1}. {category_name}")

        value_range = f"[1-{len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if 0 <= selected_index < len(expense_categories):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid category: Please try again!")

def save_expense_to_file(expense, expense_file_path):
    print(f"Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, 'a') as f:  # Append mode
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

def summarize_expenses(expense_file_path, budget):
    print("Summarizing User Expense")
    expenses = []
    
    try:
        with open(expense_file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                expense_name, expense_amount, expense_category = line.strip().split(",")
                line_expense = Expense(name=expense_name, amount=float(expense_amount), category=expense_category)
                expenses.append(line_expense)

        for exp in expenses:
            print(exp)

        # Calculate total spent
        total_spent = sum([x.amount for x in expenses])
        print(f"You have spent ${total_spent:.2f} this month!")

        # Calculate remaining budget
        remaining_budget = budget - total_spent
        print(f"Budget Remaining: ${remaining_budget:.2f} this month")

        now=datetime.now()
        days_in_month=calendar.monthrange(now.year,now.month)[1]
        remaining_days=days_in_month-now.day
        print("Remaining days in the current month:", remaining_days)

        daily_budget=remaining_budget/remaining_days
        print(f"Budget Per Day: ${daily_budget:.2f}")
    
    except FileNotFoundError:
        print("No expenses found! File does not exist.")

if __name__ == "__main__":
    main()
