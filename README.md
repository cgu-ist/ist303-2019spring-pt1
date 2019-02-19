## MiYE - Massage Reservation System

> " Mud in Your Eye” (MiYE) - a new, small hot spring health spa, located in a remote, scenic part of the US. The software must support the spa’s front desk clerks in managing service reservations and statements of service usage for customers.

MiYE is a full-time resort spa facility, provides front desk clerk the ability to manage service, customers also make reservation in the system.
By default, MiYE provides services as follows.


## Application Preparation

### Start you local environment

```shell
# Create a virtual environment and activate it
$ python3 -m venv ./venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Prepare your schema and play with it

* Step create your schema
```shell
$ python manage.py makemigrations
$ python manage.py migrate
```

* Play with your data
```shell
$ python manage.py shell_plus --notebook
# This will open a jupyter notebook and you can run it
```

### Create a super user for your application
```shell
$ python manage.py

```

### Run dev server

```shell
./manage.py runserver createsuperuser
```

## Page Overview

* [X] Login/Logout
* [X] Service administration
* [X] Customer administration
* [ ] Reservation
