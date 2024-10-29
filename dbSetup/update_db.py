from services import (
    upload_allstarfull_csv,
    upload_people_csv,
    upload_schools_csv,
    upload_teams_csv,
)

print("Updating people table from People.csv")
upload_people_csv()

print("Updating teams table from Teams.csv")
upload_teams_csv()

print("Updating allstarfull table from AllstarFull.csv")
upload_allstarfull_csv()

print("Updating teams table from Schools.csv")
upload_schools_csv()
