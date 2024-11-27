from .query_filter import (
    CareerStatFilter,
    MiscFilter,
    PositionFilter,
    SeasonStatFilter,
    TeamFilter,
)

FILTERS = {
    "career_stat": CareerStatFilter,
    "season_stat": SeasonStatFilter,
    "position": PositionFilter,
    "misc": MiscFilter,
    "team": TeamFilter,
}
