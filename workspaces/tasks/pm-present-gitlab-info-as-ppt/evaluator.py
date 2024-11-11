import os
from typing import List
from config import *
from scoring import Result, Checkpoint, bonus_for_completing_final
import pptx
from common import get_all_texts_from_slide, checkpoint

expected_repos = [
    {"name": "api-server", "description": "", "issues": 0, "merge_requests": 0},
    {"name": "bustub", "description": "The BusTub Relational Database Management System (Educational)", "issues": 28, "merge_requests": 14},
    {"name": "colly", "description": "Elegant Scraper and Crawler Framework for Golang", "issues": 152, "merge_requests": 41},
    {"name": "copilot-arena-server", "description": "", "issues": 0, "merge_requests": 0},
    {"name": "Documentation", "description": "Wiki for company-wide doc", "issues": 0, "merge_requests": 0},
    {"name": "janusgraph", "description": "JanusGraph: an open-source, distributed graph database", "issues": 491, "merge_requests": 40},
    {"name": "llama.cpp", "description": "LLM inference in C/C++", "issues": 268, "merge_requests": 277},
    {"name": "node-red", "description": "Low-code programming for event-driven applications", "issues": 304, "merge_requests": 95},
    {"name": "openhands", "description": "OpenHands: Code Less, Make More", "issues": 120, "merge_requests": 34},
    {"name": "opensearch", "description": "Open source distributed and RESTful search engine.", "issues": 1700, "merge_requests": 161},
    {"name": "raft", "description": "", "issues": 0, "merge_requests": 0},
    {"name": "risingwave", "description": "Best-in-class stream processing, analytics, and management. Unified streaming and batch. PostgreSQL compatible.", "issues": 996, "merge_requests": 88},
    {"name": "sotopia", "description": "Sotopia: an Open-ended Social Learning Environment (ICLR 2024 spotlight)", "issues": 12, "merge_requests": 6},
    {"name": "streamlit", "description": "Streamlit — A faster way to build and share data apps.", "issues": 919, "merge_requests": 38},
]

# Set tolerance for issues and merge request counts due to changes when GitLab image is rebaked
TOLERANCE = 5

def within_tolerance(actual, expected, tolerance):
    """Check if the actual count is within tolerance of the expected count."""
    return abs(actual - expected) <= tolerance

@checkpoint
def grade_checkpoint1():
    """Check if the presentation file exists."""
    return os.path.exists('/workspace/Engineering_Progress.pptx')

@checkpoint
def grade_checkpoint2():
    """Evaluate the correctness of names, descriptions, issue counts, and merge request counts."""
    slide_path = '/workspace/Engineering_Progress.pptx'
    if not os.path.exists(slide_path):
        return 0  # No presentation file found, so no points
    
    prs = pptx.Presentation(slide_path)
    name_correct, desc_correct, issues_correct, mr_correct = 0, 0, 0, 0

    for repo in expected_repos:
        name_found, desc_found, issues_found, mr_found = False, False, False, False
        for slide in prs.slides:
            slide_text = get_all_texts_from_slide(slide)
            
            # Check for correct name and description
            if repo["name"].lower() in slide_text:
                name_found = True
            if repo["description"].lower() in slide_text:
                desc_found = True

            # Check for issues count with tolerance
            if "issues:" in slide_text:
                try:
                    issues_count = int(slide_text.split("issues:")[1].split()[0])
                    if within_tolerance(issues_count, repo["issues"], TOLERANCE):
                        issues_found = True
                except (ValueError, IndexError):
                    pass  # Ignore if parsing fails or the format is unexpected

            # Check for merge requests count with tolerance
            if "merge requests:" in slide_text:
                try:
                    mr_count = int(slide_text.split("merge requests:")[1].split()[0])
                    if within_tolerance(mr_count, repo["merge_requests"], TOLERANCE):
                        mr_found = True
                except (ValueError, IndexError):
                    pass  # Ignore if parsing fails or the format is unexpected

        # Increment correct counts based on findings across all slides
        if name_found:
            name_correct += 1
        if desc_found:
            desc_correct += 1
        if issues_found:
            issues_correct += 1
        if mr_found:
            mr_correct += 1

    total_repos = len(expected_repos)
    # Award points if more than half of each category is correct
    score = 0
    if name_correct > total_repos / 2:
        score += 1
    if desc_correct > total_repos / 2:
        score += 1
    if issues_correct > total_repos / 2:
        score += 1
    if mr_correct > total_repos / 2:
        score += 1

    return score




def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints, bonus_for_completing_final)

    # Checkpoint 1: Check if the presentation file exists
    passed1 = grade_checkpoint1()
    checkpoints.append(Checkpoint(1, int(passed1)))

    # Checkpoint 2: Verify each repository slide has correct details
    passed2 = grade_checkpoint2()
    checkpoints.append(Checkpoint(4, passed2))

    return result

