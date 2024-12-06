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
        t.yearID,
        AVG(p_ERA) AS lg_ERA,
        AVG(p_HR) AS lg_HR,
        AVG(p_BB) AS lg_BB,
        AVG(p_HBP) AS lg_HBP,
        AVG(p_SO) AS lg_K,
        SUM(p_IPouts) / 3.0 AS lg_IP
    FROM pitching
    JOIN teams t
        ON t.teamID = pitching.teamID AND t.yearID = pitching.yearID
    GROUP BY t.yearID;
    """

    # Query with weighted averages
    # create_lgavg_view_sql = """
    # CREATE OR REPLACE VIEW lgavgview AS
    # SELECT
    #     t.yearID,
    #     SUM(p.p_ER) / NULLIF(SUM(p.p_IPouts) / 3.0, 0) AS lgERA,
    #     SUM(p.p_HR) / NULLIF(SUM(p.p_IPouts) / 3.0, 0) AS lgHR,
    #     SUM(p.p_BB) / NULLIF(SUM(p.p_IPouts) / 3.0, 0) AS lgBB,
    #     SUM(p.p_HBP) / NULLIF(SUM(p.p_IPouts) / 3.0, 0) AS lgHBP,
    #     SUM(p.p_SO) / NULLIF(SUM(p.p_IPouts) / 3.0, 0) AS lgK,
    #     SUM(p.p_IPouts) / 3.0 AS lgIP
    # FROM pitching p
    # JOIN teams t
    #     ON t.teamID = p.teamID AND t.yearID = p.yearID
    # GROUP BY t.yearID;
    # """

    # Create FIP View
    try:
        with session.connection() as connection:
            connection.execute(text(create_lgavg_view_sql))
        print("View 'lgavgview' created successfully")
    except Exception as e:
        print(f"Error creating 'lgavgview' view: {e}")

    session.close()

