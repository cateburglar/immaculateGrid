import argparse
import inspect

import services  # Assuming services.py is in the same directory

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
        "--create-view",
        action="store_true",
        help="Create all views (processed independently of table updates).",
    )
    args = parser.parse_args()

    # Get all views and tables
    views_to_create = get_all_views()
    if not args.tables and not args.create_view:
        print("No specific tables provided. Processing all tables and views.")
        tables_to_update = get_all_service_functions()
    else:
        tables_to_update = args.tables

    # Create views and update tables
    update_tables(tables_to_update)
    if args.create_view or (not args.create_view and not args.tables):
        create_views(views_to_create)

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
    return [
        name.replace("upload_", "").replace("_csv", "")
        for name, func in inspect.getmembers(services, inspect.isfunction)
        if name.startswith("upload_") and name.endswith("_csv")
    ]

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

