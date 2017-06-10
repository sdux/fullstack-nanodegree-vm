-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
	id serial,
	fullname varchar,
	wins int,
	losses int,
	matches int,
	primary key (id)
);

CREATE TABLE matches(
	id serial,
	player_a_id int,
	player_b_id int,
	player_a_name varchar,
	player_b_name varchar,
	winner_id int,
	loser_id int,
	player_a_score int,
	player_b_score int,
	primary key (id),
	foreign key (player_a_id) references players(id),
	foreign key (player_b_id) references players(id),
	foreign key (winner_id) references players(id),
	foreign key (loser_id) references players(id)
);