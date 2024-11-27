sh /usr/local/bin/docker-entrypoint.sh 
apache2-foreground &
sleep 3
curl -X POST "http://localhost/index.php/index.php" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "install=true" \
  -d "adminlogin=theagentcompany" \
  -d "adminpass=theagentcompany" \
  -d "adminpass-clone=theagentcompany" \
  -d "directory=/var/www/html/data" \
  -d "dbtype=sqlite" \
  -d "dbhost=localhost"

cd /var/www/html
su -s /bin/bash www-data -c  "php occ config:system:set trusted_domains 1 --value=the-agent-company.com"
su -s /bin/bash www-data -c "php occ config:app:set richdocuments wopi_url --value=http://the-agent-company.com:9980"

rm -rf /var/www/html/data/theagentcompany/*
rm -rf /var/www/html/apps

cp -r /var/www/html/owncloud_data/. /var/www/html/data/theagentcompany
mv /var/www/html/owncloud_apps /var/www/html/apps

chmod -R 777 /var/www/html/data/theagentcompany
chmod -R 777 /var/www/html/apps

rm -rf /var/www/html/owncloud_data
rm -rf /var/www/html/owncloud_apps

su -s /bin/bash www-data -c "php occ app:enable richdocuments"
su -s /bin/bash www-data -c "php occ app:enable gallery"
su -s /bin/bash www-data -c "php occ app:enable files_pdfviewer"
su -s /bin/bash www-data -c "php occ app:enable files_texteditor"
su -s /bin/bash www-data -c "php occ app:enable files_textviewer"
su -s /bin/bash www-data -c "php occ app:enable files_videoplayer"
su -s /bin/bash www-data -c "php occ app:enable music"
su -s /bin/bash www-data -c "php occ files:scan --all"