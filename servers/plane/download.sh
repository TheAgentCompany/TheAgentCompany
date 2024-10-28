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
curl -H 'Cache-Control: no-cache, no-store' -s -o $PLANE_INSTALL_DIR/docker-compose.yaml https://raw.githubusercontent.com/makeplane/plane/599092d76b076c833afbe6f1c7233fc7d5f622c1/deploy/selfhost/docker-compose.yml
curl -H 'Cache-Control: no-cache, no-store' -s -o $PLANE_INSTALL_DIR/plane.env https://raw.githubusercontent.com/makeplane/plane/599092d76b076c833afbe6f1c7233fc7d5f622c1/deploy/selfhost/variables.env
curl -H 'Cache-Control: no-cache, no-store' -s -o $PLANE_INSTALL_DIR/restore.sh https://raw.githubusercontent.com/makeplane/plane/599092d76b076c833afbe6f1c7233fc7d5f622c1/deploy/selfhost/restore.sh

sed -i 's/NGINX_PORT=80/NGINX_PORT=8091/' $PLANE_INSTALL_DIR/plane.env

