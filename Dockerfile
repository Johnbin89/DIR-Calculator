FROM python:3.6-alpine

RUN adduser -D jbin

WORKDIR /home/jbin

RUN apt-get update && \
 apt-get -y install gcc

COPY requirements.txt requirements.txt
RUN python -m venv env && \
 env/bin/pip install -r requirements.txt
#RUN venv/bin/pip install gunicorn

COPY app app
#COPY migrations migrations
COPY manage.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R jbin:jbin ./
USER jbin

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]