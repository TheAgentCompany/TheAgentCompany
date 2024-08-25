# How to run
run `make run` to start the server

# How to backup
run `make backup` and in the local directory you will get `db.dump`

# How to restore
If you already have the `db.dump`, start the service and go to the directory where `db.dump` located. Run `make restore` then data will restore into the server.

# Default user
In `compose.yml` file, I already add admin into the cluster, which username is `jobbench`, password is `jobbench`, email is `jobbench@example.com`

# How to add new user
I tried to add user directly via admin user plane, but seems not work, it will require to do email verification. But If we directly register user in plane, it can work. The email address can be fake but cannot duplicated. When login, it will not require email verification.
```
ADMIN_USERNAME: jobbench
ADMIN_PASS: jobbench
ADMIN_EMAIL: jobbench@example.com
ADMIN_NAME: jobbench
```

# How to by pass the email verification
In dockerfile, I already added the following two line to bypass it
```
Show_Setup_Wizard: completed
OVERWRITE_SETTING_Show_Setup_Wizard: completed
```