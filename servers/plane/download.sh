#!/bin/sh
set -eu

# Plane is deployed from inside the API-server image, which does not contain
# the source repository metadata. Resolve the install directory from this file.
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PLANE_INSTALL_DIR="$SCRIPT_DIR/plane-app"
mkdir -p "$PLANE_INSTALL_DIR"

TEMP_DIR=$(mktemp -d "$PLANE_INSTALL_DIR/.download.XXXXXX")
trap 'rm -rf "$TEMP_DIR"' EXIT HUP INT TERM

curl -fsSL -H 'Cache-Control: no-cache, no-store' \
    -o "$TEMP_DIR/docker-compose.yaml" \
    https://raw.githubusercontent.com/TheAgentCompany/plane/refs/heads/stable/deploy/selfhost/docker-compose.yml
curl -fsSL -H 'Cache-Control: no-cache, no-store' \
    -o "$TEMP_DIR/plane.env" \
    https://raw.githubusercontent.com/TheAgentCompany/plane/refs/heads/stable/deploy/selfhost/variables.env
curl -fsSL -H 'Cache-Control: no-cache, no-store' \
    -o "$TEMP_DIR/restore.sh" \
    https://raw.githubusercontent.com/TheAgentCompany/plane/refs/heads/stable/deploy/selfhost/restore-customized.sh

chmod +x "$TEMP_DIR/restore.sh"
mv "$TEMP_DIR/docker-compose.yaml" "$PLANE_INSTALL_DIR/docker-compose.yaml"
mv "$TEMP_DIR/plane.env" "$PLANE_INSTALL_DIR/plane.env"
mv "$TEMP_DIR/restore.sh" "$PLANE_INSTALL_DIR/restore.sh"
