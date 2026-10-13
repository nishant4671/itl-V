"""
=============================================================================
Course: Information Technology Laboratory - V (PBL Project)
File: main.py
Syllabus Coverage: 
    Unit I & II : Python Basics, Data Structures (Lists, Tuples, Dictionaries,
                  Sets, List Comprehensions), Control Flow & Try-Except Handling.
    Unit III    : SQLite3 CRUD Integration.
    Unit IV     : NumPy & Pandas Analytics Integration.
    Unit V      : Matplotlib & Seaborn Chart Generation Integration.
Description:
    The main interactive CLI application loop for the Personal Expense Tracker.
=============================================================================
"""

import sys
from datetime import datetime
from typing import List, Tuple, Dict, Set

# Import database CRUD functions (Unit III)
import database
# Import analytics engine (Unit IV)
import analytics
# Import visualization generator (Unit V)
import visualizer


# ---------------------------------------------------------------------------
# UNIT I & II DATA STRUCTURES DEMONSTRATION
# ---------------------------------------------------------------------------

# 1. LIST: Predefined ordered collection of expense categories
CATEGORIES_LIST: List[str] = [
    "Food",
    "Transport",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Education",
    "Shopping",
    "Other"
]

# 2. SET: Unique, unordered collection for O(1) category membership validation
VALID_CATEGORIES_SET: Set[str] = set(CATEGORIES_LIST)

# 3. TUPLE: Immutable structure defining menu options (Choice Number, Label)
MENU_OPTIONS_TUPLE: Tuple[Tuple[str, str], ...] = (
    ("1", "Add New Expense (Create)"),
    ("2", "View All Expenses (Read)"),
    ("3", "Update an Expense (Update)"),
    ("4", "Delete an Expense (Delete)"),
    ("5", "View Statistical Analytics (Unit IV: NumPy & Pandas)"),
    ("6", "Generate Visual Charts (Unit V: Matplotlib & Seaborn)"),
    ("7", "Filter High-Value Expenses (List Comprehension Demo)"),
    ("8", "Exit Application"),
)


# ---------------------------------------------------------------------------
# HELPER INPUT & VALIDATION FUNCTIONS (Try-Except Error Handling)
# ---------------------------------------------------------------------------

def get_valid_float(prompt: str) -> float:
    """
    Prompts the user for a floating-point number with Try-Except validation.
    
    Unit I/II: Try-Except block catching ValueError.
    """
    while True:
        try:
            raw_input = input(prompt).strip()
            val = float(raw_input)
            if val <= 0:
                print("  [Error] Amount must be a positive number greater than 0.")
                continue
            return round(val, 2)
        except ValueError:
            print("  [Error] Invalid number. Please enter a valid decimal number (e.g., 250.50).")


def get_valid_date(prompt: str) -> str:
    """
    Prompts the user for a date string in YYYY-MM-DD format with Try-Except validation.
    Defaults to today's date if left blank.
    """
    while True:
        raw_input = input(prompt).strip()
        if not raw_input:
            # Default to current date
            today_str = datetime.today().strftime("%Y-%m-%d")
            print(f"  [Auto] Using today's date: {today_str}")
            return today_str

        try:
            # Validate format with datetime parsing
            parsed_date = datetime.strptime(raw_input, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            print("  [Error] Invalid date format. Please use YYYY-MM-DD (e.g., 2026-10-13).")


def get_valid_category() -> str:
    """
    Displays the list of categories and validates user choice using Set membership.
    """
    print("\n  Available Categories:")
    # Unit I/II: Enumerating through a List
    for idx, cat in enumerate(CATEGORIES_LIST, start=1):
        print(f"    [{idx}] {cat}")

    while True:
        choice = input("  Select category number or type name: ").strip()
        # Option 1: User typed category number
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES_LIST):
            return CATEGORIES_LIST[int(choice) - 1]
        
        # Option 2: User typed category name; validated against SET
        title_cased = choice.title()
        if title_cased in VALID_CATEGORIES_SET:
            return title_cased

        print(f"  [Error] '{choice}' is not a valid category. Please choose from above.")


