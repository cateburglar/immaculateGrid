import csv
import os


def surround_fields_with_quotes(file_path):
    # Read the CSV file into a list of rows
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    # Modify the necessary rows
    modified_rows = []
    for row in rows:
        if len(row) > 5:
            row[2] = '"' + row[2]
            row[3] = row[3] + '"'
        modified_rows.append(row)

    # Write the modified data back to the CSV file
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(modified_rows)


# Example usage
base_dir = os.path.abspath(os.path.dirname(__file__))
csv_file_path = os.path.join(base_dir, "static", "csv", "Schools.csv")
surround_fields_with_quotes(csv_file_path)
