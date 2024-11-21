# This file try to download the necessary file when using plane to avoid license problem
# The backup data should manually put under this directory

ROOT_PATH=$(git rev-parse --show-toplevel)
PLANE_INSTALL_DIR=$ROOT_PATH/servers/plane/plane-app
BRANCH=master

echo $PLANE_INSTALL_DIR

if [ ! -d "$PLANE_INSTALL_DIR" ]; then
    echo "Directory $PLANE_INSTALL_DIR does not exist. Creating it."
    mkdir -p $PLANE_INSTALL_DIR
fi

rm -rf $PLANE_INSTALL_DIR/docker-compose.yml
rm -rf $PLANE_INSTALL_DIR/plane.env
rm -rf $PLANE_INSTALL_DIR/restore.sh

# v0.22-dev
# Aug 30 2024 latest commit
curl -H 'Cache-Control: no-cache, no-store' -s -o $PLANE_INSTALL_DIR/docker-compose.yaml https://raw.githubusercontent.com/TheAgentCompany/plane/refs/heads/stable/deploy/selfhost/docker-compose.yml
curl -H 'Cache-Control: no-cache, no-store' -s -o $PLANE_INSTALL_DIR/plane.env https://raw.githubusercontent.com/TheAgentCompany/plane/refs/heads/stable/deploy/selfhost/variables.env
curl -H 'Cache-Control: no-cache, no-store' -s -o $PLANE_INSTALL_DIR/restore.sh https://raw.githubusercontent.com/TheAgentCompany/plane/refs/heads/stable/deploy/selfhost/restore.sh

chmod 777 $PLANE_INSTALL_DIR/docker-compose.yaml
chmod 777 $PLANE_INSTALL_DIR/plane.env
chmod 777 $PLANE_INSTALL_DIR/restore.sh
