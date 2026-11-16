import sqlite3
 
 
def getSqliteConnection():
    """Return a connection to the studentDB.db SQLite database."""
    return sqlite3.connect('studentDB.db')
