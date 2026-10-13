"""
=============================================================================
Course: Information Technology Laboratory - V (PBL Project)
File: api.py
Syllabus Coverage: Unit VI (Web Frameworks with Flask)
Description:
    A minimal, lightweight RESTful backend API using Flask.
    Exposes two core endpoints:
      1. GET  /expenses : Retrieve all expenses formatted as JSON.
      2. POST /expenses : Add a new expense record via JSON payload.
=============================================================================
"""

from flask import Flask, request, jsonify
from database import init_db, add_expense, get_all_expenses, get_expense_by_id

# Initialize the Flask application
app = Flask(__name__)

# Ensure the database and tables are created upon module import
init_db()


@app.route('/', methods=['GET'])
def index():
    """
    Root API endpoint providing metadata and available routes.
    """
    return jsonify({
        "project": "Personal Expense Tracker API",
        "syllabus_unit": "Unit VI (Web Frameworks with Flask)",
        "status": "online",
        "endpoints": {
            "GET /expenses": "Retrieve all expenses as a JSON array",
            "POST /expenses": "Create a new expense (requires JSON body: title, amount, category, date)"
        }
    }), 200


@app.route('/expenses', methods=['GET'])
def fetch_expenses():
    """
    Unit VI Route 1: GET all expenses as JSON.
    Returns:
        JSON array of all expense dictionaries and HTTP status 200.
    """
    try:
        expenses = get_all_expenses()
        return jsonify(expenses), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve expenses", "details": str(e)}), 500


@app.route('/expenses', methods=['POST'])
def create_expense():
    """
    Unit VI Route 2: POST a new expense.
    Expects JSON body:
        {
            "title": "Textbook",
            "amount": 450.0,
            "category": "Education",
            "date": "2026-10-13"
        }
    Returns:
        JSON response with the new ID and HTTP status 201 (Created).
    """
    data = request.get_json()

    # Validate presence of JSON payload
    if not data:
        return jsonify({"error": "Bad Request", "message": "Request body must be valid JSON."}), 400

    # Required field validation
    required_keys = ["title", "amount", "category", "date"]
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return jsonify({
            "error": "Bad Request",
            "message": f"Missing required fields: {', '.join(missing_keys)}"
        }), 400

    # Type & Value Validation
    try:
        title = str(data["title"]).strip()
        amount = float(data["amount"])
        category = str(data["category"]).strip()
        date_str = str(data["date"]).strip()

        if not title or not category or not date_str:
            return jsonify({"error": "Bad Request", "message": "Fields cannot be empty."}), 400

        if amount <= 0:
            return jsonify({"error": "Bad Request", "message": "Amount must be greater than zero."}), 400

    except (ValueError, TypeError) as val_err:
        return jsonify({"error": "Bad Request", "message": f"Invalid data format: {val_err}"}), 400

    # Insert into SQLite database
    new_id = add_expense(title, amount, category, date_str)
    if new_id > 0:
        created_expense = get_expense_by_id(new_id)
        return jsonify({
            "status": "success",
            "message": "Expense added successfully",
            "expense": created_expense
        }), 201
    else:
        return jsonify({"error": "Database error", "message": "Could not insert expense."}), 500


if __name__ == '__main__':
    print("[Starting Personal Expense Tracker Flask API on http://127.0.0.1:5000 ...]")
    app.run(host='127.0.0.1', port=5000, debug=True)
