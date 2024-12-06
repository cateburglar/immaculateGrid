from csi3335f2024 import mysql
from sqlalchemy import text
from utils import create_session_from_str, create_enginestr_from_values

def create_battingstats_view():
    # Create session using the utility function
    engine_str = create_enginestr_from_values(
        mysql=mysql
    )  # Ensure `mysql` is passed correctly
    session = create_session_from_str(engine_str)

    # Define the SQL query
    create_battingstats_view_sql = """
    CREATE OR REPLACE VIEW battingstatsview AS
    SELECT DISTINCT
        b.playerID as playerID,
        (b.yearID - p.birthYear) AS age,
        b.yearID AS yearID,
        b.teamID AS teamID,
        b.stint AS stint,
        p.nameFirst,
        p.nameLast,
        p.nameGiven,
        a.G_ALL AS b_G,
        (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF) AS b_PA,
        b.b_HR AS b_HR,
        b.b_SB AS b_SB,
        (b.b_BB / (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF)) * 100 AS b_BB_percent,
        (b.b_SO / (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF)) * 100 AS b_K_percent,
        (b.b_H - b.b_HR) / (b.b_AB - b.b_SO - b.b_HR + b.b_SF) AS b_BABIP,
        (b.b_H / b.b_AB) AS b_AVG,
        ((b.b_H - (b.b_2B + b.b_3B + b.b_HR)) + (2 * b.b_2B) + (3 * b.b_3B) + (4 * b.b_HR)) / b.b_AB AS b_SLG,
        (((b.b_H - (b.b_2B + b.b_3B + b.b_HR)) + (2 * b.b_2B) + (3 * b.b_3B) + (4 * b.b_HR)) / b.b_AB) - (b.b_H / b.b_AB) AS b_ISO,
        (b.b_H - (b.b_2B + b.b_3B + b.b_HR)) AS b_b_1B,

                                                -- calculation of 1b
        (((w.wBB * (b.b_BB - b.b_IBB)) + (w.wHBP * b.b_HBP) + (w.w1b * (b.b_H - (b.b_2B + b.b_3B + b.b_HR))) + (w.w2b * b.b_2B) + (w.w3b * b.b_3B) + (w.whr * b.b_HR))
            / (b.b_AB + b.b_BB - b.b_IBB + b.b_SF + b.b_HBP))
            AS b_wOBA,

        (
        -- woba
        (    ((((w.wBB * (b.b_BB - b.b_IBB)) + (w.wHBP * b.b_HBP) + (w.w1b * (b.b_H - (b.b_2B + b.b_3B + b.b_HR))) + (w.w2b * b.b_2B) + (w.w3b * b.b_3B) + (w.whr * b.b_HR))
            / (b.b_AB + b.b_BB - b.b_IBB + b.b_SF + b.b_HBP))
            - w.league)
            /
            w.wobascale)
        +
            ( w.r_pa) )
        *
        (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF) -- PA
        AS b_wRC

        -- ,((b.b_SB - b.b_CS) * 0.2) AS b_BsR
    FROM
        batting b
    JOIN
        people p ON b.playerID = p.playerID
    JOIN
        appearances a ON b.playerID = a.playerID AND b.yearID = a.yearID AND a.teamID = b.teamID
    JOIN
        fielding f ON b.playerID = f.playerID AND b.yearID = f.yearID AND a.teamID = b.teamID
    JOIN
        wobaweights w ON w.yearID = b.yearID
    HAVING
        b_PA > 0 -- exclude pitchers;
    """

    # Create Batting Stats View
    try:
        with session.connection() as connection:
            connection.execute(text(create_battingstats_view_sql))
        print("View 'battingstatsview' created successfully")
    except Exception as e:
        print(f"Error creating 'battingstatsview': {e}")

    session.close()
