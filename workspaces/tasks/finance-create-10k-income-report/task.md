Find the provided bill in /Documents/Financials/bill.pdf on NextCloud(https://ogma.lti.cs.cmu.edu/apps/files/files).
Here you wil find 10K annual reports for multiple tech companies. Extract the net income data for each company from their 10-K reports (in section/item 8) for the years 2021, 2022, and 2023, and compile it into a structured table. 
The table should be in a csv format and should have the following column strucutre:
- 'Company Name': The company name according to the name of registrant as specified in its charter document.
- 'Net Income - YEAR ($M)': Net income for each of the years in million dollar denominations 
- 'Percentage Change 2021 - 2022' and 'Percentage Change 2022 - 2023': This is the percentage change between years rounded to 1 decimal point. Save it as /workspace/net_income_report.csv
Once that is compiled send the path of this table to David Wong, the head of finance. With this, suggest to him which company we should invest in based on the company that had the largest percentage growth between 2022-2023.
