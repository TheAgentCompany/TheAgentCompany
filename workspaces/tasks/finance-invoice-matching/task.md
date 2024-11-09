Find the provided payments file at https://ogma.lti.cs.cmu.edu/apps/files/files/1421?dir=/Documents/Financials/payments.xlsx&openfile=true and the invoice PDFs in the directory https://ogma.lti.cs.cmu.edu/apps/files/files/1422?dir=/Documents/Financials/invoices_pdfs. 

Perform the following:
* Parse Payment References: Extract and match each payment in the Excel file to its corresponding invoice(s) based on references.
* Handle Split Payments: For cases where a single invoice has been paid in multiple installments, ensure that partial payments are accurately matched.
* Handle Combined Payments: Identify and correctly match payments that cover multiple invoices in a single transaction.
* Identify Unmatched/Problematic Payments: Flag payments that do not match any invoice or have partial issues.

Create a file at /Documents/Financials/flagged_payments.xlsx with columns "Payment_ID" and "Issue". "Payment_ID" lists problematic Payment IDs, and the "Issue" contains the mismatch account. In the last row for of the "flagged_payments.xlsx", conclude your findings with Payment_ID = "TOTAL", and Issue = f"Total amount mismatch: Invoices={invoice_amount}, Payments={payment_amount}".