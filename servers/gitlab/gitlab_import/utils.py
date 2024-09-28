import collections
import json
import requests
import subprocess
import shutil
import os
import logging
import time
import pandas as pd
from csv import writer

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

# Get user_id
def get_user_id(username):
    df = pd.read_csv('users.csv', index_col='username')
    df_filter = df.filter(items=[username], axis=0)
    if df_filter.shape[0] > 0:
        return df_filter.user_id[0]
    
    script_resp = subprocess.run(['./script.sh', username], capture_output=True)
    if script_resp.returncode == 0:
        user_id = int(script_resp.stdout)
        with open('users.csv', 'a') as f:
            List = [username, user_id]
            writer_object = writer(f)
            writer_object.writerow(List)
    return int(user_id) if script_resp.returncode == 0 else -1

def create_project(user_id, proj_name):
    project_url = f'http://{HOSTNAME}:{PORT}/api/v4/projects/user/{user_id}'
    body2 = {
        'user_id': user_id,
        'name': proj_name,
        'visibility': 'public'
    }
    requests.post(project_url, json=body2, headers=ROOT_HEADER)

def clone_and_push(username, proj_name):
    try:
        subprocess.run(['git', 'clone', '--mirror', f'https://github.com/{username}/{proj_name}'], check=True,
                        stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        subprocess.run(['git', 'remote', 'add', 'gitlab', 
                        f'http://root:{ACCESS_TOKEN}@{HOSTNAME}:{PORT}/{username}/{proj_name}.git'],
                        cwd=f'{proj_name}.git', check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        subprocess.run(['git', 'push', '--mirror', 'gitlab'], cwd=f'{proj_name}.git', check=True,
                       stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    except Exception as e:
        print(e, '\n', username, proj_name, '\n\n')
    
    if os.path.exists(f'{proj_name}.git'):
        shutil.rmtree(f'{proj_name}.git')

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
        user_id = get_user_id(user) if user_id < 0 else user_id
        if user_id > 0:
            users_list.append((user, user_id))
        for assginee in pull['assignees']:
            user = assginee['login']
            name, email, extras = get_github_profile(user)
            user_id = create_user(user, name, email, **extras)
            user_id = get_user_id(user) if user_id < 0 else user_id
            if user_id > 0:
                users_list.append((user, user_id))
            
        for reviewer in pull['requested_reviewers']:
            user = reviewer['login']
            name, email, extras = get_github_profile(user)
            user_id = create_user(user, name, email, **extras)
            user_id = get_user_id(user) if user_id < 0 else user_id    
            if user_id > 0:
                users_list.append((user, user_id))
        
        if pull['head'] and pull['head']['user']:
            user = pull['head']['user']['login']
            name, email, extras = get_github_profile(user)
            user_id = create_user(user, name, email, **extras)
            user_id = get_user_id(user) if user_id < 0 else user_id
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
        user_id = get_user_id(user) if user_id < 0 else user_id
        if user_id > 0:
            users_list.append((user, user_id))
    
        for assginee in issue['assignees']:
            user = assginee['login']
            name, email, extras = get_github_profile(user)
            user_id = create_user(user, name, email, **extras)
            user_id = get_user_id(user) if user_id < 0 else user_id
            if user_id > 0:
                users_list.append((user, user_id))
    
    return users_list
    
def star_repo(user_id, username, repo_path):
    df = pd.read_csv('impersonation.csv', index_col='username')
    df_filter = df.filter(items=[username], axis=0)
    if df_filter.shape[0] > 0:
        imp_token = df_filter.token[0]
    else:
        for _ in range(2):
            imp_url = f'http://{HOSTNAME}:{PORT}/api/v4/users/{user_id}/impersonation_tokens'
            body = {
                'user_id': int(user_id),
                'name': f'imp_token_{username}',
                'scopes': ['api'],
                'state': 'active'
            }
            r = requests.post(imp_url, json=body, headers=ROOT_HEADER)
            resp = json.loads(r.text)
            if 'token' not in resp:
                res = json.loads(requests.get(imp_url, json=body, headers=ROOT_HEADER).text)
                if isinstance(res, list) and len(res) > 0:   
                    for imp in res:
                        impid = imp['id']
                        url = f'http://{HOSTNAME}:{PORT}/api/v4/users/{int(user_id)}/impersonation_tokens/{int(impid)}'
                        requests.delete(url, headers=ROOT_HEADER)
            else:
                break
                
        imp_token = resp['token']
        with open('impersonation.csv', 'a') as f:
            List = [username, user_id, repo_path, imp_token]
            writer_object = writer(f)
            writer_object.writerow(List)
        
    impersonation_header = {'PRIVATE-TOKEN': imp_token}
    star_url = f'http://{HOSTNAME}:{PORT}/api/v4/projects/{repo_path}/star'
    body2 = {
        'id': repo_path
    }
    requests.post(star_url, json=body2, headers=impersonation_header)
    
def star_with_users_from_pulls(username, repo):
    repo_path = f'{username}%2F{repo}'
    pulls_url = f'http://api.github.com/repos/{username}/{repo}/pulls'
    r = requests.get(pulls_url, headers=GITHUB_HEADER)
    resp = json.loads(r.text)
    for pull in resp:
        user = pull['user']['login']
        user_id = get_user_id(user)
        if user_id > 0:
            star_repo(user_id, user, repo_path)
        for assginee in pull['assignees']:
            user = assginee['login']
            user_id = get_user_id(user)
            if user_id > 0:
                star_repo(user_id, user, repo_path)
        for reviewer in pull['requested_reviewers']:
            user = reviewer['login']
            user_id = get_user_id(user)
            if user_id > 0:
                star_repo(user_id, user, repo_path)
        if pull['head'] and pull['head']['user']:
            user = pull['head']['user']['login']
            user_id = get_user_id(user)
            if user_id > 0:
                star_repo(user_id, user, repo_path)

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

def get_commits_from_repo():
    # get all commit users from all repos
    with open("./all_projects.json", 'r') as f:
        d = json.load(f)

    project_ids = [x['id'] for x in d]
    
    commit_log = collections.defaultdict(list)
    for project_id in project_ids:    
        url = f'http://{HOSTNAME}:{PORT}/api/v4/projects/{project_id}/repository/commits'
        r = requests.get(url, headers=ROOT_HEADER)
        resp = json.loads(r.text)
        # get the user name and email from the commit
        for commit in resp:
            commit_log[project_id].append([commit[k] for k in ['author_name', 'author_email', 'committer_name', 'committer_email']])
            
    with open("commit_log.json", 'w') as f:
        json.dump(commit_log, f, indent=4)

def get_all_users():
    url = 'http://{HOSTNAME}:{PORT}/api/v4/users'
    users = []
    page = 1
    while True:
        r = requests.get(url, headers=ROOT_HEADER, params={'per_page': 100, 'page': page})
        resp = json.loads(r.text)
        if len(resp) == 0:
            break
        users.extend(resp)
        page += 1
    with open("all_users.v2.json", 'w') as f:
        print(len(users))
        json.dump(users, f, indent=4)

def get_all_projects():
    url = 'http://{HOSTNAME}:{PORT}/api/v4/projects'
    projects = []
    page = 1
    while True:
        r = requests.get(url, headers=ROOT_HEADER, params={'per_page': 100, 'page': page})
        resp = json.loads(r.text)
        if len(resp) == 0:
            break
        projects.extend(resp)
        page += 1
    with open("all_projects.json", 'w') as f:
        print(len(projects))
        json.dump(projects, f, indent=4)
