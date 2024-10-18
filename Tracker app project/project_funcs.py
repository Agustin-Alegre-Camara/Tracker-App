from tabulate import tabulate
import datetime as dt
import sqlite3 as sq 

db = sq.connect('tracker_db.db') 
cursor = db.cursor()

# Create lists and store the column's names of each of the database's tables.

income_column_names, expense_column_names, financial_goal_column_names = [], [], []

data=cursor.execute('''SELECT * FROM income''') 
for column in data.description: 
    income_column_names.append(column[0])

data2=cursor.execute('''SELECT * FROM expense''') 
for column in data2.description: 
    expense_column_names.append(column[0])

data3=cursor.execute('''SELECT * FROM financial_goals''') 
for column in data3.description: 
    financial_goal_column_names.append(column[0])

time = dt.datetime.now() # The program will use the current date the user is connecting to the database to save the new entries.
time = time.strftime('%m/%y')

# Development of the functions for the app.

def add_delete_category(): # Function to allow user to add or delete categories from the tables.
    user_response = input('Would you like to add or delete a category? (A/D): ').upper()

    if user_response == 'A':                                                                                    # In this block, the user is requested to input a
        category_type = input('Would you like to add an income or expense category? (I/E): ')                   # new name for an income or expense categories
        if category_type == 'I':                                                                                # and added to the correspondent table.
            new_category = input('Please introduce the new income category: ').lower().replace(' ', '_')
            cursor.execute('''ALTER TABLE income ADD COLUMN {0}'''.format(new_category))
            db.commit()
            print('Category added succesfully.')
        elif category_type == 'E':
            new_category = input('Please introduce the new expense category: ').lower().replace(' ', '_')
            cursor.execute('''ALTER TABLE expense ADD COLUMN {0}'''.format(new_category))
            db.commit()
            print('Category added succesfully.')
        else:
            print('You have introduced a wrong command.')

    elif user_response == 'D':                                                                                  # In this block, the current categories are
        category_type = input('Would you like to delete an income or expense category? (I/E): ').upper()        # display for the user to input the one to be 
        if category_type == 'I':                                                                                # deleted from its correspondent table.
            cursor.execute('''SELECT * FROM income''')
            print('Listing incomes by date...')
            print(tabulate(cursor.fetchall(), headers=income_column_names))
            new_category = input('Please introduce the income category to be deleted: ').lower().replace(' ', '_')
            cursor.execute('''ALTER TABLE income DROP COLUMN {0}'''.format(new_category))
            db.commit()
            print('Category deleted succesfully.')
        elif category_type == 'E':
            cursor.execute('''SELECT * FROM expense''')
            print('Listing expenses by date...')
            print(tabulate(cursor.fetchall(), headers=expense_column_names))
            new_category = input('Please introduce the expense category to be deleted: ').lower().replace(' ', '_')
            cursor.execute('''ALTER TABLE expense DROP COLUMN {0}'''.format(new_category))
            db.commit()
            print('Category deleted succesfully.')
        else:
            print('You have introduced a wrong command.')

    else:
        print('You have introduced a wrong command.')


