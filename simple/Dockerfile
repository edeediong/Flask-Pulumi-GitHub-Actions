FROM python:3.7.3-alpine

WORKDIR /server

COPY ./requirements.txt /server/requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]