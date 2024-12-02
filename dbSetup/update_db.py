import argparse
import inspect

import services  # Assuming services.py is in the same directory
from services import create_lgavg_view, create_pitching_stats_view

def main():
    parser = argparse.ArgumentParser(description="Update database.")
    parser.add_argument(
        "tables",
        metavar="T",
        type=str,
        nargs="*",
        help="Names of the tables to update (e.g., people teams allstarfull schools). If no tables are provided, all will be updated.",
    )
    parser.add_argument(
        "--create-view",
        action="store_true",
        help="Create the 'pitchingstatsview' View",
    )
    args = parser.parse_args()

    if args.create_view:
        create_lgavg_view()
        create_pitching_stats_view()
        print("View creation triggered successfully.")
        return

    # If no tables are specified, call all functions in services
    tables_to_update = args.tables if args.tables else get_all_service_functions()

    # Execute updates
    update_tables(tables_to_update)


def get_all_service_functions():
    """Retrieve all update functions from the services module."""
    return [
        name.replace("upload_", "").replace("_csv", "")
        for name, func in inspect.getmembers(services, inspect.isfunction)
        if name.startswith("upload_") and name.endswith("_csv")
    ]


def update_tables(tables):
    for table in tables:
        func_name = f"upload_{table}_csv"
        if hasattr(services, func_name):
            func = getattr(services, func_name)
            func()  # Call the function
        else:
            print(f"Unknown table: {table}")


if __name__ == "__main__":
    main()
