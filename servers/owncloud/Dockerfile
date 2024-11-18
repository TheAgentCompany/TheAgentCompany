FROM owncloud:10.0.10

ENV OWNCLOUD_DOMAIN="localhost:8091"
ENV OWNCLOUD_TRUSTED_DOMAINS="localhost,localhost:8091"
ENV OWNCLOUD_ADMIN_USERNAME="theagentcompany"
ENV OWNCLOUD_ADMIN_PASSWORD="theagentcompany"

COPY ./init.sh /usr/local/bin
COPY ./owncloud_apps /var/www/html/owncloud_apps
COPY ./owncloud_data /var/www/html/owncloud_data
RUN chmod +x /usr/local/bin/init.sh
RUN sh /usr/local/bin/init.sh
