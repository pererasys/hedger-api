# Hedger API

### Install dependencies

Run the following commands in the root project directory.

Install pipenv

```
pip install pipenv
```

Activate virtual environment and install packages
```
pipenv shell
pipenv install
```

### Running the server

```
./src/manage.py runserver
```

### Database migrations

Run the following commands in the root project directory.

```
./src/manage.py makemigrations
./src/manage.py migrate
```

### Create user to access admin portal

Run the following command, and fill in your user information when prompted.

```
./src/manage.py createsuperuser
```
