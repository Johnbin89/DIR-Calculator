FROM python:3.10

#RUN useradd -ms /bin/bash jbin

WORKDIR /home/jbin
RUN apt-get update && apt-get install -y cron

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY explinks-crontab manage.py config.py boot.sh .flaskenv ./

RUN chmod +x boot.sh
ENV FLASK_APP manage.py

#RUN chown -R jbin:jbin .
#USER jbin

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]