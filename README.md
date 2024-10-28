# CSI3335 Project Virtual Environment

This repository provides a virtual environment setup with specified dependencies for student projects in the CSI3335 course. **Please use Python 3.10 and above**

## Description

This virtual environment contains essential Python libraries and frameworks required for the project. The `requirements.txt` file lists all the dependencies.

## Instructions

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/sanjelarun/csi3335-project-venv.git
    cd csi3335-project-venv
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

Once the virtual environment is activated and dependencies are installed, you can start working on your project within this environment. Remember to deactivate the virtual environment once you're done:

```bash
deactivate
```

## Starting the Flask dev server

After activating the virtual environment and installing the required dependencies, you're ready to get started. To start the development server, just run

```bash
flask run --debug
```

The debug flag is not required, but will let flask know to restart the server anytime changes are made so you don't have to keep shutting it down and booting it back up.

## Navigating the project

The project is divided into two main folders, app and dbSetup. The app directory is where all of the flask app code is stored, and what is run when you execute flask run.

## App Directory

- /models: This is where all of the ORM models are stored. Models used to represent tables are located in the models/tables directory

- /routes: This is where all of the routes are stored. These routes are then stored as [Blueprints](https://flask.palletsprojects.com/en/3.0.x/blueprints/) in the app/init.py

- /services: This is where all of the application logic is stored. Essentially, you can think of the route as a Controller, and these are the services we are used to interacting with in Java

- /static: This is where resources like CSS, JS, or any other files that we need to store that don't have application logic can be stored

- /template: This is where HTML is stored so that it can be loaded to the page when GET requests are sent to the routes.

### csi3335f2024 is the dictionary that stores the database connection information necessary for engine creation. You may need to make a new database for this

```sql
create database seaquail;
```

```bash
mysql -u user -p password seaquail < baseball.sql
```

## dbSetup Directory

- /models: This is where the table ORMs are stored for updating the database

- /services: This is where the services are stored for parsing the csv data and performing the updates

- /static: This is where the csv files are being stored

To run the dbSetup, execute the following command

```bash
python3 dbSetup/update_db.py
```
