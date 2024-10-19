#!/bin/bash
# Execute MongoDB commands in the Docker container
# We will delete all user and all messages
docker exec servers-mongodb-1 mongosh --eval "
  db = db.getSiblingDB('rocketchat');
  db.rocketchat_message.deleteMany({});
  db.users.deleteMany({});
  print('Deletion completed');
"


# Keep the follow code in case we want to keep some message, then we can use the time to control message, but cannot control users
# Calculate the date one year from now
# FUTURE_DATE=$(date -d "+1 year" +%Y-%m-%d)
# echo "Messages before $FUTURE_DATE will be deleted"
# db.rocketchat_message.deleteMany({ ts: { \$lt: futureDate } });
