import sqlite3
from datetime import datetime

def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
        name TEXT PRIMARY KEY,
        desc TEXT,
        periodicity TEXT,
        start_date TEXT,
        end_date TEXT,
        current_streak INTEGER,
        longest_streak INTEGER)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS completion_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_name TEXT,
        completion_date DATETIME,
        FOREIGN KEY(habit_name) REFERENCES habit(name))""")

    db.commit()


def add_habit_to_db(db, habit):
    """Stores the habit in the database"""
    cur = db.cursor()

    # formating for sqlite3
    start_str = habit.start_date.strftime("%Y-%m-%d")
    end_str = habit.end_date.strftime("%Y-%m-%d") if habit.end_date else None

    # Insert data into main.db
    cur.execute("""
                   INSERT INTO habit (name, desc, periodicity, start_date, end_date, current_streak, longest_streak)
                   VALUES (?, ?, ?, ?, ?, 0, 0)
                   """, (
                        habit.name,
                        habit.desc,
                        habit.periodicity,
                        start_str,
                        end_str
                   ))

    db.commit()

def add_completion_to_db(db, habit_name:str, completion_time:datetime):

    cur = db.cursor()
    time_str = completion_time.strftime("%Y-%m-%d")

    cur.execute("""
        INSERT INTO completion_list (habit_name, completion_date)
        VALUES (?, ?)
    """, (habit_name, time_str))

    db.commit()



def get_habit_by_name(db: sqlite3.Connection, habit_name: str) -> tuple | None:
    """Retrieves a habit's name and periodicity from the database."""
    cur = db.cursor()
    cur.execute("SELECT name, periodicity FROM habit WHERE name = ?", (habit_name,))
    return cur.fetchone()

def fetch_all_habits_raw(db: sqlite3.Connection) -> list[tuple]:
    """Retrieves all rows and columns from the habit table."""
    cur = db.cursor()
    cur.execute("SELECT name, desc, periodicity, start_date, end_date, current_streak, longest_streak FROM habit")
    return cur.fetchall()


def update_habit(db, old_name: str, new_name: str = None, new_desc: str = None, new_periodicity: str = None):
    """Aktualisiert spezifische Felder eines bestehenden Habits in der Datenbank."""

    updates = []
    parameters = []

    # Wir prüfen, ob neue Werte übergeben wurden und fügen sie dem SQL-Befehl hinzu
    if new_name is not None:
        updates.append("name = ?")
        parameters.append(new_name)

    if new_desc is not None:
        updates.append("desc = ?")
        parameters.append(new_desc)

    if new_periodicity is not None:
        updates.append("periodicity = ?")
        parameters.append(new_periodicity)

    # Wenn der User überall "Nein" geklickt hat, gibt es nichts zu tun
    if not updates:
        return

        # SQL-Befehl dynamisch zusammenbauen (z.B. "UPDATE habits SET name = ?, periodicity = ? WHERE name = ?")
    query = f"UPDATE habits SET {', '.join(updates)} WHERE name = ?"
    parameters.append(old_name)

    cur = db.cur()
    cur.execute(query, parameters)
    db.commit()


def delete_habit_from_db(db, habit_name):
    """Deletes a habit from the database"""
    cur = db.cursor()
    cur.execute("DELETE FROM completion_list WHERE habit_name = ?", (habit_name,))
    cur.execute("DELETE FROM habit WHERE name = ?", (habit_name,))
    db.commit()


def get_latest_completions(db: sqlite3.Connection, habit_name: str, limit: int = 10) -> list[str]:
    """Holt die rohen Datums-Strings der letzten N Erledigungen aus der Datenbank."""
    cur = db.cursor()
    cur.execute("""
                SELECT completion_date
                FROM completion_list
                WHERE habit_name = ?
                ORDER BY completion_date DESC LIMIT ?
                """, (habit_name, limit))

    # Packt die Ergebnisse in eine flache Liste von Strings: ['2026-07-15 14:22:10', ...]
    return [row[0] for row in cur.fetchall()]

def fetch_completion_dates(db: sqlite3.Connection, habit_name: str) -> list[tuple]:
    """Retrieves all completion dates for a specific habit ordered from oldest to newest."""
    cur = db.cursor()
    cur.execute("""
        SELECT completion_date
        FROM completion_list
        WHERE habit_name = ?
        ORDER BY completion_date ASC
    """, (habit_name,))
    return cur.fetchall()

def save_streaks(db: sqlite3.Connection, habit_name: str, current_streak: int, longest_streak: int):
    """Updates the current and longest streaks for a specific habit."""
    cur = db.cursor()
    cur.execute("""
        UPDATE habit
        SET current_streak = ?,
            longest_streak = ?
        WHERE name = ?
    """, (current_streak, longest_streak, habit_name))
    db.commit()

def fetch_habit_names_sorted(db: sqlite3.Connection) -> list[tuple]:
    """Retrieves all habit names from the database, ordered alphabetically."""
    cur = db.cursor()
    cur.execute("SELECT name FROM habit ORDER BY name ASC")
    return cur.fetchall()