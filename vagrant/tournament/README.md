##Tournament project for Udacity's Relational databases course.

The objective is to simulate a swiss style tournament storing the players
and match history in an sql database.

###Environment:

Python 3
psycopg2

###Databases:

Database and tables are created by running the tournament.sql file in postgreSQL

###Database:
CREATE DATABASE tournament;
\c tournament;

###Tables are defined as:

players
CREATE TABLE players (
	id serial,
	fullname varchar,
	primary key (id)
);

matches
CREATE TABLE matches(
	id serial,
	winner_id int,
	loser_id int,
	primary key (id),
	foreign key (winner_id) references players(id),
	foreign key (loser_id) references players(id)
);

###Description of functions in tournament.py:

registerPlayer(name)
Adds a player to the tournament by putting an entry in the database. The database assigns an ID number to the player. Different players may have the same names but will receive different ID numbers.

countPlayers()
Returns the number of currently registered players.

deletePlayers()
Clear out all the player records from the database.

reportMatch(winner, loser)
Stores the outcome of a single match between two players in the database.

deleteMatches()
Clear out all the match records from the database.

playerStandings()
Returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has.

swissPairings()
Given the existing set of registered players and the matches they have played, generates and returns a list of pairings according to the Swiss system. Each pairing is a tuple (id1, name1, id2, name2), giving the ID and name of the paired players. For instance, if there are eight registered players, this function should return four pairings. This function should use playerStandings to find the ranking of players.