"""
=============================================================================
Course: Information Technology Laboratory - V (PBL Project)
File: analytics.py
Syllabus Coverage: Unit IV (NumPy & Pandas for Data Analysis)
Description:
    Reads expense records from the SQLite database into a Pandas DataFrame.
    Performs numerical statistical calculations using NumPy (mean, median, 
    standard deviation, min, max, total) and aggregations using Pandas 
    (group by category, compute category totals, percentages, and counts).
=============================================================================
"""

import sqlite3
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
from database import DB_NAME, get_connection


def load_expenses_dataframe(db_name: str = DB_NAME) -> pd.DataFrame:
    """
    Reads the SQLite 'expenses' table directly into a Pandas DataFrame.
    
    Parameters:
        db_name (str): The filename/path of the SQLite database.
        
    Returns:
        pd.DataFrame: DataFrame containing all expense columns, or empty DataFrame.
    """
    try:
        # Connect to SQLite
        conn = sqlite3.connect(db_name)
        # Pandas read_sql_query (Unit IV Requirement)
        df = pd.read_sql_query("SELECT id, title, amount, category, date FROM expenses", conn)
        conn.close()
        
        # Ensure correct data types
        if not df.empty:
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        return df
    except sqlite3.Error as error:
        print(f"[Database Error in load_expenses_dataframe]: {error}")
        return pd.DataFrame()


def compute_numpy_statistics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Uses NumPy functions to compute essential descriptive statistics
    on expense amounts.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the 'amount' column.
        
    Returns:
        Dict[str, float]: Dictionary mapping metric names to statistical values.
    """
    if df.empty or 'amount' not in df.columns:
        return {}

    # Extract amount column as a NumPy array (Unit IV: NumPy Array operations)
    amounts = df['amount'].to_numpy()

    # Calculate statistics using NumPy
    stats = {
        "count": float(len(amounts)),
        "total": float(np.sum(amounts)),           # NumPy Sum
        "mean": float(np.mean(amounts)),           # NumPy Mean
        "median": float(np.median(amounts)),       # NumPy Median
        "std_dev": float(np.std(amounts)),         # NumPy Standard Deviation
        "min": float(np.min(amounts)),             # NumPy Minimum
        "max": float(np.max(amounts)),             # NumPy Maximum
    }
    return stats


def compute_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Uses Pandas groupby to aggregate expenses by category.
    Calculates total amount, transaction count, average amount,
    and spending percentage for each category.
    
    Parameters:
        df (pd.DataFrame): DataFrame of expenses.
        
    Returns:
        pd.DataFrame: Aggregated summary table grouped by category.
    """
    if df.empty:
        return pd.DataFrame()

    # Unit IV Requirement: Pandas groupby operation
    category_group = df.groupby('category')['amount'].agg(
        Total_Amount='sum',
        Transaction_Count='count',
        Average_Amount='mean'
    ).reset_index()

    # Calculate percentage share of total spending using Pandas vectorization
    total_spend = df['amount'].sum()
    if total_spend > 0:
        category_group['Percentage'] = (category_group['Total_Amount'] / total_spend) * 100
    else:
        category_group['Percentage'] = 0.0

    # Sort descending by Total_Amount
    category_group = category_group.sort_values(by='Total_Amount', ascending=False)
    return category_group


def print_analytics_report(db_name: str = DB_NAME) -> None:
    """
    Generates and prints a formatted terminal report showcasing
    Unit IV NumPy and Pandas computations.
    
    Parameters:
        db_name (str): The SQLite database file path.
    """
    print("\n" + "=" * 65)
    print("        EXPENSE ANALYTICS REPORT (NumPy & Pandas)")
    print("=" * 65)

    df = load_expenses_dataframe(db_name)

    if df.empty:
        print("[Notice] No expenses found in the database to analyze.")
        print("Please add some expenses first via Menu Option 1.")
        print("=" * 65)
        return

    # 1. Compute & Display NumPy Statistics
    stats = compute_numpy_statistics(df)
    print("\n--- 1. DESCRIPTIVE STATISTICS (Calculated with NumPy) ---")
    print(f"Total Transactions : {int(stats['count'])}")
    print(f"Total Spending     : Rs. {stats['total']:.2f}")
    print(f"Mean (Average)     : Rs. {stats['mean']:.2f}")
    print(f"Median Expense     : Rs. {stats['median']:.2f}")
    print(f"Standard Deviation : Rs. {stats['std_dev']:.2f}")
    print(f"Minimum Expense    : Rs. {stats['min']:.2f}")
    print(f"Maximum Expense    : Rs. {stats['max']:.2f}")

    # 2. Compute & Display Pandas Groupby Summary
    summary = compute_category_summary(df)
    print("\n--- 2. CATEGORY BREAKDOWN (Aggregated with Pandas groupby) ---")
    header = f"{'Category':<15} | {'Count':<6} | {'Total (Rs.)':<12} | {'Avg (Rs.)':<10} | {'Share (%)':<8}"
    print(header)
    print("-" * len(header))
    for _, row in summary.iterrows():
        print(
            f"{row['category']:<15} | "
            f"{int(row['Transaction_Count']):<6} | "
            f"{row['Total_Amount']:>11.2f} | "
            f"{row['Average_Amount']:>9.2f} | "
            f"{row['Percentage']:>7.2f}%"
        )

    # 3. List Comprehension filter: High-value expenses (Unit I & II demonstration)
    high_value_threshold = stats['mean']
    high_expenses = [
        f"[{row['date'].strftime('%Y-%m-%d') if pd.notnull(row['date']) else 'N/A'}] {row['title']}: Rs. {row['amount']:.2f} ({row['category']})"
        for _, row in df.iterrows()
        if row['amount'] > high_value_threshold
    ]

    print(f"\n--- 3. ABOVE-AVERAGE EXPENSES (> Rs. {high_value_threshold:.2f}) ---")
    if high_expenses:
        for item in high_expenses:
            print(f"  * {item}")
    else:
        print("  * None found.")

    print("=" * 65 + "\n")


if __name__ == "__main__":
    print("[Testing analytics.py independently...]")
    print_analytics_report()
