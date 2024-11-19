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

sed -i 's/NGINX_PORT=80/NGINX_PORT=8091/' $PLANE_INSTALL_DIR/plane.env
sed -i 's|${DOCKERHUB_USER:-makeplane}/plane-admin:${APP_RELEASE:-stable}|ghcr.io/theagentcompany/servers-plane-admin:0.0.1|g' $PLANE_INSTALL_DIR/docker-compose.yaml
sed -i 's|${DOCKERHUB_USER:-makeplane}/plane-backend:${APP_RELEASE:-stable}|ghcr.io/theagentcompany/servers-plane-backend:0.0.1|g' $PLANE_INSTALL_DIR/docker-compose.yaml
sed -i 's|${DOCKERHUB_USER:-makeplane}/plane-frontend:${APP_RELEASE:-stable}|ghcr.io/theagentcompany/servers-plane-frontend:0.0.1|g' $PLANE_INSTALL_DIR/docker-compose.yaml
sed -i 's|${DOCKERHUB_USER:-makeplane}/plane-space:${APP_RELEASE:-stable}|ghcr.io/theagentcompany/servers-plane-space:0.0.1|g' $PLANE_INSTALL_DIR/docker-compose.yaml
sed -i 's|${DOCKERHUB_USER:-makeplane}/plane-proxy:${APP_RELEASE:-stable}|ghcr.io/theagentcompany/servers-plane-proxy:0.0.1|g' $PLANE_INSTALL_DIR/docker-compose.yaml