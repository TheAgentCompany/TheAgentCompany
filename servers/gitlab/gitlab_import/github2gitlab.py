from utils import import_repos

if __name__ == '__main__':
    # Note: gitlab import is asynchronous and happens in GitLab server background process
    import_repos()