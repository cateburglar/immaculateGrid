import argparse

from services import (
    upload_allstarfull_csv,
    upload_people_csv,
    upload_schools_csv,
    upload_seriespost_csv,
    upload_teams_csv,
    upload_pitching_csv,
    upload_appearances_csv,
    upload_fielding_csv
)


def main():
    parser = argparse.ArgumentParser(description="Update database.")
    parser.add_argument(
        "tables",
        metavar="T",
        type=str,
        nargs="+",
        help="Names of the tables to update (e.g., people teams allstarfull schools)",
    )
    args = parser.parse_args()

    # Convert the list of table names to a tuple
    tables_to_update = tuple(args.tables)

    # Execute updates
    update_tables(tables_to_update)


def update_tables(tables):
    for table in tables:
        if table == "people":
            upload_people_csv()
        elif table == "teams":
            upload_teams_csv()
        elif table == "allstarfull":
            upload_allstarfull_csv()
        elif table == "schools":
            upload_schools_csv()
        elif table == "seriespost":
            upload_seriespost_csv()
        elif table == "pitching":
            upload_pitching_csv()
        elif table == "appearances":
            upload_appearances_csv()
        elif table == "fielding.csv":
            upload_fielding_csv()
        else:
            print(f"Unknown table: {table}")


if __name__ == "__main__":
    main()
