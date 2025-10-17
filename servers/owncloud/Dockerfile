FROM owncloud:10.0.10

ENV OWNCLOUD_DOMAIN="localhost:8091"
ENV OWNCLOUD_TRUSTED_DOMAINS="localhost,localhost:8091"
ENV OWNCLOUD_ADMIN_USERNAME="theagentcompany"
ENV OWNCLOUD_ADMIN_PASSWORD="theagentcompany"

COPY ./init.sh /usr/local/bin
# In the base owncloud image, /var/www/html is declared as VOLUME.
# To seed initial data and apps, we copy them to a different location (/opt/seed)
COPY ./owncloud_apps /opt/seed/owncloud_apps
COPY ./owncloud_data /opt/seed/owncloud_data
RUN chmod +x /usr/local/bin/init.sh
CMD ["/usr/local/bin/init.sh"]