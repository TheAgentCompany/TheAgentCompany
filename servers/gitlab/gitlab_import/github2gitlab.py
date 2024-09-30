from utils import import_repos

if __name__ == '__main__':
    # Note: github import is asynchronous and happens in GitLab server background process
    # the import can take tens of hours for large repos, so we don't indefinitely wait here
    # instead, we simply return after initiating the import process
    repos = [
        ('opensearch-project', 'OpenSearch'),
        ('ggerganov', 'llama.cpp'),
        ('gocolly', 'colly'),
        ('node-red', 'node-red'),
        ('risingwavelabs', 'risingwave')
    ]
    import_repos(repos)
