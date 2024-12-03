import argparse
import inspect
import os
import importlib.util
import sys

def main():
    parser = argparse.ArgumentParser(description="Create views in the database.")
    parser.add_argument(
        "views",
        metavar="V",
        type=str,
        nargs="*",
        help="Names of the views to create (e.g., battingStatsView, teamView). If no views are provided, all views will be created.",
    )
    args = parser.parse_args()

    # Get all view creation functions from the views directory
    views_to_create = get_all_views()

    if not args.views:
        print("No specific views provided. Creating all views.")
        views_to_create = get_all_views()
    else:
        # Filter for the views specified by the user
        views_to_create = [
            view for view in views_to_create if view.__name__.lower() in [v.lower() for v in args.views]
        ]

    # Create the specified views
    create_views(views_to_create)


def get_all_views():
    """Retrieve all view-creation functions from the views directory."""
    views_dir = os.path.join(os.getcwd(), 'dbSetup', 'models', 'views')  # Updated path
    print(f"Looking for views in directory: {views_dir}")  # Debugging line
    
    if not os.path.exists(views_dir):
        print(f"Error: The directory {views_dir} does not exist.")
        return []

    views = []
    for filename in os.listdir(views_dir):
        if filename.endswith(".py"):  # Only Python files
            view_module = import_view_module(filename)
            views += [
                func
                for name, func in inspect.getmembers(view_module, inspect.isfunction)
                if name.startswith("create_") and name.endswith("_view")
            ]
    
    return views



def import_view_module(filename):
    """Import a Python module from a file."""
    module_name = filename[:-3]  # Remove '.py' from the filename
    file_path = os.path.join(os.getcwd(), 'dbSetup', 'models', 'views', filename)
    
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    return module


def create_views(views):
    """Create the specified views by calling their corresponding functions."""
    print("Creating views...")
    for view_func in views:
        view_func()  # Call the view creation function
    print("View creation completed.")


if __name__ == "__main__":
    main()
