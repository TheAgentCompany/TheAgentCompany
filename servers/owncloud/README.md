nano /etc/onlyoffice/documentserver/local.json
supervisorctl status

supervisorctl restart all

supervisorctl restart ds:converter
supervisorctl restart ds:docservice


http://collabora:9980

http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8091/index.php/apps/market/#/app/richdocuments