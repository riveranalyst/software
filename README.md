# Flussdata


# Usage
- Clone this repository: `` git clone https://github.com/beatriznegreiros/sediment-analyst.git``
- Make sure to have pip3 installed by:
    ``sudo apt update``
    ``sudo apt install python3-pip``
    ``pip3 install -r requirements.txt ``
- Move to repository directory
    ``cd path/to/fluss-db``
- Make migrations (optional)
    ``python3 manage.py migrate``
Obs.: Migrations are in principle python commands passed from the django framework to the sql database as sql commands.
- Run the server locally
    ``python3 manage.py runserver``