
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import date

app = Flask(__name__)

DATABASE = "expenses.db"


# Connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create the database and expenses table
def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Homepage
@app.route("/")
def home():
    return render_template("index.html")


# Get all expenses
@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    conn = get_db_connection()

    expenses = conn.execute("""
        SELECT * FROM expenses
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return jsonify([dict(expense) for expense in expenses])


# Add a new expense
@app.route("/api/expenses", methods=["POST"])
def add_expense():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Please provide expense details."}), 400

    try:
        amount = float(data.get("amount", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Amount must be a valid number."}), 400

    category = str(data.get("category", "")).strip()
    description = str(data.get("description", "")).strip()

    if amount <= 0:
        return jsonify({"error": "Amount must be greater than zero."}), 400

    if not category:
        return jsonify({"error": "Please select a category."}), 400

    if len(category) > 100 or len(description) > 200:
        return jsonify({"error": "Category or description is too long."}), 400

    conn = get_db_connection()

    cursor = conn.execute("""
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (amount, category, description, str(date.today())))

    conn.commit()

    expense_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Expense added successfully!",
        "id": expense_id
    }), 201


# Delete an expense
@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Expense not found."}), 404

    return jsonify({"message": "Expense deleted successfully!"})


# Calculate total expenses
@app.route("/api/summary", methods=["GET"])
def expense_summary():
    conn = get_db_connection()

    result = conn.execute("""
        SELECT
            COALESCE(SUM(amount), 0) AS total,
            COUNT(*) AS transactions
        FROM expenses
    """).fetchone()

    conn.close()

    return jsonify({
        "total": result["total"],
        "transactions": result["transactions"]
    })


# Start the application
if __name__ == "__main__":
    init_db()

    print("Starting ExpenseFlow...")
    app.run(debug=True)
