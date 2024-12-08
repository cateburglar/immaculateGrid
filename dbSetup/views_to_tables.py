import csv
import os

import pymysql


def convert_views():

    mysql = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", "password"),
        "db": os.getenv("MYSQL_DATABASE", "seaquail"),
    }

    # Mapping of views to their corresponding new tables and CSV file names
    views_to_csv_and_tables = {
        "pitchingstatsview": {
            "csv": "PitchingStats.csv",
            "table": "pitchingstats",
        },
        "battingstatsview": {
            "csv": "BattingStats.csv",
            "table": "battingstats",
        },
    }

    csv_base_dir = os.path.join("dbSetup", "static", "csv")

    # Establish database connection
    try:
        connection = pymysql.connect(**mysql)
        cursor = connection.cursor()

        for view, details in views_to_csv_and_tables.items():
            # Export data from the view to a CSV file
            csv_file = os.path.join(csv_base_dir, details["csv"])
            table = details["table"]

            cursor.execute(f"SELECT * FROM {view}")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(column_names)  # Write column headers
                writer.writerows(rows)  # Write data rows

            print(f"Exported data from view '{view}' to '{csv_file}'.")

            print(f"Dropping view: {view}")
            # cursor.execute(f"DROP VIEW {view}")

            cursor.execute(f"DELETE FROM {table}")

            # Import data from the CSV file into the new table
            with open(csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                headers = next(reader)  # Skip the header row

                # Prepare SQL INSERT statement
                placeholders = ", ".join(["%s"] * len(headers))
                insert_query = f"INSERT INTO {table} ({', '.join(headers)}) VALUES ({placeholders})"

                for row in reader:
                    # Convert empty strings to None (NULL in SQL)
                    row = [None if value == "" else value for value in row]
                    cursor.execute(insert_query, row)

            print(f"Imported data from '{csv_file}' into table '{table}'.")

        # Commit changes
        connection.commit()

    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals():
            connection.close()
