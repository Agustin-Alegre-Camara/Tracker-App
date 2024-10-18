# Import 'project_funcs.py' and 'projects_plots.py' to be able to use their functions in this file.
from tabulate import tabulate
import sqlite3 as sq 
import project_funcs as funcs
import project_plots as plots

# Establish connection with the database and defining the cursor to be able to manipulate the data store on it.
db = sq.connect('tracker_db.db') 
cursor = db.cursor()


while True: # Display the menu options to the user.
    menu = input('''1. View incomes and expenses
2. Add, delete or update an income/expense entry
3. View financial goals
4. Add, delete or update financial goals
5. Add or delete income/expense categories
6. Track budget, savings and financial goals 
7. Exit
\n''')
    
# Conditional statements to evaluate the user's input and dictate the program what to do.
    try:
        if menu == '1':
            print('\nYour incomes and expenses will appear now...\n')
            cursor.execute('''SELECT * from income''')
            print('\nListing incomes by date...\n')
            print(tabulate(cursor.fetchall(), headers=funcs.income_column_names))
            cursor.execute('''SELECT * from expense''')
            print('\nListing expenses by date...\n')
            print(tabulate(cursor.fetchall(), headers=funcs.expense_column_names))
            print('\nReturning to main menu...\n')

        elif menu == '2':
            funcs.income_expense_entry()
            print('\nReturning to main menu...\n')

        elif menu == '3':
            cursor.execute('''SELECT * from financial_goals''')
            print('\nYour financial goals will appear now...')
            print('Listing financial goals by date...\n')
            print(tabulate(cursor.fetchall(), headers=funcs.financial_goal_column_names))
            print('\nReturning to main menu...\n')

        elif menu == '4':
            funcs.financial_goal_entry_removal_update()
            print('\nReturning to main menu...\n')

        elif menu == '5':
            funcs.add_delete_category()
            print('\nReturning to main menu...\n')

        elif menu == '6':
            plots.income_expense_tracking()
            print('\nReturning to main menu...\n')

        elif menu == '7':
            print('\nSee you soon!')
            db.close()
            exit()

        else:
            print('You have introduced a wrong command.')
            print('Returning to main menu...\n')

    except Exception:
            print('You have introduced a wrong command.')
            print('Returning to main menu...\n')





