import sqlite3
from datetime import date

def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
        name TEXT PRIMARY KEY,
        description TEXT,
        periodicity TEXT,
        start_date DATETIME,
        end_date DATETIME,
        current_streak INTEGER,
        longest_streak INTEGER)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS completion_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_name TEXT,
        completion_date DATETIME,
        FOREIGN KEY(habit_name) REFERENCES habit(name))""")

    db.commit()


def add_habit_to_db(name: str, periodicity: str, description: str, db_name="main.db"):
    """Fügt ein neues Habit dauerhaft in die SQLite-Datenbank ein."""
    cur = db.cursor()

    # SQL-Befehl zum Einfügen der Daten
    cur.execute("""
                   INSERT INTO habit (name, description, periodicity, start_date, end_date, current_streak, longest_streak)
                   VALUES (?, ?, ?, ?, ?, 0, 0)
                   """, (name, description, periodicity, start_date, end_date))

    db.commit()





def add_counter(db, name, description):
    cur = db.cursor()
    cur.execute("INSERT INTO counter VALUES (?, ?)", (name, description))
    db.commit()

def increment_counter(db, name, event_date=None):
    cur = db.cursor()
    if not event_date: #if the user does not provide an event date
        event_date = str(date.today())
    cur.execute("INSERT INTO tracker VALUES (?, ?)", (event_date, name))
    db.commit()

def get_habit_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM tracker WHERE counterName = ?", (name,))
    return cur.fetchall()

