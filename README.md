# River Analyst

## Introduction
River Analyst is a database application framework built with the [Django](https://www.djangoproject.com/) web application framework (Python) to leverage fast river ecosystem analyses. 

## Installation
### Linux
- Clone this repository: 
<br>
`` git clone https://github.com/beatriznegreiros/river-analyst.git``
- Make sure to have pip3 and virtualenv installed by: 
<br>
``sudo apt update``
<br>
``sudo apt install python3-pip``
<br>
``pip3 install virtualenv`` 
- Create new virtual environment:
<br>
``python3.9 -m venv /path/to/new/virtual/environment``
- Activate new virtual environment:
<br>
``source /path/to/new/virtual/environment/bin/activate``
- Install dependencies:
<br>
``pip3 install -r requirements.txt``
  
### Windows
- Clone this repository: 
<br>
`` git clone https://github.com/beatriznegreiros/river-analyst.git``
- Make sure to have [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) installed.
- Create conda environment: 
   <br>
``conda create --name [env_name] python=3.9``
- Activate conda environment:
<br>
``conda activate [env_name]``
- Install dependencies:
<br>
``pip3 install -r requirements.txt ``

    
## Usage

- Go to repository directory
    ``cd path/to/river-analyst``
- Make migrations (optional)
    ``python3 manage.py migrate``
Obs.: Migrations are in principle python commands wrapped around SQL passed from the Django framework to the sql database.
- Run the server locally
    ``python3 manage.py runserver``
- Create superuser for having full admin rights over the app:
    ``python3 manage.py createsuperuser``
  
## Initializing a new database with template csvs
- ``cd`` to the ``riveranalyst/utils`` directory
    ``cd riveranalyst/utils``
- Execute scripts to initialize targeted data models, beginning with the MeasStation model:
    
