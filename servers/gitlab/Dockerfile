FROM gitlab/gitlab-ce:17.3.1-ce.0
RUN apt-get update && apt-get install -y jq && rm -rf /var/lib/apt/lists/*

ENV GITLAB_SKIP_TAIL_LOGS=true
ENV GITLAB_ROOT_EMAIL="root@local"
ENV GITLAB_ROOT_PASSWORD="JobBench"

# Copy start script and data to the image
COPY . /assets

RUN chmod +x /assets/custom_wrapper.sh
CMD ["/assets/custom_wrapper.sh"]