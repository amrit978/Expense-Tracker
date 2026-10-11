"""Expense Tracker - a small Flask + SQLite web app."""
import sqlite3
from datetime import date
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, url_for, flash

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "expenses.db"
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Health", "Entertainment", "Other"]

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-in-production"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DATABASE) as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL CHECK (amount > 0),
                category TEXT NOT NULL,
                spent_on TEXT NOT NULL
            )"""
        )


@app.route("/")
def index():
    db = get_db()
    category = request.args.get("category", "")
    month = request.args.get("month", "")  # format YYYY-MM

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if month:
        query += " AND substr(spent_on, 1, 7) = ?"
        params.append(month)
    query += " ORDER BY spent_on DESC, id DESC"

    expenses = db.execute(query, params).fetchall()
    total = sum(e["amount"] for e in expenses)

    by_category = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]
    biggest = max(by_category.values()) if by_category else 0

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        by_category=sorted(by_category.items(), key=lambda kv: -kv[1]),
        biggest=biggest,
        categories=CATEGORIES,
        selected_category=category,
        selected_month=month,
        today=date.today().isoformat(),
    )


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "Other")
    spent_on = request.form.get("spent_on") or date.today().isoformat()
    try:
        amount = float(request.form.get("amount", ""))
    except ValueError:
        amount = 0

    if not title or amount <= 0 or category not in CATEGORIES:
        flash("Please enter a title and a positive amount.", "error")
        return redirect(url_for("index"))

    db = get_db()
    db.execute(
        "INSERT INTO expenses (title, amount, category, spent_on) VALUES (?, ?, ?, ?)",
        (title, amount, category, spent_on),
    )
    db.commit()
    flash("Expense added.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    db = get_db()
    db.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    db.commit()
    flash("Expense deleted.", "success")
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
