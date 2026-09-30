from db import *
from analyse import calc_streaks
from typing import List
from habit import Habit
from datetime import datetime, date
from resources import *


class Tracker:

    def __init__(self, db_connection):
        self.db = db_connection

    def store_new_habit(self, habit):
        """ Stores a new habit in the database
        :param habit:
        :return: tuple[bool, str]: A tuple containing a boolean flag (True if successful, False otherwise) and a descriptive feedback message
        """

        try:
            # Fetch all existing habit names to check for potential duplicates
            existing_names = self.get_habit_names()

            # Convert existing names to lowercase for case-insensitive comparison
            existing_lower = [name.lower() for name in existing_names]
            if habit.name.lower() in existing_lower:
                return False, f"A habit with the name '{habit.name}' already exists."

            # Insert habit into database
            add_habit_to_db(self.db, habit)
            return True, f"The habit '{habit.name}' was stored successfully!"

        except Exception as e:
            return False, f"Error storing habit: {str(e)}"


    def get_habit_names(self):
        """ Retrieves all habit names from the database and returns them as a sorted list

        :return: A list of habit names sorted alphabetically
        """

        rows = fetch_habit_names_sorted(self.db)
        return [row[0] for row in rows]

    def get_all_habits(self) -> List[Habit]:
        """ Retrieves all habits from the database and returns them as a list of Habit objects

        :return: A list of instantiated Habit objects fetched from the database
        """
        rows = fetch_all_habits_raw(self.db)

        habits = []
        for row in rows:
            # Convert stored date strings into Python datetime objects if available
            start_dt = datetime.strptime(row[3], "%Y-%m-%d") if row[3] else None
            end_dt = datetime.strptime(row[4], "%Y-%m-%d") if row[4] else None

            habit = Habit(
                name=row[0],
                desc=row[1],
                periodicity=row[2],
                start_date=start_dt,
                end_date=end_dt
            )
            # Assign streak attributes to the instance
            habit.current_streak = row[5]
            habit.longest_streak = row[6]
            habits.append(habit)

        return habits

    def get_predefined_habits(self):
        """Retrieves the list of all predefined habit templates

        :return: A list of predefined habits
        """
        return PREDEFINED_HABITS


    def get_habits_by_periodicity(self, periodicity: str) -> List[Habit]:
        """Filters all habits by periodicity

        :param periodicity: The target periodicity (e.g., 'daily' or 'weekly')
        :return: A list of Habit objects matching the given periodicity
        """

        selected_habits = self.get_all_habits()
        return [h for h in selected_habits if h.periodicity.lower() == periodicity.lower()]


    def complete_habit(self, habit_name: str) -> tuple[bool, str]:
        """ Logs a completion for the given habit name and updates streaks

        :param habit_name: The name of the habit to mark as completed
        """
        try:
            # Retrieve habit details from db
            selected_habit = get_habit_by_name(self.db, habit_name)

            if not selected_habit:
                return False, f"Habit '{habit_name}' does not exist."

            habit_id = get_habit_id_by_name(self.db, habit_name)
            periodicity = selected_habit[1]

            # Add the completion to the list
            now = date.today().isoformat()
            add_completion_to_db(self.db, habit_id, now)

            # Updating streaks in db
            self.update_streaks(habit_name, periodicity)

            # Success message
            return True, f"Great job! Habit '{habit_name}' marked as completed."

        except Exception as e:
            return False, f"Could not complete habit: {str(e)}"

        # XXXXXXXXX  Create a duplicate check  XXXXXXXXXXX


    def update_streaks(self, habit_name: str, periodicity: str):
        """ Calculates completion streaks for a habit

        :param habit_name: The name of the habit to calculate streaks for
        :param periodicity: The periodicity of the habit ('daily' or 'weekly')
        """
        habit_id = get_habit_id_by_name(self.db, habit_name)

        if not habit_id:
            return

        # Fetch completion dates from db
        rows = fetch_completion_dates(self.db, habit_id)

        if not rows:
            # Reset streaks to 0 if no completions exist
            save_streaks(self.db, habit_id, 0, 0)
            return

        # Convert strings to datetime
        dates = [datetime.strptime(row[0].split()[0], "%Y-%m-%d").date() for row in rows]

        # Use analyse module to calculate streaks
        current_streak, longest_streak = calc_streaks(dates, periodicity)

        # Saves data in db
        save_streaks(self.db, habit_id, current_streak, longest_streak)


    def delete_habit(self, habit_name: str) -> tuple[bool, str]:
        #delete_habit(self, habit_name):
        """ Deletes a habit and its associated data from the database

        :param habit_name: The name of the habit to be deleted
        """

        try:
            ###
            habit_id = get_habit_id_by_name(self.db, habit_name)
            if not habit_id:
                return False, f"Habit '{habit_name}' does not exist."
            ###

            delete_habit_from_db(self.db, habit_id)
            return True, f"The habit '{habit_name}' has been deleted!"
        except Exception as e:
            return False, f"Could not delete habit: {str(e)}"



    def edit_habit(self, old_name: str, new_name: str = None, new_desc: str = None, new_periodicity: str = None):
        """ Updates an existing habit's details in the database

        :param old_name: The current name of the habit
        :param new_name: Optional new name
        :param new_desc: Optional new description
        :param new_periodicity: Optional new periodicity ('daily' or 'weekly')
        """

        update_habit(self.db, old_name, new_name, new_desc, new_periodicity)


    def get_completion_history(self, habit_name: str) -> list[datetime]:
        """ Fetches the last 10 completion timestamps for a specific habit

        :param habit_name: The name of the habit
        :return: A list of datetime objects representing the latest completion dates
        """

        habit_id = get_habit_id_by_name(self.db, habit_name)
        if not habit_id:
            return []

        # Fetch raw completion data from db
        raw_dates = get_latest_completions(self.db, habit_id, limit=10)

        # Unpack raw data and parse them into datetime objects
        history = []
        for row in raw_dates:
            date_str = row[0] if isinstance(row, (tuple, list)) else row
            clean_str = str(date_str).split()[0]
            history.append(datetime.strptime(clean_str, "%Y-%m-%d"))

        return history