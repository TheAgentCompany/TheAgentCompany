from utils import import_repos

if __name__ == '__main__':
    # Note: github import is asynchronous and happens in GitLab server background process
    # TODO: move some logic from utils to here, and make helper functions in utils irrelevant to business logic
    import_repos()