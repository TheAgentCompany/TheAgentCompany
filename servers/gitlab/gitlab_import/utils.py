import json
import requests
import os
import logging
import time

# Note: if you use the GitLab image we build, then 'root-token' is already
# set up. Otherwise, please set up GitLab token by yourself.
GITLAB_ACCESS_TOKEN = os.getenv('GITLAB_TOKEN', 'root-token')

# To migrate from GitHub to GitLab, please provide a GitHub token
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_TOKEN')

HOSTNAME = os.getenv('HOSTNAME', 'localhost')
PORT = int(os.getenv('GITLAB_PORT', 8929))

ROOT_HEADER = {'PRIVATE-TOKEN': GITLAB_ACCESS_TOKEN, 'Sudo': 'root'}
GITHUB_HEADER = {
    'Authorization': f'token {GITHUB_ACCESS_TOKEN}'
}

def _check_status_code(status_code):
    if status_code != 200:
        logging.warning(f'API call status is {status_code}, sleep for 10 seconds...')
        time.sleep(10)

def get_github_profile(username):
    url = f'https://api.github.com/users/{username}'
    r = requests.get(url, headers=GITHUB_HEADER)
    _check_status_code(r.status_code)
    resp = json.loads(r.text)
    extras = {
        'bio': resp['bio'],
        'loc': resp['location'],
        'org': resp['company']
    }
    return resp['name'], resp['email'], extras

def create_user(username, name, email=None, bio=None, loc=None, org=None):
    url = f'http://{HOSTNAME}:{PORT}/api/v4/users'
    body = {
        'email': f'{username}@fakegithub.com' if not email else email,
        'name': name if name else username,
        'username': username,
        'password': 'hello1234',
        'skip_confirmation': True
    }
    if bio:
        body['bio'] = bio
    if org:
        body['organization'] = org
    if loc:
        body['location'] = loc
    r = requests.post(url, json=body, headers=ROOT_HEADER)
    resp = json.loads(r.text)
    return int(resp['id']) if 'id' in resp else -1

def get_public_repos(username):
    github_url = f'https://api.github.com/users/{username}/repos'
    r = requests.get(github_url, headers=GITHUB_HEADER)
    _check_status_code(r.status_code)
    resp = json.loads(r.text)
    return [(info['name'], info['id']) for info in resp]

def mirror(username, repo_id):
    mirror_url = f'http://{HOSTNAME}:{PORT}/api/v4/import/github'
    body = {
        'personal_access_token': GITHUB_ACCESS_TOKEN,
        'repo_id': repo_id,
        'target_namespace': username,
        'optional_stages': {
            "single_endpoint_issue_events_import": True,
            "single_endpoint_notes_import": True,
            "attachments_import": True
        }
    }
    r = requests.post(mirror_url, json=body, headers=ROOT_HEADER)
    print(r.text, flush=True)

def create_users_from_pulls(username, repo):
    pulls_url = f'http://api.github.com/repos/{username}/{repo}/pulls'
    r = requests.get(pulls_url, headers=GITHUB_HEADER)
    _check_status_code(r.status_code)
    resp = json.loads(r.text)
    users_list = []
    for pull in resp:
        user = pull['user']['login']
        name, email, extras = get_github_profile(user)
        user_id = create_user(user, name, email, **extras)
        if user_id > 0:
            users_list.append((user, user_id))
        for assginee in pull['assignees']:
            user = assginee['login']
            name, email, extras = get_github_profile(user)
            user_id = create_user(user, name, email, **extras)
            if user_id > 0:
                users_list.append((user, user_id))
            
        for reviewer in pull['requested_reviewers']:
            user = reviewer['login']
            name, email, extras = get_github_profile(user)
            user_id = create_user(user, name, email, **extras)
            if user_id > 0:
                users_list.append((user, user_id))
        
        if pull['head'] and pull['head']['user']:
            user = pull['head']['user']['login']
            name, email, extras = get_github_profile(user)
            user_id = create_user(user, name, email, **extras)
            if user_id > 0:
                users_list.append((user, user_id))
        
    return users_list

def create_users_from_issues(username, repo):
    issues_url = f'http://api.github.com/repos/{username}/{repo}/issues'
    r = requests.get(issues_url, headers=GITHUB_HEADER)
    _check_status_code(r.status_code)
    resp = json.loads(r.text)
    users_list = []
    for issue in resp:
        user = issue['user']['login']
        name, email, extras = get_github_profile(user)
        user_id = create_user(user, name, email, **extras)
        if user_id > 0:
            users_list.append((user, user_id))
    
        for assginee in issue['assignees']:
            user = assginee['login']
            name, email, extras = get_github_profile(user)
            user_id = create_user(user, name, email, **extras)
            if user_id > 0:
                users_list.append((user, user_id))
    
    return users_list
    
def delete_project(username, repo):
    delete_url = f'http://{HOSTNAME}:{PORT}/api/v4/projects/{username}%2F{repo}'
    body = {
        'id': f'{username}%2F{repo}'
    }
    r = requests.delete(delete_url, json=body, headers=ROOT_HEADER)
    print(json.loads(r.text))

def import_repos(repos):
    logging.info(f'Gitlab Access Token Used: {GITLAB_ACCESS_TOKEN}')
    logging.info(f'Github Access Token Used: {GITHUB_ACCESS_TOKEN}') 
    
    for USERNAME, REPO in repos:
        # username might be a person, or an org
        repos = get_public_repos(USERNAME)
        REPO_ID = -1
        for proj, repo_id in repos:
            if proj == REPO:
                REPO_ID = repo_id
        
        if REPO_ID < 0:
            logging.error(f'Repo: {REPO} Not Found for {USERNAME}!!')
            continue
        
        users_list = create_users_from_pulls(USERNAME, REPO)
        users_list.extend(create_users_from_issues(USERNAME, REPO))
        users_list = list(set(users_list))
        mirror(USERNAME, REPO_ID)
