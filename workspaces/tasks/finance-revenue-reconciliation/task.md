Your task is to match revenue recognition schedules with contract values to identify any discrepancies in revenue timing or amounts. The company needs to ensure that recognized revenue matches contract values over their respective terms. Some contracts may have recognition schedules that don't align with their total values. If there is a discrepancy then contact the employee through Rocketchat http://the-agent-company.com:3000/home

Navigate to Documents/Human Resources Team/Contracts on Owncloud (http://the-agent-company.com:8092/) and find the following files:
1. `contracts.xlsx`
2. `revenue_schedule.xlsx`

For each contract, sum up all revenue recognition entries
- Compare total recognized revenue against the contract value
- Identify contracts where:
   - Total recognized revenue doesn't match contract value (within a small tolerance)
   - Recognition schedule doesn't align with contract term
- Account for contracts with different terms and payment schedules

Create `flagged_contracts.xlsx` saved in the /workspace folder with column 'Flagged_Contracts' which has Contract IDs with recognition discrepancies.

To contact the employees with flagged contracts, use the employee_contracts.xlsx file to find which employees have flagged contracts.
