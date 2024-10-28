from services import upload_allstarfull_csv, upload_people_csv

print("Updating people table from People.csv")
upload_people_csv()

print("Updating allstarfull table from AllstarFull.csv")
upload_allstarfull_csv()
