import csv
import os

csv_file_path = os.path.join("dbSetup", "static", "csv", "NegroLeagues.csv")
new_csv = os.path.join("dbSetup", "static", "csv", "NegroLeaguesUpdated.csv")

print(f"CSV file path: {csv_file_path}")
print(f"New CSV file path: {new_csv}")

try:
    with open(csv_file_path, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = ["playerID"]

        with open(new_csv, "w", newline="") as csvfile_out:
            writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                # Write only the selected columns
                writer.writerow(
                    {
                        "playerID": row["playerID"],
                    }
                )

    print(f"Updated CSV file saved as {new_csv}")

except FileNotFoundError as e:
    print(f"Error: {e}")
