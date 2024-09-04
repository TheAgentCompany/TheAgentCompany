## Intro

Utilities to prepare for GitLab data. Still under heavy construction.

## Details
- `repo_sample_1.csv` and `repo_sample_2.csv` contains the sampled repositories used for dumping information into Gitlab, within which `repo_not_used_1.txt` and `repo_not_used_2.txt` contain the repos not used from the respective samples lists due to various errors or failures.
- `utils.py` is the Python script used to interact with Gitlab for various purposes, indicated by the function names.
- `github2gitlab.py` is the Python script used to import projects from GitHub to GitLab.
- `users.csv` is a local users cache file to store the username, user id of all users created in metis Gitlab.
- `impersonation.csv` is a local cache file to store the username, repository path, and impersonation token of all users created in metis Gitlab. These impersonation tokens are needed to perform API calls on their behalf by the admin/root account.
- `script.sh` is a script to find user id given the username in metis Gitlab, which is internally used by `main.py`