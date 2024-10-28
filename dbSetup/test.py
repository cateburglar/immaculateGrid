from services.test_service import (
    compare_existing_allstarfull_entries,
    compare_existing_people_entries,
    compare_existing_teams_entries,
)

print("Testing people entries against original database")
compare_existing_people_entries()

print("Testing teams entries against original database")
compare_existing_teams_entries()

print("Testing allstarfull entries against original database")
compare_existing_allstarfull_entries()
