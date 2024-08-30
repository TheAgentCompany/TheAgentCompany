FROM gitlab/gitlab-ce:17.3.1-ce.0

ENV GITLAB_SKIP_TAIL_LOGS=true
ENV GITLAB_ROOT_EMAIL="root@local"
ENV GITLAB_ROOT_PASSWORD="JobBench"

# Copy start script to the image
# This script includes setting up GitLab and populating data
COPY custom_wrapper.sh /assets

# Copy repo data to the image
# "exports" folder contains all repos [reponame.tar.gz] in GitLab proprietary format
# they are exported manually from GitLab server(s)
COPY exports /assets

RUN chmod +x /assets/custom_wrapper.sh
CMD ["/assets/custom_wrapper.sh"]