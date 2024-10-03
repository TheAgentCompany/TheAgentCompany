import json
import requests
import os
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Note: if you use the GitLab image we build, then 'root-token' is already
# set up. Otherwise, please set up GitLab token by yourself.
GITLAB_ACCESS_TOKEN = os.getenv('GITLAB_TOKEN', 'root-token')

# To migrate from GitHub to GitLab, please provide a GitHub token
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_TOKEN')

HOSTNAME = os.getenv('HOSTNAME', 'localhost')
PORT = int(os.getenv('GITLAB_PORT', 8929))

ROOT_HEADER = {'PRIVATE-TOKEN': GITLAB_ACCESS_TOKEN, 'Sudo': 'root'}
GITHUB_HEADER = {
    'Authorization': f'Bearer {GITHUB_ACCESS_TOKEN}'
}

def _check_status_code(status_code):
    if status_code != 200:
        logger.warning(f'API call status is {status_code}, sleep for 10 seconds...')
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

def mirror(username, repo_id):
    mirror_url = f'http://{HOSTNAME}:{PORT}/api/v4/import/github'
    body = {
        'personal_access_token': GITHUB_ACCESS_TOKEN,
        'repo_id': repo_id,
        'target_namespace': 'root',
        'optional_stages': {
            "single_endpoint_issue_events_import": False,
            "single_endpoint_notes_import": False,
            "attachments_import": False
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
    
def get_github_repo_id(USERNAME, REPO):
    repo_url = f'https://api.github.com/repos/{USERNAME}/{REPO}'
    r = requests.get(repo_url, headers=GITHUB_HEADER)
    _check_status_code(r.status_code)
    resp = json.loads(r.text)
    return resp['id']

def import_repos(repos):
    logger.info(f'GitLab Access Token Used: {GITLAB_ACCESS_TOKEN}')
    logger.info(f'GitHub Access Token Used: {GITHUB_ACCESS_TOKEN}')
    
    for USERNAME, REPO in repos:
        # username might be a person, or an org
        REPO_ID = get_github_repo_id(USERNAME, REPO)
        logger.info(f'Repo id for {USERNAME}/{REPO}: {REPO_ID}')
        create_users_from_pulls(USERNAME, REPO)
        create_users_from_issues(USERNAME, REPO)
        mirror(USERNAME, REPO_ID)
