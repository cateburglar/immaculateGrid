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
    CREATE OR REPLACE VIEW lgavgview AS
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
        print("View 'lgavgview' created successfully")
    except Exception as e:
        print(f"Error creating 'lgavgview' view: {e}")

    session.close()

def create_pitchingstats_view():
    # Create session
    session = create_session_from_str(create_enginestr_from_values(mysql))

    """
    Notes regarding calculations

    1. p_IP
    Innings pitched. Take the number of IPouts and divide by 3 because there
    are three outs per inning.

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
                (DATEDIFF(CURDATE(), CONCAT(pe.birthYear, '-', pe.birthMonth, '-', pe.birthDay)) / 365.25)
            ELSE
                (DATEDIFF(CONCAT(pe.deathYear, '-', pe.deathMonth, '-', pe.deathDay), CONCAT(pe.birthYear, '-', pe.birthMonth, '-', pe.birthDay)) / 365.25)
        END AS age,
        pi.p_IPouts / 3.0 AS p_IP,
        (pi.p_SO / pi.p_BFP) * 100 AS p_K_percent,
        (pi.p_BB / pi.p_BFP) * 100 AS p_BB_percent,
        (pi.p_HR / (pi.p_IPouts / 3.0)) / 9 AS p_HR_div9,
        -- BABIP = (H - HR) / (AB - K - HR + SF)
        (pi.p_H - pi.p_HR) / (pi.p_BFP - pi.p_SO - pi.p_HR + pi.p_SF) AS p_BABIP,
        -- LOB = (H + BB + HBP - R) / (H + BB + HBP - (1.4 * HR))
        (pi.p_H + pi.p_BB + pi.p_HBP - pi.p_R) / (pi.p_H + pi.p_BB + pi.p_HBP - (1.4 * pi.p_HR)) * 100 AS p_LOB_percent,
        -- NULL AS p_HR_div_FB,
        -- FIP = (((13*HR)+3*(BB+HBP)-(2*K))/IP)+FIP constant
        -- FIP Constant = lgERA - (((13 * lgHR) + (3 * (lgBB + lgHBP)) - (2 * lgK)) / lgIP)
        ((13 * pi.p_HR) + (3 * (pi.p_BB + pi.p_HBP)) - (2 * pi.p_SO)) / (pi.p_IPouts / 3.0) + (l.lgERA - (((13 * l.lgHR) + (3 * (l.lgBB + l.lgHBP)) - (2 * l.lgK)) / l.lgIP)) AS p_FIP
        -- ((13 * (pi.p_FB * (l.lgHR / l.lgFB)) + (3 * (pi.p_BB + pi.p_HBP)) - (2 * pi.p_SO)) / (pi.p_IPouts / 3.0) + (l.lgERA - (((13 * l.lgHR) + (3 * (l.lgBB + l.lgHBP)) - (2 * l.lgK)) / l.lgIP)) AS p_xFIP,
        -- NULL AS p_xFIP,
        -- NULL AS p_WAR
    FROM pitching pi
    JOIN people pe ON pe.playerID = pi.playerID
    JOIN lgavgview l ON pi.yearID = l.yearID;
    """

    # Create Pitching Stats View
    try:
        with session.connection() as connection:
            connection.execute(text(create_pitchingview_sql))
        print("View 'pitchingstatsview' created successfully")
    except Exception as e:
        print(f"Error creating 'pitchingstatsview' view: {e}")

    session.close()

def create_battingstats_view():
    # Create session using the utility function
    engine_str = create_enginestr_from_values(mysql=mysql)  # Ensure `mysql` is passed correctly
    session = create_session_from_str(engine_str)

    # Define the SQL query
    create_battingstats_view_sql = """
    CREATE OR REPLACE VIEW battingstatsview AS
    SELECT
        CONCAT(p.nameFirst, ' ', p.nameLast) AS name,
        (b.yearID - p.birthYear) AS age,
        b.yearID AS yearID,
        b.teamID AS teamID,
        b.stint AS stint,
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
        (((w.wBB * b.b_BB) + (w.wHBP * b.b_HBP) + (w.w1b * (b.b_H - (b.b_2B + b.b_3B + b.b_HR))) + (w.w2b * b.b_2B) + (w.w3b * b.b_3B) + (w.whr * b.b_HR)) 
            / (b.b_AB + b.b_BB - b.b_IBB + b.b_SF + b.b_HBP)) AS b_wOBA,
        
        (   
        ((
        (((w.wBB * b.b_BB) + (w.wHBP * b.b_HBP) + (w.w1b * (b.b_H - (b.b_2B + b.b_3B + b.b_HR))) + (w.w2b * b.b_2B) + (w.w3b * b.b_3B) + (w.whr * b.b_HR)) 
            / (b.b_AB + b.b_BB - b.b_IBB + b.b_SF + b.b_HBP))
            - w.league
        )  / w.wobascale)
        + ( w.r_pa)
        ) * (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF) -- PA
        AS b_wRC,        

        ((b.b_SB - b.b_CS) * 0.2) AS b_BsR
    FROM
        batting b
    JOIN
        people p ON b.playerID = p.playerID
    JOIN
        appearances a ON b.playerID = a.playerID AND b.yearID = a.yearID
    JOIN
        fielding f ON b.playerID = f.playerID AND b.yearID = f.yearID
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