# Hedger API

### Environment Setup

Python 3.8 required.

Run the following commands in the root project directory.

```
touch .env
```

In the file you just created, you will need to include the following:

```
# REQUIRED
export DEBUG=     # True/False
export SECRET_KEY=
export REDIS_HOST=
export REDIS_PORT=
export MARKETSTACK_ACCESS_KEY=

# REQUIRED IF DEBUG=FALSE
export DB_NAME=
export DB_USERNAME=
export DB_PASSWORD=
export DB_HOST=
export DB_PORT=
```

Install pipenv

```
pip install pipenv
```

Activate virtual environment and install packages

```
pipenv shell
pipenv install
```

### Database migrations

Run the following commands in the root project directory.

```
./manage.py migrate
```

### Running the server

```
./manage.py runserver
```

### Create user to access admin portal

Run the following command, and fill in your user information when prompted.

```
./manage.py createsuperuser
```

### Using Docker

A sample docker-compose configuration can be found below.

```
  api:
    build: [BUILD_DIRECTORY]
    ports:
      - 8000:8000
    environment:
      - DEBUG=False
      - SECRET_KEY=somesupersecretkey
      - DB_NAME=
      - DB_USERNAME=
      - DB_PASSWORD=
      - DB_HOST=
      - DB_PORT=
      - REDIS_HOST=
      - REDIS_PORT=
      - MARKETSTACK_ACCESS_KEY=
    restart: always
```
