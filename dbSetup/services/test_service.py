import csi3335f2024 as cfg
from models import AllstarFull, Appearances, Fielding, People, Pitching, Schools, Teams
from utils import create_enginestr_from_values, create_session_from_str


def execute_tests(tests):
    for test in tests:
        if test == "allstarfull":
            compare_existing_allstarfull_entries()
        elif test == "people":
            compare_existing_people_entries()
        elif test == "schools":
            compare_existing_schools_entries()
        elif test == "teams":
            compare_existing_teams_entries()
        elif test == "pitching":
            compare_existing_pitching_entries()
        elif test == "appearances":
            compare_existing_appearances_entries()
        elif test == "fielding":
            compare_existing_fielding_entries()
        elif test == "homegames":
            compare_existing_homegames_entries()
        else:
            print(f"Unknown test: {test}")


def compare_existing_allstarfull_entries():
    print("Executing allstarfull test")

    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    # Get the original AllstarFull rows
    bb_result = bb_session.query(AllstarFull).all()

    # Go through each row in the original baseball database to make sure ours matches
    rows_match = True
    for row in bb_result:
        row_exists = (
            sq_session.query(AllstarFull)
            .filter_by(
                allstarfull_ID=row.allstarfull_ID,
                playerID=row.playerID,
                yearID=row.yearID,
                lgID=row.lgID,
                teamID=row.teamID,
                gameID=row.gameID,
                GP=row.GP,
                startingPos=row.startingPos,
            )
            .first()
        )

        # Alert that test failed, and for what row
        if not row_exists:
            print(
                f"Row could not be found for: playerid={row.playerID}, yearid={row.yearID}, lgID={row.lgID}, teamID={row.teamID}"
            )
            rows_match = False

    # Commit and close sessions
    sq_session.commit()
    sq_session.close()
    bb_session.commit()
    bb_session.close()

    # Output test result
    if not rows_match:
        return "FAILURE: allstarfull"
    else:
        return ""


def compare_existing_people_entries():
    print("Executing people entries")

    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    # Get all rows from the original People table
    bb_result = bb_session.query(People).all()

    # Go through each row in the original baseball database to make sure ours matches
    rows_match = True
    for row in bb_result:
        # Test without death dates, as those can change
        if row.deathYear is None:
            row_exists = (
                sq_session.query(People)
                .filter_by(
                    playerID=row.playerID,
                    birthYear=row.birthYear,
                    birthMonth=row.birthMonth,
                    birthDay=row.birthDay,
                    birthCity=row.birthCity,
                    birthCountry=row.birthCountry,
                    birthState=row.birthState,
                    nameFirst=row.nameFirst,
                    nameLast=row.nameLast,
                    nameGiven=row.nameGiven,
                    weight=row.weight,
                    height=row.height,
                    bats=row.bats,
                    throws=row.throws,
                    debutDate=row.debutDate,
                    finalGameDate=row.finalGameDate,
                )
                .first()
            )
        else:
            row_exists = (
                sq_session.query(People)
                .filter_by(
                    playerID=row.playerID,
                    birthYear=row.birthYear,
                    birthMonth=row.birthMonth,
                    birthDay=row.birthDay,
                    birthCity=row.birthCity,
                    birthCountry=row.birthCountry,
                    birthState=row.birthState,
                    deathYear=row.deathYear,
                    deathMonth=row.deathMonth,
                    deathDay=row.deathDay,
                    deathCountry=row.deathCountry,
                    deathState=row.deathState,
                    deathCity=row.deathCity,
                    nameFirst=row.nameFirst,
                    nameLast=row.nameLast,
                    nameGiven=row.nameGiven,
                    weight=row.weight,
                    height=row.height,
                    bats=row.bats,
                    throws=row.throws,
                    debutDate=row.debutDate,
                    finalGameDate=row.finalGameDate,
                )
                .first()
            )

        # Alert that test failed, and for what row
        if not row_exists:
            print(f"Row does not match for: playerid={row.playerID}")
            rows_match = False

    # Commit and close sessions
    sq_session.commit()
    sq_session.close()
    bb_session.commit()
    bb_session.close()

    # Output test result
    if not rows_match:
        return "FAILURE: people"
    else:
        return ""


