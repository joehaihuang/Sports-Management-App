use tm;

-- MISC PROCEDURES

-- Gets all columns from a table
drop procedure if exists get_columns_from_table;
DELIMITER //
create procedure get_columns_from_table(IN tab_name VARCHAR(255), db_name VARCHAR(255))
BEGIN
    SELECT COLUMN_NAME, DATA_TYPE, COLUMN_KEY, IS_NULLABLE
	FROM INFORMATION_SCHEMA.COLUMNS
	WHERE TABLE_NAME = tab_name and TABLE_SCHEMA = db_name
    ORDER BY ORDINAL_POSITION;
END //
DELIMITER ;

call get_columns_from_table('team', 'tm');

-- SCHOOL PROCEDURES

-- Gets all school info
drop procedure if exists view_all_schools;
DELIMITER //
create procedure view_all_schools()
BEGIN
    SELECT * FROM school;
END //
DELIMITER ;

call view_all_schools();

-- Gets specific school info
drop procedure if exists view_specific_school;
DELIMITER //
create procedure view_specific_school(IN s_id INT)
BEGIN
	SELECT * FROM school WHERE id = s_id;
END //
DELIMITER ;

call view_specific_school(0);

-- Gets all the players from this specific school
drop procedure if exists get_players_from_school;
DELIMITER //
create procedure get_players_from_school(IN s_id INT)
BEGIN
    SELECT * FROM player WHERE school_id_FK = s_id;
END //
DELIMITER ;

call get_players_from_school(0);


-- PLAYER PROCEDURES

-- Gets all player info
drop procedure if exists view_all_players;
DELIMITER //
create procedure view_all_players()
BEGIN
	SELECT * FROM player;
END //
DELIMITER ;

call view_all_players();

-- Gets specific player info
drop procedure if exists view_specific_player;
DELIMITER //
create procedure view_specific_player(IN p_id INT)
BEGIN
	SELECT * FROM player WHERE id = p_id;
END //
DELIMITER ;

call view_specific_player(1);

-- Gets all players from a specific team
drop procedure if exists view_all_team_players;
DELIMITER //
create procedure view_all_team_players(IN te_id INT)
BEGIN
    SELECT * FROM player WHERE id in
    (SELECT player1_id_FK as ids FROM team WHERE id = te_id
    UNION
    SELECT player2_id_FK as ids FROM team WHERE id = te_id);

END //
DELIMITER ;

call view_all_team_players(1);


-- TOURNAMENT PROCEDURES

-- Gets all tournament info
drop procedure if exists view_all_tournaments;
DELIMITER //
create procedure view_all_tournaments()
BEGIN
	SELECT * FROM tournament;
END //
DELIMITER ;

call view_all_tournaments();

-- Gets specific tournament info
drop procedure if exists view_specific_tournament;
DELIMITER //
create procedure view_specific_tournament(IN to_id INT)
BEGIN
	SELECT * FROM tournament WHERE id = to_id;
END //
DELIMITER ;

call view_specific_tournament(2);


-- DIVISION PROCEDURES

-- Gets all division info for a specific tournament
drop procedure if exists view_all_tournament_divisions;
DELIMITER //
create procedure view_all_tournament_divisions(IN to_id INT)
BEGIN
	SELECT * FROM division WHERE tournament_id_FK = to_id;
END //
DELIMITER ;

call view_all_tournament_divisions(2);

-- Gets specific division info
drop procedure if exists view_specific_division;
DELIMITER //
create procedure view_specific_division(IN d_id INT)
BEGIN
	SELECT * FROM division WHERE id = d_id;
END //
DELIMITER ;

call view_specific_division(2);


-- TEAM PROCEDURES

-- Gets all team info for a specific division
drop procedure if exists view_all_division_teams;
DELIMITER //
create procedure view_all_division_teams(IN d_id INT)
BEGIN
	SELECT * FROM team WHERE division_id_FK = d_id;
END //
DELIMITER ;

call view_all_division_teams(2);

-- Gets specific team info
drop procedure if exists view_specific_division;
DELIMITER //
create procedure view_specific_division(IN to_id INT)
BEGIN
	SELECT * FROM team WHERE id = to_id;
END //
DELIMITER ;

call view_specific_division(3);


-- MATCH PROCEDURES

-- Gets all match info for a specific division
drop procedure if exists view_all_division_matches;
DELIMITER //
create procedure view_all_division_matches(IN d_id INT)
BEGIN
	SELECT * FROM match_data WHERE division_id_FK = d_id;
END //
DELIMITER ;

call view_all_division_matches(2);

-- Gets specific match info
drop procedure if exists view_specific_match;
DELIMITER //
create procedure view_specific_match(IN m_id INT)
BEGIN
	SELECT * FROM match_data WHERE id = m_id;
END //
DELIMITER ;

call view_specific_match(3);

-- Update match info
drop procedure if exists update_match_winner;
DELIMITER //
create procedure update_match_winner(IN m_id INT)
BEGIN
	DECLARE team1_wins INT;
    DECLARE team2_wins INT;
	DECLARE best_of INT;

    SELECT count(*) INTO team1_wins
    FROM game_data as gd
    WHERE gd.match_id_FK = m_id and gd.team1_score > gd.team2_score;

    SELECT count(*) INTO team2_wins
    FROM game_data as gd
    WHERE gd.match_id_FK = m_id and gd.team2_score > gd.team1_score;

	SELECT best_of INTO best_of
    FROM match_data as md
    WHERE md.id = m_id;

    IF team1_wins = CEIL(best_of) THEN
        UPDATE match_data as md
        SET md.winner_id_FK = md.team1_id_FK
        WHERE md.id = m_id;
    ELSEIF team2_wins = CEIL(best_of) THEN
        UPDATE match_data as md
        SET md.winner_id_FK = md.team2_id_FK
        WHERE md.id = m_id;
    END IF;
END //
DELIMITER ;


-- GAME PROCEDURES

-- Gets all game info for a specific match
drop procedure if exists view_all_match_games;
DELIMITER //
create procedure view_all_match_games(IN m_id INT)
BEGIN
	SELECT * FROM game_data WHERE match_id_FK = m_id;
END //
DELIMITER ;

call view_all_match_games(2);

-- Gets specific game info
drop procedure if exists view_specific_game;
DELIMITER //
create procedure view_specific_game(IN g_id INT)
BEGIN
	SELECT * FROM game_data WHERE id = g_id;
END //
DELIMITER ;

call view_specific_game(3);


-- MATCH TRIGGERS

-- Create games based on match info
drop trigger if exists create_games_on_new_match;
delimiter //
create trigger create_games_on_new_match
	after insert on match_data
    for each row
BEGIN
    DECLARE games INT;
    SET games = NEW.best_of;

    WHILE games > 0 DO
        INSERT INTO game_data (team1_score, team2_score, match_id_FK) VALUES (0, 0, NEW.id);
        SET games = games - 1;
    END WHILE;
END //
delimiter ;


-- GAME TRIGGERS

-- Update match winner on game update
drop trigger if exists update_match_on_update_game;
delimiter //
create trigger update_match_on_update_game
	after update on game_data
    for each row
BEGIN
    CALL update_match_winner(NEW.match_id_FK);
END //
delimiter ;