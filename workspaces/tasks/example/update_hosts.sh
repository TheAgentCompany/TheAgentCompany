#!/bin/sh

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

BLOCKED_DOMAINS=${BLOCKED_DOMAINS:-"youtube.com reddit.com"}

cp /etc/hosts /etc/hosts.backup

for domain in $BLOCKED_DOMAINS; do
    if ! grep -q "$domain" /etc/hosts; then
        echo "127.0.0.1 $domain" >> /etc/hosts
        echo "127.0.0.1 www.$domain" >> /etc/hosts
        echo "Blocked: $domain"
    else
        echo "$domain is already in hosts file"
    fi
done

rm /etc/hosts.backup
echo "Hosts file updated successfully"