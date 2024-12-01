from csi3335f2024 import mysql
from sqlalchemy import text
from utils import create_session_from_str, create_enginestr_from_values

def create_pitching_stats_view():
    # Create session
    session = create_session_from_str(create_enginestr_from_values(mysql))

    # Query to create the view
    create_view_sql = """
    CREATE OR REPLACE VIEW pitchingstatsview AS
    SELECT
        pi.playerID,
        pi.teamID,
        pi.yearID,
        pi.stint,
        pe.nameFirst,
        pe.nameLast,
        pe.nameGiven,
        pi.p_G,
        pi.P_GS,
        pi.p_ERA,
        CASE
            WHEN pe.deathYear IS NULL THEN
                (DATEDIFF(CURDATE(), CONCAT(pe.birthYear, '-', pe.birthMonth, '-', pe.birthDay)) / 365.25)
            ELSE
                (DATEDIFF(CONCAT(pe.deathYear, '-', pe.deathMonth, '-', pe.deathDay), CONCAT(pe.birthYear, '-', pe.birthMonth, '-', pe.birthDay)) / 365.25)
        END AS age,
        pi.p_IPouts / 3.0 AS p_IP,
        (pi.p_SO / pi.p_BFP) * 100 AS p_K_percent,
        (pi.p_BB / pi.p_BFP) * 100 AS p_BB_percent,
        (pi.p_HR / (pi.p_IPouts / 3.0)) * 9 AS p_HR_div9,
        (pi.p_H - pi.p_HR) / (pi.p_BFP - pi.p_SO - pi.p_HR + pi.p_BB) AS p_BABIP,
        ((pi.p_BFP - pi.p_R) / (pi.p_BFP - pi.p_BB - pi.p_HBP - pi.p_SO)) * 100 AS p_LOB_percent,
        (pi.p_HR / (pi.p_HR + pi.p_SO)) AS p_HR_div_FB,
        ((13 * pi.p_HR + 3 * (pi.p_BB + pi.p_HBP) - 2 * pi.p_SO) / (pi.p_IPouts / 3.0)) AS p_FIP,
        -- p_xFIP requires league avg HR rates
        -- xFIP = ((13*HR)+(3*(BB+HBP))-(2*K))/IP + FIP Constant
        -- FIP Constant = lgERA - (((13*lgHR)+(3*(lgBB+lgHBP))-(2*lgK))/lgIP)
        NULL AS p_xFIP,
        -- p_WAR requires additional data not present in our current database
        NULL AS p_WAR
    FROM pitching pi
    JOIN people pe ON pe.playerID = pi.playerID;
    """

    try:
        with session.connection() as connection:
            connection.execute(text(create_view_sql))
        print("View 'pitchingstatsview created successfully'")
    except Exception as e:
        print(f"Error creating view: {e}")
