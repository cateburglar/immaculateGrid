from csi3335f2024 import mysql
from sqlalchemy import text
from utils import create_session_from_str, create_enginestr_from_values
def create_lgavg_view():
    # Create session
    session = create_session_from_str(create_enginestr_from_values(mysql))

    # Query to create league average view
    create_lgavg_view_sql = """
    CREATE OR REPLACE VIEW lgavgview AS
    SELECT DISTINCT
        t.yearID,
        AVG(p_ERA) AS lgERA,
        AVG(p_HR) AS lgHR,
        AVG(p_BB) AS lgBB,
        AVG(p_HBP) AS lgHBP,
        AVG(p_SO) AS lgK,
        SUM(p_IPouts) / 3.0 AS lgIP
    FROM pitching
    JOIN teams t ON t.teamID = pitching.teamID
    GROUP BY t.yearID;
    """

    # Create FIP View
    try:
        with session.connection() as connection:
            connection.execute(text(create_lgavg_view_sql))
        print("View 'lgavgview' created successfully")
    except Exception as e:
        print(f"Error creating 'lgavgview' view: {e}")

    session.close()

