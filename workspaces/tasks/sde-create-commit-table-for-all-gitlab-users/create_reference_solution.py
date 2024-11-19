import requests
import csv
from collections import defaultdict
from datetime import datetime, timedelta
from dateutil import parser  # Handles ISO-8601 timestamps
import urllib.parse
import logging

from common import make_gitlab_request

# Get all projects
def get_projects():
    projects = []
    page = 1
    while True:
        response = make_gitlab_request(additional_path="projects", params={"page": page, "per_page": 100})
        if response and response.status_code == 200:
            data = response.json()
            if not data:
                break
            projects.extend(data)
            page += 1
        else:
            raise Exception(f"Error fetching projects: {response.status_code if response else 'No response'}")
    return projects

# Get commits for a specific project
def get_commits(project_id):
    commits = []
    page = 1
    while True:
        # Convert project_id to a string before passing it
        response = make_gitlab_request(project_identifier=str(project_id), additional_path="repository/commits", params={"page": page, "per_page": 100})
        if response and response.status_code == 200:
            data = response.json()
            if not data:
                break
            commits.extend(data)
            page += 1
        else:
            raise Exception(f"Error fetching commits for project {project_id}: {response.status_code if response else 'No response'}")
    return commits


# Get the start date of the week (Sunday)
def get_week_start(date_str):
    # Use `dateutil.parser.parse` to handle timezone-aware strings
    date = parser.parse(date_str)
    # Normalize to UTC and calculate the start of the week (Sunday)
    start_of_week = date - timedelta(days=date.weekday() + 1)
    return start_of_week.strftime("%Y/%m/%d")

# Process data and create CSV
def generate_commit_report():
    projects = get_projects()
    commit_data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # {week: {user: {repo: count}}}

    # Fetch commits for each project
    for project in projects:
        project_id = project['id']
        project_name = project['name']
        print(f"Processing commits for project: {project_name}...")

        commits = get_commits(project_id)
        for commit in commits:
            week = get_week_start(commit['created_at'])
            author_name = commit.get('author_name', 'Unknown')
            commit_data[week][author_name][project_name] += 1

    # Prepare CSV data
    all_repos = sorted({repo for week_data in commit_data.values() for user_data in week_data.values() for repo in user_data})
    csv_data = [["week", "user"] + all_repos]

    for week, week_data in sorted(commit_data.items()):
        for user, user_data in week_data.items():
            row = [week, user] + [user_data.get(repo, 0) for repo in all_repos]
            csv_data.append(row)

    # Write to CSV
    with open("/workspace/reference_report.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    print("Commit report generated: commit_report.csv")


