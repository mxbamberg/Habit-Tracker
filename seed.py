from datetime import datetime, timedelta
from db import get_db, add_habit_to_db, add_completion_to_db
from tracker import Tracker
from habit import Habit


def seed_database():
    print("🌱 Starte das Befüllen der Datenbank mit Beispieldaten...")

    # DB-Verbindung und Tracker initialisieren
    db = get_db()
    tracker = Tracker(db)

    # 1. Beispieldaten definieren (5 vordefinierte Habits laut Modulvorgabe)
    habits_data = [
        # Daily Habits
        {
            "name": "Drink Water",
            "desc": "Drink at least 2 liters of water daily",
            "periodicity": "daily",
            "start_date": datetime.now() - timedelta(days=28),
            "completes_daily": True,  # Jeden Tag erledigt
        },
        {
            "name": "Read Book",
            "desc": "Read 15 pages of a book",
            "periodicity": "daily",
            "start_date": datetime.now() - timedelta(days=28),
            "completes_daily": False,  # Gelegentlich ausgelassen für Lücken/Breaks
        },
        {
            "name": "Exercise",
            "desc": "30 minutes workout",
            "periodicity": "daily",
            "start_date": datetime.now() - timedelta(days=28),
            "completes_daily": False,
        },
        # Weekly Habits
        {
            "name": "Clean Apartment",
            "desc": "Deep clean the entire flat",
            "periodicity": "weekly",
            "start_date": datetime.now() - timedelta(days=28),
            "completes_weekly": True,
        },
        {
            "name": "Weekly Review",
            "desc": "Reflect on goals and budget",
            "periodicity": "weekly",
            "start_date": datetime.now() - timedelta(days=28),
            "completes_weekly": True,
        }
    ]

    # 2. Habits und Completion-Historie in DB schreiben
    today = datetime.now()

    for data in habits_data:
        # Habit-Objekt anlegen
        habit = Habit(
            name=data["name"],
            desc=data["desc"],
            periodicity=data["periodicity"],
            start_date=data["start_date"]
        )

        # In DB speichern (falls noch nicht vorhanden)
        success, msg = tracker.store(habit)
        if success:
            print(f"✅ Habit '{habit.name}' angelegt.")
        else:
            print(f"ℹ️ {msg}")

        # Erledigungen der letzten 4 Wochen (28 Tage) simuliert eintragen
        if habit.periodicity == "daily":
            for i in range(28, 0, -1):
                completion_date = today - timedelta(days=i)

                # Bei 'Drink Water' jeden Tag eintragen
                if data["name"] == "Drink Water":
                    add_completion_to_db(db, habit.name, completion_date)

                # Bei 'Read Book' hin und wieder einen Tag auslassen
                elif data["name"] == "Read Book" and i not in [5, 12, 19]:
                    add_completion_to_db(db, habit.name, completion_date)

                # Bei 'Exercise' mehrmals auslassen (gebrochene Streaks)
                elif data["name"] == "Exercise" and i % 3 != 0:
                    add_completion_to_db(db, habit.name, completion_date)

        elif habit.periodicity == "weekly":
            # 4 wöchentliche Erledigungen (1x pro Woche)
            for week in range(4, 0, -1):
                completion_date = today - timedelta(weeks=week)
                add_completion_to_db(db, habit.name, completion_date)

        # 3. Streaks berechnen und in der DB aktualisieren
        tracker.update_streaks(habit.name, habit.periodicity)

    db.close()
    print("\n🎉 Beispieldaten erfolgreich eingespielt und Streaks berechnet!")


if __name__ == "__main__":
    seed_database()