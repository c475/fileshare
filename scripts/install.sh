apt-get -y update
apt-get -y upgrade
apt-get -y dist-upgrade
apt-get install -y build-essential
apt-get install -y nginx
apt-get install -y sqlite3
apt-get install -y python-dev
apt-get install -y python-pip
apt-get install -y libpq-dev
apt-get install -y libxml2-dev
apt-get install -y libxslt1-dev
apt-get install -y libldap2-dev
apt-get install -y libsasl2-dev
apt-get install -y libffi-dev
apt-get install -y redis-server
apt auto-remove

pip install --upgrade pip

git clone https://github.com/c475/fileshare.git /srv/

pip install -r /srv/requirements.txt

mkdir /var/log/gunicorn

#### SET UP CERTS BEFORE CROSSING THIS LINE ####

rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default
cp /srv/config/ytdjb.conf /etc/nginx/sites-enabled
systemctl enable nginx.service
systemctl restart nginx.service

sudo cp /srv/config/signaling_server.service /etc/systemd/system
sudo cp /srv/config/gunicorn.service /etc/systemd/system
sudo systemctl enable signaling_server.service
sudo systemctl enable gunicorn.service
sudo systemctl restart signaling_server.service
sudo systemctl restart gunicorn.service

sudo python /srv/manage.py collectstatic --noinput
sudo python /srv/manage.py makemigrations
sudo python /srv/manage.py migrate
