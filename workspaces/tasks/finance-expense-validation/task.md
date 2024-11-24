Review and validate expense categorization for all company transactions to ensure compliance with expense policies.

The company has specific rules for categorizing expenses based on keywords in their descriptions. Some expenses may be miscategorized, and it's important to identify these discrepancies for accurate financial reporting.

Navigate to owncloud on http://the-agent-company.com:8092/ and navigate to the folder Documents/Financials/Expenses. Here you will find two files:

1. `expenses.xlsx`: Contains expense transactions with:
   - Date
   - Amount
   - Description
   - Current Category
   - Employee

2. `category_rules.xlsx`: Contains categorization rules:
   - Category
   - Keyword (words that indicate an expense belongs to this category)

Your job is to:
1. Review each expense transaction in expenses.xlsx
2. Compare the description against category rules in category_rules.xlsx
3. Identify expenses where the current category doesn't match the rules
4. Create a file called expenses_corrected.xlsx saved in the /workspace folder.
5. Using the corrected transactions create analysis report in workspace/expenses_analysis that is a csv with the following structure:
   - 'Category': The expense category
   - 'Total_Amount': Which is the total amount spent for that category
   - 'Number_of_Employees': The number of employees that have made an expense for that category
   - 'Cost_Per_Employee': Which is just the total amount divided by the number of employees

Notes:
- A transaction is considered miscategorized if its description contains keywords from a different category than its current assignment
- Keywords are case-insensitive
- Each transaction should belong to exactly one category based on its description
