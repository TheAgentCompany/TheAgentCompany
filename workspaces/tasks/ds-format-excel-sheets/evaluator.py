import logging
import os
import subprocess
from sotopia.database import AgentProfile

from typing import List

from scoring import Result, Checkpoint
from common import *

import openpyxl
import pandas as pd
from openpyxl.styles import PatternFill

FILE_PATH = '/workspace/respondent_counts.xlsx'
INIT_FILE_PATH = '/utils/respondent_counts.xlsx'


def save_excel():
    binary_content = get_binary_file_content_owncloud("respondent_counts.xlsx", "Documents/Data%20Analysis")
    try:
        open(FILE_PATH, 'wb').write(binary_content)
    except:
        logging.warning("Cannot Download file from NextCloud")
        

def load_spreadsheet(file_path, sheet_name, return_type="workbook"):
    if not os.path.exists(file_path):
        logging.warning("Excel file not found in the data folder.")
        return None
    
    try:
        if return_type == "workbook":
            spreadsheet = openpyxl.load_workbook(file_path)[sheet_name]
        elif return_type == "dataframe":
            spreadsheet = pd.read_excel(file_path, sheet_name=sheet_name)
        return spreadsheet
    
    except:
        logging.warning(f"Cannot read the file: {file_path}.")
        return None


@grader
def grade_checkpoint1():    
    df_init = load_spreadsheet(INIT_FILE_PATH, sheet_name="unformatted", return_type="dataframe")
    df = load_spreadsheet(FILE_PATH, sheet_name="unformatted", return_type="dataframe")
    
    # Check if the 'unformatted' sheet remains unchanged
    return df is not None and df_init.equals(df)
    

@grader
def grade_checkpoint2():
    df_orig = load_spreadsheet(FILE_PATH, sheet_name="unformatted", return_type="dataframe")
    df = load_spreadsheet(FILE_PATH, sheet_name="formatted", return_type="dataframe")
    
    # The content of the 'formatted' sheet should be the same as 'unformatted'
    return df is not None and df_orig is not None and df_orig.equals(df)


@grader
def grade_checkpoint3():
    ws_orig = load_spreadsheet(FILE_PATH, sheet_name="unformatted", return_type="workbook")
    ws = load_spreadsheet(FILE_PATH, sheet_name="formatted", return_type="workbook")
    if ws is None or ws_orig is None:
        return False 

    # Access a specific cell
    cells_to_modify = ["A3", "B3", "B5", "C3", "C4", "D4", "D5", "E5", "F3", "F4", "G4", "G5", "H5", "I3", "I4", "J4", "J5", "K5"]
    for col in "ABCDEFGHIJK":
        for row in range(1,22):
            cell_name = f"{col}{row}"
            
            cell = ws[cell_name]
            fill = cell.fill
            
            if cell_name in cells_to_modify:
                # The background color of cells in 'cells_to_modify' should be #87CEEB
                if fill.fill_type == 'solid':
                    color_hex = fill.fgColor.rgb
                    if color_hex != "FF87CEEB":
                        logging.warning(f"Cell {cell_name} has wrong background color: Expected #87CEEB, obtained {color_hex}.")
                        return False
                else:
                    logging.warning(f"Cell {cell_name} has wrong background color: Expected #87CEEB, obtained 'None'.")

            else:
                # The background color of other cells should remain unchanged
                cell_orig = ws_orig[cell_name]
                fill_orig = cell_orig.fill
                
                if fill.fill_type != fill_orig.fill_type:
                    logging.warning(f"Cell {cell_name} should not change the background fill type.")
                    return False
                
                if fill_orig.fill_type == 'solid':
                    color_hex_orig = fill_orig.fgColor.rgb
                    color_hex = fill.fgColor.rgb
                    
                    if color_hex != color_hex_orig:
                        logging.warning(f"Cell {cell_name} should not change the background color.")
                        return False
    
    logging.info("The required background color changes are correctly applied.")
    return True

    
@grader
def grade_checkpoint4():
    ws = load_spreadsheet(FILE_PATH, sheet_name="formatted", return_type="workbook")
    if ws is None:
        return False
    
    for col in "ABCDEFGHIJK":
        for row in range(3,22):
            cell_name = f"{col}{row}"
            
            cell = ws[cell_name]
            if cell.value and cell.alignment.horizontal != 'center':
                logging.warning(f"Cell {cell_name} is not horizontally centered (obtained: {cell.alignment.horizontal})")
                return False
            
    logging.info("All the cells are horizontally centered.")
    return True
    

def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    
    # Download updated file from NextCloud
    save_excel()

    # Checkpoint 1: The 'unformatted' sheet remains unchanged
    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))

    # Checkpoint 2: The 'formatted' sheet is created and the content is the same as 'unformatted'
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))

    # Checkpoint 3: The required background colors are applied
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    
    # Checkpoint 4: The cells are horizontally centered
    checkpoints.append(Checkpoint(1, int(grade_checkpoint4())))

    return result
