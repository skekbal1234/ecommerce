#!/bin/bash
set -e

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <ec2-user@host> <remote-path> [domain]"
  echo "Example: $0 ubuntu@1.2.3.4 /home/ubuntu/leather-ecommerce www.goldhands.com"
  exit 1
fi

REMOTE="$1"
REMOTE_PATH="$2"
DOMAIN="${3:-www.goldhands.com}"

echo "Preparing remote path: $REMOTE:$REMOTE_PATH"
ssh "$REMOTE" "mkdir -p '$REMOTE_PATH'"

echo "Copying project files to remote host..."
tar --exclude='.git' -czf - . | ssh "$REMOTE" "tar -xzf - -C '$REMOTE_PATH'"

echo "Running deploy script on remote host..."
ssh "$REMOTE" "cd '$REMOTE_PATH' && chmod +x deploy_ec2.sh && DOMAIN=$DOMAIN ./deploy_ec2.sh"

echo "Deployment complete. Visit http://$DOMAIN"
