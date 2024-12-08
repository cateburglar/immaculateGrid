from csi3335f2024 import mysql
from sqlalchemy import text
from utils import create_enginestr_from_values, create_session_from_str


def setup_tables():
    session = create_session_from_str(create_enginestr_from_values(mysql))
    sql = get_sql()

    # Run the queries
    try:
        with session.connection() as connection:
            for query in sql:
                connection.execute(text(query))
        print("Table setup completed successfully")
    except Exception as e:
        print(f"Error setting up table: {e}")
        raise

    session.close()


# Creates the queries to modify the baseball database
def get_sql():
    sql = []

    # Increase park_name size to fit all park name
    teams_sql = (
        """ALTER TABLE teams MODIFY COLUMN park_name VARCHAR(100) DEFAULT NULL"""
    )
    sql.append(teams_sql)

    # Created this so that we could calculate woba correctly
    woba_weights_sql = """CREATE TABLE IF NOT EXISTS wobaweights ( 
    wobaweights_ID INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT, 
    yearID SMALLINT UNIQUE NOT NULL, 
    League FLOAT NOT NULL, 
    wOBAScale FLOAT NOT NULL, 
    wBB FLOAT NOT NULL, 
    wHBP FLOAT NOT NULL, 
    w1B FLOAT NOT NULL, 
    w2B FLOAT NOT NULL, 
    w3B FLOAT NOT NULL, 
    wHR FLOAT NOT NULL, 
    runSB FLOAT NOT NULL, 
    runCS FLOAT NOT NULL, 
    R_PA FLOAT NOT NULL, 
    R_W FLOAT NOT NULL, 
    cFIP FLOAT NOT NULL 
    )"""
    sql.append(woba_weights_sql)

    # Modifying columns to be non-null as they aren't and never should be
    schools_1 = (
        """ALTER TABLE schools MODIFY COLUMN school_name VARCHAR(255) NOT NULL"""
    )
    schools_2 = """ALTER TABLE schools MODIFY COLUMN school_city VARCHAR(55) NOT NULL"""
    schools_3 = (
        """ALTER TABLE schools MODIFY COLUMN school_state VARCHAR(55) NOT NULL"""
    )
    schools_4 = (
        """ALTER TABLE schools MODIFY COLUMN school_country VARCHAR(55) NOT NULL"""
    )
    sql.append(schools_1)
    sql.append(schools_2)
    sql.append(schools_3)
    sql.append(schools_4)

    # Alter seriespost table
    seriespost_1 = """ALTER TABLE seriespost ADD COLUMN lgIDwinner CHAR(3) NOT NULL AFTER teamIDwinner"""
    seriespost_2 = """ALTER TABLE seriespost ADD COLUMN lgIDloser CHAR(3) NOT NULL AFTER teamIDloser"""
    seriespost_3 = """ALTER TABLE seriespost ADD CONSTRAINT fk_lgIDwinner FOREIGN KEY (lgIDwinner) REFERENCES leagues(lgID)"""
    seriespost_4 = """ALTER TABLE seriespost ADD CONSTRAINT fk_lgIDloser FOREIGN KEY (lgIDloser) REFERENCES leagues(lgID);"""
    sql.append(seriespost_1)
    sql.append(seriespost_2)
    sql.append(seriespost_3)
    sql.append(seriespost_4)

    nl_hof_sql = "alter table people add column nl_hof boolean default false"
    sql.append(nl_hof_sql)

    # Changed note field in database to be varchar(255) to account for longer notes found in lahman database
    halloffame_sql = """ALTER TABLE halloffame MODIFY COLUMN note VARCHAR(255)"""
    sql.append(halloffame_sql)

    # Including draft information for the immaculate grid
    draft_sql = """CREATE TABLE IF NOT EXISTS `draft` ( 
        `draft_ID` int(12) NOT NULL AUTO_INCREMENT, 
        `playerID` varchar(9) NOT NULL, 
        `yearID` smallint(6) NOT NULL, 
        `teamID` char(3) NOT NULL, 
        PRIMARY KEY (`draft_ID`), 
        KEY `k_draft_team` (`teamID`), 
        KEY `draft_playerID_yearID_teamID` (`playerID`,`yearId`,`teamID`), 
        CONSTRAINT `draft_ibfk_1` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`) 
        ) ENGINE=InnoDB AUTO_INCREMENT=339783 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci"""
    sql.append(draft_sql)

    # Adding no_hitter information for the immaculate grid
    no_hitter_sql = """CREATE TABLE IF NOT EXISTS `nohitters` ( 
      `nohitters_ID` int(12) NOT NULL AUTO_INCREMENT, 
      `playerID` varchar(9) NOT NULL, 
      `yearID` smallint(6) NOT NULL, 
      `teamID` char(3) NOT NULL, 
      `date` char(9) NOT NULL, 
      `type` char(1) NOT NULL, 
      PRIMARY KEY (`nohitters_ID`), 
      KEY `k_nohitters_team` (`teamID`), 
      KEY `nohitters_playerID_yearID_teamID_date_type` (`playerID`,`yearId`,`teamID`, `date`, `type`), 
      CONSTRAINT `nohitters_ibfk_1` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`) 
    ) ENGINE=InnoDB AUTO_INCREMENT=339783 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci"""
    sql.append(no_hitter_sql)

    # Updating these rows for consistency
    awards_sql = """update awards set awardID = 'Rookie of the Year' where awardID = 'Rookie of the Year Award'"""
    sql.append(awards_sql)

    # Adding career war info for the immaculate grid
    career_war_sql = """CREATE TABLE IF NOT EXISTS `careerwarleaders` ( 
      `careerwarleaders_ID` int(12) NOT NULL AUTO_INCREMENT, 
      `playerID` varchar(9) NOT NULL, 
      `war` double NOT NULL, 
      PRIMARY KEY (`careerwarleaders_ID`), 
      KEY `careerwarleaders_playerID_war` (`playerID`,`war`), 
      CONSTRAINT `careerwarleaders_ibfk_1` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`) 
    ) ENGINE=InnoDB AUTO_INCREMENT=339815 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci"""
    sql.append(career_war_sql)

    # Adding season war info for the immaculate grid
    season_war_sql = """CREATE TABLE IF NOT EXISTS `seasonwarleaders` ( 
      `seasonwarleaders_ID` int(12) NOT NULL AUTO_INCREMENT, 
      `playerID` varchar(9) NOT NULL, 
      `war` double NOT NULL, 
       `yearID` smallint(6) NOT NULL, 
      PRIMARY KEY (`seasonwarleaders_ID`), 
      KEY `seasonwarleaders_playerID_war` (`playerID`,`war`), 
      CONSTRAINT `seasonwarleaders_ibfk_1` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`) 
    ) ENGINE=InnoDB AUTO_INCREMENT=339815 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci"""
    sql.append(season_war_sql)

    batting_sql = """ALTER TABLE batting ADD COLUMN b_1B SMALLINT(6) AS (b_H - (b_2B + b_3B + b_HR)) STORED AFTER b_H"""
    sql.append(batting_sql)

    # Added to provide an easy way to access summary and depth chart info
    pitching_stats_sql = """CREATE TABLE IF NOT EXISTS `pitchingstats` ( 
        pitchingstats_ID int(12) not null auto_increment, 
        playerID VARCHAR(9) NOT NULL, 
        teamID CHAR(3) NOT NULL, 
        yearID SMALLINT(6) NOT NULL, 
        stint SMALLINT(4) NOT NULL, 
        nameFirst VARCHAR(255), 
        nameLast VARCHAR(255), 
        nameGiven VARCHAR(255), 
        p_G SMALLINT(6), 
        P_GS SMALLINT(6), 
        p_ERA DOUBLE, 
        age DECIMAL(13,4), 
        p_IP DECIMAL(15,4), 
        p_K_percent DECIMAL(12,4), 
        p_BB_percent DECIMAL(12,4), 
        p_HR_div9 DECIMAL(17,8), 
        p_BABIP DECIMAL(10,4), 
        p_LOB_percent DECIMAL(16,4), 
        p_FIP DOUBLE, 
        p_playing_time INTEGER,
        PRIMARY KEY (`pitchingstats_ID`), 
        KEY `k_pstats_team` (`teamID`), 
        KEY `pstats_playerID_yearID_teamID` (`playerID`,`yearID`,`teamID`), 
        CONSTRAINT `pstats_ibfk_1` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`) 
        ) ENGINE=InnoDB AUTO_INCREMENT=227599 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci"""
    sql.append(pitching_stats_sql)

    # Added to provide an easy way to access summary and depth chart info
    batting_stats_sql = """CREATE TABLE IF NOT EXISTS `battingstats` ( 
        battingstats_ID INT(12) NOT NULL AUTO_INCREMENT, 
        playerID VARCHAR(9) NOT NULL, 
        age BIGINT(13), 
        yearID SMALLINT(6) NOT NULL, 
        teamID CHAR(3) NOT NULL, 
        stint SMALLINT(4) NOT NULL, 
        nameFirst VARCHAR(255), 
        nameLast VARCHAR(255), 
        nameGiven VARCHAR(255), 
        b_G SMALLINT(6), 
        b_PA BIGINT(10), 
        b_HR SMALLINT(6), 
        b_SB SMALLINT(6), 
        b_BB_percent DECIMAL(12,4), 
        b_K_percent DECIMAL(12,4), 
        b_BABIP DECIMAL(10,4), 
        b_AVG DECIMAL(9,4), 
        b_SLG DECIMAL(15,4), 
        b_ISO DECIMAL(16,4), 
        b_b_1B INT(9), 
        b_wOBA DOUBLE, 
        b_wRC DOUBLE, 
        PRIMARY KEY (`battingstats_ID`), 
        KEY `k_bstats_team` (`teamID`), 
        KEY `bstats_playerID_yearID_teamID` (`playerID`, `yearID`, `teamID`), 
        CONSTRAINT `bstats_ibfk_1` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`) 
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci"""
    sql.append(batting_stats_sql)

    return sql
