# Resources
#
# [Calculating FIP](https://library.fangraphs.com/pitching/fip/)
# [Calculating xFIP](https://www.mlb.com/glossary/advanced-stats/expected-fielding-independent-pitching)
# [WAR Calculations](https://www.samford.edu/sports-analytics/fans/2023/Sabermetrics-101-Understanding-the-Calculation-of-WAR)
# [WAR Calculation - fangraph](https://library.fangraphs.com/war/calculating-war-pitchers/)

from csi3335f2024 import mysql
from sqlalchemy import text
from utils import create_session_from_str, create_enginestr_from_values

def create_lgavg_view():
    # Create session
    session = create_session_from_str(create_enginestr_from_values(mysql))

    # Query to create league average view
    create_lgavg_view_sql = """
    CREATE OR REPLACE VIEW lgavg AS
    SELECT
        yearID,
        AVG(p_ERA) AS lgERA,
        AVG(p_HR) AS lgHR,
        AVG(p_BB) AS lgBB,
        AVG(p_HBP) AS lgHBP,
        AVG(p_SO) AS lgK,
        SUM(p_IPouts) / 3.0 AS lgIP
    FROM pitching
    GROUP BY yearID;
    """

    # Create FIP View
    try:
        with session.connection() as connection:
            connection.execute(text(create_lgavg_view_sql))
        print("View 'lgavg' created successfully")
    except Exception as e:
        print(f"Error creating 'lgavg' view: {e}")

    session.close()

def create_pitching_stats_view():
    # Create session
    session = create_session_from_str(create_enginestr_from_values(mysql))

    """
    Notes regarding calculations

    1.  FIP
    -- FIP = (((13*HR)+3*(BB+HBP)-(2*K))/IP)+FIP constant
    -- FIP Constant = lgERA - (((13 * lgHR) + (3 * (lgBB + lgHBP)) - (2 * lgK)) / lgIP)

    2.  xFIP
    -- p_xFIP requires league avg HR rates
    -- xFIP = ((13 * (FB * (lgHR / lgFB)) + 3 * (BB + HBP) - 2 * K) / IP) + FIP constant
    -- FIP Constant = lgERA - (((13*lgHR)+(3*(lgBB+lgHBP))-(2*lgK))/lgIP)
    -- well... p_FB and lgFB is not present in our database

    3.  WAR
    There are two different ways to calculate WAR, noted as fWAR and bWAR
    [WAR Calculations](https://www.samford.edu/sports-analytics/fans/2023/Sabermetrics-101-Understanding-the-Calculation-of-WAR)

    -- From <https://library.fangraphs.com/war/calculating-war-pitchers/>
    -- WAR = [[([(League FIP - FIP) / Pitcher specific runs per win] + Replacement Level) * (IP / 9)] * Leverage Multiplier for Relievers] + League Correction

    -- fWAR from samford
    -- fWAR = (Batting runs + Base Running runs + Fielding Runs + Positional Adjustment + League Adjustment + Replacement Runs) / (Runs per win)

    -- bWAR from samford
    -- bWAR = (Batting runs + Base running runs +/- Runs from GIDP + Fielding Runs + Positional Adjustment runs + Replacement level runs) / (Runs per win)
    """

    # Query to create pitching stats view
    create_pitchingview_sql = """
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
        ((13 * pi.p_HR) + (3 * (pi.p_BB + pi.p_HBP)) - (2 * pi.p_SO)) / (pi.p_IPouts / 3.0) + (l.lgERA - (((13 * l.lgHR) + (3 * (l.lgBB + l.lgHBP)) - (2 * l.lgK)) / l.lgIP)) AS p_FIP,
        -- ((13 * (pi.p_FB * (l.lgHR / l.lgFB)) + (3 * (pi.p_BB + pi.p_HBP)) - (2 * pi.p_SO)) / (pi.p_IPouts / 3.0) + (l.lgERA - (((13 * l.lgHR) + (3 * (l.lgBB + l.lgHBP)) - (2 * l.lgK)) / l.lgIP)) AS p_xFIP,
        NULL AS p_xFIP,
        NULL AS p_WAR
    FROM pitching pi
    JOIN people pe ON pe.playerID = pi.playerID
    JOIN lgavg l ON pi.yearID = l.yearID;
    """

    # Create Pitching Stats View
    try:
        with session.connection() as connection:
            connection.execute(text(create_pitchingview_sql))
        print("View 'pitchingstatsview' created successfully")
    except Exception as e:
        print(f"Error creating 'pitchingstatsview' view: {e}")

    session.close()
