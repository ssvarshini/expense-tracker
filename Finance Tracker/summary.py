from datetime import datetime, date
from expense import Expense
import sqlite3
from collections import defaultdict


def summarise_expense(filter_month, filter_year, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    month = f"{filter_month:02}"
    year = str(filter_year)

    #Expenses
    cursor.execute('''
        SELECT amount, category FROM expenses
        WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
    ''', (month, year))
    expenses = cursor.fetchall()

    total_category = defaultdict(float)
    total_spent = 0
    for amount, category in expenses:
        total_category[category] += amount
        total_spent += amount

    # Income
    cursor.execute('''
        SELECT amount FROM income
        WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
    ''', (month, year))
    income_entries = cursor.fetchall()
    total_income = sum(row[0] for row in income_entries)

    # Budget
    cursor.execute('''
        SELECT category, amount FROM budget
        WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
    ''', (month, year))
    budget_rows = cursor.fetchall()
    budget_by_category = {category: amount for category, amount in budget_rows}
    
    conn.close()
    
    savings = total_income - total_spent

    return {
        "total_spent": total_spent,
        "total_income": total_income,
        "savings": savings,
        "total_by_category": total_category,
        "budget_by_category": budget_by_category
    }