# ---------------------------------------------------------------------------
# CRUD MENU ACTIONS
# ---------------------------------------------------------------------------

def handle_add_expense() -> None:
    """Creates a new expense record in the SQLite database."""
    print("\n--- ADD NEW EXPENSE ---")
    title = input("  Enter expense title/description: ").strip()
    while not title:
        print("  [Error] Title cannot be empty.")
        title = input("  Enter expense title/description: ").strip()

    amount = get_valid_float("  Enter amount (Rs.): ")
    category = get_valid_category()
    date_str = get_valid_date("  Enter date (YYYY-MM-DD) [Press Enter for today]: ")

    # Unit I/II: Storing input in a Tuple
    expense_record_tuple = (title, amount, category, date_str)

    # Unit III: Inserting tuple unpacked into SQLite
    new_id = database.add_expense(*expense_record_tuple)
    if new_id > 0:
        print(f"\n[Success] Expense #{new_id} ('{title}', Rs. {amount:.2f}) added successfully!")
    else:
        print("\n[Failure] Could not save expense to database.")


def handle_view_expenses() -> None:
    """Reads and displays all expenses formatted in a terminal table."""
    print("\n--- ALL EXPENSES LIST ---")
    # Unit III: Read operation
    expenses: List[Dict] = database.get_all_expenses()

    if not expenses:
        print("  No expenses recorded yet. Use Option 1 to add some.")
        return

    # Print ASCII table
    header = f"{'ID':<5} | {'Date':<10} | {'Category':<15} | {'Title':<28} | {'Amount (Rs.)':>12}"
    print(header)
    print("-" * len(header))
    
    # Unit I/II: Iterating through list of dictionaries
    total_sum = 0.0
    for exp in expenses:
        print(
            f"{exp['id']:<5} | "
            f"{exp['date']:<10} | "
            f"{exp['category']:<15} | "
            f"{exp['title'][:28]:<28} | "
            f"{exp['amount']:>12.2f}"
        )
        total_sum += exp['amount']

    print("-" * len(header))
    print(f"Total Records: {len(expenses)} | Grand Total: Rs. {total_sum:.2f}\n")


def handle_update_expense() -> None:
    """Updates an existing expense in the database."""
    print("\n--- UPDATE EXPENSE ---")
    try:
        exp_id = int(input("  Enter the ID of the expense to update: ").strip())
    except ValueError:
        print("  [Error] ID must be a valid integer.")
        return

    # Unit III: Fetch existing record
    existing = database.get_expense_by_id(exp_id)
    if not existing:
        print(f"  [Error] No expense found with ID #{exp_id}.")
        return

    print(f"  Found Expense: #{existing['id']} - {existing['title']} (Rs. {existing['amount']}) [{existing['category']}] on {existing['date']}")
    print("  (Leave fields blank to retain current values)\n")

    new_title = input(f"  New title [{existing['title']}]: ").strip()
    if not new_title:
        new_title = existing['title']

    amt_raw = input(f"  New amount (Rs.) [{existing['amount']}]: ").strip()
    if amt_raw:
        try:
            new_amount = float(amt_raw)
        except ValueError:
            print("  [Warning] Invalid number; keeping existing amount.")
            new_amount = existing['amount']
    else:
        new_amount = existing['amount']

    change_cat = input(f"  Change category [{existing['category']}]? (y/N): ").strip().lower()
    if change_cat == 'y':
        new_category = get_valid_category()
    else:
        new_category = existing['category']

    new_date = input(f"  New date (YYYY-MM-DD) [{existing['date']}]: ").strip()
    if not new_date:
        new_date = existing['date']

    success = database.update_expense(exp_id, new_title, new_amount, new_category, new_date)
    if success:
        print(f"\n[Success] Expense #{exp_id} updated successfully!")
    else:
        print(f"\n[Failure] Failed to update expense #{exp_id}.")


