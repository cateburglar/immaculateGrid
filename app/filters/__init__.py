from .position_filter import PositionFilter
from .team_filter import TeamFilter

# Optionally, you can define a list of available filters for easier imports
FILTERS = {
    "team": TeamFilter,
    "position": PositionFilter,
}
