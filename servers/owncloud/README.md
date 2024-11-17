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

docker exec -it 4616b8eaa768 bash
docker restart 4616b8eaa768
cd /var/www/html/config



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

