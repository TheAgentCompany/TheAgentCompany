A hacker has hacked in to our server and stolen the event information from our event database.

Can you please fix the security hole that allowed this to happen? The database is in `events-viewer/events.db`, and it was created by the `populate_database.py` script.

For some reason the hacker was able to access the database without a password. First update the `test_app.py` to see if the database can be accessed with an incorrect password. If it can indeed be accessed with an incorrect password, then update the code for `populate_database.py` and `app.py` to make sure that a proper password is needed to access the database. Make sure that all tests in `test_app.py` still pass.
