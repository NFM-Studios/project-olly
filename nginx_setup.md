# NGINX setup instructions

### Note: This document assumes a Debian or Ubuntu system

## HTTP Setup

1. Install nginx by running `sudo apt install -y nginx`
2. Save the following to `/etc/nginx/sites-available/olly`. Be sure to replace `example.com` with your domain. (This should be the same as `ALLOWED_HOSTS` in `settings.py`.)
```nginx
server {
    listen 80;

    client_max_body_size 4G;
    server_name example.com;
    keepalive_timeout 5;
    root /var/www/static;

    location /static {
      alias /var/www/static;
    }

    location / {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header Host $http_host;
      proxy_redirect off;
      proxy_pass http://unix:/tmp/olly.sock;
    }
}
```
3.Create a symlink in the `sites-enabled` directory to the configuration file you just created `sudo ln -s /etc/nginx/sites-available/netbox /etc/nginx/sites-enabled` and restart nginx `sudo nginx -s reload`

## HTTPS setup with Let's Encrypt

After setting up nginx you will likely want to add HTTPS support

1. (Ubuntu only, if you are running Debian skip this step.) Run the following commands to add the certbot PPA
```bash
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
```
2. Install certbot `sudo apt install -y certbot python-certbot-nginx`
3. Configure certbot by running `sudo certbot --nginx` and following the prompts
