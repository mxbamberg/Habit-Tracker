from datetime import datetime, timedelta
import db
from habit import Habit
from tracker import Tracker


def seed_database():
    print("Initializing the database with 4 weeks of sample tracking data...")

    # Connect to database
    db_conn = db.get_db()
    db.create_tables(db_conn)
    tracker = Tracker(db_conn)

    # 5 predefined habits
    habits_data = [
        # Daily Habits
        {
            "name": "Drink Water",
            "desc": "Drink at least 2 liters of water daily",
            "periodicity": "daily",
            "start_date": datetime.now() - timedelta(days=28),
        },
        {
            "name": "Read Book",
            "desc": "Read 15 pages of a book",
            "periodicity": "daily",
            "start_date": datetime.now() - timedelta(days=28),
        },
        {
            "name": "Exercise",
            "desc": "30 minutes workout",
            "periodicity": "daily",
            "start_date": datetime.now() - timedelta(days=28),
        },
        # Weekly Habits
        {
            "name": "Clean Apartment",
            "desc": "Deep clean the entire flat",
            "periodicity": "weekly",
            "start_date": datetime.now() - timedelta(days=28),
        },
        {
            "name": "Weekly Review",
            "desc": "Reflect on goals and budget",
            "periodicity": "weekly",
            "start_date": datetime.now() - timedelta(days=28),
        },
    ]

    today = datetime.now()

    for data in habits_data:
        habit = Habit(
            name=data["name"],
            desc=data["desc"],
            periodicity=data["periodicity"],
            start_date=data["start_date"],
        )

        # Save in db (if necessary)
        success, msg = tracker.store_new_habit(habit)
        if success:
            print(f"Habit '{habit.name}' stored successfully!")
        else:
            print(f"Info for '{habit.name}': {msg}")

        habit_id = db.get_habit_id_by_name(db_conn, habit.name)
        if not habit_id:
            continue

        if habit.periodicity == "daily":
            for i in range(28, 0, -1):
                completion_date = today - timedelta(days=i)
                date_str = completion_date.strftime("%Y-%m-%d %H:%M:%S")

                if data["name"] == "Drink Water":
                    db.add_completion_to_db(db_conn, habit_id, date_str)

                elif data["name"] == "Read Book" and i not in [5, 12, 19]:
                    db.add_completion_to_db(db_conn, habit_id, date_str)

                elif data["name"] == "Exercise" and i % 3 != 0:
                    db.add_completion_to_db(db_conn, habit_id, date_str)

        elif habit.periodicity == "weekly":
            for week in range(4, 0, -1):
                completion_date = today - timedelta(weeks=week)
                date_str = completion_date.strftime("%Y-%m-%d %H:%M:%S")
                db.add_completion_to_db(db_conn, habit_id, date_str)

        # Calculate streaks
        tracker.update_streaks(habit.name, habit.periodicity)

    db_conn.close()
    print("\nDatabase successfully initialized! You can now run the app or execute tests.\n")


if __name__ == "__main__":
    seed_database()