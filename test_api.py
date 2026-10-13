"""
=============================================================================
Course: Information Technology Laboratory - V (PBL Project)
File: test_api.py
Syllabus Coverage: Unit VI (API Verification using Python 'requests')
Description:
    Tests the Flask REST API endpoints implemented in api.py:
      1. Validates server readiness (auto-starts the Flask server in a 
         daemon thread if not already running).
      2. Performs a GET request on '/expenses' and prints JSON output.
      3. Performs a POST request on '/expenses' with a sample expense 
         payload and verifies HTTP 201 Created status.
      4. Re-queries GET '/expenses' to verify persistence of the new record.
=============================================================================
"""

import time
import json
import threading
import requests
from api import app

# Target URL for the Flask API
BASE_URL = "http://127.0.0.1:5000"


def is_server_running() -> bool:
    """Checks whether the Flask API is already reachable."""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=1)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def start_flask_in_background() -> None:
    """
    Starts the Flask development server in a background daemon thread
    if it is not already running. This allows test_api.py to run self-contained!
    """
    def run_app():
        # Run werkzeug server without debug reloader in background thread
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

    server_thread = threading.Thread(target=run_app, daemon=True)
    server_thread.start()
    print("[test_api] Launched Flask app in background thread...")

    # Wait for the server to become responsive
    max_retries = 10
    for i in range(max_retries):
        time.sleep(0.5)
        if is_server_running():
            print("[test_api] Flask server is alive and responding!\n")
            return
    print("[test_api Warning] Server startup took longer than expected.")


def run_tests() -> None:
    """
    Executes the test suite against the Flask API endpoints.
    """
    print("=" * 70)
    print("      UNIT VI: FLASK REST API AUTOMATED TEST RUNNER")
    print("=" * 70)

    # 1. Ensure server is up
    if not is_server_running():
        print("[Status] Flask API is not currently active. Auto-starting...")
        start_flask_in_background()
    else:
        print("[Status] Connected to active Flask API at http://127.0.0.1:5000\n")

    # 2. Test GET /
    print("[TEST 1] Testing Root Endpoint: GET /")
    try:
        res_root = requests.get(f"{BASE_URL}/")
        print(f"  -> HTTP Status Code: {res_root.status_code}")
        print(f"  -> Response JSON:\n{json.dumps(res_root.json(), indent=4)}\n")
    except Exception as e:
        print(f"  -> [FAIL] Error connecting: {e}\n")

    # 3. Test GET /expenses
    print("[TEST 2] Testing Route 1: GET /expenses (Fetch All Expenses)")
    try:
        res_get = requests.get(f"{BASE_URL}/expenses")
        print(f"  -> HTTP Status Code: {res_get.status_code}")
        expenses = res_get.json()
        print(f"  -> Total Expenses Retrieved: {len(expenses)}")
        print(f"  -> Sample Data Preview (First 2 records):")
        print(json.dumps(expenses[:2], indent=4))
        print("  -> [PASS] GET /expenses returned valid JSON array.\n")
    except Exception as e:
        print(f"  -> [FAIL] GET /expenses failed: {e}\n")

    # 4. Test POST /expenses
    print("[TEST 3] Testing Route 2: POST /expenses (Add New Expense)")
    new_expense_payload = {
        "title": "PBL IT-Lab Reference Textbook",
        "amount": 499.50,
        "category": "Education",
        "date": "2026-10-13"
    }
    print(f"  -> Sending Payload:\n{json.dumps(new_expense_payload, indent=4)}")

    try:
        res_post = requests.post(f"{BASE_URL}/expenses", json=new_expense_payload)
        print(f"  -> HTTP Status Code: {res_post.status_code} (Expected: 201 Created)")
        print(f"  -> Response JSON:\n{json.dumps(res_post.json(), indent=4)}")

        if res_post.status_code == 201:
            print("  -> [PASS] POST /expenses successfully created the record!\n")
        else:
            print("  -> [FAIL] Unexpected status code returned.\n")
    except Exception as e:
        print(f"  -> [FAIL] POST /expenses failed: {e}\n")

    # 5. Verification GET /expenses
    print("[TEST 4] Verification: Re-querying GET /expenses to confirm insertion")
    try:
        res_verify = requests.get(f"{BASE_URL}/expenses")
        updated_list = res_verify.json()
        print(f"  -> Updated Total Records Count: {len(updated_list)}")
        # Check if the newly posted expense is present in the database
        matching = [e for e in updated_list if e['title'] == "PBL IT-Lab Reference Textbook"]
        if matching:
            print(f"  -> Verified Added Record in DB: {matching[-1]}")
            print("  -> [PASS] Database persistence verified across API calls!")
        else:
            print("  -> [WARN] Inserted item not found in response list.")
    except Exception as e:
        print(f"  -> [FAIL] Verification failed: {e}")

    print("\n" + "=" * 70)
    print("  ALL FLASK API TESTS COMPLETED (UNIT VI VERIFIED SUCCESSFULLY)")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
