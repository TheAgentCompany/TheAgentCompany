#!/bin/sh
set -e

# Initialize variables to track total wait time and which services need resetting
# TODO (yufansong): make this script more robust by making the api-server itself
# wait until all resets are complete. A websocket solution might be needed.
# Alternatively, a more robust healthcheck endpoint might be needed.
total_wait=0
reset_services=()

# Check for each service using grep
if grep -q "rocketchat" /utils/dependencies.yml; then
    echo "Resetting rocketchat..."
    curl -X POST "http://the-agent-company.com:2999/api/reset-rocketchat"
    reset_services+=("rocketchat")
    if [ $total_wait -lt 120 ]; then
        total_wait=120
    fi
fi

if grep -q "plane" /utils/dependencies.yml; then
    echo "Resetting plane..."
    curl -X POST "http://the-agent-company.com:2999/api/reset-plane"
    reset_services+=("plane")
    if [ $total_wait -lt 1=360 ]; then
        total_wait=360
    fi
fi

if grep -q "gitlab" /utils/dependencies.yml; then
    echo "Resetting gitlab..."
    curl -X POST "http://the-agent-company.com:2999/api/reset-gitlab"
    reset_services+=("gitlab")
    if [ $total_wait -lt 600 ]; then
        total_wait=600
    fi
fi

if grep -q "nextcloud" /utils/dependencies.yml; then
    echo "Resetting nextcloud..."
    curl -X POST "http://the-agent-company.com:2999/api/reset-nextcloud"
    reset_services+=("nextcloud")
    if [ $total_wait -lt 120 ]; then
        total_wait=120
    fi
fi

# If any services were reset, wait the required time
if [ ${#reset_services[@]} -gt 0 ]; then
    echo "Reset initiated for services: ${reset_services[*]}"
    echo "Waiting for $total_wait seconds..."
    sleep $total_wait
    echo "All resets completed"
else
    echo "No matching services found in dependencies.yml"
fi