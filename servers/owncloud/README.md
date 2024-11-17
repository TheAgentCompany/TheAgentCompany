nano /etc/onlyoffice/documentserver/local.json
supervisorctl status

supervisorctl restart all

supervisorctl restart ds:converter
supervisorctl restart ds:docservice


http://collabora:9980

download gallary
download pdf viewer

http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8091/index.php/apps/market/#/app/richdocuments

18.219.239.190

docker run -t -d -p 9980:9980 -e "extra_params=--o:ssl.enable=false" collabora/code
http://18.219.239.190:8091/index.php/apps/market/#/app/richdocuments

security cors:
http://18.219.239.190:8091	

http://host.docker.internal:9980

- OWNCLOUD_TRUSTED_DOMAINS=localhost the-agent-company.com
extra_hosts:
  - "host.docker.internal:host-gateway"
  - "the-agent-company.com:172.17.0.1"

docker exec -it owncloud bash
cd /var/www/html/config

============= pay attention, the following new added addres not include port

cat > config.php << 'EOL'
<?php
$CONFIG = array (
  'instanceid' => 'ocxfnq0ry514',
  'passwordsalt' => 'tUgNZKNGe4MI3oLwxHLhRpnG1i3kiE',
  'secret' => 'Xufclulrkw4XWQRgmwA1932yb9wN4lyRrdUjfRuhaHvaUorO',
  'trusted_domains' => 
  array (
    0 => '18.219.239.190:8091',
    1 => 'the-agent-company.com',
    2 => 'ec2-18-219-239-190.us-east-2.compute.amazonaws.com',
  ),
  'datadirectory' => '/var/www/html/data',
  'overwrite.cli.url' => 'http://18.219.239.190:8091',
  'dbtype' => 'sqlite3',
  'version' => '10.0.10.4',
  'logtimezone' => 'UTC',
  'installed' => true,
);
EOL

exit

docker restart owncloud
docker exec -it owncloud bash


========================= How to update the file
in the contianer: 
cd /var/www/html
su -s /bin/bash www-data -c "php occ files:scan --all"

```
Scanning files for 1 users
Starting scan for user 1 out of 1 (theagentcompany)

+---------+-------+--------------+------------------+
| Folders | Files | Elapsed time | Items per second |
+---------+-------+--------------+------------------+
| 5       | 5     | 00:00:00     | 167              |
+---------+-------+--------------+------------------+
```


============================ change collabora url
cd /var/www/html
su -s /bin/bash www-data -c "php occ config:app:set richdocuments wopi_url --value=http://192.168.0.161:9980"

```
Config value wopi_url for app richdocuments set to http://192.168.0.161:9980
```

======================== data 
docker cp owncloud:/var/www/html/data/theagentcompany ./owncloud_data && tar -czf owncloud_data.tar.gz owncloud_data && rm -rf owncloud_data

docker exec owncloud sh -c 'rm -rf /var/www/html/data/theagentcompany/*'
tar -xzf owncloud_data.tar.gz && docker cp ./owncloud_data/. owncloud:/var/www/html/data/theagentcompany && rm -rf owncloud_data
docker exec owncloud sh -c 'chmod -R 777 /var/www/html/data/theagentcompany'

================== apps
docker cp owncloud:/var/www/html/apps ./owncloud_apps && tar -czf owncloud_apps.tar.gz owncloud_apps && rm -rf owncloud_apps

docker exec owncloud sh -c 'rm -rf /var/www/html/apps/*'
tar -xzf owncloud_apps.tar.gz && docker cp ./owncloud_apps/. owncloud:/var/www/html/apps && rm -rf owncloud_apps
