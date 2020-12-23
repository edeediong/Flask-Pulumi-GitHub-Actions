#!/bin/sh

cd aws-codedeploy/
python3.6 -m venv accure
source accure/bin/activate
pip install -r requirements.txt

sudo cp -rf aws-codedeploy/gunicorn.service /etc/systemd/system/

sudo systemctl daemon-reload

sudo systemctl start gunicorn

echo "Gunicorn has started."

sudo systemctl enable gunicorn

echo "Gunicorn has been enabled."

sudo systemctl status gunicorn

sudo systemctl restart gunicorn