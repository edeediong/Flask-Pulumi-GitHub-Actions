#!/bin/bash

sudo chown -R ubuntu:ubuntu /home/ubuntu/accure/
cd /home/ubuntu/accure

python3.6 -m venv accurevenv
source accurevenv/bin/activate
pip install -r requirements.txt

sudo cp -rf /home/ubuntu/accure/accure.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl start accure
echo "Accure Gunicorn has started."
sudo systemctl enable accure
echo "Accure Gunicorn has been enabled."

sudo systemctl status accure
sudo systemctl restart accure

sudo cp -rf /home/ubuntu/accure/nginx/accure /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/accure /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
