# Based on the task requirements, I'll proceed with the following steps:
# 1. Load the data from both documents and identify team members' monthly availability (effort capacity) and their core competencies.
# 2. Match competencies with required roles, and allocate team members based on availability to meet the goal as quickly as possible.

import pandas as pd

# The data extracted from document 1, showing each team member's monthly allocation.
# Define a dictionary representing team members' availability per month for faster processing (from parsed data in the Word document).
availability_data = {
    "January": {
        "Sarah Johnson": 30, "Li Ming": 15, "Zhang Wei": 0, "Wang Fang": 35, "Mike Chen": 0,
        "Emily Zhou": 46, "Liu Qiang": 55, "Priya Sharma": 37, "Mark Johnson": 41,
        "Jessica Lee": 30, "Chen Xinyi": 31, "David Wong": 43, "Huang Jie": 50,
        "Sophia Rodriguez": 27, "Alex Turner": 40, "Emma Lewis": 39, "Jessica Chen": 39
    },
    "February": {
        "Sarah Johnson": 40, "Li Ming": 40, "Zhang Wei": 45, "Wang Fang": 0, "Mike Chen": 30,
        "Emily Zhou": 41, "Liu Qiang": 33, "Priya Sharma": 50, "Mark Johnson": 42,
        "Jessica Lee": 31, "Chen Xinyi": 11, "David Wong": 41, "Huang Jie": 58,
        "Sophia Rodriguez": 51, "Alex Turner": 38, "Emma Lewis": 34, "Jessica Chen": 53
    },
    "March": {
        "Sarah Johnson": 55, "Li Ming": 0, "Zhang Wei": 30, "Wang Fang": 25, "Mike Chen": 0,
        "Emily Zhou": 29, "Liu Qiang": 38, "Priya Sharma": 29, "Mark Johnson": 31,
        "Jessica Lee": 0, "Chen Xinyi": 55, "David Wong": 48, "Huang Jie": 49,
        "Sophia Rodriguez": 36, "Alex Turner": 40, "Emma Lewis": 36, "Jessica Chen": 45
    },
    "April": {
        "Sarah Johnson": 40, "Li Ming": 40, "Zhang Wei": 0, "Wang Fang": 0, "Mike Chen": 30,
        "Emily Zhou": 27, "Liu Qiang": 28, "Priya Sharma": 38, "Mark Johnson": 35,
        "Jessica Lee": 0, "Chen Xinyi": 27, "David Wong": 0, "Huang Jie": 37,
        "Sophia Rodriguez": 32, "Alex Turner": 51, "Emma Lewis": 49, "Jessica Chen": 39
    }
}

# Loading competencies data from the Excel file (parsed previously)
competencies_data = {
    "Sarah Johnson": ["management"],
    "Li Ming": ["management"],
    "Zhang Wei": ["management", "frontend eng", "backend eng"],
    "Wang Fang": ["backend eng"],
    "Mike Chen": ["management", "frontend eng", "backend eng"],
    "Emily Zhou": ["frontend eng"],
    "Liu Qiang": ["backend eng"],
    "Priya Sharma": ["frontend eng"],
    "Mark Johnson": ["management"],
    "Jessica Lee": ["design"],
    "Chen Xinyi": ["backend eng"],
    "David Wong": ["infra"],
    "Huang Jie": ["frontend eng"],
    "Sophia Rodriguez": ["design"],
    "Alex Turner": ["frontend eng"],
    "Emma Lewis": ["frontend eng", "backend eng"],
    "Jessica Chen": ["infra"]
}

# Define goal requirements
goal_requirements = {
    "Li Ming": 50,            # 50% effort needed from Li Ming or equivalent
    "project management": 50, # 50% effort for project management
    "design": 50,             # 50% effort for design
    "frontend": 100,          # 100% effort for frontend work
    "backend": 150,           # 150% effort for backend work
    "infra": 50               # 50% effort for infrastructure
}

# Step-by-step allocation plan based on availability, competencies, and requirements
# Track progress for allocation in each category
allocation_plan = []
allocation_progress = {key: 0 for key in goal_requirements.keys()}

# Define helper function to allocate effort
def allocate_effort(month, person, available_effort, role):
    global allocation_progress, allocation_plan
    required_effort = goal_requirements[role] - allocation_progress[role]
    allocation = min(available_effort, required_effort)
    allocation_progress[role] += allocation
    allocation_plan.append({"month": month, "person": person, "effort percent": allocation, "role": role})

# Perform allocation based on monthly availability and competencies
for month, members in availability_data.items():
    for person, available_effort in members.items():
        competencies = competencies_data.get(person, [])
        
        # Allocating effort based on competencies
        if "management" in competencies and allocation_progress["project management"] < goal_requirements["project management"]:
            allocate_effort(month, person, available_effort, "project management")
        if "design" in competencies and allocation_progress["design"] < goal_requirements["design"]:
            allocate_effort(month, person, available_effort, "design")
        if "frontend eng" in competencies and allocation_progress["frontend"] < goal_requirements["frontend"]:
            allocate_effort(month, person, available_effort, "frontend")
        if "backend eng" in competencies and allocation_progress["backend"] < goal_requirements["backend"]:
            allocate_effort(month, person, available_effort, "backend")
        if "infra" in competencies and allocation_progress["infra"] < goal_requirements["infra"]:
            allocate_effort(month, person, available_effort, "infra")
        if person == "Li Ming" and allocation_progress["Li Ming"] < goal_requirements["Li Ming"]:
            allocate_effort(month, person, available_effort, "Li Ming")

# Convert allocation plan to DataFrame for easy viewing
allocation_df = pd.DataFrame(allocation_plan)