def handle_delete_expense() -> None:
    """Deletes an expense record from the database."""
    print("\n--- DELETE EXPENSE ---")
    try:
        exp_id = int(input("  Enter the ID of the expense to delete: ").strip())
    except ValueError:
        print("  [Error] ID must be an integer.")
        return

    existing = database.get_expense_by_id(exp_id)
    if not existing:
        print(f"  [Error] No expense found with ID #{exp_id}.")
        return

    confirm = input(f"  Are you sure you want to delete '{existing['title']}' (Rs. {existing['amount']})? (y/N): ").strip().lower()
    if confirm == 'y':
        if database.delete_expense(exp_id):
            print(f"\n[Success] Expense #{exp_id} deleted successfully.")
        else:
            print(f"\n[Failure] Could not delete expense #{exp_id}.")
    else:
        print("  Deletion canceled.")


def handle_list_comprehension_filter() -> None:
    """
    Demonstrates Unit I & II List Comprehensions by filtering expenses 
    above a user-defined threshold and formatting display strings.
    """
    print("\n--- LIST COMPREHENSION FILTER (Unit I & II Demo) ---")
    threshold = get_valid_float("  Enter minimum amount threshold (Rs.): ")

    expenses = database.get_all_expenses()
    if not expenses:
        print("  Database is empty.")
        return

    # List Comprehension 1: Filtering matching expense records
    filtered_expenses = [exp for exp in expenses if exp['amount'] >= threshold]

    # List Comprehension 2: Extracting formatted strings
    formatted_summaries = [
        f"  * [ID {e['id']}] {e['date']} | {e['category']:<12} | {e['title']}: Rs. {e['amount']:.2f}"
        for e in filtered_expenses
    ]

    # List Comprehension 3: Computing sum of filtered values
    filtered_amounts = [e['amount'] for e in filtered_expenses]
    total_filtered = sum(filtered_amounts)

    print(f"\nExpenses matching threshold (>= Rs. {threshold:.2f}): {len(filtered_expenses)} record(s)")
    if formatted_summaries:
        for line in formatted_summaries:
            print(line)
        print(f"Subtotal for filtered expenses: Rs. {total_filtered:.2f}\n")
    else:
        print("  No expenses match this threshold.")


# ---------------------------------------------------------------------------
# MAIN APPLICATION LOOP
# ---------------------------------------------------------------------------

def display_menu() -> None:
    """Prints the terminal banner and numbered menu choices."""
    print("=" * 60)
    print("        PERSONAL EXPENSE TRACKER (PBL PROJECT)        ")
    print("         Information Technology Laboratory - V         ")
    print("=" * 60)
    # Unit I/II: Unpacking Tuples in a loop
    for key, label in MENU_OPTIONS_TUPLE:
        print(f"  [{key}] {label}")
    print("=" * 60)


def main() -> None:
    """Main program entry point with persistent interactive menu loop."""
    # Ensure database exists and is populated
    database.init_db()

    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            handle_add_expense()
        elif choice == "2":
            handle_view_expenses()
        elif choice == "3":
            handle_update_expense()
        elif choice == "4":
            handle_delete_expense()
        elif choice == "5":
            # Unit IV: NumPy & Pandas Analytics
            analytics.print_analytics_report()
        elif choice == "6":
            # Unit V: Matplotlib & Seaborn Chart Generation
            visualizer.generate_all_charts()
        elif choice == "7":
            # Unit I & II: List Comprehensions Feature
            handle_list_comprehension_filter()
        elif choice == "8":
            print("\nThank you for using Personal Expense Tracker. Goodbye!\n")
            sys.exit(0)
        else:
            print("\n[Error] Invalid selection. Please enter a number between 1 and 8.\n")

        # Pause briefly for user readability before re-showing menu
        input("\n[Press Enter to return to main menu...]")


if __name__ == "__main__":
    main()
