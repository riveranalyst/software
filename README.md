# Intro
River Analyst is a database application framework built with the [Django](https://www.djangoproject.com/) web application framework (Python) to leverage fast river ecosystem analyses. 

# Installation
### Linux
- Clone this repository: 
    ```console 
    git clone https://github.com/beatriznegreiros/river-analyst.git
    ```
- Make sure to have pip3 and [virtualenv](https://pypi.org/project/virtualenv/) installed by: 
    ```console
    sudo apt update
    sudo apt install python3-pip
    pip3 install virtualenv
    ```
- Create new virtual environment:
    ```console
    python3.9 -m venv /path/to/new/virtual/environment
    ```
- Activate new virtual environment:
    ```console
    source /path/to/new/virtual/environment/bin/activate
    ```
- Install dependencies:
    ```console
    pip3 install -r requirements.txt
    ```
  
### Windows
- Clone this repository: 
    ```console
    git clone https://github.com/beatriznegreiros/river-analyst.git
    ```
- Make sure to have [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) installed.
- Create conda environment: 
    ```console
    conda create --name [env_name] python=3.9
    ```
- Activate conda environment:
    ```console
    conda activate [env_name]
    ```
- Install dependencies:
    ```console
    pip3 install -r requirements.txt 
    ```

    
# Usage
## Database architecture

![Database architecture](https://github.com/beatriznegreiros/river-analyst/blob/master/static/images/river_analyst_DBMS%20ER%20diagram%20(UML%20notation).png)


## Running the app
- Go to repository directory
    ``cd path/to/river-analyst``
- Make migrations (optional)
    ``python3 manage.py migrate``
Obs.: Migrations are in principle python commands wrapped around SQL passed from the Django framework to the sql database.
- Run the server locally
    ``python3 manage.py runserver``
- Create superuser for having full admin rights over the app:
    ``python3 manage.py createsuperuser``
  
# Initializing a new database with template CSVs
- Add data to the csv templates under the path ``riveranalyst/river-analyst/media/``
- ``cd`` to the ``riveranalyst/utils`` directory
    ``cd riveranalyst/utils``
- Execute scripts to initialize targeted data models
    - It is important to begin with populating the **MeasStation** model, which is where all data models connect:
        - Here, it is crucial that the field ``meas_station`` is unique and contains no typos. This field will be used to generate foreign keys to link data models.
    ``python fill_stations_tab.py``
    - Then, any data model can be populated afterwards, for instance:
        - the field ``meas_station`` needs to match the names given in the MeasStation data model.
            - ``python fill_surf_tab.py`` for filling the **SurfaceSed** data model
            - ``python fill_subsurf_tab.py`` for the **SubSurfaceSed** data model
            - ``python fill_kf_tab.py`` for the **Kf** (Riverbed Hydraulic Conductivity) data model
            - ``python fill_do_tab.py`` for the **IDO** (Interstitial Dissolved Oxygen) data model
            - ``python fill_hydraulics_tab.py`` for the **Hydraulics** data model

    
