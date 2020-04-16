FROM python:3.6

RUN adduser -D jbin

WORKDIR /home/jbin

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