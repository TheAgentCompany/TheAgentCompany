from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import grader, download_nextcloud_content, get_binary_file_content_nextcloud
import pandas as pd

# devnote: @grader is required for each checkpoint function
#         it would capture runtime errors, log them, and return False
#         this is a safe guard to prevent any unexpected errors that causes
#         the evaluator to fail the entire task
@grader
def grade_checkpoint1():
    # [2pts] Check if all missing values (previously 'x') are replaced with "0"
    
    ref_file_path = "/workspace/ref_data.xlsx"
    content = get_binary_file_content_nextcloud(
        dir_name="Documents/Data%20Analysis",
        file_name="Other%20Corp%20Area%20Totals.xlsx",
    )
    with open(ref_file_path, "wb") as f:
        f.write(content)
    
    # download_nextcloud_content("https://ogma.lti.cs.cmu.edu/apps/files/files/1738?dir=Documents/Data%20Analysis/Other%20Crop%20Area%20Totals.xlsx", ref_file_path)
    generated_file_path = "/workspace/Other Corp Area Totals.xlsx"
    
    ref_file = pd.read_excel(ref_file_path)
    generated_file = pd.read_excel(generated_file_path)
    
    # check all x (in ref_file) has been replaced with 0 (in generated_file)
    return ref_file.replace("x", 0).equals(generated_file)  

@grader
def grade_checkpoint2():
    # [2pts] Check if question 1 is correctly answered with "2809" or formula "=B5"
    # find the answer in B24
    generated_file_path = "/workspace/Other Corp Area Totals.xlsx"
    generated_file = pd.read_excel(generated_file_path)
    answer = generated_file.iloc[22, 1]
    return answer == 2809 or answer == "=B5"

@grader
def grade_checkpoint3():
    # [2pts] Check if question 2 is correctly answered with "98.8%" or formula "=H18/B18"
    # find the answer in B92
    
    generated_file_path = "/workspace/Other Crop Area Totals.xlsx"
    generated_file = pd.read_excel(generated_file_path)
    answer = generated_file.loc[92, 1]
    # the answer could be in percentage or pure number, check both
    numerical_ref_answer = 0.988
    # change the percentage to number
    if isinstance(answer, str) and "%" in answer:
        answer = float(answer.replace("%", "")) / 100
    # allow some tolerance
    return abs(answer - numerical_ref_answer) < 0.01 or answer == "=H18/B18"


def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(2, 2 * int(passed1)))

    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(2, 2 * int(passed2)))
    
    passed3 = grade_checkpoint3()
    checkpoints.append(Checkpoint(2, 2 * int(passed3)))

    return result



