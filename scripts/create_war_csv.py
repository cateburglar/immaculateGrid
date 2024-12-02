import csv
import os
import unicodedata
import re

war_file_path = os.path.join("dbSetup", "static", "csv", "warcsvnotgood.csv")
people_csv_path = os.path.join("dbSetup", "static", "csv", "People.csv")
new_csv = os.path.join("dbSetup", "static", "csv", "SeasonWAR.csv")

SPANISH_TO_ENGLISH = {
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ú": "u",
    "ü": "u",
    "ñ": "n",
    "Á": "A",
    "É": "E",
    "Í": "I",
    "Ó": "O",
    "Ú": "U",
    "Ü": "U",
    "Ñ": "N",
}


def replace_spanish_characters(text):
    # Remove non-breaking spaces and Unicode artifacts
    text = text.replace("\xa0", " ").replace("Â", "")
    # Replace Spanish characters
    for spanish_char, english_char in SPANISH_TO_ENGLISH.items():
        text = text.replace(spanish_char, english_char)
    return text.strip()  # Ensure no leading/trailing whitespace


# Read the People.csv file and create a dictionary mapping full names to rows
people_dict = {}
with open(people_csv_path, mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        full_name = f"{row['nameFirst']} {row['nameLast']}".strip()
        full_name = replace_spanish_characters(full_name)
        people_dict[full_name] = row


# Process the CareerWAR.csv data
rows = []
with open(war_file_path, mode="r") as file:
    reader = csv.reader(file)

    # Print out raw lines for debugging
    print("Raw data lines:")
    lines = list(reader)
    for line in lines:
        print(repr(line))  # Use repr to see any hidden characters

    # Skip the header line
    headers = lines[0]
    for line in lines[1:]:
        # Extract the relevant fields
        player = replace_spanish_characters(line[0]).strip()
        war = line[1]
        year = line[2]

        people_row = people_dict[player] if player in people_dict else None
        if people_row:
            playerid = people_row["playerID"]
        else:
            playerid = "NULL"

        row = [player, war, playerid, year]
        rows.append(row)

        # Print row data for debugging
        print(f"Row Data: {row}")


# Write the processed data to the new CSV file
with open(new_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        headers + ["playerID"] + ["year"]
    )  # Add any other headers from People.csv as needed
    writer.writerows(rows)

print(f"Updated CSV file saved as {new_csv}")
