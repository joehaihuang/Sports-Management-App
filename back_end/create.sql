DROP DATABASE IF EXISTS tm;

create database tm;
use tm;

-- A registered school
create table school (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL
);

-- Player information
create table player (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    dob DATE,
    phone_number VARCHAR(20),

    school_id_FK INT,
    FOREIGN KEY(school_id_FK) REFERENCES school(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tournament information
create table tournament(
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    address VARCHAR(100) NOT NULL

);

-- A competitive division within a tournament
create table division(
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    max_teams INT,
    
    tournament_id_FK INT NOT NULL,
    FOREIGN KEY (tournament_id_FK) REFERENCES tournament(id)
		ON UPDATE CASCADE ON DELETE CASCADE
);

-- Two players competing in a division together
create table team (
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    
    division_id_FK INT NOT NULL,
    FOREIGN KEY (division_id_FK) REFERENCES division(id)
		ON UPDATE CASCADE ON DELETE CASCADE,
    
	player1_id_FK INT NOT NULL,
    player2_id_FK INT NOT NULL,
    
    FOREIGN KEY (player1_id_FK) REFERENCES player(id)
		ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (player2_id_FK) REFERENCES player(id)
		ON UPDATE CASCADE ON DELETE RESTRICT
);

-- General match data
create table match_data (
	id INT AUTO_INCREMENT PRIMARY KEY,
    play_to INT NOT NULL,
    hard_cap INT,
    best_of INT NOT NULL,

    team1_id_FK INT NOT NULL,
    team2_id_FK INT NOT NULL,

    FOREIGN KEY (team1_id_FK) REFERENCES team(id)
		ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (team2_id_FK) REFERENCES team(id)
		ON UPDATE CASCADE ON DELETE RESTRICT,

	winner_id_FK INT,
	FOREIGN KEY (winner_id_FK) REFERENCES team(id)
		ON UPDATE CASCADE ON DELETE RESTRICT,
    
    division_id_FK INT NOT NULL,
    FOREIGN KEY (division_id_FK) REFERENCES division(id)
		ON UPDATE CASCADE ON DELETE CASCADE
);

-- Game data within a match
create table game_data (
	id INT AUTO_INCREMENT PRIMARY KEY,
    team1_score INT,
    team2_score INT,
    
    match_id_FK INT NOT NULL,
    FOREIGN KEY (match_id_FK) REFERENCES match_data(id)
		ON UPDATE CASCADE ON DELETE CASCADE
);











