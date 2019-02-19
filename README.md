# MiYE

> " Mud in Your Eye” (MiYE) - a new, small hot spring health spa, located in a remote, scenic part of the US. The software must support the spa’s front desk clerks in managing service reservations and statements of service usage for customers.

MiYE is a an application that work for full-time resort spa facility, provides front desk clerk the ability to manage service, customers also make reservation in the system.
By default, MiYE provides services as follows.

## Team Member/Role

* [Karen Snow](https://github.com/karensnow2019) - Business Design, Programmer
* [Okechukwu Ugwuanyi](https://github.com/okechukwuugwuanyi) - UI Desiner, Programmer
* [Haibo Yan](https://github.com/billyean) - System Design, Programmer

## Design

#### Logic Design

MiYE provides at least below functions.

#### Administration

MiYE has two administration pages that provide customers' management and services' management.

#### reservation

MiYE provides a reservation page that clerk can manage customer's reservation also query customer's reservation by given condition

### Architecture

MiYE is a pure Django application that can be run in Linux/MacOSX/Window.MiYE is using JQuery to provide AJAX support for implementation of so-called one page application. MiYE is using sqllite3 as local storage, which means MiYE doesn't support multiple user scenarios.

MiYE is a secure application that only authorized clerk can manage the system. MiYE provides initial user creation mechanism that customer makes sure they can their system safe.

MiYE is using both Django rest API to manipulate data, data will be transfer between customer's browser and MiYE asynchronously.

## Application Preparation

### Start you local environment

* MacOSX/Linux

  ```shell
  # Create a virtual environment and activate it
  $ python3 -m venv venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt
  ```

* Windows

  ```shell
  # Create a virtual environment and activate it
  python -m venv venv
  venv\Scripts\activate
  (venv) pip install -r requirements.txt
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
$ python manage.py createsuperuser
```

### Run dev server

```shell
$ python manage.py runserver
```

## Page Overview

* [X] Login/Logout
* [X] Service administration
* [X] Customer administration
* [ ] Reservation
