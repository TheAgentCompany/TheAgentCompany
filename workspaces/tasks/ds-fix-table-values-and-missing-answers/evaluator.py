from typing import List

from scoring import Result, Checkpoint, bonus_for_completing_final
from common import grader, download_owncloud_content
import pandas as pd

generated_file_path = r"/workspace/corrected_other_corp_area_totals.xlsx"

# devnote: @grader is required for each checkpoint function
#         it would capture runtime errors, log them, and return False
#         this is a safe guard to prevent any unexpected errors that causes
#         the evaluator to fail the entire task

def read_xlsx(path):
    return pd.read_excel(path, engine='openpyxl')

@grader
def grade_checkpoint1():
    # [2pts] Check if all missing values (previously 'x') are replaced with "0"
    
    ref_file_path = r"/workspace/ref_data.xlsx"
    
    # download_owncloud_content(
    #     link="http://the-agent-company.com:8092/index.php/s/b61rG8gHESP84Na/download",
    #     output_file_path=ref_file_path,
    # )
    
    ref_file = read_xlsx(ref_file_path)
    generated_file = read_xlsx(generated_file_path)
    for row in range(ref_file.shape[0]):
        for col in range(ref_file.shape[1]):
            if ref_file.iloc[row, col] == "x":
                if generated_file.iloc[row, col] not in [0, "0"]:
                    return False
    return True

@grader
def grade_checkpoint2():
    # [2pts] Check if question 1 is correctly answered with "2809" or formula "=B5"
    # find the answer in B24
    generated_file = read_xlsx(generated_file_path)
    answer = generated_file.iloc[22, 1]
    return answer == 2809 or answer == "=B5"

@grader
def grade_checkpoint3():
    # [2pts] Check if question 2 is correctly answered with "98.8%" or formula "=H18/B18"
    # find the answer in B92
    
    generated_file = read_xlsx(generated_file_path)
    answer = generated_file.iloc[90, 1]
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
