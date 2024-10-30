import os
from typing import List
from scoring import Result, Checkpoint


def get_summary_file_content():
    filepath = "summary.txt"
    try:
        with open(filepath, 'r') as f:
            result = f.read()
            return result
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")
        return ""


def check_emily_info():
    file_content = get_summary_file_content()
    required_content = [
        "Emily Johnson",
        "University of California, Berkeley",
        "Google", "Amazon",
        "Python", "Java, C++", "JavaScript",
        "React", "Node.js", "Flask",
        "Git", "Docker", "AWS", "MySQL",
    ]
    if all([rc in file_content for rc in required_content]):
        return 1
    else:
        return 0


def check_michael_info():
    file_content = get_summary_file_content()
    required_content = [
        "Michael Davis",
        "New York University",
        "Meta", "Spotify",
        "JavaScript", "Python", "Swift", "Ruby",
        "Django", "Angular", "React Native",
        "Git", "Firebase", "PostgreSQL", "Jenkins",
    ]
    if all([rc in file_content for rc in required_content]):
        return 1
    else:
        return 0


def check_sarah_info():
    file_content = get_summary_file_content()
    required_content = [
        "Sarah Thompson",
        "University of Texas at Austin",
        "Microsoft", "Oracle",
        "Python", "Java", "C#", "HTML/CSS",
        "Angular", "Spring Boot", "Express.js",
        "Git", "Docker", "MongoDB", "Kubernetes",
    ]
    if all([rc in file_content for rc in required_content]):
        return 1
    else:
        return 0


def grade_checkpoints(trajectory=""):
    checkpoints: List[Checkpoint] = []
    result = Result(checkpoints)
    checkpoints.append(Checkpoint(1, check_emily_info()))
    checkpoints.append(Checkpoint(1, check_michael_info()))
    checkpoints.append(Checkpoint(1, check_sarah_info()))
    return result
