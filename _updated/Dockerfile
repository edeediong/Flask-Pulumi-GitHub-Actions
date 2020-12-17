FROM python:3.7.9-alpine

LABEL "Edidiong Etuk" edeediong@gmail.com

WORKDIR /server

COPY ./config/development/requirements.txt /server/requirements.txt

RUN pip install -r requirements.txt

COPY ./app /server/app
COPY ./tests /server/tests
COPY ./Makefile ./Makefile
COPY run.py shell.py ./

RUN make test

ENTRYPOINT [ "make" ]

CMD [ "server" ]