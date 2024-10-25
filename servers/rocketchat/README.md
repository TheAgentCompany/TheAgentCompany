# How to run
Try make `start-rocketchat` under server directory. It will start at `http://localhost:3000` which is `http://ogma.lti.cs.cmu.edu:3000/` when you launch in server.

# How to backup
run `make backup` and in the local directory you will get `db.dump`

# How to restore
If you already have the `db.dump`, start the service and go to the directory where `db.dump` located. Run `make restore` then data will restore into the server.

# Default user
In `compose.yml` file, I already add admin into the cluster, which username is `theagentcompany`, password is `theagentcompany`, email is `theagentcompany@example.com`

# How to add new user
I tried to add user directly via admin user plane, but seems not work, it will require to do email verification. But If we directly register user in plane, it can work. The email address can be fake but cannot duplicated. When login, it will not require email verification.
```
ADMIN_USERNAME: theagentcompany
ADMIN_PASS: theagentcompany
ADMIN_EMAIL: theagentcompany@example.com
ADMIN_NAME: theagentcompany
```

# How to by pass the email verification
In dockerfile, I already added the following two line to bypass it
```
Show_Setup_Wizard: completed
OVERWRITE_SETTING_Show_Setup_Wizard: completed
```