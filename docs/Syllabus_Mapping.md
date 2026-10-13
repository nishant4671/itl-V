# Syllabus Mapping & Academic Compliance

## Course: Information Technology Laboratory - V (PBL Project)
**Project Title:** Personal Expense Tracker  
**Language & Runtime:** Python 3.10+ (CLI & Backend Only)  
**Architectural Style:** Modular, Beginner-Friendly, Multi-Tier (Persistence, Analytics, Visualization, API)

---

### Comprehensive Unit-by-Unit Syllabus Matrix

| Unit | Syllabus Topic | Specific Requirement | Implementation File | Key Functions / Constructs | Educational Explanation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Unit I & II** | **Python Basics & Core Data Structures** | Terminal Loop & Interactive Menu | `main.py` | `main()`, `display_menu()` | Infinite `while True` loop presenting numbered choices 1 through 8, driving user interaction without GUI dependencies. |
| **Unit I & II** | **Data Structures: Lists** | Ordered dynamic sequences | `main.py` | `CATEGORIES_LIST` (Line 36), `expenses` list | List of predefined categories used for indexing, iteration, and selection. |
| **Unit I & II** | **Data Structures: Tuples** | Immutable fixed structures & unpacking | `main.py`, `database.py` | `MENU_OPTIONS_TUPLE`, `expense_record_tuple` | Menu items defined as immutable `(code, label)` pairs. Parameter passing uses tuple packing/unpacking `*expense_record_tuple`. |
| **Unit I & II** | **Data Structures: Dictionaries** | Key-Value mappings | `database.py`, `api.py` | `get_all_expenses()` | Database cursor rows converted to structured Python dictionaries `{"id": ..., "title": ..., "amount": ..., "category": ..., "date": ...}`. |
| **Unit I & II** | **Data Structures: Sets** | Unique collections & fast lookup | `main.py` | `VALID_CATEGORIES_SET` | Category validation transformed from list to set for $O(1)$ constant-time membership testing (`title_cased in VALID_CATEGORIES_SET`). |
| **Unit I & II** | **List Comprehensions** | Compact Pythonic transformation & filtering | `main.py`, `analytics.py` | `handle_list_comprehension_filter()`, `print_analytics_report()` | Concise one-line filtering: `[exp for exp in expenses if exp['amount'] >= threshold]` and string formatting `[f"..." for row in ...]`. |
| **Unit I & II** | **Exception Handling** | Robust defensive programming | `main.py`, `database.py`, `api.py` | `get_valid_float()`, `get_valid_date()`, `try...except` | Validates user input by catching `ValueError` during float conversion and date parsing, preventing application crashes. |
| **Unit III** | **Databases (SQLite3)** | Local DB storage & schema | `database.py` | `init_db()`, `get_connection()` | Initializes `expenses.db` with an auto-incrementing schema and seeds starter records on first launch. |
| **Unit III** | **Database CRUD: Create** | Insert new records | `database.py` | `add_expense()` | Parameterized SQL query: `INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)`. Protects against SQL injection. |
| **Unit III** | **Database CRUD: Read** | Query all and by ID | `database.py` | `get_all_expenses()`, `get_expense_by_id()` | `SELECT` queries returning rows ordered chronologically and fetching single records by primary key. |
| **Unit III** | **Database CRUD: Update** | Modify existing records | `database.py` | `update_expense()` | Parameterized `UPDATE expenses SET ... WHERE id = ?`. Validates number of rows affected. |
| **Unit III** | **Database CRUD: Delete** | Remove records | `database.py` | `delete_expense()` | Parameterized `DELETE FROM expenses WHERE id = ?`. Confirms deletion status. |
| **Unit IV** | **NumPy & Pandas** | Read SQL data into DataFrame | `analytics.py` | `load_expenses_dataframe()` | Reads records directly from SQLite into a Pandas DataFrame using `pd.read_sql_query()`. |
| **Unit IV** | **NumPy & Pandas** | Descriptive numerical statistics | `analytics.py` | `compute_numpy_statistics()` | Applies `np.mean()`, `np.median()`, `np.std()`, `np.sum()`, `np.min()`, and `np.max()` on the amounts array. |
| **Unit IV** | **NumPy & Pandas** | Aggregation & Grouping | `analytics.py` | `compute_category_summary()` | Performs `df.groupby('category')['amount'].agg(...)` to calculate group totals, frequencies, averages, and percentage share. |
| **Unit V** | **Matplotlib & Seaborn** | Categorical Bar Chart | `visualizer.py` | `generate_bar_chart()` | Generates a styled Seaborn `sns.barplot` of total expenses per category and saves it as `bar_chart.png`. |
| **Unit V** | **Matplotlib & Seaborn** | Time-series Line Chart | `visualizer.py` | `generate_line_chart()` | Generates a chronological spending trend using `ax.plot()` and saves it as `line_chart.png`. |
| **Unit V** | **Matplotlib & Seaborn** | Headless File Generation | `visualizer.py` | `matplotlib.use('Agg')` | Strictly headless backend configuration to prevent opening interactive GUI windows while saving crisp 300 DPI images. |
| **Unit VI** | **Web Frameworks (Flask)** | REST API Implementation | `api.py` | `GET /expenses`, `POST /expenses` | Minimal Flask backend exposing JSON endpoints for fetching and recording expenses. |
| **Unit VI** | **Web Frameworks (Flask)** | API Client Verification | `test_api.py` | `run_tests()` | Uses Python's `requests` library to auto-launch the server in a daemon thread, test GET/POST endpoints, and print formatted JSON. |

---

### Verification Checklist for Evaluator / Viva
- [x] **Terminal-only Interface:** Zero HTML, CSS, or JavaScript code.
- [x] **Relational Persistence:** SQLite3 database file `expenses.db` created dynamically.
- [x] **Data Science Stack:** NumPy array computations and Pandas DataFrame groupby aggregations.
- [x] **Visualization Stack:** Static charts saved as PNG image files without GUI popup blockers.
- [x] **Backend Framework:** RESTful Flask endpoints verified with the `requests` library.
