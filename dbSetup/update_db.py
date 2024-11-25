import argparse
import inspect
import signal

import services


def timeout_handler(signum, frame):
    raise TimeoutError("Function call timed out")


def main():
    parser = argparse.ArgumentParser(description="Update database.")
    parser.add_argument(
        "tables",
        metavar="T",
        type=str,
        nargs="*",
        help="Names of the tables to update (e.g., people teams allstarfull schools). If no tables are provided, all will be updated.",
    )
    args = parser.parse_args()

    # If no tables are specified, call all functions in services
    tables_to_update = (
        args.tables
        if (args.tables and args.tables != ["ci"])
        else get_all_service_functions()
    )
    isCI = True if args.tables == "test" else False

    # Execute updates
    update_tables(tables_to_update, isCI)


def get_all_service_functions():
    """Retrieve all update functions from the services module."""
    return [
        name.replace("upload_", "").replace("_csv", "")
        for name, func in inspect.getmembers(services, inspect.isfunction)
        if name.startswith("upload_") and name.endswith("_csv")
    ]


def update_tables(tables, isCI):
    for table in tables:
        func_name = f"upload_{table}_csv"
        if hasattr(services, func_name):
            func = getattr(services, func_name)
            if isCI:
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)
                try:
                    func()  # Call function in test mode
                except TimeoutError:
                    print(f"Update for table {table} timed out")
                finally:
                    signal.alarm(0)  # Disable the alarm
            else:
                func()  # Call function normally
        else:
            print(f"Unknown table: {table}")


if __name__ == "__main__":
    main()
