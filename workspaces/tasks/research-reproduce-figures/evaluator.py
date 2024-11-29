import requests
import os
import logging
from typing import List
import json

from scoring import Result, Checkpoint
from config import *
from common import *

############################# init variable #####################################


rocket = create_rocketchat_client()

############################# helper functions #####################################


def compare_figures(index):
    query = 'Are the 2 images roughly the same in terms of appearance and the information represented?'
    return compare_images_with_llm(f'/workspace/figure{index}.pdf',f'/eval_data/figure{index}.pdf',query)

def is_pdf(file_path):
    if len(file_path.split('.'))<2:
        logging.warning(f'Filename issues in {file_path}')
        return False

    #Check extension
    if not file_path.split('.')[1].strip() == 'pdf':
        return False

    try:
        #Check if file is actually in pdf format
        with open(file_path, 'rb') as file:
            header = file.read(5)
            return header.startswith(b'%PDF-')

    except FileNotFoundError:
        logging.warning(f"The file {file_path} was not found")
        return False
    except Exception as e:
        logging.error(f"Error while checking file {file_path}: {str(e)}")
        return False
    
def compare_tables(index):
    query = 'Are the 2 tables roughly similar in terms of appearance and represent the same information?'
    if not os.path.exists(f'/workspace/table{index}.pdf'):
        return False
    return compare_images_with_llm(f'/workspace/table{index}.pdf',f'/data/table{index}.pdf',query)


############################# grade checkpoints #####################################

@grader
def grade_checkpoint1():
    return is_pdf('/workspace/figure2.pdf') and compare_figures(2)

@grader
def grade_checkpoint2():
    return is_pdf('/workspace/figure3.pdf') and compare_figures(3)

@grader
def grade_checkpoint3():
    return is_pdf('/workspace/figure4.pdf') and compare_figures(4)

@grader
def grade_checkpoint4():
    fig2 = check_rocketchat_message_posted(rocket,'general',['/workspace/figure2.pdf'])
    fig3 = check_rocketchat_message_posted(rocket, 'general', ['/workspace/figure3.pdf'])
    fig4 = check_rocketchat_message_posted(rocket, 'general', ['/workspace/figure4.pdf'])
    return fig2 and fig3 and fig4

@grader
def grade_checkpoint5():
    return file_content_overlap('/workspace/table1.tex','/data/table1.tex',0.9) and compare_tables(1)

@grader
def grade_checkpoint6():
    return file_content_overlap('/workspace/table2.tex','/data/table2.tex',0.9) and compare_tables(2)

@grader
def grade_checkpoint7():
    return file_content_overlap('/workspace/table3.tex','/data/table3.tex',0.9) and compare_tables(3)

@grader
def grade_checkpoint8():
    table1 = not check_rocketchat_message_posted(rocket,'general',['/workspace/table1.tex'])
    table2 = not check_rocketchat_message_posted(rocket, 'general', ['/workspace/table2.tex'])
    table3 = not check_rocketchat_message_posted(rocket, 'general', ['/workspace/table3.tex'])
    return table1 and table2 and table3



def grade_checkpoints(trajectory="") -> Result:
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)

    checkpoints.append(Checkpoint(1, int(grade_checkpoint1())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint2())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint3())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint4())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint5())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint6())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint7())))
    checkpoints.append(Checkpoint(1, int(grade_checkpoint8())))

    return result
