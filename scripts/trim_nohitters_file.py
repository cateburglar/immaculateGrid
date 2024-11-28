import csv
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
csv_file_path = os.path.join(base_dir, "static", "csv", "com.csv")
new_csv = os.path.join(base_dir, "static", "csv", "comUpdated.csv")

print(f"CSV file path: {csv_file_path}")
print(f"New CSV file path: {new_csv}")

try:
    with open(csv_file_path, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = ["yearID", "teamID", "playerID", "date", "type"]

        with open(new_csv, "w", newline="") as csvfile_out:
            writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
            writer.writeheader()

            current_year = None
            current_team = None
            current_date = None
            for row in reader:
                if row["yearID"]:
                    current_year = row["yearID"]
                else:
                    row["yearID"] = current_year
                if row["teamID"]:
                    current_team = row["teamID"]
                else:
                    row["teamID"] = current_team
                if row["date"]:
                    current_date = row["date"]
                else:
                    row["date"] = current_date

                # Write only the selected columns
                writer.writerow(
                    {
                        "playerID": row["playerID"],
                        "yearID": row["yearID"],
                        "teamID": row["teamID"],
                        "date": row["date"],
                        "type": "C",
                    }
                )

    print(f"Updated CSV file saved as {new_csv}")

except FileNotFoundError as e:
    print(f"Error: {e}")
