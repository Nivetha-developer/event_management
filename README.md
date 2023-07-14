## Fixxer | Backend
Django rest framework

### Installation 
First ensure you have python globally installed in your computer. If not, you can get python [here](https://python.org).

### Install IDE
Install VisualStudio Code in your computer. Use the [this](https://code.visualstudio.com/download) link to install VisualStudio Code.

### Setup

After doing this, confirm that you have installed virtualenv globally as well. If not, run this:

    $ pip install virtualenv
    or
    $ python -m venv env

Then, Git clone this repo to your PC

    $ git clone - ***url
    $ cd event_management
    
### Create a virtual environment

    $ virtualenv .venv && source .venv/bin/activate
    $ env\Scripts\activate (windows)
Install dependancies

    $ pip install -r requirements.txt

### In configurations need change database credentials inside settings.py

        'NAME': YOUR_DATABASE_NAME,
        'USER' : YOUR_DATABASE_USER,
        'PASSWORD' : YOUR_DATABASE_PASSWORD,


<!-- Make migrations & migrate -->

    $ python manage.py makemigrations 'apps' && python manage.py migrate 
###createsuperuser
    $ python manage.py createsuperuser
### Launching the app
    $ python manage.py runserver


