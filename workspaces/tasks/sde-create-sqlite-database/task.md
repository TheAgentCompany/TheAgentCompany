On our office cloud at https://ogma.lti.cs.cmu.edu/, find the July-Sep 2024
financial report for our company, and create a SQLite database with two tables that
appropriately populates the data in the report:

- financial_categories
- financial_details

The financial_categories table has the following columns:

- category_id
- category_name
- category_type

The financial_details table has the following columns:

- detail_id
- category_id
- month (strings in the format YYYY-MM)
- actual
- budget
- variance
- percent_of_budget

The SQLite database should be named "financial_report.db".