def compare_existing_teams_entries():
    print("Executing teams entries")
    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    # Get all rows from the original People table
    bb_result = bb_session.query(Teams).all()

    # Go through each row in the original baseball database to make sure ours matches
    rows_match = True
    for row in bb_result:
        row_exists = (
            sq_session.query(Teams)
            .filter_by(
                yearID=row.yearID,
                lgID=row.lgID,
                teamID=row.teamID,
                franchID=row.franchID,
                divID=row.divID,
                team_name=row.team_name,
                team_rank=row.team_rank,
                team_G=row.team_G,
                team_G_home=row.team_G_home,
                team_W=row.team_W,
                team_L=row.team_L,
                DivWin=row.DivWin,
                WCWin=row.WCWin,
                LgWin=row.LgWin,
                WSWin=row.WSWin,
                team_R=row.team_R,
                team_AB=row.team_AB,
                team_H=row.team_H,
                team_2B=row.team_2B,
                team_3B=row.team_3B,
                team_HR=row.team_HR,
                team_BB=row.team_BB,
                team_SO=row.team_SO,
                team_SB=row.team_SB,
                team_CS=row.team_CS,
                team_HBP=row.team_HBP,
                team_SF=row.team_SF,
                team_RA=row.team_RA,
                team_ER=row.team_ER,
                team_ERA=row.team_ERA,
                team_CG=row.team_CG,
                team_SHO=row.team_SHO,
                team_SV=row.team_SV,
                team_IPouts=row.team_IPouts,
                team_HA=row.team_HA,
                team_HRA=row.team_HRA,
                team_BBA=row.team_BBA,
                team_SOA=row.team_SOA,
                team_E=row.team_E,
                team_DP=row.team_DP,
                team_FP=row.team_FP,
                park_name=row.park_name,
                team_attendance=row.team_attendance,
                team_BPF=row.team_BPF,
                team_PPF=row.team_PPF,
                # team_projW=row.team_projW, # Excluded as these are calculated
                # team_projL=row.team_projL,
            )
            .first()
        )

        # Alert that test failed, and for what row
        if not row_exists:
            print(
                f"Row does not match for: teamID={row.teamID}, yearID={row.yearID}, lgID={row.lgID}"
            )
            rows_match = False

    # Commit and close sessions
    sq_session.commit()
    sq_session.close()
    bb_session.commit()
    bb_session.close()

    # Output test result
    if not rows_match:
        return "FAILURE: teams"
    else:
        return ""


def compare_existing_schools_entries():
    print("Executing schools test")

    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    # Get the original Schools rows
    bb_result = bb_session.query(Schools).all()

    # Go through each row in the original baseball database to make sure ours matches
    rows_match = True
    for row in bb_result:
        row_exists = (
            sq_session.query(Schools)
            .filter_by(
                schoolId=row.schoolId,
                school_name=row.school_name,
                school_city=row.school_city,
                school_state=row.school_state,
                # school_country=row.school_country, # Countries aren't stored correctly in the original baseball db
            )
            .first()
        )

        # Alert that test failed, and for what row
        if not row_exists:
            print(
                f"Row does not match for: schoolId={row.schoolId}, school_name={row.school_name}"
            )
            rows_match = False

    # Commit and close sessions
    sq_session.commit()
    sq_session.close()
    bb_session.commit()
    bb_session.close()

    # Output test result
    if not rows_match:
        return "FAILURE: schools"
    else:
        return ""


def compare_existing_pitching_entries():
    print("Executing pitching test")

    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    # Get the original pitching csv rows
    bb_result = bb_session.query(Pitching).all()

    # Go through each row in the original baseball database to make sure ours matches
    rows_match = True
    for pitching_record in bb_result:
        row_exists = (
            sq_session.query(Pitching)
            .filter_by(
                playerID=pitching_record.playerID,
                yearID=pitching_record.yearID,
                teamID=pitching_record.teamID,
                stint=pitching_record.stint,
                p_W=pitching_record.p_W,
                p_L=pitching_record.p_L,
                p_G=pitching_record.p_G,
                p_GS=pitching_record.p_GS,
                p_CG=pitching_record.p_CG,
                p_SHO=pitching_record.p_SHO,
                p_SV=pitching_record.p_SV,
                p_IPouts=pitching_record.p_IPouts,
                p_H=pitching_record.p_H,
                p_ER=pitching_record.p_ER,
                p_BB=pitching_record.p_BB,
                p_SO=pitching_record.p_SO,
                p_BAOpp=pitching_record.p_BAOpp,
                p_ERA=pitching_record.p_ERA,
                p_IBB=pitching_record.p_IBB,
                p_WP=pitching_record.p_WP,
                p_HBP=pitching_record.p_HBP,
                p_BK=pitching_record.p_BK,
                p_BFP=pitching_record.p_BFP,
                p_GF=pitching_record.p_GF,
                p_R=pitching_record.p_R,
                p_SH=pitching_record.p_SH,
                p_SF=pitching_record.p_SF,
                p_GIDP=pitching_record.p_GIDP,
            )
            .first()
        )

        # Alert that test failed, and for what row
        if not row_exists:
            print(
                f"Row could not be found for: playerid={pitching_record.playerID}, "
                f"yearid={pitching_record.yearID}, teamId={pitching_record.teamID}, "
                f"stint={pitching_record.stint}"
            )
            rows_match = False

    # Commit and close sessions
    sq_session.commit()
    sq_session.close()
    bb_session.commit()
    bb_session.close()

    # Output test result
    if not rows_match:
        return "FAILURE: pitching"
    else:
        return ""


