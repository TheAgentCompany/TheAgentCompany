FROM gitlab/gitlab-ce:17.3.1-ce.0

COPY custom_wrapper.sh /assets/custom_wrapper.sh
RUN chmod +x /assets/custom_wrapper.sh

# Use the custom wrapper as the entrypoint
ENTRYPOINT ["/assets/custom_wrapper.sh"]