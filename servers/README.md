# Intro

This directory contains code & configs needed to run all services,
including GitLab, ownCloud, Plane, and RocketChat. Below are the URLs, usernames,
and passwords for each service.

Caveat: `the-agent-company.com` is a real domain where we host the project website
with the leaderboard. For benchmarking purpose, all tasks assume this domain hosts
the services. Since this domain does not really host any of the following services,
you need to change your `/etc/hosts` file to point to your own server ip, if you'd like to use your browser to poke around the services. For evaluation
purpose, the hostname routing is taken care of by the initialization script.

<details>
  <summary>Mac and Linux users</summary>

Please run the following command:

```bash
echo "<server-ip> the-agent-company.com" | sudo tee -a /etc/hosts
# e.g. if you are hosting the services on your local machine, use
# echo "127.0.0.1 the-agent-company.com" | sudo tee -a /etc/hosts
```
</details>

<details>
    <summary>Windows users</summary>

Please use notepad or any other editor with admin privilege to open
`c:\Windows\System32\Drivers\etc\hosts` file and append `<server-ip> the-agent-company.com`
to the file. If you are hosting the services on your local machine, use
`127.0.0.1 the-agent-company.com`.

</details>

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

Use incognito mode to open the URLs.
