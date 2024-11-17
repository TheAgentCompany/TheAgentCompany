"""Evaluator for sde-create-sqlite-database."""

import os
import sys
import logging

from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_any
from common import grader

@grader
def grade_checkpoint1(trajectory):
    return "dir=/Documents/Financials" in trajectory

@grader
def grade_checkpoint2():
    return os.path.exists('/workspace/July-September 2024 Financials.ods')

@grader
def grade_checkpoint3():
    # Check if sqlite3 is installed
    try:
        import sqlite3
        return True
    except ImportError:
        return False 

@grader
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

@grader
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

@grader
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

@grader
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

@grader
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


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any)

    checkpoints.append(Checkpoint(1, grade_checkpoint1(trajectory)))
    checkpoints.append(Checkpoint(1, grade_checkpoint2()))
    checkpoints.append(Checkpoint(1, grade_checkpoint3()))
    checkpoints.append(Checkpoint(1, grade_checkpoint4()))
    checkpoints.append(Checkpoint(1, grade_checkpoint5()))
    checkpoints.append(Checkpoint(1, grade_checkpoint6()))
    checkpoints.append(Checkpoint(1, grade_checkpoint7()))
    checkpoints.append(Checkpoint(1, grade_checkpoint8()))

    return result
    


