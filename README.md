# eduInventory

eduInventory is a web-based inventory management system developed as part of a collaborative group project for the School of Computer Science and Engineering. The system enables users to view, search, filter, and reserve equipment, while administrators can manage inventory, approve users, and generate reports. Built using Django and SQLite, the application emphasizes usability, security, and maintainability.

## Features

* Secure user sign up and login

* View and filter equipment inventory

* Make and manage reservations

* Admin dashboard for managing inventory and users

* Generate inventory and usage reports

## Installation & Running the Project

* Delete all migration files except __init__.py

* Delete the database file db.sqlite3

### Install required packages:

* pip install django
* pip install openpyxl
* pip install reportlab


### Run the following commands:

* python manage.py makemigrations
* python manage.py migrate
* python manage.py populate_inventory
* python manage.py createsuperuser
* python manage.py runserver


- Open http://127.0.0.1:8000/ in your browser to access the application.

Admin Account:

Username: yhuen24

Password: hihi

### Notes

* All project files are relative paths to ensure portability.

* The project uses GitHub for version control and collaboration.

* Includes both frontend and backend functionalities.
