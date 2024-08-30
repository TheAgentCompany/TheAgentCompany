#!/bin/bash
set -ex

# Run the original wrapper script, but remove the last five lines
# NOTE: this magic number 2 comes from the fact that 17.3.1-ce.0 version's
# wrapper file has last 2 lines of "waiting for SIGTERM",
# which we'd like to get rid of
head -n -2 /assets/wrapper > /tmp/modified_wrapper
source /tmp/modified_wrapper

echo "GitLab is up and running. Performing post-launch actions..."

# Create token "root-token" with sudo and api permissions
gitlab-rails runner "token = User.find_by_username('root').personal_access_tokens\
    .create(scopes: ['api', 'read_user', 'read_api', 'read_repository', 'write_repository', 'sudo', 'admin_mode'], name: 'root-token', expires_at: 365.days.from_now); \
    token.set_token('root-token'); \
    token.save!"

# Change configs to enable import from GitLab exports
# in addition, enable project export
# TODO: figure out how to allow github imports as well
curl --request PUT --header "PRIVATE-TOKEN: root-token" \
    "http://localhost:8929/api/v4/application/settings?import_sources=gitlab_project&project_export_enabled=true"

# Import projects (please make sure they are available under local exports directory)
# this way, we can build and ship a GitLab image with pre-imported repos
export_dir="/assets/exports"

# Iterate over all .tar.gz files in the export directory
for file in "$export_dir"/*.tar.gz; do
    # Extract the filename without the path and extension
    filename=$(basename "$file" .tar.gz)
    
    curl --request POST \
         --header "PRIVATE-TOKEN: root-token" \
         --form "path=$filename" \
         --form "file=@$file" \
         "http://localhost:8929/api/v4/projects/import"
    
    echo "Imported $filename"
done

# TODO: change authorship of issues/prs/commits

# Keep the container running
wait