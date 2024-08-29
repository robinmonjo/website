apt update
apt install nginx -y
systemctl enable nginx
systemctl start nginx

cp nginx.conf /etc/nginx/sites-available/www.hellorob.in.conf
ln -s /etc/nginx/sites-available/www.hellorob.in.conf /etc/nginx/sites-enabled/
systemctl reload nginx

apt install certbot python3-certbot-nginx -y
certbot

# then follow instructions, certbot will change nginx conf file

## On the 2 listen directive, add http2 at the end to enable http2:
# listen [::]:443 ssl ipv6only=on http2; # managed by Certbot
# listen 443 ssl http2; # managed by Certbot

# auto-renew certificate
systemctl status certbot.timer
