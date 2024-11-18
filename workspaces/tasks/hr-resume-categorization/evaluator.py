from typing import List
from pathlib import Path
import logging

from scoring import Result, Checkpoint
from common import grader


workspace_path = '/workspace'
subdirs = ['early-career', 'mid-level', 'senior', 'unsure']


@grader
def run_checkpoint_1():
    pdf_counts = {}
    total_pdfs = 0
    
    # Check each subdirectory
    for subdir in subdirs:
        dir_path = Path(workspace_path) / subdir
        
        try:
            # Count PDF files in the directory
            pdf_count = len(list(dir_path.glob('*.pdf')))
            pdf_counts[subdir] = pdf_count
            total_pdfs += pdf_count
            
        except FileNotFoundError:
            pdf_counts[subdir] = 0
            logging.warning(f"Warning: Directory {dir_path} not found")

    logging.info(f"Total PDF files: {total_pdfs}, correct answer: 94")
    return total_pdfs == 94


@grader
def run_checkpoint_2():
    """
    Ground truth:
    Aaliyah_Thompson.pdf        Emma_Smith.pdf              John_Smith.pdf              Lu_Jian.pdf                 Taylor_Swift_Bootcamp.pdf
    Avery_Williams_Bootcamp.pdf Ethan_Anderson.pdf          Jordan_Lee_Bootcamp.pdf     Luo_Jie.pdf                 Wang_Hai_Yan.pdf
    Blake_Anderson_Bootcamp.pdf Feng_Feng_Ying.pdf          Keisha_Washington.pdf       Lv_Yang.pdf                 Xiao_Xia.pdf
    Charlie_Brown_Bootcamp.pdf  Finley_Moore_Bootcamp.pdf   Kendall_Wright_Bootcamp.pdf Mei_Chen.pdf                Xu_Gui_Hua.pdf
    Chen_Tao.pdf                Harper_Garcia_Bootcamp.pdf  Lai_Li.pdf                  Noah_Garcia.pdf             Xu_Yan.pdf
    Christopher_Brown.pdf       He_Chen.pdf                 Li_Bing.pdf                 Olivia_Martinez.pdf         Yang_Shu_Zhen.pdf
    Cui_Xue_Mei.pdf             Hiroshi_Tanaka.pdf          Li_Jie.pdf                  Peyton_Clark_Bootcamp.pdf   Yao_Xiu_Ying.pdf
    DeShawn_Robinson.pdf        Huang_Bin.pdf               Li_Mei.pdf                  Reese_Campbell_Bootcamp.pdf Yuki_Nakamura.pdf
    Deng_Cheng.pdf              Huang_Ting_Ting.pdf         Li_Tao.pdf                  Skylar_White_Bootcamp.pdf   Zhang_Gui_Lan.pdf
    Ding_Shu_Zhen.pdf           Huang_Yu_Zhen.pdf           Lin_Yan.pdf                 Song_Shu_Ying.pdf           Zhang_Hong.pdf
    Drew_Martinez_Bootcamp.pdf  Jamie_Davis_Bootcamp.pdf    Liu_Wei.pdf                 Soo-Jin_Kim.pdf
    Emerson_Scott_Bootcamp.pdf  Jessica_Wilson.pdf          Lu_Hui.pdf                  Tan_Rui.pdf
    """
    dir_path = Path(workspace_path) / 'early-career'
    resumes = list(dir_path.glob('*.pdf'))
    logging.info(f"Resumes in early-career folder: {resumes}")
    early_career_count = len(resumes)
    logging.info(f"Number of files in early-career folder: {early_career_count}, correct answer: 58")
    return early_career_count == 58


@grader
def run_checkpoint_3():
    # the only resume in mid-level folder is named "Alex_Chen.pdf"
    dir_path = Path(workspace_path) / 'mid-level'
    resumes = list(dir_path.glob('*.pdf'))
    logging.info(f"Resumes in mid-level folder: {resumes}, correct answer: Alex_Chen.pdf")
    mid_level_count = len(resumes)
    return mid_level_count == 1 and resumes[0].name == 'Alex_Chen.pdf'


@grader
def run_checkpoint_4():
    # the only resume in senior folder is named "Emily_Zhang.pdf"
    dir_path = Path(workspace_path) / 'senior'
    resumes = list(dir_path.glob('*.pdf'))
    logging.info(f"Resumes in senior folder: {resumes}, correct answer: Emily_Zhang.pdf")
    senior_count = len(resumes)
    return senior_count == 1 and resumes[0].name == 'Emily_Zhang.pdf'


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    checkpoints.append(Checkpoint(1, int(run_checkpoint_1())))
    checkpoints.append(Checkpoint(1, int(run_checkpoint_2())))
    checkpoints.append(Checkpoint(1, int(run_checkpoint_3())))
    checkpoints.append(Checkpoint(1, int(run_checkpoint_4())))
    return result
