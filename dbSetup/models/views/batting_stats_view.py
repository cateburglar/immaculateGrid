from flask import session
from sqlalchemy import text
from utils import create_enginestr_from_values, create_session_from_str
from sqlalchemy.orm import Session

# Generate engine string from utility function
database_values = {
    "dialect": "sqlite",  # Replace with your actual database dialect
    "database": "your_database.db",  # Replace with your actual database name
}


# Define the SQL query
create_view_query = """
CREATE VIEW Batting_Stats_2 AS
SELECT 
    Name,
    Age,
    G,
    PA,
    HR,
    SB,
    `BB%`,
    `K%`,
    BABIP,
    AVG,
    SLG,
    ISO,
    b_1B,
    wOBA,
    wRCplus,
    BsR,
    Total_Defensive_Plays,
    FRAA,
    ((wRCplus - 100) / 100 * PA / 10 + BsR + FRAA + 
    (CASE 
        WHEN position = 'SS' THEN 2
        WHEN position = 'CF' THEN 1
        WHEN position = '1B' THEN -1
        ELSE 0
    END) + 0.5 + 25) / 10 AS WAR,
    YearID,
    TeamID,
    Team_Name
FROM (
    SELECT 
        CONCAT(p.nameFirst, ' ', p.nameLast) AS Name,
        (b.yearID - p.birthYear) AS Age,
        a.G_ALL AS G,
        (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF) AS PA,
        b.b_HR AS HR,
        b.b_SB AS SB,
        (b.b_BB / (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF)) * 100 AS `BB%`,
        (b.b_SO / (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF)) * 100 AS `K%`,
        (b.b_H - b.b_HR) / (b.b_AB - b.b_SO - b.b_HR + b.b_SF) AS BABIP,
        (b.b_H / b.b_AB) AS AVG,
        ((b.b_H - (b.b_2B + b.b_3B + b.b_HR)) + (2 * b.b_2B) + (3 * b.b_3B) + (4 * b.b_HR)) / b.b_AB AS SLG,
        (((b.b_H - (b.b_2B + b.b_3B + b.b_HR)) + (2 * b.b_2B) + (3 * b.b_3B) + (4 * b.b_HR)) / b.b_AB) - (b.b_H / b.b_AB) AS ISO,
        (b.b_H - (b.b_2B + b.b_3B + b.b_HR)) AS b_1B,
        (((0.69 * b.b_BB) + (0.72 * b.b_HBP) + (0.88 * (b.b_H - (b.b_2B + b.b_3B + b.b_HR))) + (1.24 * b.b_2B) + (1.56 * b.b_3B) + (2.0 * b.b_HR)) / (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF)) AS wOBA,
        ((((((0.69 * b.b_BB) + (0.72 * b.b_HBP) + (0.88 * (b.b_H - (b.b_2B + b.b_3B + b.b_HR))) + (1.24 * b.b_2B) + (1.56 * b.b_3B) + (2.0 * b.b_HR)) / (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF)) - 0.320) / 1.25 * (b.b_AB + b.b_BB + b.b_HBP + b.b_SH + b.b_SF) + 6500) / 4000 * 100) AS wRCplus,
        ((b.b_SB - b.b_CS) * 0.2) AS BsR,
        (f.f_PO + f.f_A) AS Total_Defensive_Plays,
        ((f.f_PO + f.f_A) * 0.1 + f.f_ZR * 0.2 + f.f_DP * 0.5) AS FRAA,
        b.yearID AS YearID,
        t.teamID AS TeamID,
        t.team_name AS Team_Name,
        f.position AS position
    FROM 
        batting b
    JOIN 
        people p ON b.playerID = p.playerID
    JOIN 
        appearances a ON b.playerID = a.playerID AND b.yearID = a.yearID
    JOIN 
        teams t ON b.teamID = t.teamID AND b.yearID = t.yearID
    JOIN 
        fielding f ON b.playerID = f.playerID AND b.yearID = f.yearID
) AS SubQuery;
"""

# Execute the raw SQL
session.commit()
session.close()
