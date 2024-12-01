import requests
import os
import logging
from typing import List
import json

from scoring import Result, Checkpoint
from config import *
from common import *
import sqlite3
import pandas as pd

############################# init variable #####################################

DB_PATH = '/data/coffee_shop.db'
CSV_DIRECTORY = '/data'
SHORT_STOCK_VIEW_CSV = '/utils/short_stock.csv'
AVERAGE_SALES_VIEW = '/utils/average_sales.csv'
ANALYSIS_SHEET = 'analysis.txt'

############################# helper functions #####################################

def view_exists(view_name, conn):
    try:
        cursor = conn.cursor()

        # Query sqlite_master table
        cursor.execute("""
            SELECT COUNT(*) 
            FROM sqlite_master 
            WHERE type='view' AND name=?
        """, (view_name,))

        exists = cursor.fetchone()[0] > 0
        return exists

    except sqlite3.Error as e:
        print(f"Error checking view existence: {e}")
        return False

def dataframes_are_equal(df1,df2):
    #Column order invariant
    df1.sort_index(axis=1)
    df2.sort_index(axis=1)

    # Compare column names (case-insensitive)
    df1_cols = set(col.lower() for col in df1.columns)
    df2_cols = set(col.lower() for col in df2.columns)
    if df1_cols != df2_cols:
        logging.warning(f'Columns do not match')
        return False

    # Compare row counts
    if len(df1) != len(df2):
        logging.warning(f'Number of rows do not match')
        return False

    df1_sorted = df1.sort_values(by=list(df1.columns)).reset_index(drop=True).round(2)
    df2_sorted = df2.sort_values(by=list(df2.columns)).reset_index(drop=True).round(2)

    # Compare content
    if not df1_sorted.equals(df2_sorted):
        logging.warning(f'Content does not match')
        return False
    return True


def validate_tables_with_csv(conn):
    """
    Validate if database tables match corresponding CSV files.
    """
    try:
        # Get all CSV files in directory
        csv_files = [f for f in os.listdir(CSV_DIRECTORY) if f.endswith('.csv')]

        # Get all tables in database
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        db_tables = [table[0] for table in cursor.fetchall()]
        logging.info(f'Following tables found: {db_tables}')

        for csv_file in csv_files:
            table_name = csv_file.replace('.csv', '')


            if table_name not in db_tables:
                logging.warning(f'Table {table_name} not present in the DB')
                return False

            #Read source csv
            csv_path = os.path.join(CSV_DIRECTORY, csv_file)
            df_csv = pd.read_csv(csv_path)

            # Read database table
            df_db = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

            if not dataframes_are_equal(df_csv, df_db):
                return False

        return True

    except Exception as e:
        logging.error(f'Error validating tables: {e}')
        return False

############################# grade checkpoints #####################################

@grader
def grade_checkpoint1():
    filenames=[
        'customers.csv',
        'products.csv',
        'inventory.csv',
        'orders.csv',
        'order_items.csv'
    ]
    for filename in filenames:
        if not os.path.exists(os.path.join('/workspace',filename)):
            logging.warning(f'{filename} not downloaded')
            return False
    return True

@grader
def grade_checkpoint2(conn):
    return validate_tables_with_csv(conn)

@grader
def grade_checkpoint3(conn):

    if not view_exists('v_short_stock',conn):
        logging.warning('View v_short_stock does not exist')
        return False

    csv_path = os.path.join('/utils', SHORT_STOCK_VIEW_CSV)
    df_csv = pd.read_csv(csv_path)

    df_db = pd.read_sql_query(f"SELECT * FROM v_short_stock", conn)

    return dataframes_are_equal(df_csv, df_db)

@grader
def grade_checkpoint4(conn):
    if not view_exists('v_sales', conn):
        logging.warning('View v_sales does not exist')
        return False

    csv_path = os.path.join('/utils', AVERAGE_SALES_VIEW)
    df_csv = pd.read_csv(csv_path)

    df_db = pd.read_sql_query(f"SELECT * FROM v_sales", conn)

    return dataframes_are_equal(df_csv, df_db)

@grader
def grade_checkpoint5():
    
    ref_answers = [['p001','p003','p005'],['p001','p002','p004'],['sarah johnson','emma brown']]
    score = 0
    
    if not os.path.exists(os.path.join('/workspace',ANALYSIS_SHEET)):
        logging.warning('Analysis sheet does not exist in the workspace directory')
        return 0
    
    with open(os.path.join('/workspace',ANALYSIS_SHEET),'r') as f:
        for i, line in enumerate(f):
            qa_pair = line.split(':')
            if len(qa_pair)<2:
                logging.warning('Analysis sheet corrupted')
                return 0
            answers = qa_pair[1].strip().split(',')
            answers = set(answer.strip().lower().replace("'","").replace('"',"") for answer in answers)
            score+= 1 if answers == set(ref_answers[i]) else 0
            logging.info(f'Question {qa_pair[0]}, Expected Answer: {ref_answers[i]}, Agent Answer: {answers}')

    return score

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    conn = None

    try:
        conn = sqlite3.connect(DB_PATH)
    except Exception as e:
        logging.error(f'Could not connect to database: {e}')


    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2(conn)) if conn else 0))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3(conn)) if conn else 0))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint4(conn)) if conn else 0))
    checkpoints.append(Checkpoint(3, int(grade_checkpoint5())))

    return result
