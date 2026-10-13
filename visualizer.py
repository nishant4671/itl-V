"""
=============================================================================
Course: Information Technology Laboratory - V (PBL Project)
File: visualizer.py
Syllabus Coverage: Unit V (Matplotlib & Seaborn for Data Visualization)
Description:
    Generates static graphical charts using Matplotlib and Seaborn based on
    stored expense data:
      1. 'bar_chart.png'  : Bar chart of total spending by category.
      2. 'line_chart.png' : Line chart tracking expense amounts over time.
    Note: As per project requirements, charts are saved directly to disk 
          and are NOT displayed interactively (no blocking GUI windows).
=============================================================================
"""

import os
# Configure Matplotlib to use the headless 'Agg' backend
# This ensures figures can be saved on servers/terminals without a GUI window.
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from analytics import load_expenses_dataframe
from database import DB_NAME


def generate_bar_chart(
    db_name: str = DB_NAME, 
    output_filename: str = "bar_chart.png"
) -> bool:
    """
    Generates a bar chart showing total expenses per category using Seaborn 
    and Matplotlib, then saves it as an image file.
    
    Parameters:
        db_name (str): The SQLite database filename.
        output_filename (str): Name of the file to save (bar_chart.png).
        
    Returns:
        bool: True if chart was successfully generated and saved, False otherwise.
    """
    df = load_expenses_dataframe(db_name)
    if df.empty:
        print("[Visualizer] No data available to generate bar chart.")
        return False

    # Aggregate total spending per category using Pandas
    category_totals = (
        df.groupby('category')['amount']
        .sum()
        .reset_index()
        .sort_values(by='amount', ascending=False)
    )

    # Set Seaborn theme and figure size
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(9, 5))

    # Unit V: Generate bar chart using Seaborn
    palette = sns.color_palette("mako", n_colors=len(category_totals))
    barplot = sns.barplot(
        data=category_totals,
        x='category',
        y='amount',
        hue='category',
        palette=palette,
        legend=False,
        ax=ax
    )

    # Add numeric labels above each bar for clarity
    for bar in barplot.patches:
        height = bar.get_height()
        ax.annotate(
            f'Rs. {height:.1f}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha='center',
            va='bottom',
            fontsize=9,
            fontweight='bold'
        )

    # Chart formatting using Matplotlib
    ax.set_title("Total Expenses by Category", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Expense Category", fontsize=11, labelpad=10)
    ax.set_ylabel("Total Amount (Rs.)", fontsize=11, labelpad=10)
    plt.xticks(rotation=20, ha='right')

    # Save figure directly to disk (Unit V Requirement: Save without displaying)
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.close(fig)  # Release memory resources

    print(f"[Visualizer Success] Bar chart saved to: {output_filename}")
    return True


def generate_line_chart(
    db_name: str = DB_NAME, 
    output_filename: str = "line_chart.png"
) -> bool:
    """
    Generates a line chart showing daily spending trends over time using 
    Matplotlib and Seaborn, then saves it as an image file.
    
    Parameters:
        db_name (str): The SQLite database filename.
        output_filename (str): Name of the file to save (line_chart.png).
        
    Returns:
        bool: True if chart was successfully generated and saved, False otherwise.
    """
    df = load_expenses_dataframe(db_name)
    if df.empty:
        print("[Visualizer] No data available to generate line chart.")
        return False

    # Ensure date sorting and group by date for daily spending trend
    daily_trend = (
        df.groupby(df['date'].dt.strftime('%Y-%m-%d'))['amount']
        .sum()
        .reset_index()
    )
    daily_trend.rename(columns={'date': 'Date_Str', 'amount': 'Daily_Total'}, inplace=True)
    daily_trend.sort_values(by='Date_Str', inplace=True)

    # Set theme and figure size
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 5))

    # Unit V: Generate line chart using Matplotlib & Seaborn
    ax.plot(
        daily_trend['Date_Str'],
        daily_trend['Daily_Total'],
        color='#1f77b4',
        marker='o',
        linewidth=2.5,
        markersize=6,
        label="Daily Spending"
    )

    # Highlight data points with values
    for x, y in zip(daily_trend['Date_Str'], daily_trend['Daily_Total']):
        ax.annotate(
            f'Rs. {y:.0f}',
            xy=(x, y),
            xytext=(0, 6),
            textcoords="offset points",
            ha='center',
            fontsize=8
        )

    # Chart formatting using Matplotlib
    ax.set_title("Expense Trend Over Time", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Date (YYYY-MM-DD)", fontsize=11, labelpad=10)
    ax.set_ylabel("Total Daily Spending (Rs.)", fontsize=11, labelpad=10)
    plt.xticks(rotation=30, ha='right')
    ax.legend(loc="upper right")

    # Save figure directly to disk (Unit V Requirement: Save without displaying)
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.close(fig)  # Release memory resources

    print(f"[Visualizer Success] Line chart saved to: {output_filename}")
    return True


def generate_all_charts(db_name: str = DB_NAME) -> None:
    """
    Convenience function that generates and saves both the bar chart 
    and line chart in one call.
    """
    print("\n--- Generating Visualization Charts (Unit V) ---")
    bar_ok = generate_bar_chart(db_name, "bar_chart.png")
    line_ok = generate_line_chart(db_name, "line_chart.png")
    if bar_ok and line_ok:
        print("[Visualizer] Both charts ('bar_chart.png', 'line_chart.png') generated successfully!")
    else:
        print("[Visualizer Warning] One or more charts could not be created. Please check data.")


if __name__ == "__main__":
    print("[Testing visualizer.py independently...]")
    generate_all_charts()
