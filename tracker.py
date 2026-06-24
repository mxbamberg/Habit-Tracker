from analyse import calc_current_streak


class Tracker:

    def __init__(self, db_connection):
        self.db = db_connection


    def create_habit(self):
        # gibt es dieses habit schon?
        # has been created successfully
        pass
    # self.select_predefined

    def delete(self):
        # Are you sure o delete?
        pass

    def reset(self):   # Du möchtest deinen Fortschritt zurücksetzen und neu anfangen (start date = today, completion_list = reset
        pass

    def complete_habit(self, habit_name:str):
        # 1. Gewohnheit als "heute erledigt" in die Datenbank eintragen
        # Was habit already completed today (this week) ?
        # für daily: datum heute = datum letzte completion
        # für weekly: datum heute = innerhalb dieser kalenderwoche oder letzte 6 tage
        # 2. Alle bisherigen Erledigungen (Completions) aus der DB holen
        completions = get_completions_for_habit(habit_name)

        # 3. Den Taschenrechner (analyse.py) bemühen
        current_streak = calc_current_streak(completions, "daily")
        longest_streak = calc_longest_streak_habit(completions, "times")

        # 4. Prüfen, ob die aktuelle Streak ein neuer Rekord ist!
        if current_streak > longest_streak:
            print(f"New record for {habit_name}: {current} times in a row!")
        pass

            '''
            # Kopiert von anderem: Avoid duplicate completions for the same day or calendar week
            if self._completions:
                last_completion = self._completions[-1]
                if self._periodicity == 'daily' and last_completion.date() == completion_date.date():
                    print("Habit already completed today.")
                    return
                elif self._periodicity == 'weekly' and last_completion.isocalendar()[1] == completion_date.isocalendar()[1]:
                    print("Habit already completed this week.")
                    return
            '''
        # Ist das end date bereits gewesen? -> habit nicht rechtzeitig gemacht. Bzw herzlichen glückwunsch. Du hast es geschafft.
        # Was the habit missed?

    def edit_habit(self):
        # welches habit?
        # was willst du ändern? (name, periodicity, description, end date
        pass

    #self.current_streak
    #self.longest_streak

    def store(habit: Habit):
        if not habit.name.strip():
            return False, "The habit name cannot be empty!"

        try:
            # Wir lesen die Daten aus dem Objekt aus und geben sie an die DB
            add_habit_to_db(self.db, habit.name, habit.periodicity, habit.desc)
            return True, f"The habit '{habit.name}' was stored successfully!"
        except Exception as e:
            return False, f"Error storing habit: {str(e)}"

    def logout(self):
        # Motivierender satz
        # Verabschiedung
        pass

    if current_streak > longest_streak:
        print("Congratulation! Your longest streak has been reached!")
        
    # check if date is correct