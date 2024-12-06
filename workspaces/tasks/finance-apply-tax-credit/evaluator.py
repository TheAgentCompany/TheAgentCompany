import logging
from typing import List
import fitz

from common import create_rocketchat_client, evaluate_chat_history_with_llm, grader
from scoring import Result, Checkpoint

rocket = create_rocketchat_client()

target_values = {
    'topmostSubform[0].Page1[0].f1_20[0]': '80168.46',
    'topmostSubform[0].Page1[0].f1_21[0]': '4836.38',
    'topmostSubform[0].Page1[0].f1_22[0]': '0',
    'topmostSubform[0].Page1[0].f1_23[0]': '4836.38',
    'topmostSubform[0].Page1[0].f1_24[0]': '101297.75',
    'topmostSubform[0].Page1[0].f1_25[0]': '20259.55',
    'topmostSubform[0].Page1[0].f1_26[0]': '8569.71',
    'topmostSubform[0].Page1[0].f1_27[0]': '65465.27',
    'topmostSubform[0].Page1[0].f1_28[0]': '16268.11',
    'topmostSubform[0].Page1[0].f1_29[0]': '16292.91',
    'topmostSubform[0].Page1[0].f1_30[0]': '106596',
    'topmostSubform[0].Page1[0].f1_31[0]': '27386.29',
    'topmostSubform[0].Page1[0].f1_32[0]': '4564.38',
    'topmostSubform[0].Page1[0].f1_33[0]': '102031.62',
    'topmostSubform[0].Page1[0].f1_34[0]': '14284.4268',
    'topmostSubform[0].Page1[0].f1_35[0]': '34543.9768',
    'topmostSubform[0].Page1[0].c1_2[1]': "2"
}

@grader
def grade_checkpoint1():
    try:
        pdf_document = fitz.open("/workspace/filled_f6765.pdf")
    except Exception as e:
        logging.warning(f"Failed to read filled_f6765.pdf: {e}")
        return 0

    extracted_values = {}

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        form_fields = page.widgets()

        if form_fields:
            for field in form_fields:
                field_name = field.field_name
                field_value = field.field_value
                if field_name:
                    extracted_values[field_name] = field_value or ''  # Use empty string if value is None

    pdf_document.close()

    # Compare extracted values with target values
    score = 0
    for field, target_value in target_values.items():
        if extracted_values.get(field) == target_value:
            score += 1

    if score == 16:
        return 5
    else:
        return round((score / 16) * 5)
    
@grader
def grade_checkpoint2():
    return evaluate_chat_history_with_llm(
        rocket, 
        "David Wong", 
        "This person has been asked about whether we are electing the reduced credit under section 280C, and whether we have research expenses for the prior 3 tax years")
    
    
def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(5, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(3, int(grade_checkpoint2())*3))

    return result

