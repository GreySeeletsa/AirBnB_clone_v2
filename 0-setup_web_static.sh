#!/usr/bin/env bash
# set my web servers for deployment of the web_static

echo -e "\e[1;32m START\e[0m"

#--Update packages
sudo apt-get -y update
sudo apt-get -y install nginx
echo -e "\e[1;32m Packages updated\e[0m"
echo

#--configures the firewall
sudo ufw allow 'Nginx HTTP'
echo -e "\e[1;32m Allow incomming NGINX HTTP connections\e[0m"
echo

#--creating a dir
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
echo -e "\e[1;32m directories created"
echo

#--add the test string
echo "<h1>Welcome to www.bryson-nyamwange.tech</h1>" > /data/web_static/releases/test/index.html
echo -e "\e[1;32m Test string added\e[0m"
echo

#--preventing overwrite
if [ -d "/data/web_static/current" ];
then
    echo "path /data/web_static/current exists"
    sudo rm -rf /data/web_static/current;
fi;
echo -e "\e[1;32m prevent overwrite\e[0m"
echo

#--creating a symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data

sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

sudo ln -sf '/etc/nginx/sites-available/default' '/etc/nginx/sites-enabled/default'
echo -e "\e[1;32m Symbolic link created\e[0m"
echo

#--restarting NGINX
sudo service nginx restart
echo -e "\e[1;32m restart NGINX\e[0m"
