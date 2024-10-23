import csv

from app.extensions import db
from app.models import AllStarFull


def process_all_star_full(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Assuming the CSV contains columns 'name' and 'value'
            data_entry = AllStarFull.query.filter_by(name=row["name"]).first()

            if data_entry:
                # Update the existing entry
                data_entry.value = row["value"]
            else:
                # Insert new entry if it doesn't exist
                new_entry = AllStarFull(name=row["name"], value=row["value"])
                db.session.add(new_entry)

        db.session.commit()
