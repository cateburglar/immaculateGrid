import argparse

from services.test_service import execute_tests


def main():
    parser = argparse.ArgumentParser(description="Run database tests.")
    parser.add_argument(
        "tables",
        metavar="T",
        type=str,
        nargs="+",
        help="Names of the tables to test (e.g., People Teams AllstarFull Schools)",
    )
    args = parser.parse_args()

    # Convert the list of table names to a tuple
    tables_to_test = tuple(args.tables)

    # Execute the tests
    execute_tests(tables_to_test)


if __name__ == "__main__":
    main()
