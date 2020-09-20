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
export DEBUG=True/False
export SECRET_KEY=some_secret_key

# REQUIRED IF DEBUG=FALSE
export DB_NAME=some_database_name 
export DB_USERNAME=some_username
export DB_PASSWORD=some_password
export DB_HOST=some_host_address
export DB_PORT=some_port
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
./manage.py makemigrations
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
