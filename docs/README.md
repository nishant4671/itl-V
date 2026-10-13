# Personal Expense Tracker (PBL Project)

### Course: Information Technology Laboratory - V
**Domain:** Python Programming, Database Management, Data Analytics, Visualization & Web Frameworks  
**Platform:** Terminal / CLI & Headless REST API (No HTML/CSS/JS frontend)

---

## 📖 Project Overview
The **Personal Expense Tracker** is an academic Project-Based Learning (PBL) application built to cover all 6 units of the **Information Technology Laboratory - V** syllabus in a clean, modular, and beginner-friendly structure. 

The application enables users to log, view, edit, and analyze daily expenses via an interactive terminal menu, stores persistent records in a local SQLite database, performs statistical computations using **NumPy** and **Pandas**, generates publication-quality data visualizations using **Matplotlib** and **Seaborn**, and exposes a minimal **Flask REST API** tested via the `requests` library.

---

## 📁 Project Structure

```text
itl-V-project/
│
├── main.py                  # Unit I & II: Terminal interactive loop, data structures & validation
├── database.py              # Unit III: SQLite3 local database setup and CRUD operations
├── analytics.py             # Unit IV: NumPy statistical metrics & Pandas groupby aggregations
├── visualizer.py            # Unit V: Matplotlib & Seaborn static chart generation (PNG)
├── api.py                   # Unit VI: Minimal Flask REST API (GET & POST /expenses)
├── test_api.py              # Unit VI: Automated test runner using Python 'requests'
├── requirements.txt         # Required third-party libraries (numpy, pandas, matplotlib, seaborn, flask, requests)
│
├── docs/
│   ├── README.md            # Comprehensive project setup and execution manual
│   └── Syllabus_Mapping.md  # Detailed matrix mapping code constructs to syllabus units
│
├── expenses.db              # SQLite3 database file (generated automatically upon first launch)
├── bar_chart.png            # Generated category-wise spending bar chart
└── line_chart.png           # Generated daily expense trend line chart
```

---

## 🛠️ Prerequisites & Installation

### Step 1: Verify Python Installation
Ensure Python 3.10 or higher is installed:
```powershell
python --version
```

### Step 2: Create a Virtual Environment (Recommended)
```powershell
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### Step 3: Install Required Dependencies
Install all required libraries for Units IV, V, and VI using `requirements.txt`:
```powershell
pip install -r requirements.txt
```

---

## 🚀 Step-by-Step Execution Guide

### 1. Launch the Main Terminal Application
Run the interactive CLI menu:
```powershell
python main.py
```
From the interactive menu:
- **[1] Add New Expense:** Input title, positive amount, choose from validated categories, and specify date (or press Enter for today).
- **[2] View All Expenses:** Displays an organized ASCII table of all expenses and the grand total.
- **[3] Update an Expense:** Select any expense ID to edit title, amount, category, or date.
- **[4] Delete an Expense:** Remove an expense with confirmation prompt.
- **[5] View Statistical Analytics:** Displays NumPy metrics (mean, median, standard deviation) and Pandas category breakdowns.
- **[6] Generate Visual Charts:** Generates and saves `bar_chart.png` and `line_chart.png` directly to the project directory without opening blocking windows.
- **[7] Filter High-Value Expenses:** Interactive demonstration of Python List Comprehensions.
- **[8] Exit:** Cleanly closes the program.

---

### 2. Run the Visualizer Directly (Unit V)
You can also generate the charts directly at any time:
```powershell
python visualizer.py
```
This produces:
- `bar_chart.png`: High-resolution Seaborn bar chart displaying spending distribution per category.
- `line_chart.png`: Chronological Matplotlib line plot showing daily expenditure trends.

---

### 3. Run and Test the Flask REST API (Unit VI)

The API verification script `test_api.py` is self-contained. You can test it in either of two ways:

#### Option A: Quick Standalone Verification (Single Command)
Run `test_api.py` directly. If the Flask server is not yet running, it will automatically launch it in a background thread, perform all GET and POST tests, print JSON responses to the terminal, and finish cleanly:
```powershell
python test_api.py
```

#### Option B: Multi-Terminal Workflow
**Terminal 1 (Start Server):**
```powershell
python api.py
```
*Output: Running on http://127.0.0.1:5000*

**Terminal 2 (Execute Client Tests):**
```powershell
python test_api.py
```

---

## 📊 Endpoints Implemented in Flask API (`api.py`)

| Method | Endpoint | Description | Sample Request / Response |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | API Health & Info | Returns JSON object with project description and route map. |
| **GET** | `/expenses` | Retrieve all expenses | Returns JSON array of all expense objects with HTTP 200. |
| **POST** | `/expenses` | Insert a new expense | Accepts JSON body: `{"title": "...", "amount": 100.0, "category": "Food", "date": "2026-10-13"}`. Returns HTTP 201 Created. |

---

## 📚 Syllabus Compliance Summary

| Unit | Focus Area | Code Files |
| :--- | :--- | :--- |
| **Unit I & II** | Basics, Data Types, Control Structures, Error Handling | `main.py` |
| **Unit III** | Relational Database Persistence (SQLite3 CRUD) | `database.py` |
| **Unit IV** | Numerical & Tabular Data Science (NumPy, Pandas) | `analytics.py` |
| **Unit V** | Static Chart Generation (Matplotlib, Seaborn) | `visualizer.py` |
| **Unit VI** | Web Frameworks & Client Testing (Flask, Requests) | `api.py`, `test_api.py` |

For an in-depth code-to-syllabus line mapping, see [`docs/Syllabus_Mapping.md`](Syllabus_Mapping.md).
