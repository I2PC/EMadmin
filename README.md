

# EMadmin

EMadmin is a _short description_. It is built with [Python][0] using the [Django Web Framework][1].


## Installation

### Quick start

Start virtual enviroment (if developement) or just default python (production)

alias vir_emadmin='source /home/roberto/Scipion/webservices/EMadminVirt/bin/activate'
cd /home/roberto/Scipion/webservices/EMadmin
rm -rf */migrations
rm db.sqlite3 


for APPLICATION in */models.py
   do 
        echo $APPLICATION
        rm -rf $(dirname $APPLICATION)/migrations
   done
for APPLICATION in */models.py
   do 
        echo $APPLICATION
        python manage.py makemigrations $(dirname $APPLICATION)
   done

python manage.py makemigrations accounts create_proj create_report create_stat invoice profiles
python manage.py migrate
python manage.py runserver

To set up a development environment quickly, first install Python 3. It
comes with virtualenv built-in. So create a virtual env by:

    1. `$ python -m venv EMadmin`
    2. `$ . EMadmin/bin/activate`
    
NOTE: your virtualenv needs to be python 2

Install all dependencies:

    pip install -r requirements.txt

Run migrations:

    python manage.py migrate
python manage.py collectstatic

### Detailed instructions

start django

    python manage,py runserver
    
connect to server

   http://localhost:8000

DROP
 create_proj_adquisition2
   dose_per_frame
   dose_rate
   nominal_defocus
 create_proj_microscope
   dose_per_fraction
 invoce_concept
   * unit_proce_university
   * unitprice_empresa
 invoice_invoice
  * startDate
  * endDate
  * type
  * concept



   
