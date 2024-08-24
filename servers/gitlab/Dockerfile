FROM gitlab/gitlab-ce:17.3.1-ce.0

ENV GITLAB_OMNIBUS_CONFIG="external_url 'http://ogma.lti.cs.cmu.edu:8929'; gitlab_rails['gitlab_shell_ssh_port'] = 2424"

EXPOSE 8929 443 2424

# TODO: populate data

CMD ["/assets/wrapper"]