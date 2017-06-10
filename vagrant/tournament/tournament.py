#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2 as psql


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psql.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from matches")  
    db.commit()

    #remove matches,wins,losses from players table
    sql = ("""update players
    set wins = %s, losses = %s, matches = %s;""")
    c.execute(sql,(0,0,0))
    print(' //// Test Remove Scores from Players /////')
    playerStandings()
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) as num_players from players")
    n_players = c.fetchall()[0][0]
    print('Number of players: ',n_players)
    db.close()
    return n_players


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """   
    db = connect()
    c = db.cursor()
    sql = ("""insert into players (fullname, wins, losses, matches)
        values (%s,%s,%s,%s);""")
        
    c.execute(sql,(name,0,0,0))
    #c.execute("insert into players (fullname,wins,losses,matches) values ('%s','%s','%s')" %(name,0,0))
    db.commit()
    db.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("select id, fullname, wins, matches from players order by wins desc")
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # update matches table
    db = connect()
    c = db.cursor()
    sql = ('insert into matches (winner_id, loser_id)'
        'values (%s,%s);')
    c.execute(sql,(winner,loser))
    db.commit()

    # update wins and match count
    sql = ("""update players
        set wins = wins+%s, matches = matches+%s
        where id = %s;""")
    c.execute(sql, (1,1,winner))
    db.commit()

    # update losses and match count
    sql = ("""update players
        set losses = losses+%s, matches = losses+%s
        where id = %s;""")
    c.execute(sql,(1,1,loser))
    db.commit()

    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    
    standings = playerStandings()
    print('/// QC Swiss Pair ///')
    # standings is sorted by wins descending
    # get every other row starting from zero
    set_a = standings[::2]
    # get every other row starting from 1
    set_b = standings[1::2]
    # get only the first 2 items from the nested lists (id, name)
    plr_a = [set_a[i][0:2] for i in range(len(set_a))]
    plr_b = [set_b[i][0:2] for i in range(len(set_b))]

    # create new list with zip and list comprehension
    pairs = [a+b for a,b in zip(plr_a,plr_b)]
    db.close()
    return pairs

