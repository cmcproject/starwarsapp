# Introduction
Star Wars App

# Project layout
* common/ - helpers + services
* people/ - people app
* starwarsapp/ - project configuration
* templates/ - html templates
* storage/ - csv files directory


# Prerequisites
## Pre-commit
Install [pre-commit](https://pre-commit.com/) firstly.

Execute `pre-commit install` once after downloading the repo code.

Run `pre-commit run --all-files` if you want to check your code

## Install packages
Run cmds:

`virtualenv venv`

`venv\Scripts\activate`

`pip install -r requirements.txt`


# Run app

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver`


## 1. Launch app
http://127.0.0.1:8000
## 2. Download new data
Press Download button from navbar
## 3. Inspect Datasets
Press Datasets button from navbar
## 4. Count by columns by providing col1 and col2 params
http://127.0.0.1:8000/datasets/<id>?col1=skin_color&col2=hair_color
## 5. Load less/more people by providing number_per_page param
http://127.0.0.1:8000/datasets/<id>?number_per_page=50