def compare_existing_appearances_entries():
    print("Executing appearances entries")

    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    # Get all rows from the original People table
    bb_result = bb_session.query(Appearances).all()

    # Go through each row in the original baseball database to make sure ours matches
    rows_match = True
    for row in bb_result:
        row_exists = (
            sq_session.query(Appearances)
            .filter_by(
                playerID=row.playerID,
                yearID=row.yearID,
                teamID=row.teamID,
                G_all=row.G_all,
                GS=row.GS,
                G_batting=row.G_batting,
                G_defense=row.G_defense,
                G_p=row.G_p,
                G_c=row.G_c,
                G_1b=row.G_1b,
                G_2b=row.G_2b,
                G_3b=row.G_3b,
                G_ss=row.G_ss,
                G_lf=row.G_lf,
                G_cf=row.G_cf,
                G_rf=row.G_rf,
                G_of=row.G_of,
                G_dh=row.G_dh,
                G_ph=row.G_ph,
                G_pr=row.G_pr,
            )
            .first()
        )

        # Alert that test failed, and for what row
        if not row_exists:
            print(f"Row does match for: playerid={row.playerID}")
            rows_match = False

    # Commit and close sessions
    sq_session.commit()
    sq_session.close()
    bb_session.commit()
    bb_session.close()

    # Output test result
    if not rows_match:
        return "FAILURE: appearances"
    else:
        return ""


def compare_existing_fielding_entries():
    print("Executing fielding entries")

    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    # Get all rows from the original People table
    bb_result = bb_session.query(Fielding).all()

    # Go through each row in the original baseball database to make sure ours matches
    rows_match = True
    for row in bb_result:
        row_exists = (
            sq_session.query(Fielding)
            .filter_by(
                playerID=row.playerID,
                yearID=row.yearID,
                teamID=row.teamID,
                stint=row.stint,
                position=row.position,
                f_G=row.f_G,
                f_GS=row.f_GS,
                f_InnOuts=row.f_InnOuts,
                f_PO=row.f_PO,
                f_A=row.f_A,
                f_E=row.f_E,
                f_DP=row.f_DP,
                f_PB=row.f_PB,
                f_WP=row.f_WP,
                f_SB=row.f_SB,
                f_CS=row.f_CS,
                f_ZR=row.f_ZR,
            )
            .first()
        )

        # Alert that test failed, and for what row
        if not row_exists:
            print(f"Row does match for: playerid={row.playerID}")
            rows_match = False

    # Commit and close sessions
    sq_session.commit()
    sq_session.close()
    bb_session.commit()
    bb_session.close()

    # Output test result
    if not rows_match:
        return "FAILURE: fielding"
    else:
        return ""


def compare_existing_homegames_entries():
    print("Executing homegames entries")

    # Create sessions
    sq_session = create_session_from_str(create_enginestr_from_values(cfg.mysql))
    bb_session = create_session_from_str(
        create_enginestr_from_values(cfg.baseballmysql)
    )

    # Get all rows from the original HomeGames table
    bb_result = bb_session.query(HomeGames).all()

    # Go through each row in the original baseball database to make sure ours matches
    rows_match = True
    for row in bb_result:
        row_exists = (
            sq_session.query(HomeGames)
            .filter_by(
                homegames_ID = row.homegames_ID,
                teamID = row.teamID ,
                parkID = row.parkID,
                yearID = row.yearID,
                firstGame = row.firstGame, 
                lastGame = row.lastGame,
                games = row.games,
                openings = row.openings,
                attendance = row.attendance, 
            )
            .first()
        )

        # Alert that test failed, and for what row
        if not row_exists:
            print(f"Row does match for: homegames id={row.homegames_ID}")
            rows_match = False

    # Commit and close sessions
    sq_session.commit()
    sq_session.close()
    bb_session.commit()
    bb_session.close()

    # Output test result
    if not rows_match:
        return "FAILURE: home games"
    else:
        return ""
