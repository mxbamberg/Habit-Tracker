import sqlite3
from datetime import datetime

def get_db(name="main.db"):
    db = sqlite3.connect(name)
    db.execute("PRAGMA foreign_keys = ON;") # activate ON DELETE CASCADE
    create_tables(db)
    return db


def create_tables(db: sqlite3.Connection):
    """Creates the 'habit' and 'completion_list' tables in the database if they do not exist"""

    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        desc TEXT,
        periodicity TEXT,
        start_date TEXT,
        end_date TEXT,
        current_streak INTEGER,
        longest_streak INTEGER)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS completion_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        completion_date DATETIME,
        FOREIGN KEY(habit_id) REFERENCES habit(id) ON DELETE CASCADE)""")

    db.commit()


def add_habit_to_db(db: sqlite3.Connection, habit):
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

def add_completion_to_db(db: sqlite3.Connection, habit_id: int, completion_time):

    cur = db.cursor()
    time_str = completion_time.isoformat() if hasattr(completion_time, "isoformat") else str(completion_time)

    cur.execute("""
        INSERT INTO completion_list (habit_id, completion_date)
        VALUES (?, ?)
    """, (habit_id, time_str))
    db.commit()

def get_habit_id_by_name(db: sqlite3.Connection, habit_name: str) -> int | None:
  """Fetch the database ID for a specific habit name"""
  cur = db.cursor()
  cur.execute("SELECT id FROM habit WHERE name = ?", (habit_name,))
  row = cur.fetchone()
  return row[0] if row else None


def get_habit_by_name(db: sqlite3.Connection, habit_name: str) -> tuple | None:
    """Retrieves a habit's name and periodicity from the database"""
    cur = db.cursor()
    cur.execute("SELECT name, periodicity FROM habit WHERE name = ?", (habit_name,))
    return cur.fetchone()

def fetch_all_habits_raw(db: sqlite3.Connection) -> list[tuple]:
    """Retrieves all rows and columns from the habit table"""
    cur = db.cursor()
    cur.execute("SELECT name, desc, periodicity, start_date, end_date, current_streak, longest_streak FROM habit")
    return cur.fetchall()


def update_habit(db: sqlite3.Connection, habit_id: str, new_name: str = None, new_desc: str = None, new_periodicity: str = None):
    """Updates specific entries of an existing habit in the database"""

    updates = []
    parameters = []

    # check if new values have been passed and add them to the SQL statement
    if new_name is not None:
        updates.append("name = ?")
        parameters.append(new_name)

    if new_desc is not None:
        updates.append("desc = ?")
        parameters.append(new_desc)

    if new_periodicity is not None:
        updates.append("periodicity = ?")
        parameters.append(new_periodicity)

    if not updates:
        return

    query = f"UPDATE habit SET {', '.join(updates)} WHERE name = ?"
    parameters.append(habit_id)

    cur = db.cursor()
    cur.execute(query, parameters)
    db.commit()


def delete_habit_from_db(db: sqlite3.Connection, habit_id: int):
    """Deletes a habit from the database"""
    cur = db.cursor()
    cur.execute("DELETE FROM completion_list WHERE habit_id = ?", (habit_id,))
    cur.execute("DELETE FROM habit WHERE id = ?", (habit_id,))
    db.commit()


def get_latest_completions(db: sqlite3.Connection, habit_id: int, limit: int = 10):
    """Retrieve the raw date strings for the last n-completed tasks from the database"""
    cur = db.cursor()
    cur.execute("""
                SELECT completion_date
                FROM completion_list
                WHERE habit_id = ?
                ORDER BY completion_date DESC LIMIT ?
                """, (habit_id, limit))

    return cur.fetchall()

def fetch_completion_dates(db: sqlite3.Connection, habit_id: int) -> list[tuple]:
    """Retrieves all completion dates for a specific habit ordered from oldest to newest"""
    cur = db.cursor()
    cur.execute("""
        SELECT completion_date
        FROM completion_list
        WHERE habit_id = ?
        ORDER BY completion_date ASC
    """, (habit_id,))
    return cur.fetchall()

def save_streaks(db: sqlite3.Connection, habit_id: int, current_streak: int, longest_streak: int):
    """Updates the current and longest streaks for a specific habit"""
    cur = db.cursor()
    cur.execute("""
        UPDATE habit
        SET current_streak = ?,
            longest_streak = ?
        WHERE id = ?
    """, (current_streak, longest_streak, habit_id))
    db.commit()

def fetch_habit_names_sorted(db: sqlite3.Connection) -> list[tuple]:
    """Retrieves all habit names from the database, ordered alphabetically"""
    cur = db.cursor()
    cur.execute("SELECT name FROM habit ORDER BY name ASC")
    return cur.fetchall()