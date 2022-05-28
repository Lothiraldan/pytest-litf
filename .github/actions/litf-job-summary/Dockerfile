FROM python:3

ADD . /app
WORKDIR /app

RUN python -m pip install -U pip

RUN python -m pip install -r /app/requirements.txt

CMD ["/usr/local/bin/python", "/app/main.py"]