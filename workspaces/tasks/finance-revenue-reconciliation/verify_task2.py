import pandas as pd
import numpy as np

def verify_revenue_recognition():
    """
    Verify revenue recognition schedule against contracts.
    """
    try:
        # Load the data
        contracts_df = pd.read_excel('contracts.xlsx')
        revenue_df = pd.read_excel('revenue_schedule.xlsx')
        solution_df = pd.read_excel('task2_solution.xlsx')
        
        # Group revenue by contract
        revenue_by_contract = revenue_df.groupby('Contract_ID')['Amount'].sum().round(2)
        
        # Check total amounts match contract values
        discrepancies = []
        for _, contract in contracts_df.iterrows():
            contract_id = contract['Contract_ID']
            total_recognized = revenue_by_contract.get(contract_id, 0)
            
            if not np.isclose(total_recognized, contract['Total_Value'], rtol=1e-5):
                discrepancies.append({
                    'Contract_ID': contract_id,
                    'Contract_Value': contract['Total_Value'],
                    'Recognized_Value': total_recognized,
                    'Difference': contract['Total_Value'] - total_recognized
                })
        
        discrepancies_df = pd.DataFrame(discrepancies)
        print(discrepancies_df['Contract_ID'])
        # Compare with solution
        if not solution_df['Flagged_Contracts'].equals(discrepancies_df['Contract_ID']):
            print("❌ Verification failed: Incorrect identification of revenue recognition discrepancies")
            return False
            
        print(f"✅ Verification passed!")
        print(f"Found {len(discrepancies)} contracts with revenue recognition discrepancies")
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    verify_revenue_recognition()
