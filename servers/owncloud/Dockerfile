FROM owncloud:10.0.10

ENV OWNCLOUD_DOMAIN="localhost:8091"
ENV OWNCLOUD_TRUSTED_DOMAINS="localhost,localhost:8091"
ENV OWNCLOUD_ADMIN_USERNAME="theagentcompany"
ENV OWNCLOUD_ADMIN_PASSWORD="theagentcompany"

COPY ./init.sh /usr/local/bin
COPY ./owncloud_apps.tar.gz /var/www/html
COPY ./owncloud_data.tar.gz /var/www/html
RUN chmod +x /usr/local/bin/init.sh
RUN sh /usr/local/bin/init.sh
