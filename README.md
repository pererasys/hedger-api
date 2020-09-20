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
