import sqlite3
from pathlib import Path


DB_PATH = Path("data/expenses.db")


def get_connection():
    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return sqlite3.connect(DB_PATH)


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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

    cursor.execute(
        "PRAGMA table_info(expenses)"
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "expense_date" not in columns:

        cursor.execute("""
            ALTER TABLE expenses
            ADD COLUMN expense_date TEXT
        """)

    if "source" not in columns:

        cursor.execute("""
            ALTER TABLE expenses
            ADD COLUMN source TEXT
        """)

    cursor.execute("""
        UPDATE expenses
        SET source = 'Unknown'
        WHERE source IS NULL
    """)

    cursor.execute("""
        UPDATE expenses
        SET expense_date = DATE('now')
        WHERE expense_date IS NULL
    """)

    conn.commit()
    conn.close()


def add_expense(
    merchant,
    amount,
    category,
    raw_text,
    expense_date,
    source
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (
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


def get_expenses():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            merchant,
            amount,
            category,
            expense_date,
            source
        FROM expenses
        ORDER BY expense_date DESC, id DESC
    """)

    expenses = cursor.fetchall()

    conn.close()

    return expenses


def delete_expense(expense_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE id = ?
        """,
        (expense_id,)
    )

    conn.commit()
    conn.close()