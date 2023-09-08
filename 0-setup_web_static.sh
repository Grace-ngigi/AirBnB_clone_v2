#!/bin/bash

# Install Nginx if it's not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create the necessary directories
sudo mkdir -p /data/web_static/{releases/test,shared}
sudo touch /data/web_static/releases/test/index.html
sudo chown -R ubuntu:ubuntu /data/

# Create a fake HTML file
echo "This is a test HTML file." | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or recreate the symbolic link
sudo rm -f /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"
echo "server {
    listen 80;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
    }
    location / {
        proxy_pass http://localhost:5000; # Adjust this line if needed
    }
}" | sudo tee "$nginx_config" > /dev/null

# Restart Nginx
sudo service nginx restart

