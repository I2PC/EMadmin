

# EMadmin

EMadmin is a web tool designed to use scipion software at microscopy facilities. It is built with Python using the Django Web Framework.

## Installation

Create a Python 3 virtual environment, activate it and install all dependencies (make sure your pip installation is upgraded):

```
cd EMadmin
python3 -m venv ./venv
source venv/bin/activate
cd EMadmin
pip install --upgrade pip
pip install -r requirements.txt
```

Then, make and run migrations, create a superuser and launch the server on a free port:

```
cd src
python manage.py makemigrations accounts create_proj create_report create_stat invoice profiles
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

Finally, you can connect to the server at http://localhost:8000