def income_expense_entry(): # Function to allow user to add, delete or update an entry into the tables 'income' and 'expense'.
    user_response = input('Would you like to add, remove or update an entry? (A/R/U): ').upper()

    if user_response == 'A':                                                                                    # In the first block, the user is requested to 
        user_choice = input('Would you like to make an income or expense entry? (I/E): ').upper()               # introduce the data for each category. Then, it
                                                                                                                # is added to the table with the current date as the
        if user_choice == 'I':                                                                                  # date of the entry.
            income_entry = []                                                                                   
            print('Please introduce the amount for the following income categories\n')
            monthly_income = 0.0
            for i in range(len(income_column_names[1:-1])):
                income = input('{0}: '.format(income_column_names[1:-1][i]))
                income_entry.append(income)
                income_entry[i] = float(income_entry[i])
                monthly_income = monthly_income + income_entry[i]
            income_entry.insert(0, time)
            income_entry.append(monthly_income)
            cursor.execute('''INSERT INTO income VALUES(?, ?, ?, ?)''', income_entry)
            db.commit()
            print('Entry added succesfully!')
        elif user_choice == 'E':
            expense_entry = []
            print('Please introduce the amount for the following expense categories\n')
            monthly_expense = 0.0
            for i in range(len(expense_column_names[1:-1])):
                expense = input('{0}: '.format(expense_column_names[1:-1][i]))
                expense_entry.append(expense)
                expense_entry[i] = float(expense_entry[i])
                monthly_expense = monthly_expense + expense_entry[i]
            expense_entry.insert(0, time)
            expense_entry.append(monthly_expense)
            cursor.execute('''INSERT INTO expense VALUES(?, ?, ?, ?, ?, ?, ?)''', expense_entry)
            db.commit()
            print('Entry added succesfully!')
        else:
            print('You have introduced a wrong command.')

    elif user_response == 'R':                                                                                  # In the second block, the existing entries will be 
        user_choice = input('Would you like to delete an income or expense category? (I/E): ').upper()          # displayed for the user. They will introduce
                                                                                                                # the date of the entry that needs to be deleted
        if user_choice == 'I':                                                                                  # and the program removes it from the table.
            cursor.execute('''SELECT * FROM income''')                                                          
            print('Listing incomes by date...')
            print(tabulate(cursor.fetchall(), headers=income_column_names))
            income_date = input('Please introduce the income date to be deleted: ')
            cursor.execute('''DELETE FROM income WHERE date = ?''', (income_date, ))
            db.commit()
            print('Entry deleted succesfully.')
        
        elif user_choice == 'E':
            cursor.execute('''SELECT * FROM expense''')
            print('Listing expenses by date...')
            print(tabulate(cursor.fetchall(), headers=expense_column_names))
            expense_date = input('Please introduce the expense date to be deleted: ')
            cursor.execute('''DELETE FROM expense WHERE date = ?''', (expense_date, ))
            db.commit()
            print('Entry deleted succesfully.')
        
        else:
            print('You have introduced a wrong command.')

    elif user_response == 'U':                                                                                  # In the third block, the entries are displayed
        user_choice = input('Would you like to update an income or expense entry? (I/E): ').upper()             # for the user, who introduces the date of the entry
                                                                                                                # to be updated. After that, they are asked to
        if user_choice == 'I':                                                                                  # introduce new data for some of the categories
            cursor.execute('''SELECT * FROM income''')                                                          # and the program updates the entry with the new data.
            print('Listing incomes by date...')                                                                 
            print(tabulate(cursor.fetchall(), headers=income_column_names))
            new_income_entry = []
            user_date = input('Please introduce the date (MM/YY) of the entry to be updated: ')
            print('Please introduce the amount for the following income categories\n')
            new_monthly_income = 0.0
            for i in range(len(income_column_names[1:-1])):
                new_income = input('{0}: '.format(income_column_names[1:-1][i]))
                new_income_entry.append(new_income)
                new_income_entry[i] = float(new_income_entry[i])
                new_monthly_income = new_monthly_income + new_income_entry[i]
                cursor.execute('''UPDATE income SET {0} = ? WHERE date = ? '''.format(income_column_names[1:-1][i]), (new_income_entry[i], user_date))
                db.commit()
            new_income_entry.append(new_monthly_income)
            cursor.execute('''UPDATE income SET {0} = ? WHERE date = ? '''.format(income_column_names[-1]), (new_monthly_income, user_date))
            db.commit()
            print('Entry updated succesfully!')
        
        elif user_choice == 'E':
            cursor.execute('''SELECT * FROM expense''')
            print('Listing expenses by date...')
            print(tabulate(cursor.fetchall(), headers=expense_column_names))
            new_expense_entry = []
            monthly_expense = 0.0
            user_date = input('Please introduce the date (MM/YY) of the entry to be updated: ')
            print('Please introduce the amount for the following expense categories\n')
            for i in range(len(expense_column_names[1:-1])):
                new_expense = input('{0}: '.format(expense_column_names[1:-1][i]))
                new_expense_entry.append(new_expense)
                new_expense_entry[i] = float(new_expense_entry[i])
                monthly_expense = monthly_expense + new_expense_entry[i]
                cursor.execute('''UPDATE expense SET {0} = ? WHERE date = ? '''.format(expense_column_names[1:-1][i]), (new_expense_entry[i], user_date))
                db.commit()
            new_expense_entry.append(monthly_expense)
            cursor.execute('''UPDATE expense SET {0} = ? WHERE date = ? '''.format(expense_column_names[-1]), (monthly_expense, user_date))
            db.commit()
            print('Entry updated succesfully!')
        
        else:
            print('You have introduced a wrong command.')

    else:
        print('You have introduced a wrong command.')


def financial_goal_entry_removal_update(): # Function to allow the user to add, delete or update financial goals.
    user_response = input('Would you like to add, remove or update a financial goal? (A/R/U): ').upper()

    if user_response == 'A':                                                                                    # In the first block, the user is requested to 
        financial_goal_entry = []                                                                               # introduce the data for the financial goals
        print('Please introduce the data for the following categories\n')                                       # categories, being the status 'Not completed' and
        for i in range(len(financial_goal_column_names[1:-1])):                                                 # the date as the current date. After all the data
            financial_goal = input('{0}: '.format(financial_goal_column_names[1:-1][i])).lower()                # is introduced, the program adds the new entry to 
            financial_goal_entry.append(financial_goal)                                                         # the table.
            if income_column_names[i] == 'budget':
                financial_goal_entry[i] = float(financial_goal_entry[i])
        financial_goal_entry.insert(0, time)
        financial_goal_entry.append('Not completed')
        cursor.execute('''INSERT INTO financial_goals VALUES(?, ?, ?, ?, ?)''', financial_goal_entry)
        db.commit()

    elif user_response == 'R':                                                                                  # In the second block, the user is requested to 
        cursor.execute('''SELECT * FROM financial_goals''')                                                     # introduce the title of the entry to be deleted.
        print('Listing financial goals by date...')
        print(tabulate(cursor.fetchall(), headers=financial_goal_column_names))
        user_title = input("Please introduce the financial goal's title to be deleted: ").lower()
        cursor.execute('''DELETE FROM financial_goals WHERE title = ?''', (user_title, ))
        db.commit()
        print('Financial goal deleted succesfully.')

    elif user_response == 'U':                                                                                 # In the third block, the user is requested to 
        cursor.execute('''SELECT * FROM financial_goals''')                                                    # input the title of the entry to be updated.
        print('Listing financial goals by date...')                                                            # After that, they will input the new data requested
        print(tabulate(cursor.fetchall(), headers=financial_goal_column_names))                                # by the program and it will update the entry with the
        user_title = input("Please introduce the financial goal's title to be updated: ")                      # data given.
        financial_goal_entry = []
        for i in range(len(financial_goal_column_names[2:])):
            financial_goal = input('{0}: '.format(financial_goal_column_names[2:][i]))
            financial_goal_entry.append(financial_goal)
            if income_column_names[i] == 'budget':
                financial_goal_entry[i] = float(financial_goal_entry[i])
            cursor.execute('''UPDATE financial_goals SET {0} = ? WHERE title = ? '''.format(financial_goal_column_names[2:][i]), (financial_goal_entry[i], user_title))
            db.commit()
        print('Financial goal updated succesfully.')

    else:
        print('You have introduced a wrong command.')

