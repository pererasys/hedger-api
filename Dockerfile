FROM python:3.8

RUN pip install pipenv

RUN mkdir -p /app
WORKDIR /app

COPY . .

RUN pipenv lock --requirements > requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --no-input; python manage.py makemigrations; python manage.py migrate; gunicorn hedger.wsgi -b 0.0.0.0:8000"]
