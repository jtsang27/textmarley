FROM python:3.11.5

RUN pip freeze > requirements.txt
RUN pip install -r requirements.txt

COPY src/ app/
WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :${PORT} --workers 1 --threads 8 app:app
