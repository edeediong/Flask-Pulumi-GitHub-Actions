#!/bin/bash

cd /home/ubuntu/accure

python3.6 -m venv accurevenv
source accurevenv/bin/activate
pip install -r requirements.txt

sudo cp -rf /home/ubuntu/accure/accure.service /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl start accure

echo "Gunicorn has started."

sudo systemctl enable accure

echo "Gunicorn has been enabled."

sudo systemctl status accure

sudo systemctl restart accure