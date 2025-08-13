from flask import Flask, render_template, request, redirect, url_for
from expense import Expense
from summary import summarise_expense 
from datetime import datetime, date
import sqlite3

app = Flask(__name__)

DATABASE = "database.db"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():
    categories = ["Food", "Home", "Transport", "Bills", "Travel", "Shopping", "Healthcare", "Miscellaneous"]
    if request.method == "POST":
        name = request.form["name"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        date_str = request.form["date"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (name, amount, category, date)
            VALUES (?, ?, ?, ?)
        ''', (name, amount, category, date_str))
        conn.commit()
        conn.close()
        
        return redirect(url_for("index"))

    return render_template("add_expense.html", categories=categories)

@app.route("/add-income", methods=["GET", "POST"])
def add_income():
    if request.method == "POST":
        amount = float(request.form["amount"])
        date_str = request.form["date"]

        if len(date_str) == 7:
            date_str += "-01"

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO income (amount, date)
            VALUES (?, ?)
        ''', (amount, date_str))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))
    return render_template("add_income.html")

@app.route("/add-budget", methods=["GET", "POST"])
def add_budget():
     categories = ["Overall","Food", "Home", "Transport", "Bills", "Travel", "Shopping", "Healthcare", "Miscellaneous"]
     if request.method == "POST":
        amount = float(request.form["amount"])
        date_str = request.form["date"]
        category = request.form["category"]

        if len(date_str) == 7:
            date_str += "-01"

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO budget (amount, date, category)
            VALUES (?, ?, ?)
        ''', (amount, date_str, category))
        conn.commit()
        conn.close()

        return redirect(url_for("index"))
     return render_template("add_budget.html", categories=categories)

@app.route("/add-summary", methods=["GET", "POST"])
def add_summary():
    if request.method == "POST":
        month = int(request.form["month"])
        year = int(request.form["year"])

        # You'll need to update this function to use the database now
        result = summarise_expense(month, year, DATABASE)
        return render_template("get_summary.html", result=result, month=month, year=year)
    
    return render_template("get_summary.html", result=None)

@app.route("/view-expense", methods=["GET", "POST"])
def view_expense():
    if request.method == "POST":
        month = int(request.form["month"])
        year = int(request.form["year"])

        month_str = str(month).zfill(2)
        year_str = str(year)

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, amount, date
            FROM expenses
            WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
            ORDER BY date DESC
        ''', (month_str, year_str))
        expenses = cursor.fetchall()
        conn.close()

        return render_template("view_expense.html", expenses=expenses, month=month, year=year)

    return render_template("view_expense.html", expenses=None)



if __name__ == "__main__":
    app.run(debug=True)


