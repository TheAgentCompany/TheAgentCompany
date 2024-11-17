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