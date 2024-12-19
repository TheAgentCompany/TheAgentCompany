# Intro

This directory contains code & configs needed to run all services,
including GitLab, ownCloud, Plane, and RocketChat.

Below are the URLs, usernames, and passwords for each service. Note that you must
add `<server-ip> the-agent-company.com` to your `/etc/hosts` file, since
we use the synthetic hostname `the-agent-company.com` everywhere among all tasks.
You could use `127.0.0.1` as the server ip if your services are running locally.

Caveat: `the-agent-company.com` is a real domain where we host the project website
with the leaderboard. For benchmarking purpose, all tasks assume this domain hosts
the services. Since this domain does not really host any of the following services,
you need to change your `/etc/hosts` file to point to your own server ip, if and
only if you'd like to use your browser to poke around the services. For evaluation
purpose, the hostname routing is taken care of by the initialization script.

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

## RocketChat
* service url: http://the-agent-company.com:3000
* email: `theagentcompany`
* password: `theagentcompany`

# Troubleshooting

## SSL Error

Some modern browsers (e.g., Chrome) have strict security policies that block insecure connections. You
might not be able to visit the services using `http` protocol directly.

### Solution 1:
Open chrome://settings/security and disable "Always use secure connections". It will disable the redirect in ALL web url.

### Solution 2:
* When use open the web using chrome, it will show `Not Secure` beside the url. 
* Click it, select the "site settings". 


<img src="https://github.com/user-attachments/assets/24452c97-f16d-444b-9b24-3bb733622a24" width="300" alt="image">

* Set `Insecure Content` into allow. It will disable the redirect only in this web url.

<img src="https://github.com/user-attachments/assets/e552b6ff-b2c5-408a-930a-8afef3927940" width="300" alt="image">

### Solution 3:

Use incognito mode to open the URLs.
