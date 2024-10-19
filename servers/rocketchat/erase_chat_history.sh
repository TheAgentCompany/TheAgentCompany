#!/bin/bash

# Create a variable for the future date (1 year from now)
FUTURE_DATE=$(date -d "+1 year" +%Y-%m-%d)

# Connect to the MongoDB Docker container and run commands
docker exec servers-mongodb-1 bash << EOF
# Use mongosh instead of mongo for newer versions
mongosh << EOL
use rocketchat

// Delete messages before the future date
var result = db.rocketchat_message.deleteMany({ ts: { \$lt: ISODate("2025-10-19") } });

// Show the number of deleted messages
print("The number of messages deleted: " + result.deletedCount);

// Exit the MongoDB shell
exit
EOL
EOF

echo "Script execution completed."
