#!/bin/sh

cd ~/accure

python3.6 -m venv accurevenv
source accurevenv/bin/activate
pip install -r requirements.txt

sudo cp -rf /home/ubuntu/accure/gunicorn.service /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl start gunicorn

echo "Gunicorn has started."

sudo systemctl enable gunicorn

echo "Gunicorn has been enabled."

sudo systemctl status gunicorn

sudo systemctl restart gunicorn