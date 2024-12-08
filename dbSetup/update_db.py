import argparse
import inspect

import services  # Assuming services.py is in the same directory
from services import setup_tables
from views_to_tables import convert_views


def main():
    parser = argparse.ArgumentParser(description="Update database.")
    parser.add_argument(
        "tables",
        metavar="T",
        type=str,
        nargs="*",
        help="Names of the tables to update (e.g., people teams allstarfull schools). If no tables are provided, all tables and views will be processed.",
    )
    parser.add_argument(
        "--init-database",
        action="store_true",
        help="Modify baseball database",
    )

    args = parser.parse_args()

    if args.init_database:
        print("Setting up database")
        setup_tables()
        print("Loading wobaweights")
        services.upload_wobaweights_csv()
        views_to_create = get_all_views()
        create_views(views_to_create)
        print("Converting views to tables")
        convert_views()
        return

    # Get all views and tables
    if not args.tables:
        print("No specific tables provided. Processing all tables.")
        tables_to_update = get_all_service_functions()
        update_tables(tables_to_update)
        views_to_create = get_all_views()
        create_views(views_to_create)
        convert_views()
    else:
        tables_to_update = args.tables
        # Update tables
        update_tables(tables_to_update)


def get_all_views():
    """Retrieve all view-creation functions from the services module."""
    return [
        func
        for name, func in inspect.getmembers(services, inspect.isfunction)
        if name.startswith("create_") and name.endswith("_view")
    ]


def create_views(views):
    """Create the specified views by calling their corresponding functions."""
    print("Creating views...")
    for view_func in views:
        view_func()
    print("View creation completed.")


def get_all_service_functions():
    """Retrieve all update functions from the services module."""
    functions = [
        name.replace("upload_", "").replace("_csv", "")
        for name, func in inspect.getmembers(services, inspect.isfunction)
        if name.startswith("upload_") and name.endswith("_csv")
    ]

    # Sort the list to ensure the function containing "people" is first
    functions.sort(key=lambda x: "people" not in x)

    return functions


def update_tables(tables):
    """Update specified tables by calling their corresponding upload functions."""
    print("Updating tables...")
    for table in tables:
        func_name = f"upload_{table}_csv"
        if hasattr(services, func_name):
            func = getattr(services, func_name)
            func()  # Call the function
        else:
            print(f"Unknown table: {table}")
    print("Table updates completed.")


if __name__ == "__main__":
    main()
