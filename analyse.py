from typing import List
from habit import Habit
from datetime import datetime, timedelta, date



def calc_streaks(dates: List[date], periodicity: str) -> tuple[int, int]:
    """ Calculate the current streak and longest streak

    :param dates:
    :param periodicity:
    :return: current_streak, longest_streak
    """

    if not dates:
        return 0, 0

    dates = sorted(list(set(dates)))

    current_streak = 0
    longest_streak = 0
    temp_streak = 0

    # 2. Calculate current streak
    if periodicity == "daily":
        for i in range(len(dates)):
            if i == 0:
                temp_streak = 1
            else:
                # Streak is alive
                if dates[i] - dates[i - 1] == timedelta(days=1):
                    temp_streak += 1
                # Checking for duplicates
                elif dates[i] - dates[i - 1] == timedelta(days=0):
                    continue
                else:
                    temp_streak = 1  # Streak is broken and starts at 1 again

            #Check if current streak is new longest_streak
            longest_streak = max(longest_streak, temp_streak)

        # Check if there is an existing streak or if streak is broken
        today = datetime.now().date()
        last_entry = dates[-1]
        if today - last_entry <= timedelta(days=1):
            current_streak = temp_streak
        else:
            current_streak = 0

    elif periodicity == "weekly":
        # Weekly means completed once in a calender week
        for i in range(len(dates)):
            if i == 0:
                temp_streak = 1
            else:
                prev_year, prev_week, _ = dates[i - 1].isocalendar()
                curr_year, curr_week, _ = dates[i].isocalendar()

                # Check if streak is alive or broken
                weeks_diff = (dates[i] - dates[i - 1]).days / 7
                if weeks_diff <= 1.5:
                    if (curr_year == prev_year and curr_week - prev_week == 1) or \
                            (curr_year - prev_year == 1 and curr_week == 1 and prev_week >= 52):
                        temp_streak += 1
                    elif curr_year == prev_year and curr_week == prev_week:
                        continue  # Same week, streak is still alive
                    else:
                        temp_streak = 1
                else:
                    temp_streak = 1

            # Check if current streak is new longest_streak
            longest_streak = max(longest_streak, temp_streak)

        # Check if streak is alive
        today = datetime.now().date()
        curr_year, curr_week, _ = today.isocalendar()
        last_year, last_week, _ = dates[-1].isocalendar()

        if (curr_year == last_year and curr_week - last_week <= 1) or \
                (curr_year - last_year == 1 and curr_week == 1 and last_week >= 52):
            current_streak = temp_streak
        else:
            current_streak = 0

    return current_streak, longest_streak


def get_longest_streak_alltime(habits:List[Habit]) -> int:
    """Gibt den Namen und die Länge des Habits mit der historisch längsten Streak zurück."""
    if not habits:
        return "No habits found", 0
    best_habit = max(habits, key=lambda h: h.longest_streak)
    return best_habit.name, best_habit.longest_streak

def get_longest_active_streak(habits: List[Habit]) -> tuple[str, int]:
    """Gibt den Namen und die Länge des Habits mit der aktuell längsten aktiven Streak zurück."""
    if not habits:
        return "No habits found", 0
    best_habit = max(habits, key=lambda h: h.current_streak)
    return best_habit.name, best_habit.current_streak


def count_broken_streaks(dates: List[date], periodicity: str) -> int:
    """Calculates how many times a habit streak was broken based on completion history."""
    if not dates or len(dates) < 2:
        return 0

    dates = sorted(list(set(dates)))
    breaks = 0

    if periodicity == "daily":
        for i in range(1, len(dates)):
            # Wenn der Abstand größer als 1 Tag ist, gab es einen Bruch
            if (dates[i] - dates[i - 1]).days > 1:
                breaks += 1

    elif periodicity == "weekly":
        for i in range(1, len(dates)):
            # Nutze die ISO-Wochennummern für den Vergleich
            year_prev, week_prev, _ = dates[i - 1].isocalendar()
            year_curr, week_curr, _ = dates[i].isocalendar()

            # Einfache Annäherung: Wenn es nicht dieselbe und nicht die darauffolgende Woche ist
            weeks_diff = (dates[i] - dates[i - 1]).days / 7
            if weeks_diff > 1.5:  # Mehr als eine Woche Lücke
                breaks += 1

    return breaks

'''
def generate_streak_info(habits):
    """
    Parameters
    ----------

    habits:
        A dataframe containing data about habits.
        Must contain a `completions` column with two
        unique values for made and missed shots.
        Must be homogenous (contain only shots
        that qualify for the streak type you want
        to calculate (eg all FT for a single
        player) and be pre-sorted by time.

    Returns
    -------

    shots_with_streaks:
        The original dataframe with a new column
        `streak_counter` containing integers with
        counts for each streak.
    """

    data = habits['result'].to_frame()
    data['start_of_streak'] = data['result'].ne(data['result'].shift())
    data['streak_id'] = data.start_of_streak.cumsum()
    data['streak_counter'] = data.groupby('streak_id').cumcount() + 1
    habits_with_streaks = pd.concat([habits, data['streak_counter']], axis=1)
    return habits_with_streaks


shots = streaks['result'].to_frame()
generate_streak_info(habits)
'''