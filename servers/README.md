# Intro

This directory contains code & configs needed to run all services,
including GitLab, NextCloud, Plane, and RocketChat. All services
are launched and running on CMU ogma server, but if you'd like
to launch them by yourself, please refer to [Development Guide](https://github.com/neulab/JobBench/blob/main/DEVELOPMENT.md).

Below are the addresses, usernames, and passwords for each service:

## GitLab
* service url: http://ogma.lti.cs.cmu.edu:8929/
* root email: `root@local`
* root password: `JobBench`

## NextCloud
* service url: https://ogma.lti.cs.cmu.edu/login
* username: admin
* password: 
    * If you use the backup in server: `e42a78e0ca1ca798d98827946cb271cb9e428d357069d547`
    * else try `make get-nextcloud-config` then check `secrets.NEXTCLOUD_PASSWORD`
* admin panel: https://ogma.lti.cs.cmu.edu:8090/
* backup: 
    * volume name: nextcloud_aio_backupdir
    * password: d352748d4845e6a70d0517c568b879d1e3dba54deb0b7e6c

## Plane:
* http://ogma.lti.cs.cmu.edu:8091
* email: job@bench.com
* password: jobbenchJobBench

## RocketChat
* http://ogma.lti.cs.cmu.edu:3000/
* email: jobbench
* password: jobbench

# Troubleshooting

## SSL Error

Note that only NextCloud is hosted on SSL-enabled address, starting with `https`.
Other services are only accessible via `http` protocol. Sometimes your browser
might force you to use `https`, and you would see SSL-related errors. In such cases,
you need to delete domain security policies. For example, if you are using Chrome,
you could visit `chrome://net-internals/#hsts` and make the following change:

![image](https://github.com/user-attachments/assets/a8657d53-313e-4b02-ac26-b551273f9277)

Now you should be able to use `http` protocol to visit the services.

