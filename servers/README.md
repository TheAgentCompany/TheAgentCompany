# Intro

This directory contains code & configs needed to run all services,
including GitLab, ownCloud, Plane, and RocketChat. All services
are launched and running on CMU ogma server, but if you'd like
to launch them by yourself, please refer to [Development Guide](../docs/DEVELOPMENT.md).

Below are the addresses, usernames, and passwords for each service. Note that you must
add `<server-ip> the-agent-company.com` to your `/etc/hosts` file. For example, `128.2.205.27`
is the IP address of ogma.lti.cs.cmu.edu.

## GitLab
* service url: http://the-agent-company.com:8929
* root email: `root@local`
* root password: `theagentcompany`

## ownCloud
* service url: http://the-agent-company.com:8092
* username: `theagentcompany`
* password: `theagentcompany`

## Plane
* service url: http://the-agent-company.com:8091
* email: `agent@company.com`
* password: `theagentcompany`
* API_KEY:`plane_api_83f868352c6f490aba59b869ffdae1cf`
* If the API_KEY not work, ping @Yufan Song. And feel free to follow [here](https://developers.plane.so/api-reference/introduction) to create your temporary key to develop. We will always reset the server, so your temporary key may be deleted sometime after reset.

## RocketChat
* service url: http://the-agent-company.com:3000
* email: `theagentcompany`
* password: `theagentcompany`

# Troubleshooting

## SSL Error

### Solution 1:

All services are only accessible via `http` protocol. Sometimes your browser
might force you to use `https`, and you would see SSL-related errors. 
In such cases,
you need to delete domain security policies. For example, if you are using Chrome,
you could visit `chrome://net-internals/#hsts` and make the following change to remove the domain from the list by entering domain name under *Delete domain security policies* and press the Delete button:

![image](https://github.com/user-attachments/assets/a8657d53-313e-4b02-ac26-b551273f9277)

Then, go to chrome://settings/clearBrowserData, tick *only* the box Cached images and files and press click the button Clear data.


Now you should be able to use `http` protocol to visit the services.

### Solution 2:
Open chrome://settings/security and disable "Always use secure connections". It will disable the redirect in ALL web url.

### Solution 3:
* When use open the web using chrome, it will show `Not Secure` beside the url. 
* Click it, select the "site settings". 


<img src="https://github.com/user-attachments/assets/24452c97-f16d-444b-9b24-3bb733622a24" width="300" alt="image">



* Set `Insecure Content` into allow. It will disable the redirect only in this web url.

<img src="https://github.com/user-attachments/assets/e552b6ff-b2c5-408a-930a-8afef3927940" width="300" alt="image">
