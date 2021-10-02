FROM python:3.6

RUN useradd -ms /bin/bash jbin

WORKDIR /home/jbin

COPY requirements.txt requirements.txt
RUN python -m venv env && \
 env/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY manage.py config.py boot.sh ./

#ENV FLASK_APP manage.py
RUN apt-get update && apt-get install -y cron
COPY explinks-crontab /etc/cron.d/explinks-crontab
RUN chmod 0644 /etc/cron.d/explinks-crontab &&\
    crontab /etc/cron.d/explinks-crontab

RUN chown -R jbin:jbin ./
USER jbin

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]