#!/bin/bash
set -ex

# start from a clean state without any configs or data
rm -rf /etc/gitlab/*
rm -rf /var/log/gitlab/*
rm -rf /var/opt/gitlab/*

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

# Create a dedicated project to place all wiki (company-wide doc)
# NOTE: this project is created first such that its ID is always 1
curl --request POST --header "PRIVATE-TOKEN: root-token" \
     --header "Content-Type: application/json" --data '{
        "name": "Documentation", "description": "Wiki for company-wide doc", "path": "doc",
        "wiki_access_level": "enabled", "with_issues_enabled": "false",
        "with_merge_requests_enabled": "false",
        "visibility": "public"}' \
     --url "http://localhost:8929/api/v4/projects/"

curl --request POST --header "PRIVATE-TOKEN: root-token" \
     --header "Content-Type: application/json" --data '{
        "branch": "main", "author_email": "root@local", "author_name": "Administrator",
        "content": "Welcome to Documentation hub. Please navigate to [wiki](/wikis/home) to find all documentation.",
        "commit_message": "Add README"}' \
     --url "http://localhost:8929/api/v4/projects/1/repository/files/README.md"

# Import projects (please make sure they are available under local exports directory)
# this way, we can build and ship a GitLab image with pre-imported repos
if ls /assets/exports/*.tar.gz 1> /dev/null 2>&1; then
    for file in $(ls /assets/exports/*.tar.gz); do
        # Extract the filename without the path and extension
        filename=$(basename "$file" .tar.gz)

        echo "Importing $filename..."
        curl --request POST \
             --header "PRIVATE-TOKEN: root-token" \
             --form "path=$filename" \
             --form "file=@$file" \
             "http://localhost:8929/api/v4/projects/import"
    done
else
    echo "No .tar.gz file found in /assets/exports/. Nothing to import."
fi

echo "Finished importing all repos"

# Import wikis
if ls /assets/wikis/*.md 1> /dev/null 2>&1; then
    for file in $(ls /assets/wikis/*.md); do
        # Extract the filename without the path and extension
        title=$(basename "$file" .md)

        # Read the content of the file and URL encode it
        content=$(cat "$file" | jq -sRr @uri)

        curl --data "title=$title&content=$content" \
             --header "PRIVATE-TOKEN: root-token" \
             "http://localhost:8929/api/v4/projects/1/wikis"

        echo "Uploaded $title"
    done
else
    echo "No .md file found in /assets/wikis/. Nothing to import."
fi

# TODO: change authorship of issues/prs/commits

# Keep the container running
wait