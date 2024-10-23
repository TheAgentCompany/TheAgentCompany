# Intro

This directory contains code & configs needed to run all services,
including GitLab, NextCloud, Plane, and RocketChat. All services
are launched and running on CMU ogma server, but if you'd like
to launch them by yourself, please refer to [Development Guide](https://github.com/neulab/TheAgentCompany/blob/main/DEVELOPMENT.md).

Below are the addresses, usernames, and passwords for each service:

## GitLab
* service url: http://ogma.lti.cs.cmu.edu:8929/
* root email: `root@local`
* root password: `JobBench`

## NextCloud
* service url: https://ogma.lti.cs.cmu.edu/login
* username: admin
* password: 
    * current password `cf6a70e7fbef0dc2f6e8c48369b30ab8357b3c10063f5fbe`
    * if out of date, try `make get-nextcloud-config` then check `secrets.NEXTCLOUD_PASSWORD`

## Plane
* http://ogma.lti.cs.cmu.edu:8091
* email:`job@bench.com`
* password:`jobbenchJobBench`
* API_KEY:`plane_api_569b8e604e0c46d0b65ef56bb9e76f03`

## RocketChat
* http://ogma.lti.cs.cmu.edu:3000/
* email: theagentcompany
* password: theagentcompany

# Troubleshooting

## SSL Error

### Solution 1 (Recommend):
The hosts trick actually work arounds the https problem.

Add `128.2.205.27 the-agent-company.com` to your `/etc/hosts` file and then you can start using http://the-agent-company.com:8929/ in your browser.

Note: for NextCloud you still have to use https://ogma.lti.cs.cmu.edu as of now.

This is a useful for Linux/Mac, Windows user should find the similar way to change your DNS.

### Solution 2:

Note that only NextCloud is hosted on SSL-enabled address, starting with `https`.
Other services are only accessible via `http` protocol. Sometimes your browser
might force you to use `https`, and you would see SSL-related errors. 
In such cases,
you need to delete domain security policies. For example, if you are using Chrome,
you could visit `chrome://net-internals/#hsts` and make the following change to remove the domain from the list by entering domain name under *Delete domain security policies* and press the Delete button:

![image](https://github.com/user-attachments/assets/a8657d53-313e-4b02-ac26-b551273f9277)

Then, go to chrome://settings/clearBrowserData, tick *only* the box Cached images and files and press click the button Clear data.


Now you should be able to use `http` protocol to visit the services.

### Solution 3:
Open chrome://settings/security and disable "Always use secure connections". It will disable the redirect in ALL web url.

### Solution 4:
* When use open the web using chrome, it will show `Not Secure` beside the url. 
* Click it, select the "site settings". 


<img src="https://github.com/user-attachments/assets/24452c97-f16d-444b-9b24-3bb733622a24" width="300" alt="image">



* Set `Insecure Content` into allow. It will disable the redirect only in this web url.

<img src="https://github.com/user-attachments/assets/e552b6ff-b2c5-408a-930a-8afef3927940" width="300" alt="image">
