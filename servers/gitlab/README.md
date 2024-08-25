## Server: gitlab


### Starting up server

Navigate to parent directory (servers), and run the below commands:

```bash
# start gitlab
make start-gitlab
# reveal password for root user
make gitlab-root-password
```

Then you can navigate to http://$HOSTNAME:8929 to visit GitLab on your browser.

Root user name: `root`
Root user password: `JobBench`

### Import data

Check out `gitlab_import` directory.
