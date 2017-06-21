#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2 as psql

database_name = "tournament"


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    db = psql.connect("dbname={}".format(database_name))
    cur = db.cursor()
    return db, cur


def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()
    c.execute("TRUNCATE matches;")
    db.commit()

    print(' //// Test Remove Scores from Players /////')
    playerStandings()
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()
    '''
    clear the players table with TRUNCATE, faster
    than delete and frees memory immediately
    append CASCADE to handle linked tables
    '''
    c.execute("TRUNCATE players CASCADE;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()
    c.execute("select count(*) as num_players from players")
    n_players = c.fetchone()[0]
    print('Number of players: ', n_players)
    db.close()
    return n_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db, c = connect()
    sql = ("""insert into players (fullname)
        values (%s);""")
    c.execute(sql, ([name]))

    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in
    first place, or a player tied for first place if there
    is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, c = connect()
    sql = ("""
    SELECT
        a.id,
        a.fullname,
        count(b.winner_id) as wins,
        count(b.winner_id) + count(c.loser_id) as total_matches
    FROM
        players a
            left join matches b
                on a.id = b.winner_id
            left join matches c
                on a.id = c.loser_id
    group by
        a.id
    order by
        wins

    ;""")
    c.execute(sql)

    standings = c.fetchall()
    c.execute(sql)
    # sql_print(c)
    print('/// QC Standings ///')
    for row in standings:
        print row
    # print(standings)
    db.close()
    return standings


def sql_print(cursor):
    results = cursor.fetchall()

    widths = []
    columns = []
    tavnit = '|'
    separator = '+'

    for cd in cursor.description:
        widths.append(max(cd[2], len(cd[0])))
        columns.append(cd[0])

    for w in widths:
        tavnit += " %-"+"%ss |" % (w,)
        separator += '-'*w + '--+'

    print(separator)
    print(tavnit % tuple(columns))
    print(separator)
    for row in results:
        print(tavnit % row)
    print(separator)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # update matches table
    db, c = connect()
    sql = ("""insert into matches (winner_id, loser_id)
        values (%s, %s);""")
    c.execute(sql, (winner, loser))
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
    pairs = [a+b for a, b in zip(plr_a, plr_b)]

    return pairs
