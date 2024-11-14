#!/bin/bash

# Check if SERVER_HOSTNAME is set
if [ -z "$SERVER_HOSTNAME" ]; then
    echo "Error: SERVER_HOSTNAME environment variable is not set"
    exit 1
fi

# Stop nginx if it's running
if [ -f /var/run/nginx.pid ]; then
    nginx -s stop || true
    rm -f /var/run/nginx.pid
fi

# Remove default nginx configuration
rm -f /etc/nginx/sites-enabled/default

echo "127.0.0.1 the-agent-company.com" >> /etc/hosts

# Create SSL directory if it doesn't exist
mkdir -p /etc/nginx/ssl
cd /etc/nginx/ssl

# Generate self-signed certificate and key
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout the-agent-company.com.key -out the-agent-company.com.crt \
-subj "/CN=the-agent-company.com"

# Set proper permissions
chmod 644 the-agent-company.com.crt
chmod 600 the-agent-company.com.key

# Create the main configuration
cat > /etc/nginx/conf.d/the-agent-company.conf << EOF
# Forward HTTP to HTTPS for main domain
server {
    listen 80;
    listen [::]:80;
    server_name the-agent-company.com;
    return 301 https://\$host\$request_uri;
}

# Main HTTPS server block
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name the-agent-company.com;

    error_log /var/log/nginx/error.log debug;
    access_log /var/log/nginx/access.log combined;

    ssl_certificate /etc/nginx/ssl/the-agent-company.com.crt;
    ssl_certificate_key /etc/nginx/ssl/the-agent-company.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    proxy_ssl_protocols TLSv1.2 TLSv1.3;
    proxy_ssl_ciphers HIGH:!aNULL:!MD5;
    proxy_ssl_trusted_certificate /etc/ssl/certs/ca-certificates.crt;
    proxy_ssl_verify off;
    proxy_ssl_server_name on;

    location / {
        proxy_pass https://${SERVER_HOSTNAME};
        proxy_set_header Host ${SERVER_HOSTNAME};
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Websocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Buffer settings
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }

    # Custom error page for debugging
    error_page 502 = @fallback;

    location @fallback {
        return 502 'Bad Gateway Error. Remote host: ${SERVER_HOSTNAME}\n';
        add_header Content-Type text/plain always;
    }
}

# HTTP-only ports
server {
    listen 8929;
    listen [::]:8929;
    server_name the-agent-company.com;
    
    location / {
        proxy_pass http://${SERVER_HOSTNAME}:8929;
        include /etc/nginx/conf.d/proxy-settings.inc;
    }
}

server {
    listen 3000;
    listen [::]:3000;
    server_name the-agent-company.com;
    
    location / {
        proxy_pass http://${SERVER_HOSTNAME}:3000;
        include /etc/nginx/conf.d/proxy-settings.inc;
    }
}

server {
    listen 2999;
    listen [::]:2999;
    server_name the-agent-company.com;
    
    location / {
        proxy_pass http://${SERVER_HOSTNAME}:2999;
        include /etc/nginx/conf.d/proxy-settings.inc;
    }
}

server {
    listen 8091;
    listen [::]:8091;
    server_name the-agent-company.com;
    
    location / {
        proxy_pass http://${SERVER_HOSTNAME}:8091;
        include /etc/nginx/conf.d/proxy-settings.inc;
    }
}

# HTTPS for port 8080
server {
    listen 8080;
    listen [::]:8080;
    server_name the-agent-company.com;
    return 301 https://\$host:8443\$request_uri;
}

server {
    listen 8443 ssl http2;
    listen [::]:8443 ssl http2;
    server_name the-agent-company.com;
    
    ssl_certificate /etc/nginx/ssl/the-agent-company.com.crt;
    ssl_certificate_key /etc/nginx/ssl/the-agent-company.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass https://${SERVER_HOSTNAME}:8443;
        include /etc/nginx/conf.d/proxy-settings.inc;
    }
}
EOF

# Create the proxy settings include file
cat > /etc/nginx/conf.d/proxy-settings.inc << EOF
proxy_set_header Host ${SERVER_HOSTNAME};
proxy_set_header X-Real-IP \$remote_addr;
proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto \$scheme;

proxy_http_version 1.1;
proxy_set_header Upgrade \$http_upgrade;
proxy_set_header Connection "upgrade";

proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;

proxy_buffer_size 128k;
proxy_buffers 4 256k;
proxy_busy_buffers_size 256k;

resolver 8.8.8.8 valid=30s;
EOF

# Create required directories for nginx
mkdir -p /var/log/nginx
mkdir -p /var/run

# Add certificate to trusted roots
cp /etc/nginx/ssl/the-agent-company.com.crt /usr/local/share/ca-certificates/
update-ca-certificates 2>/dev/null

# Test the configuration
nginx -t

# If test is successful, start nginx
if [ $? -eq 0 ]; then
    # Remove old pid file if it exists
    rm -f /var/run/nginx.pid
    
    # Start nginx fresh
    nginx
    
    echo "Configuration updated and nginx started successfully"
else
    echo "Error in nginx configuration"
    exit 1
fi