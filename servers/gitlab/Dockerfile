FROM gitlab/gitlab-ce:17.3.1-ce.0

# TODO: populate data

# create token "root-token" with sudo and api permissions
RUN gitlab-rails runner "token = User.find_by_username('root').personal_access_tokens.create(scopes: ['api', 'sudo', 'admin', 'read_user', 'read_api'], name: 'root token', expires_at: 365.days.from_now); token.set_token('root-token'); token.save!"

CMD ["/assets/wrapper"]