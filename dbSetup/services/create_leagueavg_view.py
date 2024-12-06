from csi3335f2024 import mysql
from sqlalchemy import text
from utils import create_session_from_str, create_enginestr_from_values
def create_lgavg_view():
    # Create session
    session = create_session_from_str(create_enginestr_from_values(mysql))

    # Query to create league average view
    create_lgavg_view_sql = """
    CREATE OR REPLACE VIEW lgavgview AS
    SELECT
        yearID,
        (SUM(p_ER) / NULLIF(sum(p_IPouts) / 3.0, 0)) * 9 AS lg_ERA,
        (SUM(p_HR) / NULLIF(sum(p_IPouts) / 3.0, 0)) * 9 AS lg_HR,
        (SUM(p_BB) / NULLIF(sum(p_IPouts) / 3.0, 0)) * 9 AS lg_BB,
        (SUM(p_HBP) / NULLIF(sum(p_IPouts) / 3.0, 0)) * 9 AS lg_HBP,
        (SUM(p_SO) / NULLIF(sum(p_IPouts) / 3.0, 0)) * 9 AS lg_K,
        NULLIF(SUM(p_IPouts) / 3.0, 0) AS lg_IP
    FROM pitching
    GROUP BY yearID;
    """

    # Create FIP View
    try:
        with session.connection() as connection:
            connection.execute(text(create_lgavg_view_sql))
        print("View 'lgavgview' created successfully")
    except Exception as e:
        print(f"Error creating 'lgavgview' view: {e}")

    session.close()

