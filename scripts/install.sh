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

cp /srv/config/crossbar.service /etc/systemd/system
cp /srv/config/gunicorn.service /etc/systemd/system
