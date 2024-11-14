from typing import List
import PyPDF2
import pandas as pd
import os
import logging

from scoring import Result, Checkpoint
from common import grader

@grader
def run_checkpoint_1(trajectory: str):
    pdf_folder_path = "/workspace/i_9_forms"
    csv_path = "/utils/personell_data_golden.csv"

    df = pd.read_csv(csv_path, dtype=str)

    discrepancies = {}
    for name in df["Name"]:
        discrepancies[name] = []

    num_fields = 0

    for index, row in df.iterrows():
        pdf_path = os.path.join(pdf_folder_path, f"i-9_{row['First Name (Given Name)']}_{row['Last Name (Family Name)']}.pdf")
        if not os.path.exists(pdf_path):
            discrepancies.append((pdf_path, "File missing"))
            continue
        
        # Extract data from the PDF
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        form_data = pdf_reader.get_fields()
        pdf_data = {key: form_data[key].get('/V') for key in form_data.keys() if form_data[key].get('/V')}
        
        # Compare extracted data with CSV row data
        name = row['Name']
        golden_values = {
            'Last Name (Family Name)': row['Last Name (Family Name)'],
            'First Name Given Name': row['First Name (Given Name)'],
            'Employee Middle Initial (if any)': row['Middle Initial (if any)'] if pd.notnull(row['Middle Initial (if any)']) else '',
            'Employee Other Last Names Used (if any)': row['Other Last Names Used (if any)'] if pd.notnull(row['Other Last Names Used (if any)']) else '',
            'Address Street Number and Name': row['Address (Street Number and Name)'],
            'Apt Number (if any)': row['Apt. Number (if any)'] if pd.notnull(row['Apt. Number (if any)']) else '',
            'City or Town': row['City or Town'],
            'ZIP Code': row['ZIP Code'],
            'Date of Birth mmddyyyy': row['Date of Birth (mm/dd/yyyy)'],
            'US Social Security Number': str(row['U.S. Social Security Number']),
            'Employees E-mail Address': row["Employee's Email Address"],
            'Telephone Number': str(row["Employee's Telephone Number"]),
            '3 A lawful permanent resident Enter USCIS or ANumber': str(row['USCIS A-Number']) if pd.notnull(row['USCIS A-Number']) else '',
            'Exp Date mmddyyyy': row['Expiration Date (mm/dd/yyyy)'] if pd.notnull(row['Expiration Date (mm/dd/yyyy)']) else '',
            'USCIS ANumber': str(row['USCIS A-Number']) if pd.notnull(row['USCIS A-Number']) and row['Citizenship/Immigration Status'] == "A noncitizen authorized to work" else '',
            'Form I94 Admission Number': str(row['Form I-94 Admission Number']) if pd.notnull(row['Form I-94 Admission Number']) else '',
            'Foreign Passport Number and Country of IssuanceRow1': f"{row['Foreign Passport Number']} {row['Country of Issuance']}" if pd.notnull(row['Foreign Passport Number']) else '',
            'Signature of Employee': row['Signature of Employee'],
            "Today's Date mmddyyy": row["Today's Date (mm/dd/yyyy)"],
            'State': f"{row['State']}",
            'CB_1': '/On' if row['Citizenship/Immigration Status'] == "A citizen of the United States" else "/Off",
            'CB_2': '/On' if row['Citizenship/Immigration Status'] == "A noncitizen national of the United States" else "/Off",
            'CB_3': '/On' if row['Citizenship/Immigration Status'] == "A lawful permanent resident" else "/Off",
            'CB_4': '/On' if row['Citizenship/Immigration Status'] == "A noncitizen authorized to work" else "/Off",
        }
        # add non-nan or non-empty or non-off fields to num_fields
        num_fields += len([field for field in golden_values if golden_values[field] and golden_values[field] != "/Off"])
        for field, expected_value in golden_values.items():
            pdf_value = pdf_data.get(field, "")
            if expected_value == "/Off":
                if not pdf_value:
                    continue
                elif pdf_value not in ["", "/Off"]:
                    discrepancies[name].append(f"{pdf_path}: {field} - Expected: {expected_value}, Found: {pdf_value}")
            if str(pdf_value) != expected_value:
                discrepancies[name].append(f"{pdf_path}: {field} - Expected: {expected_value}, Found: {pdf_value}")

    num_forms = len(df)
    total_correct_forms = sum([1 for name in discrepancies if not discrepancies[name]])
    total_incorrect_fields = sum([len(discrepancies[name]) for name in discrepancies])

    logging.info(f"Total correct forms: {total_correct_forms}")
    if total_correct_forms == num_forms:
        logging.info("All I-9 forms are correctly filled.")
        return 5
    else:
        logging.warning(f"Total incorrect fields: {total_incorrect_fields} out of {num_fields} fields, total incorrect forms: {num_forms - total_correct_forms} out of {num_forms} forms.")
        return min(round(5 * total_incorrect_fields / num_fields), round(5 * (num_forms - total_correct_forms) / num_forms))   


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    checkpoints.append(Checkpoint(5, int(run_checkpoint_1(trajectory))))
    return result
