# Avita Ingram API Backend

Backend For Avita Ingram APIs and admin panel in python with Django Framework

## Setup

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Make sure you have `python3` and `virtualenv` installed on your system


### Installing

Clone the Repository and `cd` into it.


Create a new Virtual environment for the project

```
$ python -m virtualenv .venv
```

Install the requirements

```
$ pip install -r requirements.txt
```

Run the app

```
$ python manage.py runserver
```

## Project Settings

You can change this project's configuration in the `local_settings.py` file inside the `Avita_finance_API` sub folder.

#### Project Environment

For Production change the debug mode to `False` and add your server's IP into `ALLOWED_HOSTS`

```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['PRODUCTION_SERVER_IP',]
```

#### Database

Update your database configurations here. More details can be found [here](https://docs.djangoproject.com/en/3.0/intro/tutorial02/#database-setup).
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

#### Production Key

if you are deploying on a production environment consider changing the `SECRET_KEY` to a different one.

```python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'Your_Secret_Key_Here'
```

#### Email SMTP configuration

Update the Email server's SMTP configuration by modifying

```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 465
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_SSL = True
EMAIL_FROM = 'Avita<avita@example.com>'
```