#!/bin/bash
set -e

APP_PATH="${APP_PATH:-$(pwd)}"
IMAGE_NAME="leather-ecommerce"
CONTAINER_NAME="leather-ecommerce"
NGINX_CONF_PATH="/etc/nginx/sites-available/leather-ecommerce"
NGINX_ENABLED_PATH="/etc/nginx/sites-enabled/leather-ecommerce"
DOMAIN="${DOMAIN:-www.goldhands.com}"

cd "$APP_PATH"

echo "Building Docker image..."
docker build -t "$IMAGE_NAME:latest" .

echo "Stopping existing container if present..."
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  docker stop "$CONTAINER_NAME" || true
  docker rm "$CONTAINER_NAME" || true
fi

echo "Starting container..."
docker run -d --restart unless-stopped -p 5000:5000 --name "$CONTAINER_NAME" "$IMAGE_NAME:latest"

echo "Configuring Nginx reverse proxy for domain: $DOMAIN"

sudo apt-get update -y
sudo apt-get install -y nginx

sudo bash -c "cat > $NGINX_CONF_PATH <<'EOF'
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF"

sudo ln -sf "$NGINX_CONF_PATH" "$NGINX_ENABLED_PATH"
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "Deployment complete. Visit http://$DOMAIN to access the site."
