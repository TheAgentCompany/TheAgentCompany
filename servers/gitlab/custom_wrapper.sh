#!/bin/bash

# Make sure we start from a clean state
rm -rf /etc/gitlab
rm -rf /var/log/gitlab
rm -rf /var/opt/gitlab

# Run the original wrapper script, but remove the last five lines
# NOTE: this magic number 5 comes from the fact that 17.3.1-ce.0 version's
# Dockerfile has last 5 lines of "tailing logs" and "waiting for SIGTERM",
# which we'd like to get rid of
head -n -5 /assets/wrapper > /tmp/modified_wrapper
source /tmp/modified_wrapper

# Tail all logs (from the original wrapper script)
gitlab-ctl tail &

echo "GitLab is up and running. Performing post-launch actions..."

# Create token "root-token" with sudo and api permissions
gitlab-rails runner "token = User.find_by_username('root').personal_access_tokens\
    .create(scopes: ['api', 'read_user', 'read_api', 'read_repository', 'write_repository', 'sudo', 'admin_mode'], name: 'root-token', expires_at: 365.days.from_now); \
    token.set_token('root-token'); \
    token.save!"

# Change configs to enable import from GitLab exports and GitHub
# in addition, enable project export
curl --request PUT --header "PRIVATE-TOKEN: root-token" \
    "http://localhost:8929/api/v4/application/settings?import_sources=gitlab_project&import_sources=github&project_export_enabled=true"

# Import projects (please make sure they are available at the mounted location)
# this way, we can build and ship a GitLab image with pre-imported repos
#
# devnote: add new projects (that are exported from GitLab) here if you'd like to add
# more repos to the benchmark
curl --request POST --header "PRIVATE-TOKEN: root-token" --form "path=janusgraph" \
     --form "file=@/etc/gitlab_exports/janusgraph.tar.gz" "http://localhost:8929/api/v4/projects/import"

# Keep the container running
wait