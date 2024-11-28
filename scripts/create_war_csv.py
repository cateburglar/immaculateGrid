import csv
import os
import re

csv_file_path = os.path.join("dbSetup", "static", "csv", "CareerWAR.csv")
new_csv = os.path.join("dbSetup", "static", "csv", "CareerWARUpdated.csv")

# Process the raw data
rows = []
with open(csv_file_path, mode="r") as file:
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
        player = line[0]
        war = line[1]
        pa = line[2]
        ip = line[3]
        bats_throws = line[4]
        age = line[5]

        # Print player for debugging
        print(f"Player: {player}")

        # Remove all numeric characters from the player name
        player_name = re.sub(r"[\d\(\)\+]", "", player).strip()

        # Print cleaned player name for debugging
        print(f"Cleaned Player Name: {player_name}")

        # Prepare the row data
        row_data = [
            player_name,
            war,
            pa,
            ip,
            bats_throws,
            age,
        ]

        # Print row data for debugging
        print(f"Row Data: {row_data}")

        # Add the row data to the output list
        rows.append(row_data)

# Write the processed data to the new CSV file
with open(new_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"Updated CSV file saved as {new_csv}")
