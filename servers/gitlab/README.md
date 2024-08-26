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

Data is prepared and imported as part of Dockerfile. As a benchmark user, you
don't need to worry about data population. Everything is set up automatically.

If you are a benchmark developer and would like to add a new repo, please follow
the below steps:

1. Launch GitLab server
2. Import repos from outside, e.g. GitHub. You could do so either [manually](https://docs.gitlab.com/ee/user/project/import/)
or [programmatically](https://docs.gitlab.com/ee/api/import.html). Alternatively,
you could also create a new repo on your own. Note, this involves a lot of Internet
traffic and might be slow.
3. [Export](https://docs.gitlab.com/ee/user/project/settings/import_export.html#export-a-project-and-its-data) repo from GitLab. A tar file would be generated and you could download to your local machine. Note, this might
be slow.
4. Upload the exported file to a publicly accessible place, e.g. Amazon S3, HuggingFace.
5. Include the file as part of the Docker image build process.