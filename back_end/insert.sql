use tm;

-- School Data
INSERT INTO school (id, name, address) VALUES (1, "Northeastern University", "Boston");
INSERT INTO school (id, name, address) VALUES (2, "Boston University", "Boston");

-- Player Data
INSERT INTO player (id, name, dob, phone_number, school_id_FK) VALUES (1, "John", "2001-01-01", "213-481-4123", 1);
INSERT INTO player (id, name, dob, phone_number, school_id_FK) VALUES (2, "Bob", "2002-01-01", "213-455-4173", 1);
INSERT INTO player (id, name, dob, phone_number, school_id_FK) VALUES (3, "Dave", "2001-04-01", "293-451-4124", 1);

INSERT INTO player (id, name, dob, phone_number, school_id_FK) VALUES (4, "Ron", "2003-05-07", "213-132-4123", 2);
INSERT INTO player (id, name, dob, phone_number, school_id_FK) VALUES (5, "Liam", "2004-11-12", "412-451-4123", 2);
INSERT INTO player (id, name, dob, phone_number, school_id_FK) VALUES (6, "Nate", "2002-02-23", "213-451-4143", 2);

INSERT INTO player (id, name, dob, phone_number, school_id_FK) VALUES (7, "James", "2003-05-07", "213-132-4153", 1);
INSERT INTO player (id, name, dob, phone_number, school_id_FK) VALUES (8, "Inigo", "2004-11-12", "412-434-4123", 1);
INSERT INTO player (id, name, dob, phone_number, school_id_FK) VALUES (9, "Sadge", "2002-02-23", "213-451-2143",1 );

-- Tournament Data
INSERT INTO tournament (id, name , date, time, address) VALUES (1, "Big T", "2019-01-01", "12:30:00", "Boston");
INSERT INTO tournament (id, name , date, time, address) VALUES (2, "Big L", "2019-04-01", "12:45:00", "Dallas");
INSERT INTO tournament (id, name , date, time, address) VALUES (3, "Big X", "2018-02-01", "01:00:00", "Marlough");

-- Division Data
INSERT INTO division (id, name, description, max_teams, tournament_id_FK) VALUES (1, "Division A", "Cool division", 4, 1);
INSERT INTO division (id, name, description, max_teams, tournament_id_FK) VALUES (2, "Division B", "Cool division", 6, 1);

INSERT INTO division (id, name, description, max_teams, tournament_id_FK) VALUES (3, "Division C", "Cool division", 4, 2);
INSERT INTO division (id, name, description, max_teams, tournament_id_FK) VALUES (4, "Division D", "Cool division", 5, 2);

INSERT INTO division (id, name, description, max_teams, tournament_id_FK) VALUES (5, "Division E", "Cool division", 2, 3);
INSERT INTO division (id, name, description, max_teams, tournament_id_FK) VALUES (6, "Division F", "Cool division", 3, 3);

-- Team Data
INSERT INTO team (id, name, player1_id_FK, player2_id_FK, division_id_FK) VALUES (1, "The Boys", 1, 2, 2);
INSERT INTO team (id, name, player1_id_FK, player2_id_FK, division_id_FK) VALUES (2, "Folks", 3, 4, 2);

INSERT INTO team (id, name, player1_id_FK, player2_id_FK, division_id_FK) VALUES (3, "Hmmm", 5, 6, 2);
INSERT INTO team (id, name, player1_id_FK, player2_id_FK, division_id_FK) VALUES (4, "Wonners", 1, 4, 2);

INSERT INTO team (id, name, player1_id_FK, player2_id_FK, division_id_FK) VALUES (5, "Ahhh", 7, 8, 2);
INSERT INTO team (id, name, player1_id_FK, player2_id_FK, division_id_FK) VALUES (6, "Losers", 4, 9, 2);

-- Match Data
INSERT INTO match_data (id, play_to, hard_cap, best_of, team1_id_FK, team2_id_FK, division_id_FK) VALUES (1, 21, 25, 3, 1, 2, 2);
INSERT INTO match_data (id, play_to, hard_cap, best_of, team1_id_FK, team2_id_FK, division_id_FK) VALUES (2, 21, 25, 5, 2, 3, 2);
INSERT INTO match_data (id, play_to, hard_cap, best_of, team1_id_FK, team2_id_FK, division_id_FK) VALUES (3, 21, 25, 5, 3, 4, 2);
INSERT INTO match_data (id, play_to, hard_cap, best_of, team1_id_FK, team2_id_FK, division_id_FK) VALUES (4, 21, 25, 3, 5, 6, 2);
INSERT INTO match_data (id, play_to, hard_cap, best_of, team1_id_FK, team2_id_FK, division_id_FK) VALUES (5, 21, 25, 3, 1, 4, 2);
INSERT INTO match_data (id, play_to, hard_cap, best_of, team1_id_FK, team2_id_FK, division_id_FK) VALUES (6, 21, 25, 3, 2, 5, 2);
INSERT INTO match_data (id, play_to, hard_cap, best_of, team1_id_FK, team2_id_FK, division_id_FK) VALUES (7, 21, 25, 3, 3, 6, 2);
