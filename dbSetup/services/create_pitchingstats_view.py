# Resources
#
# [Calculating FIP](https://library.fangraphs.com/pitching/fip/)
# [Calculating xFIP](https://www.mlb.com/glossary/advanced-stats/expected-fielding-independent-pitching)
# [WAR Calculations](https://www.samford.edu/sports-analytics/fans/2023/Sabermetrics-101-Understanding-the-Calculation-of-WAR)
# [WAR Calculation - fangraph](https://library.fangraphs.com/war/calculating-war-pitchers/)

from csi3335f2024 import mysql
from sqlalchemy import text
from utils import create_enginestr_from_values, create_session_from_str

def create_pitchingstats_view():
    # Create session
    session = create_session_from_str(create_enginestr_from_values(mysql))

    """
    Notes regarding calculations

    1. p_IP
    Innings pitched. Take the number of IPouts and divide by 3 because there
    are three outs per inning. Baseball uses .1 and .2 to indicate partial
    innings pitched instead of .333 and .667.

    2. p_K_percent
    Percentage of strikeouts against batters faced. Take the number of
    strikeouts and divide by number of batters faced.

    3. p_BB_percent
    Percentage of walks against batters faced. Take the number of walks
    and divide by number of batters faced.

    4. p_HR_div9
    Home runs per 9 innings. Take the number of home runs and divide by
    number of innings. This gets the amount of home runs per inning. Then
    divide this number by 9 to get the number of home runs per 9 innings.

    5. p_BABIP
    <https://www.mlb.com/glossary/advanced-stats/babip>
    Batting Average on Balls In Play. i.e. batting average exclusively on
    balls hit into the field of play. This removes outcomes that the opponents
    defense has no affect on (strikeouts and homeruns). SF = sacrifice flies
    -- BABIP = (H - HR) / (AB - K - HR + SF)
    -- AB = BFP - BB - HBP - SF

    6. p_LOB_percent
    <https://library.fangraphs.com/pitching/lob/>
    Percentage of batters left on base. This means the number of batters
    that reach a base but are not allowed to score.
    -- LOB = (H + BB + HBP - R) / (H + BB + HBP - (1.4 * HR))

    7. p_HR_div_FB
    Uncalculatable. We do not have FB values.

    8.  FIP
    <https://library.fangraphs.com/pitching/fip/>
    -- FIP = (((13*HR)+3*(BB+HBP)-(2*K))/IP)+FIP constant
    -- FIP Constant = lgERA - (((13 * lgHR) + (3 * (lgBB + lgHBP)) - (2 * lgK)) / lgIP)

    9.  xFIP
    <https://www.mlb.com/glossary/advanced-stats/expected-fielding-independent-pitching>
    -- xFIP = ((13 * (FB * (lgHR / lgFB)) + 3 * (BB + HBP) - 2 * K) / IP) + FIP constant
    -- FIP Constant = lgERA - (((13*lgHR)+(3*(lgBB+lgHBP))-(2*lgK))/lgIP)
    -- well... p_FB and lgFB is not present in our database

    10. WAR
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
                -- IDK when they actually find the guys age for that season so i put 03.27 which is usually opening day
                (DATEDIFF(CONCAT(pi.yearID, '-03-27'), CONCAT(pe.birthYear, '-', pe.birthMonth, '-', pe.birthDay)) / 365.25)
            ELSE
                (DATEDIFF(CONCAT(pe.deathYear, '-', pe.deathMonth, '-', pe.deathDay), CONCAT(pe.birthYear, '-', pe.birthMonth, '-', pe.birthDay)) / 365.25)
        END AS age,
        FLOOR(pi.p_IPouts / 3) + (pi.p_IPouts % 3) * 0.1 AS p_IP,
        (pi.p_SO / pi.p_BFP) * 100 AS p_K_percent,
        (pi.p_BB / pi.p_BFP) * 100 AS p_BB_percent,
        (pi.p_HR / (pi.p_IPouts / 3.0)) * 9 AS p_HR_div9,
        (pi.p_H - pi.p_HR) / NULLIF((pi.p_BFP - pi.p_BB - pi.p_HBP - pi.p_SO - pi.p_HR), 0) AS p_BABIP,
        (pi.p_H + pi.p_BB + pi.p_HBP - pi.p_R) / NULLIF((pi.p_H + pi.p_BB + pi.p_HBP - (1.4 * pi.p_HR)), 0) * 100 AS p_LOB_percent,
        (
            ((13 * pi.p_HR) + (3 * (pi.p_BB + pi.p_HBP)) - (2 * pi.p_SO))
            /
            NULLIF((pi.p_IPouts / 3.0), 0)
        )
        +
        w.cFIP
        AS p_FIP
    FROM pitching pi
    JOIN people pe ON pe.playerID = pi.playerID
    JOIN lgavgview l ON pi.yearID = l.yearID
    JOIN wobaweights w ON w.yearID = pi.yearID;
    """

    # Create Pitching Stats View
    try:
        with session.connection() as connection:
            connection.execute(text(create_pitchingview_sql))
        print("View 'pitchingstatsview' created successfully")
    except Exception as e:
        print(f"Error creating 'pitchingstatsview' view: {e}")

    session.close()
