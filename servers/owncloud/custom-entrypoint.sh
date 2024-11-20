#!/bin/bash

# 运行原始的 apache2-foreground 命令
apache2-foreground &

# 等待 ownCloud 启动
sleep 5

# 使用 OCC 命令行工具创建用户
if [ ! -f /var/www/html/config/config.php ]; then
    cd /var/www/html
    sudo -u www-data php occ maintenance:install \
        --database "sqlite" \
        --admin-user "$OWNCLOUD_ADMIN_USERNAME" \
        --admin-pass "$OWNCLOUD_ADMIN_PASSWORD"

    # 设置trusted domains
    sudo -u www-data php occ config:system:set trusted_domains 1 --value=the-agent-company.com:8091
fi

# 保持容器运行
tail -f /dev/null




su -s /bin/bash www-data -c  'php occ maintenance:install \
        --database "sqlite" \
        --admin-user "$OWNCLOUD_ADMIN_USERNAME" \
        --admin-pass "$OWNCLOUD_ADMIN_PASSWORD"'
        
su -s /bin/bash www-data -c  "php occ config:system:set trusted_domains 1 --value=the-agent-company.com"
docker restart owncloud


curl -X POST "http://the-agent-company.com:8091/index.php/index.php" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "install=true" \
  -d "adminlogin=theagentcompany" \
  -d "adminpass=theagentcompany" \
  -d "adminpass-clone=theagentcompany" \
  -d "directory=/var/www/html/data" \
  -d "dbtype=sqlite" \
  -d "dbhost=localhost"


docker rmi owncloud:test || true && docker build -t owncloud:test .

docker run -d --name owncloud -p 8080:80 owncloud:test
docker build -t owncloud:test .
BUILDKIT_PROGRESS=plain docker build --no-cache --progress=plain -t owncloud:test .