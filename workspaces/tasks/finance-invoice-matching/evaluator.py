import pandas as pd
import logging
from typing import List
import re
import numpy as np
from io import BytesIO

from common import check_file_in_nextcloud_directory, get_binary_file_content_nextcloud, checkpoint
from scoring import Result, Checkpoint, bonus_for_completing_any
from config import NEXTCLOUD_URL


@checkpoint
def grade_checkpoint1(trajectory):
    urls = [f"/Documents/Financials/payments.xlsx&openfile=true", f"/Documents/Financials/invoices_pdfs"]
            
    return all(url in trajectory for url in urls)

@checkpoint
def grade_checkpoint2():
    file_name = "flagged_payments.xlsx"
    dir_name = "Documents/Financials"
    if not check_file_in_nextcloud_directory(file_name, dir_name):
        return 0

    content = get_binary_file_content_nextcloud(file_name, dir_name)
    if not content:
        logging.warning("Failed to download content")
        return 0

    # read content as df
    try:
        flagged_df = pd.read_excel(BytesIO(content))
    except Exception as e:
        logging.warning(f"Failed to read flagged_payments.xlsx: {e}")
        return 0

    required_columns = ["Payment_ID", "Issue"]
    if not all(column in flagged_df.columns for column in required_columns):
        return 1

    # Check if the last row follows the specified format
    pattern = r"^Total amount mismatch: Invoices=\d+(\.\d{2})?, Payments=\d+(\.\d{2})?$"
        
    last_row = flagged_df.iloc[-1]
    issue_format = re.match(pattern, last_row["Issue"])
    if (
        last_row["Payment_ID"] == "TOTAL"
        and (issue_format is not None)
    ):
        return 2
    else:
        return 1
    
@checkpoint
def grade_checkpoint3():
    file_name = "flagged_payments.xlsx"
    dir_name = "Documents/Financials"
    try:
        content = get_binary_file_content_nextcloud(file_name, dir_name)
        flagged_df = pd.read_excel(BytesIO(content))
    except Exception as e:
        logging.warning(f"Failed to read flagged_payments.xlsx: {e}")
        return 0
    
    # Load the uploaded Excel files
    invoices_df = pd.read_excel('/utils/invoices.xlsx')
    payments_df = pd.read_excel('/utils/payments.xlsx')

    # Create a dictionary to store invoice amounts by Invoice_ID
    invoice_amounts = {}
    for _, invoice in invoices_df.iterrows():
        invoice_amounts[invoice['Invoice_ID']] = invoice['Amount']

    # Initialize a list to store any identified issues
    issues = []
    processed_payments = set()

    # Process each payment to handle references, split, and combined payments
    for _, payment in payments_df.iterrows():
        references = payment['Reference'].replace(' ', '').split(',')
        payment_id = payment['Payment_ID']
        payment_amount = payment['Amount']
        
        matched_invoices = []
        total_matched_amount = 0

        # Handle references in the payment
        for ref in references:
            if ref.startswith("INV"):
                invoice_id = ref[:7]
                partial_flag = "(Partial)" in ref or "(Remaining)" in ref
                if invoice_id not in invoice_amounts:
                    # Flag payment if referenced invoice is not found
                    issues.append({
                        'Payment_ID': payment_id,
                        'Issue': f'Referenced invoice {invoice_id} not found'
                    })
                else:
                    matched_invoices.append(invoice_id)
                    total_matched_amount += invoice_amounts[invoice_id] if not partial_flag else payment_amount
            else:
                # Skip if reference does not start with INV
                continue

        # Check if payment is a combined or split payment
        if len(matched_invoices) > 1:
            # Combined payment case
            if not np.isclose(total_matched_amount, payment_amount, rtol=1e-5):
                issues.append({
                    'Payment_ID': payment_id,
                    'Issue': f'Combined payment amount mismatch for invoices {matched_invoices}'
                })
        elif len(matched_invoices) == 1 and '(Partial)' in payment['Reference']:
            # Split payment case - partial payment for a single invoice
            invoice_id = matched_invoices[0]
            remaining_amount = invoice_amounts[invoice_id] - payment_amount
            if remaining_amount > 0:
                # Add partial payment info for split payments
                issues.append({
                    'Payment_ID': payment_id,
                    'Issue': f'Partial payment for invoice {invoice_id}, remaining amount {remaining_amount:.2f}'
                })

        processed_payments.add(payment_id)

    # Check for unmatched invoices and overall balance discrepancy
    total_invoice_amount = invoices_df['Amount'].sum()
    total_payment_amount = payments_df['Amount'].sum()
    if not np.isclose(total_invoice_amount, total_payment_amount, rtol=1e-5):
        issues.append({
            'Payment_ID': 'TOTAL',
            'Issue': f'Total amount mismatch: Invoices={total_invoice_amount:.2f}, Payments={total_payment_amount:.2f}'
        })

    # Convert issues to a DataFrame and save as an Excel file
    issues_df = pd.DataFrame(issues)

    # Check if issues_df's last row is the same as flagged_df's last row
    last_row_flagged = flagged_df.iloc[-1]
    last_row_issues = issues_df.iloc[-1]
    if not last_row_flagged.equals(last_row_issues):
        return 0
    
    # Check if the payment id columns are the same in two dfs
    if not issues_df['Payment_ID'].equals(flagged_df['Payment_ID']):
        return 1
    else:
        return 2
    
def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    checkpoints.append(Checkpoint(2, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(2, int(grade_checkpoint3())))

    return result

