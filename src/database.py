import sqlite3
import os

DB_PATH = "data/expenses.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_database():
    try:
        conn = get_connection()

        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                merchant TEXT,
                amount REAL,
                category TEXT,
                raw_text TEXT,
                expense_date TEXT,
                source TEXT
            )
        """)

        columns = [
            row[1]
            for row in conn.execute(
                "PRAGMA table_info(expenses)"
            ).fetchall()
        ]

        if "expense_date" not in columns:
            conn.execute(
                "ALTER TABLE expenses ADD COLUMN expense_date TEXT"
            )

        if "source" not in columns:
            conn.execute(
                "ALTER TABLE expenses ADD COLUMN source TEXT"
            )

        conn.execute("""
            UPDATE expenses
            SET expense_date = DATE('now')
            WHERE expense_date IS NULL
        """)

        conn.execute("""
            UPDATE expenses
            SET source = 'Unknown'
            WHERE source IS NULL
        """)

        conn.commit()
        conn.close()

        return True

    except sqlite3.Error:
        return False


def add_expense(
    merchant,
    amount,
    category,
    raw_text,
    expense_date,
    source
):
    try:
        conn = get_connection()

        conn.execute("""
            INSERT INTO expenses
            (
                merchant,
                amount,
                category,
                raw_text,
                expense_date,
                source
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            merchant,
            amount,
            category,
            raw_text,
            expense_date,
            source
        ))

        conn.commit()
        conn.close()

        return True

    except sqlite3.Error:
        return False


def get_expenses():
    try:
        conn = get_connection()

        cursor = conn.execute("""
            SELECT
                id,
                merchant,
                amount,
                category,
                expense_date,
                source
            FROM expenses
            ORDER BY id DESC
        """)

        expenses = cursor.fetchall()
        conn.close()

        return expenses

    except sqlite3.Error:
        return []


def delete_expense(expense_id):
    try:
        conn = get_connection()

        conn.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

        conn.commit()
        conn.close()

        return True

    except sqlite3.Error:
        return False