FROM gitlab/gitlab-ce:17.5.1-ce.0
RUN apt-get update && apt-get install -y jq && rm -rf /var/lib/apt/lists/*

ENV GITLAB_SKIP_TAIL_LOGS=true
ENV GITLAB_ROOT_EMAIL="root@local"
ENV GITLAB_ROOT_PASSWORD="theagentcompany"

# Copy start script and data to the image
COPY . /assets

# Start GitLab service, change configs and populate data during image build time
RUN chmod +x /assets/init.sh
RUN bash "/assets/init.sh"

# This is the original CMD used by gitlab-ce image
# During container run time, this will be executed to launch GitLab service
CMD ["/assets/wrapper"]
