import sqlite3
import llm
import os

def init_db():
    """
    Initiates the database, verifies or creates required directory.
    Establishes connection to database.
    Creates "expenses" table.
    """
        
    os.makedirs('data', exist_ok=True)

    with sqlite3.connect("data/expenses.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS expenses(" \
        "expense_id INTEGER PRIMARY KEY AUTOINCREMENT," \
        "items TEXT NOT NULL," \
        "category TEXT," \
        "amount REAL NOT NULL," \
        "date TEXT," \
        "time TEXT," \
        "description TEXT)")

def save_expense(expense_dict):
    """
    Takes expense dictionary as argument.
    Establishes connection to database.
    Inserts the data into a new row of "expenses" table.
    Confirms the save by showing "lastrowid".
    """


    with sqlite3.connect("data/expenses.db") as conn:
        cursor = conn.cursor()

        print("Saving Expenses!")

        items = " & ".join(expense_dict['Items'])
        category = expense_dict['Category']
        amount = expense_dict['Amount']
        date = (expense_dict['Date & Time'].split())[0]
        time = (expense_dict['Date & Time'].split())[1]
        description = expense_dict['Description']
    
        cursor.execute("INSERT INTO expenses (items, category, amount, date, time, description)" \
        "VALUES (?, ?, ?, ?, ?, ?)", (items, category, amount, date, time, description))

        print(f"Expenses saved with ID no: {cursor.lastrowid}")


def fetch_expenses():
    """
    Establishes a new connection.
    Retrieves all data from "expenses" table.
    Returns a list of all expenses, each item in the list is a sqlite.Row object!  
    If table is empty, it returns an empty list.
    """

    with sqlite3.connect("data/expenses.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        all_expenses = []

        cursor.execute("SELECT * FROM expenses")
        for row in cursor.fetchall():
            all_expenses.append(row)
        
        return all_expenses

if __name__ == "__main__":
    init_db()

    expense_description = input("Enter the expense: ")
    expense_dict = llm.json_to_dict(llm.parse_expense(expense_description))
    print(expense_dict)

    save_expense(expense_dict)

    # using f-string to retrieve data from Row object
    for expense in fetch_expenses():
        print(f'\nID: {expense['expense_id']}\n Items: {expense['items']}\n Category: {expense['category']}\n Amount: {expense['amount']}\n Date: {expense['date']}\n Time: {expense['time']}\n Description: {expense['description']}\n')