FROM python:3.8

RUN pip install pipenv

RUN mkdir -p /app
WORKDIR /app

COPY . .

RUN pipenv lock --requirements > requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait wait
RUN chmod +x wait

CMD ["sh", "-c", "./wait; python manage.py collectstatic --no-input; python manage.py makemigrations; python manage.py migrate; gunicorn monitoring.wsgi -b 0.0.0.0:8000"]
