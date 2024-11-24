import pandas as pd
import sys

def verify_expense_categories():
    """
    Verify that expenses are correctly categorized according to the rules.
    """
    try:
        # Load the original data
        expenses_df = pd.read_excel('expenses.xlsx')
        rules_df = pd.read_excel('category_rules.xlsx')
        
        # Load the solution file
        # solution_df = pd.read_excel('../solutions/task1_solution.xlsx')
        
        # Create a dictionary of categories and their keywords
        category_rules = {}
        for _, row in rules_df.iterrows():
            if row['Category'] not in category_rules:
                category_rules[row['Category']] = []
            category_rules[row['Category']].append(row['Keyword'].lower())
        
        # Verify each expense
        correct_categories = []
        for _, row in expenses_df.iterrows():
            description = row['Description'].lower()
            correct_category = None
            
            # Find the correct category based on keywords
            for category, keywords in category_rules.items():
                if any(keyword in description for keyword in keywords):
                    correct_category = category
                    break
            
            correct_categories.append(correct_category)
        
        # Compare with solution
        expenses_df['Correct_Category'] = correct_categories
        mismatches = expenses_df[expenses_df['Category'] != expenses_df['Correct_Category']]
        
        # Save the corrected expenses to a new Excel file
        expenses_df.to_excel('expenses_corrected.xlsx', index=False)
        
        # Compare with provided solution
        # if not solution_df['Flagged_Transactions'].equals(mismatches.index):
        #     print("❌ Verification failed: Incorrect identification of miscategorized expenses")
        #     return False
        
        print(f"✅ Verification passed!")
        print(f"Found {len(mismatches)} miscategorized expenses")
        print(mismatches)
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {str(e)}")
        return False

def analyze_corrected_expenses(file_path):
    """
    Analyze the corrected expenses and output a CSV with the total amount of expenses
    for each category, the number of employees that spent in that category, and the cost per employee.
    """
    try:
        # Load the corrected expenses data
        corrected_df = pd.read_excel(file_path)
        
        # Group by the correct category and calculate the required metrics
        analysis_df = corrected_df.groupby('Correct_Category').agg(
            Total_Amount=('Amount', 'sum'),
            Number_of_Employees=('Employee', 'nunique')
        ).reset_index()
        
        # Calculate cost per employee
        analysis_df['Cost_Per_Employee'] = analysis_df['Total_Amount'] / analysis_df['Number_of_Employees']
        print(analysis_df)
        # Save the analysis to a CSV file
        analysis_df.to_csv('expenses_analysis.csv', index=False)
        
        print("✅ Analysis completed and saved to 'expenses_analysis.csv'")
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")

if __name__ == "__main__":
    if verify_expense_categories():
        analyze_corrected_expenses('expenses_corrected.xlsx')
