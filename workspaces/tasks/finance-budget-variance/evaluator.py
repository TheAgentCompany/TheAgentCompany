import pandas as pd
import logging
from typing import List
from io import BytesIO

from common import check_file_in_nextcloud_directory, get_binary_file_content_nextcloud, checkpoint
from scoring import Result, Checkpoint, bonus_for_completing_any


@checkpoint
def grade_checkpoint1(trajectory):
    urls = [f"/Documents/Financials"]
            
    return all(url in trajectory for url in urls)
    
@checkpoint
def grade_checkpoint2():
    file_name = "flagged_variances.xlsx"
    dir_name = "Documents/Financials"
    if not check_file_in_nextcloud_directory(file_name, dir_name):
        return 0

    try:
        content = get_binary_file_content_nextcloud(file_name, dir_name)
        flagged_df = pd.read_excel(BytesIO(content))
    except Exception as e:
        logging.warning(f"Failed to read flagged_budgets.xlsx: {e}")
        return 0
    
    # check if "Flagged_Variances" column exists
    if 'Flagged_Variances' not in flagged_df.columns:
        logging.warning(f"❌ Verification failed: 'Flagged_Variances' column not found in flagged_variances.xlsx")
        return 1

    # check if the column is in the format Department_Category_YYYYMM
    if not flagged_df['Flagged_Variances'].str.match(r'^[a-zA-Z]+_[a-zA-Z]+_[0-9]{6}$').all():
        logging.warning(f"❌ Verification failed: 'Flagged_Variances' column is not in the correct format")
        return 2
    
    try:
        # Load the data
        budget_df = pd.read_excel('/utils/budget.xlsx')
        actual_df = pd.read_excel('/utils/actual_spending.xlsx')
        
        # Merge budget and actual data
        analysis_df = pd.merge(
            budget_df,
            actual_df,
            on=['Department', 'Category', 'Month']
        )
        
        # Calculate variances
        analysis_df['Variance_Amount'] = analysis_df['Actual_Amount'] - analysis_df['Budgeted_Amount']
        analysis_df['Variance_Percentage'] = (analysis_df['Variance_Amount'] / analysis_df['Budgeted_Amount'] * 100).round(2)
        
        # Identify significant variances (>10% and >$5000)
        significant_variances = analysis_df[
            (abs(analysis_df['Variance_Percentage']) > 10) &
            (abs(analysis_df['Variance_Amount']) > 5000)
        ]
        
        # Create unique identifiers for variances
        significant_variances['Variance_ID'] = significant_variances.apply(
            lambda x: f"{x['Department']}_{x['Category']}_{x['Month'].strftime('%Y%m')}", 
            axis=1
        )

        # Compare with solution
        variance_id = significant_variances['Variance_ID'].reset_index(drop=True)
        if not flagged_df['Flagged_Variances'].equals(variance_id):
            logging.warning("❌ Verification failed: Incorrect identification of significant budget variances")
            return 2
            
        logging.info(f"✅ Verification passed!")
        logging.info(f"Found {len(variance_id)} significant budget variances")
        return 3
        
    except Exception as e:
        logging.warning(f"❌ Verification failed: {str(e)}")
        return 2
    
def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_any)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1(trajectory))))
    checkpoints.append(Checkpoint(3, int(grade_checkpoint2())))

    return result

