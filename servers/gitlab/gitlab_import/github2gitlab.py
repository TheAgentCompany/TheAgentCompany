from utils import import_repos, export_repos

if __name__ == '__main__':
    # Note: since gitlab import is asynchronous, we should either only
    # run import or only run export at a time
    # TODO: add argparser
    import_repos()
    # export_repos()