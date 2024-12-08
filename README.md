# Seaquail Database Project Report

## Table of Contents

1. [Project Setup](#project-setup)
2. [Usage](#usage)
3. [Starting The App](#starting-the-app)
4. [Documentation](#documentation)
5. [Navigating the Project](#navigating-the-project)
6. [Modifications of the Baseball schema/data](#modifications-of-the-baseball-schemadata)
7. [App Features](#app-features)
8. [App Additions](#app-additions)
9. [Task Logs](#task-logs)

## Project Setup

1. **Clone the Project**:

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

## Starting the App

After activating the venv and setting up the database, you're ready to get started!

```bash
flask run
```

### Note: If you manually set up the database using the baseball.sql file, you will need to seed the users after running to have access to an admin

#### For Windows

```bash
python scripts/seed_users.py
```

#### For Linux/MacOs

```bash
python3 scripts/seed_users.py
```

### The username and password for the admin account are super secure

1. username: admin
2. password: password123

## Documentation

Below is a report on everything you need to know about the project, including change logs, general project documentation, and a list of which member(s) was responsible for each task.

### Navigating the Project

The project is divided into two main folders, app and dbSetup. The app directory is where all of the flask app code is stored, and what is run when you execute flask run.

#### App Directory

- /filters: This is where the filters used to modify the Immaculate Grid queries are stored. These are applied to each query to ensure the answer fits the users specified criteria

- /forms: This is where the forms used in the HTML templates are stored. Anything ranging for login to the team summary request forms are stored here

- /logging: This is where the log files are stored. These contain relevant information from the routes requests

- /models: This is where all of the ORM models are stored. Models used to represent tables are located in the models/tables directory

- /routes: This is where all of the routes are stored. These routes are then stored as Blueprints in the app/init.py

- /static: This is where resources like CSS, JS, or any other files that we need to store that don't have application logic can be stored

- /templates: This is where HTML is stored so that it can be loaded to the page when GET requests are sent to the routes.

#### dbSetup Directory

- /models: This is where the table ORMs are stored for updating the database

- /services: This is where the services are stored for parsing the csv data and performing the updates

- /static: This is where the csv and dump files are being stored

### There are also two minor directories that contain utility files

#### scripts Directory

This is where any scripts used in the project are stored. Below you can find a brief overview of their respective purposes

- findbadline.py: This was used to find bad lines in the csvs that would cause the updates to fail. This could be anything from hidden characters to characters not supported by our database

- seed_users.py: This is used to seed the database with users including the admin user

- switchdeaths.py: This was used to correct the formmating of the People.csv as the new information had the death information in the incorrect order

- trim_csv_file.py: This was used to trim out unneccesary information from csv files that we created, such as the career and season WAR csvs

- viewRows.sh: This is used to allow us to see the values of the header row of the csv files

#### benchmark Directory

This directory contains the information needed to analyze a systems cores so that our update script can effectively run with process pooling

### Modifications of the Baseball schema/data

#### Tables Added to the Baseball database

- wobaweights: Added to calculate wOBA

- users: Added to store user information

- nohitters: Added to store combined and individual no-hitter information since it is asked by the Immaculate Grid

- draft: Added to store the first draft picks for every year since it is asked by the Immaculate Grid

- careerwarleaders: Added the top 1000 career WAR leaders from Baseball Reference to the database since the Immaculate Grid only asks for WAR above a certain amount

- seasonwarleaders: Added the top WAR leaders since 1884 from Baseball Reference to the database to answer the Immaculate Grid question

- pitchingstats: Added to create an easy way to get a players season pitching stats for things like the Team Summary, Depth Chart, and Player pages

- battingstats: Added to create an easy way to get a players season batting stats for things like the Team Summary, Depth Chart, and Player pages

#### Alterations to existing tables

- Teams:
    1. park_name size was increased to fit all park names

- Schools:
    1. Changed all columns to be non-nullable since it never happens (You would never be given just a school name without the location) and multiple schools can have the same name and id (There are 3 columbia colleges).

- SeriesPost:
    1. Added lgIDwinner and lgIDloser as foreign key columns

- HallofFame:
    1. Increased note size to account for longer notes found in the Lahman Database

- Fielding:
    1. Foreign Key added for teamsID

- Appearances:
    1. Foreign Key added for teamsID

- Awards:
    1. Updated the awardID 'Rookie of the Year' to be 'Rookie of the Year Award' for consistency

- People:
    1. Added the nl_hof field to indicate which players were in the Negro League Hall of Fame so that we can answer the Immaculate Grid question of players that played in the Negro Leagues

- Batting:
    1. Added b_1B to keep track of first base runs

#### CSV Change logs

- NegroLeaguePlayers.csv
    1. Added to track which players were inducted into the Negro League hall of fame to answer the Immaculate Grid Question

- BattingStats.csv
    1. Used to export the view information and import it into the BattingStats table

- PitchingStats.csv
    1. Used to export the view information and import it into the PitchingStats tabel

- CareerWar.csv
    1. Created to have the information on career war leaders

- SeasonWar.csv
    1. Created to have the information on season war leaders

- wobaWeights.csv
    1. Created to store woba weight information for the wobaweights table

- People.csv
    1. Special characters like ñ and é were null characters, which had to be manually changed
    2. The new rows added to the bottom of the file (probably the last 1000), had the deathCountry, deathState, and deathCity values switched. To fix this, a script was written to swap the values to their correct spots

- Teams.csv
    1. Projected wins and projected losses have been updated to use the Baseball Pythagorean Theorem over all entries, including past entries
    2. The version of the theorem being used is 1.83 as the exponent

- Schools.csv
    1. City was sometimes comma separated and was too long to store in the database

    2. Comma separated city names only take the actual city name, not storing any specifications on locality such as campus names to the database

- Parks.csv
    1. Changed line 511 because there were two messed up characters that were interfering with data processing.

### App features

- Immaculate Grid Solver

- Team Summary Page + Depth Chart
    1. Clicking on a players name will take you to their Player Page
    2. Clicking on a teams name at the top will take you to their Team Page

- League Standings: A user can pull up the standings for each league by division by selecting a league name and year

- Users: Admin can browse all user info and view specific user information

- Update Profile: Users can update their profile information, including resetting their password

- Team Page
    1. This page is accessed by clicking the team name in their Team Summary
    2. This includes information like past stats and managers
    3. Users can click on the League ID to be navigated to the league standings for the year specified on the row

- Player Page
    1. Each player has their own page that contains information like past batting and pitching stats, awards, and other noteworthy information

- About Page
    1. Gives a brief overview of our project and features
    2. Each team member can be clicked on to navigate to their personal GitHub account

- Footer
    1. The footer contains linked images to the CSI 3335 Syllabus and the project GitHub repo

### App Additions

- Users
    1. Users with a first name, last name, password, banned status, and privilege were created
    2. Middleware created to verify if someone is logged in before accessing the website
    3. Middleware created to check if someone is banned before allowing them to access the website

- Admin
    1. Admin can view a searchable users page with all users and view the specific user information for each user
    2. Amin can ban/unban users as needed

- Immaculate Grid Prompt Handling
    1. A modular and extensible querying system was created using a Filter abstract class
    2. Basic QueryFilter abstract class has an apply method all filters inherit from
    3. QueryFilter implementations can store certain filter data allowing us to ensure if a stat is assocaited with a team, only players that accomplished that stat with that team are returned

- Views
    1. The original intent was to make views to calculate the BattingStats and PitchingStats, but those ended up being too slow when generating the Team Summary and Depth Chart
    2. We used these views to calculate and compile the data that was then imported into the tables to make the process much quicker

- HTML Macros
    1. Marcos were created to make an easily extensible set of dropdown menus, in theory you should be able to add more than two prompts if the Immaculate Grid someday became the Immaculate Cube

- Constants File
    1. This python file was created to track key value pairs for things like teamIDs and team names

- Update Script
    1. The update script allows the user to initialize the database, specify which tables they want to update, or perform a full update
    2. Some services use multiprocessing to process the updates faster

### Task Logs

- Brendon
    1. Table Updates / Additions
        1. Allstarfull
        2. Leagues
        3. People
        4. Schools
        5. Seriespost
        6. Teams
        7. CareerWarLeaders
    2. Immaculate Grid Page
    3. Login Page
    4. Team Summary and Depth Chart Page
    5. About Page
    6. League Standings
    7. Team Page
    8. Player Page
    9. Logging
    10. Misc Filter
    11. Team Filter
    12. Career Filter
    13. Footer Bar
    14. Users
    15. Registration
    16. Update Page

- Catherine
    1. Table Updates / Additions
        1. Appearances
        2. Fielding
        3. Homegames
        4. Parks
        5. Pitching
        6. Divisions
        7. WobaWeights
        8. SeasonWarLeaders
    2. Position Filter
    3. Season Filter
    4. Rarity
    5. Depth Chart Page
    6. Team Summary Page
    7. Update Page
    8. Database testing, debugging, and modifying
    9. Code Review
    10. UI Testing and bug fixing
    11. BattingStats debugging / fixing

- Icko
    1. Table Updates
        1. Pitchingpost
        2. Battingpost
        3. Batting
        4. Awardsshare
        5. Awards
        6. Fieldingpost
        7. Managers
        8. Collegeplaying
    2. Benchmarking
    3. Updating views
    4. PitchingStatsView and PitchingStats
    5. Code Review
    6. Database debugging
    7. Research for pitching stats calculations
    8. Immaculate Grid Research

- Noah
    1. Table Updates
        1. Salaries
        2. Halloffame
    2. Battingstatsview and BattingStats
    3. Database debugging
    4. Research for batting stats calculations
