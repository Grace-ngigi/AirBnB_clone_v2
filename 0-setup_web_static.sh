#!/bin/bash

# Install Nginx if it's not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
    sudo service nginx start
fi

# Create the directories and give ownership
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared

# Create a fake HTML file
echo "<!DOCTYPE html>
<html>
<head>
<title>Deploying web static</title>
<head>
<body>
<h1>Deploying to two servers.</h1>
</body>" | sudo tee /data/web_static/releases/test/index.html

# Create or recreate the symbolic link
sudo rm -f /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# change ownership
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"
echo "server {
    listen 80 default_server;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current/;
    } 
}" | sudo tee "$nginx_config"
# Restart Nginx
sudo service nginx restart
# exit
exit
