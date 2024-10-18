import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sq 

db = sq.connect('tracker_db.db') 
cursor = db.cursor() 


def income_expense_tracking(): # Declaration of the function to display information to the user.
    print('Your incomes and expenses will appear now.')
    dates, total_income, total_expense, total_budget, saving_total, budget_goals, title_goals, end_date, date_goals = [], [], [], [], [], [], [], [], []
    saving_sum = 0.0

# Addition of the data on the tables to lists
    
    cursor.execute('''SELECT * from income''')
    for i in cursor:
        dates.append(i[0])
        total_income.append(float(i[-1]))

    cursor.execute('''SELECT * from expense''')
    for i in cursor:
        total_expense.append(float(i[-1]))

    cursor.execute('''SELECT * from financial_goals''')
    for i in cursor:
        date_goals.append(i[0])
        budget_goals.append(float(i[2]))
        title_goals.append(i[1])
        end_date.append(i[3])
    
# Below, the program updates the status of the financial goal if required and avoid some errors adding elements to each list to be able to plot them.
        
    for i, j in zip(total_income, total_expense):
        total_budget.append(float(i) - float(j))
    for i in total_budget:
        saving_sum = saving_sum + float(i)
        saving_total.append(saving_sum)

    for i, j in zip(budget_goals, saving_total):
        if i >= j:
            cursor.execute('''UPDATE financial_goals SET status = ? WHERE budget = ? ''', ('not completed', i))
    
    if len(budget_goals) != len(end_date):
        len_total = len(dates) - len(budget_goals)
        for i in range(len_total):
            budget_goals.append(None)

    if len(total_income) != len(dates):
        len_total = len(dates) - len(total_income)
        for i in range(len_total):
            total_income.append(0)

    if len(total_expense) != len(dates):
        len_total = len(dates) - len(total_expense)
        for i in range(len_total):
            total_expense.append(0)

# Definition of the graphs that will be display for the user
            
    # First graph
    plt.subplot(2, 3, 1)
    r = np.arange(0, len(dates), 1)
    plt.bar(r, total_expense, width=0.5)
    plt.bar(r + 0.5, total_income, width=0.5)
    plt.title('Monthly incomes and expenses')
    plt.xlabel("Date (MM/YY)")
    plt.xticks(r + 0.5/2, dates, rotation=45, ha='right')
    plt.ylabel("Money ({0})".format('\u00A3'))
    plt.grid()
    plt.legend(['expenses', 'incomes'])

    # Second graph
    plt.subplot(2, 3, 3)
    plt.plot(dates, total_budget)
    plt.title('Monthly budget (budget = incomes - expenses)')
    plt.xlabel("Date (MM/YY)")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Money ({0})".format('\u00A3'))
    plt.grid()

    # Third graph
    plt.subplot(2, 3, 5)
    plt.plot(dates, saving_total)
    plt.plot(end_date, budget_goals, 'o')
    plt.title('Financial goals progress')
    plt.xlabel("Due date (MM/YY)")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Money ({0})".format('\u00A3'))
    plt.grid()
    plt.legend(['actual savings (accumulated \nmonthly budget)', 'projected savings to achieve financial goals'], prop = { "size": 7 })
    plt.show()


