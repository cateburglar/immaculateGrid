# Project Setup

1. **Clone the Repository (If you don't already have it)**:

    ```bash
    git clone https://github.com/Sea-Quail/finalProj.git
    cd finalProj
    ```

2. **Create a Virtual Environment**

    **For Windows**

    ```bash
    python -m venv project_env
    ```

    **For Linux/MacOs**

    ```bash
    python3 -m venv project_env
    ```

3. **Activate the Virtual Environment**

    **For Windows**

    ```bash
    .\project_env\Scripts\activate
    ```

    **For Linux/MacOs**

    ```bash
    source project_env/bin/activate
    ```

4. **Install the dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Once the virtual environment is activated and dependencies are installed, you can start setting up the database. **There is a dictionary in csi3335f2024 in both the dbSetup and app directories that contains the relevant info to access the database, which may need to be modified to fit your specifications**

### Using the Seaquail Dump

If you're using the sql dump, just run the following commands and you'll be good to go!

1. **Create the database**

    ```bash
    mysql -u <username> -p -e "CREATE DATABASE IF NOT EXISTS seaquail;"
    ```

2. **Load the dump file**

    ```bash
    mysql -u <username> -p seaquail < dbSetup/static/seaquail.sql
    ```

### Manual Setup

If you're starting from scratch with the original baseball database, follow these instructions!

1. **Create the database**

    ```bash
    mysql -u <username> -p -e "CREATE DATABASE IF NOT EXISTS seaquail;"
    ```

2. **Load the baseball dump file**

    ```bash
    mysql -u <username> -p seaquail < dbSetup/static/baseball.sql
    ```

3. **Run the update script with init flag**

    **For Windows**

    ```bash
    python dbSetup/update_db.py --init-database
    ```

    **For Linux/MacOs**

    ```bash
    python3 dbSetup/update_db.py --init-database
    ```

4. **Run the full update script**

    **For Windows**

    ```bash
    python dbSetup/update_db.py
    ```

    **For Linux/MacOs**

    ```bash
    python3 dbSetup/update_db.py
    ```

## Starting the Flask dev server

After activating the venv and setting up the database, you're ready to get started!

```bash
flask run
```

### Note: If you manually set up the database using the baseball.sql file, you will need to seed the users to have access to an admin

#### For Windows

```bash
python scripts/seed_users.py
```

#### For Linux/MacOs

```bash
python3 scripts/seed_users.py
```

## Navigating the project

The project is divided into two main folders, app and dbSetup. The app directory is where all of the flask app code is stored, and what is run when you execute flask run.

## App Directory

- /models: This is where all of the ORM models are stored. Models used to represent tables are located in the models/tables directory

- /routes: This is where all of the routes are stored. These routes are then stored as [Blueprints](https://flask.palletsprojects.com/en/3.0.x/blueprints/) in the app/init.py

- /static: This is where resources like CSS, JS, or any other files that we need to store that don't have application logic can be stored

- /template: This is where HTML is stored so that it can be loaded to the page when GET requests are sent to the routes.

### csi3335f2024 is the dictionary that stores the database connection information necessary for engine creation. You may need to make a new database for this

## dbSetup Directory

- /models: This is where the table ORMs are stored for updating the database

- /services: This is where the services are stored for parsing the csv data and performing the updates

- /static: This is where the csv files are being stored
