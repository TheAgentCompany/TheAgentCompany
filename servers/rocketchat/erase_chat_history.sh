#!/bin/bash
# Calculate the date one year from now
FUTURE_DATE=$(date -d "+1 year" +%Y-%m-%d)
echo "Messages before $FUTURE_DATE will be deleted"

# Execute MongoDB commands in the Docker container
docker exec servers-mongodb-1 mongosh --eval "
  db = db.getSiblingDB('rocketchat');
  var futureDate = new Date('$FUTURE_DATE');
  db.rocketchat_message.deleteMany({ ts: { \$lt: futureDate } });
  print('Deletion completed');
"