from db import add_habit_to_db, add_completion_to_db, get_habit_by_name, fetch_all_habits_raw, update_habit, delete_habit_from_db, get_latest_completions, fetch_completion_dates, save_streaks, fetch_habit_names_sorted
from analyse import calc_streaks
from typing import List
from habit import Habit
from datetime import datetime


class Tracker:

    def __init__(self, db_connection):
        self.db = db_connection

    def store_new_habit(self, habit):
        """Passes the habit to the DB
        :param habit: new habit to store
        """

        try:
            # Logic to identify duplicates before storing in db
            existing_names = self.get_habit_names()

            existing_lower = [name.lower() for name in existing_names]
            if habit.name.lower() in existing_lower:
                return False, f"A habit with the name '{habit.name}' already exists."

            add_habit_to_db(self.db, habit)
            return True, f"The habit '{habit.name}' was stored successfully!"

        except Exception as e:
            return False, f"Error storing habit: {str(e)}"


    def get_habit_names(self):

        # 1. Rohe Daten aus der DB-Schicht holen
        rows = fetch_habit_names_sorted(self.db)
        # 2. In eine flache Liste von Strings transformieren
        return [row[0] for row in rows]

    def get_all_habits(self) -> List[Habit]:
        """Holt alle Habits aus der Datenbank und gibt sie als Liste von Habit-Objekten zurück."""
        rows = fetch_all_habits_raw(self.db)

        habits = []
        for row in rows:
            # Hier wandeln wir die gespeicherten Text-Daten zurück in Python-Datetime-Objekte
            start_dt = datetime.strptime(row[3], "%Y-%m-%d") if row[3] else None
            end_dt = datetime.strptime(row[4], "%Y-%m-%d") if row[4] else None

            # Erstelle das Habit-Objekt (passe die Parameter an deine Habit-Klassendefinition an)
            habit = Habit(
                name=row[0],
                desc=row[1],
                periodicity=row[2],
                start_date=start_dt,
                end_date=end_dt
            )
            # Streaks nachträglich setzen, falls deine Klasse diese Attribute hat
            habit.current_streak = row[5]
            habit.longest_streak = row[6]
            habits.append(habit)

        return habits


    def get_habits_by_periodicity(self, periodicity: str) -> List[Habit]:

        selected_habits = self.get_all_habits()
        return [h for h in selected_habits if h.periodicity.lower() == periodicity.lower()]


    def complete_habit(self, habit_name: str) -> tuple[bool, str]:
        """Logs a completion for the given habit name

        :param habit_name:
        """
        try:
            # Abfrage über die ausgelagerte DB-Funktion machen
            selected_habit = get_habit_by_name(self.db, habit_name)

            if not selected_habit:
                return False, f"Habit '{habit_name}' does not exist."

            periodicity = selected_habit[1]

            # Add the completion to the list
            now = datetime.now()
            add_completion_to_db(self.db, habit_name, now)

            # Updating streaks in db
            self.update_streaks(habit_name, periodicity)

            # Success message
            return True, f"Great job! Habit '{habit_name}' marked as completed."

        except Exception as e:
            return False, f"Could not complete habit: {str(e)}"

        # XXXXXXXXX  Create a duplicate check  XXXXXXXXXXX


    def update_streaks(self, habit_name: str, periodicity: str):
        """ Calculates streaks and saves them to database
        """
        # 1. Daten holen über db.py-Funktion
        rows = fetch_completion_dates(self.db, habit_name)

        if not rows:
            return  # Keine Einträge = Streak ist 0

        # Convert strings to datetime
        dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in rows]

        # Use analyse module to calculate streaks
        current_streak, longest_streak = calc_streaks(dates, periodicity)

        # Saves data in db
        save_streaks(self.db, habit_name, current_streak, longest_streak)


    def delete_habit(self, habit_name):
        """Handles logic verification before executing deletions."""
        try:
            delete_habit_from_db(self.db, habit_name)
            return True, f"The habit '{habit_name}' has been deleted!"
        except Exception as e:
            return False, f"Could not delete habit: {str(e)}"



    def edit_habit(self, old_name: str, new_name: str = None, new_desc: str = None, new_periodicity: str = None):
        """Update a habit, that was created before"""

        """Reicht die Änderungen an die DB weiter und aktualisiert das Objekt."""

        update_habit(self.db, old_name, new_name, new_desc, new_periodicity)


    def get_completion_history(self, habit_name: str) -> list[datetime]:
        """Holt die Historie über db.py und bereitet sie für die App vor."""
        # 1. Rufe die nackte SQL-Funktion ab
        raw_dates = get_latest_completions(self.db, habit_name, limit=10)

        # 2. Mache daraus schicke Python datetime-Objekte (falls nötig, sonst als Text lassen)
        return [datetime.strptime(d, "%Y-%m-%d") for d in raw_dates]


"""
Ab hier ist der Code noch nicht 100% sicher und abgenickt !!!!!
"""

"""
    def reset(self):   # Du möchtest deinen Fortschritt zurücksetzen und neu anfangen (start date = today, completion_list = reset
        pass


    
    def edit_habit(self):
        # welches habit?
        # was willst du ändern? (name, periodicity, description, end date
        pass
    
    #self.current_streak
    #self.longest_streak



    # 3. Methode: Platzhalter für das spätere Editieren
    def edit_habit(self, old_name, new_name, new_desc, new_periodicity):
        #Placeholder for editing a habit later.
        pass


    def logout(self):
        # Motivierender satz
        # Verabschiedung
        pass
    '''
    if current_streak > longest_streak:
        print("Congratulation! Your longest streak has been reached!")
    '''
    # check if date is correct

"""


''' Braucht man diese Funktion überhaupt ????

    def get_stored_habit_names(self):
        """Requests all existing habit names from storage and sorts them alphabetically."""
        # Wir nutzen self.db anstatt db
        raw_names = get_all_habit_names(self.db)
        return sorted(raw_names)
'''