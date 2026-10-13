"""
=============================================================================
Course: Information Technology Laboratory - V (PBL Project)
File: database.py
Syllabus Coverage: Unit III (Databases with SQLite3)
Description:
    Handles all SQLite3 database connections and CRUD operations (Create, 
    Read, Update, Delete) for the Personal Expense Tracker application.
    All SQL queries use parameter substitution (?) to prevent SQL injection.
=============================================================================
"""

import sqlite3
from typing import List, Tuple, Optional, Dict, Any

# Name of the local SQLite database file
DB_NAME = "expenses.db"


def get_connection(db_name: str = DB_NAME) -> sqlite3.Connection:
    """
    Establishes and returns a connection to the SQLite database.
    
    Parameters:
        db_name (str): The filename/path of the SQLite database.
        
    Returns:
        sqlite3.Connection: SQLite database connection object.
    """
    conn = sqlite3.connect(db_name)
    # Enable foreign keys and row access by column names if needed
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_name: str = DB_NAME, seed_sample_data: bool = True) -> None:
    """
    Initializes the database schema and optionally seeds initial sample data.
    Creates the 'expenses' table if it does not already exist.
    
    Parameters:
        db_name (str): Database file path.
        seed_sample_data (bool): Whether to insert realistic starter records
                                 if the table is currently empty.
    """
    try:
        conn = get_connection(db_name)
        cursor = conn.cursor()

        # CREATE TABLE statement (Unit III: Schema Definition)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
            """
        )
        conn.commit()

        # Check if the table is empty; if so, populate with initial sample expenses
        # so analytics and visualization charts work immediately upon first launch.
        if seed_sample_data:
            cursor.execute("SELECT COUNT(*) FROM expenses")
            count = cursor.fetchone()[0]
            if count == 0:
                # Tuples of sample data (Demonstrating Tuples & Lists)
                sample_expenses = [
                    ("Grocery Shopping", 1250.50, "Food", "2026-10-01"),
                    ("Metro Smart Card Recharge", 500.00, "Transport", "2026-10-02"),
                    ("Broadband Internet Bill", 899.00, "Utilities", "2026-10-03"),
                    ("Python Data Science Book", 650.00, "Education", "2026-10-05"),
                    ("Weekend Movie Ticket", 350.00, "Entertainment", "2026-10-07"),
                    ("Pharmacy & Vitamins", 420.00, "Healthcare", "2026-10-08"),
                    ("Dinner with Friends", 1100.00, "Food", "2026-10-09"),
                    ("Cab to College Lab", 220.00, "Transport", "2026-10-10"),
                    ("Electricity Bill", 1450.00, "Utilities", "2026-10-11"),
                    ("Online Course Certification", 1200.00, "Education", "2026-10-12"),
                ]
                cursor.executemany(
                    """
                    INSERT INTO expenses (title, amount, category, date)
                    VALUES (?, ?, ?, ?)
                    """,
                    sample_expenses,
                )
                conn.commit()
        conn.close()
    except sqlite3.Error as error:
        print(f"[Database Error in init_db]: {error}")


# =============================================================================
# CRUD OPERATION 1: CREATE (Insert a new expense)
# =============================================================================
def add_expense(
    title: str, amount: float, category: str, date_str: str, db_name: str = DB_NAME
) -> int:
    """
    Inserts a new expense record into the SQLite database.
    
    Parameters:
        title (str): Brief description of the expense.
        amount (float): Monetary value of the expense.
        category (str): Classification category (e.g., Food, Travel).
        date_str (str): Date in 'YYYY-MM-DD' format.
        db_name (str): Database file path.
        
    Returns:
        int: The primary key ID of the newly inserted expense.
    """
    try:
        conn = get_connection(db_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO expenses (title, amount, category, date)
            VALUES (?, ?, ?, ?)
            """,
            (title, amount, category, date_str),
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id
    except sqlite3.Error as error:
        print(f"[Database Error in add_expense]: {error}")
        return -1


# =============================================================================
# CRUD OPERATION 2: READ (Fetch all expenses or a single expense by ID)
# =============================================================================
def get_all_expenses(db_name: str = DB_NAME) -> List[Dict[str, Any]]:
    """
    Fetches all expense records from the database, ordered by date descending.
    
    Parameters:
        db_name (str): Database file path.
        
    Returns:
        List[Dict[str, Any]]: List of dictionary representations of all expenses.
    """
    expenses = []
    try:
        conn = get_connection(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, amount, category, date FROM expenses ORDER BY date ASC, id ASC")
        rows = cursor.fetchall()
        
        # Unit I/II: Converting SQLite Row tuples into Python Dictionaries
        for row in rows:
            expenses.append({
                "id": row["id"],
                "title": row["title"],
                "amount": float(row["amount"]),
                "category": row["category"],
                "date": row["date"],
            })
        conn.close()
    except sqlite3.Error as error:
        print(f"[Database Error in get_all_expenses]: {error}")
    return expenses


def get_expense_by_id(expense_id: int, db_name: str = DB_NAME) -> Optional[Dict[str, Any]]:
    """
    Fetches a single expense record by its unique ID.
    
    Parameters:
        expense_id (int): Primary key ID of the expense.
        db_name (str): Database file path.
        
    Returns:
        Optional[Dict[str, Any]]: Dictionary of expense data if found, else None.
    """
    try:
        conn = get_connection(db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, amount, category, date FROM expenses WHERE id = ?",
            (expense_id,),
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "id": row["id"],
                "title": row["title"],
                "amount": float(row["amount"]),
                "category": row["category"],
                "date": row["date"],
            }
        return None
    except sqlite3.Error as error:
        print(f"[Database Error in get_expense_by_id]: {error}")
        return None


# =============================================================================
# CRUD OPERATION 3: UPDATE (Modify an existing expense)
# =============================================================================
def update_expense(
    expense_id: int,
    title: str,
    amount: float,
    category: str,
    date_str: str,
    db_name: str = DB_NAME,
) -> bool:
    """
    Updates an existing expense in the database matching the given ID.
    
    Parameters:
        expense_id (int): Primary key ID of the record to update.
        title (str): New title.
        amount (float): New amount.
        category (str): New category.
        date_str (str): New date ('YYYY-MM-DD').
        db_name (str): Database file path.
        
    Returns:
        bool: True if a row was updated, False otherwise.
    """
    try:
        conn = get_connection(db_name)
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE expenses
            SET title = ?, amount = ?, category = ?, date = ?
            WHERE id = ?
            """,
            (title, amount, category, date_str, expense_id),
        )
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0
    except sqlite3.Error as error:
        print(f"[Database Error in update_expense]: {error}")
        return False


# =============================================================================
# CRUD OPERATION 4: DELETE (Remove an existing expense)
# =============================================================================
def delete_expense(expense_id: int, db_name: str = DB_NAME) -> bool:
    """
    Deletes an expense from the database matching the given ID.
    
    Parameters:
        expense_id (int): Primary key ID of the record to delete.
        db_name (str): Database file path.
        
    Returns:
        bool: True if the record was deleted, False otherwise.
    """
    try:
        conn = get_connection(db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0
    except sqlite3.Error as error:
        print(f"[Database Error in delete_expense]: {error}")
        return False


# Module self-test (Unit test for standalone execution)
if __name__ == "__main__":
    print("[Testing database.py independently...]")
    init_db()
    all_records = get_all_expenses()
    print(f"Total expenses loaded: {len(all_records)}")
    if all_records:
        print("First record preview:", all_records[0])
    print("[Database test completed successfully!]")
