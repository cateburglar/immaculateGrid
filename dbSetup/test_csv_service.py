import argparse
import inspect
import services

def main():
    parser = argparse.ArgumentParser(description="Test a specific database service.")
    parser.add_argument(
        "service",
        metavar="SERVICE",
        type=str,
        help="Name of the service to test (e.g., batting, people, teams).",
    )
    args = parser.parse_args()

    # Dynamically call the specified service
    run_service(args.service)


def run_service(service_name):
    """Run a specific service update based on the given name."""
    func_name = f"upload_{service_name}_csv"

    try:
        if hasattr(services, func_name):
            print(f"Starting update for {service_name}...")
            func = getattr(services, func_name)
            func()  # Call the function dynamically
            print(f"{service_name.capitalize()} service completed successfully.")
        else:
            print(f"Error: No service found for '{service_name}'. Please check the service name.")
    except Exception as e:
        print(f"An error occurred while running the {service_name} service: {e}")


if __name__ == "__main__":
    main()

