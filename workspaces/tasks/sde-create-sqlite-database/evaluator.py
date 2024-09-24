"""Evaluator for sde-create-sqlite-database."""

import os
import sys
import logging

def grade_checkpoint1(trajectory):
    return "https://ogma.lti.cs.cmu.edu/apps/files/files/626?dir=/Documents/Financials" in trajectory

def grade_checkpoint2():
    return os.path.exists('/workspace/July-September 2024 Financials.ods')

def grade_checkpoint3():
    # Check if sqlite3 is installed
    try:
        import sqlite3
        return True
    except ImportError:
        return False 

def grade_checkpoint4():
    try:
        import sqlite3
        conn = sqlite3.connect('financial_report.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        return len(tables) > 0
    except sqlite3.Error:
        return False

def grade_checkpoint5():
    try:
        import sqlite3
        conn = sqlite3.connect('financial_data.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(financial_categories);")
        columns = [col[1] for col in cursor.fetchall()]
        conn.close()
        return set(columns) == {'category_id', 'category_name', 'category_type'}
    except sqlite3.Error:
        return False

def grade_checkpoint6():
    try:
        import sqlite3
        conn = sqlite3.connect('financial_data.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(financial_details);")
        columns = [col[1] for col in cursor.fetchall()]
        conn.close()
        return set(columns) == {'detail_id', 'category_id', 'month', 'actual', 'budget', 'variance', 'percent_of_budget'}
    except sqlite3.Error:
        return False

def grade_checkpoint7():
    try:
        import sqlite3
        conn = sqlite3.connect('financial_data.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT month, variance
            FROM financial_details
            JOIN financial_categories ON financial_details.category_id = financial_categories.category_id
            WHERE category_name = 'Total Income'
            ORDER BY variance ASC
            LIMIT 1
        """)
        result = cursor.fetchone()
        conn.close()
        return result == ('2024-08', -35000)
    except sqlite3.Error:
        return False

def grade_checkpoint8():
    try:
        import sqlite3
        conn = sqlite3.connect('financial_data.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(actual)
            FROM financial_details
            JOIN financial_categories ON financial_details.category_id = financial_categories.category_id
            WHERE category_name IN ('Software Development', 'Consulting')
            AND month = '2024-07'
        """)
        result = cursor.fetchone()
        conn.close()
        return result[0] == 95000
    except sqlite3.Error:
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.warning("No trajectory file provided, partial credit might not be granted")
        trajectory = ""
    else:
        try:
            with open(sys.argv[1], 'r') as file:
                trajectory = file.read()
        except Exception as e:
            print(f"Error reading trajectory file: {e}")
            exit(1)

    # if pass checkpoint2, then give full credit for checkpoint1
    grade_checkpoint1 = grade_checkpoint1(trajectory)
    grade_checkpoint2 = grade_checkpoint2()
    first_two_checkpoints = grade_checkpoint2 + max(grade_checkpoint1, grade_checkpoint2)

    points = sum([
        first_two_checkpoints,
        grade_checkpoint3(),
        grade_checkpoint4(),
        grade_checkpoint5(),
        grade_checkpoint6(),
        grade_checkpoint7(),
        grade_checkpoint8()
    ])

    print(f"Final points for task: {points}")
