nano /etc/onlyoffice/documentserver/local.json
supervisorctl status

supervisorctl restart all

supervisorctl restart ds:converter
supervisorctl restart ds:docservice