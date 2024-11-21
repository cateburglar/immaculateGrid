from .query_filter import (
    CareerStatFilter,
    MiscFilter,
    PositionFilter,
    SeasonStatFilter,
    TeamFilter,
)

# Optionally, you can define a list of available filters for easier imports
FILTERS = {
    "career_stat": CareerStatFilter,
    "season_stat": SeasonStatFilter,
    "position": PositionFilter,
    "misc": MiscFilter,
    "team": TeamFilter,
}
