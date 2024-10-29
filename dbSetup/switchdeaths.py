import csv
import os


def switch_death_columns(file_path, start_row):
    # Read the CSV file into a list of dictionaries
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    # Modify the necessary rows
    for row in rows[start_row - 1 :]:
        deathState = row["deathCountry"]
        deathCity = row["deathState"]
        deathCountry = row["deathCity"]

        # Switch the values
        row["deathCountry"] = deathCountry
        row["deathState"] = deathState
        row["deathCity"] = deathCity

    # Write the modified data back to the CSV file
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)


# Example usage
base_dir = os.path.abspath(os.path.dirname(__file__))
csv_file_path = os.path.join(base_dir, "static", "csv", "People.csv")
start_row = 20927
switch_death_columns(csv_file_path, start_row)
