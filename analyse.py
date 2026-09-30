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

    # check if entries are datetime objects
    clean_dates = []
    for d in dates:
        if isinstance(d, str):
            # strip time
            clean_date_str = d.split()[0]
            clean_dates.append(datetime.strptime(clean_date_str, "%Y-%m-%d").date())
        elif isinstance(d, datetime):
            clean_dates.append(d.date())
        elif isinstance(d, date):
            clean_dates.append(d)

    if not clean_dates:
        return 0, 0

    # sort & delete duplicates
    dates = sorted(list(set(clean_dates)))

    current_streak = 0
    longest_streak = 0
    temp_streak = 0

    # Calculate current streak
    if periodicity.lower() == "daily":
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

    elif periodicity.lower() == "weekly":
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
    """Retrieves the habit name and streak length for the all-time longest streak

    :param habits: A list of Habit objects
    :return: Name of the top habit and its longest streak value
    """

    if not habits:
        return "No habits found", 0

    # Determine the habit with the maximum all-time streak using a key function
    best_habit = max(habits, key=lambda h: h.longest_streak)
    return best_habit.name, best_habit.longest_streak

def get_longest_active_streak(habits: List[Habit]) -> tuple[str, int]:
    """Retrieves the habit name and streak length for the currently highest active streak

    :param habits: A list of Habit objects
    :return: Name of the top habit and its current active streak value
    """

    if not habits:
        return "No habits found", 0

    # Determine the habit with the maximum active current streak
    best_habit = max(habits, key=lambda h: h.current_streak)
    return best_habit.name, best_habit.current_streak


def count_broken_streaks(dates: List[date], periodicity: str) -> int:
    """Calculates how many times a habit streak was broken

    :param dates: A list of date objects representing completion timestamp
    :param periodicity: 'daily' or 'weekly'
    :return: The total number of broken streaks as an integer
    """

    if not dates or len(dates) < 2:
        return 0

    # Ensure dates are unique and sorted chronologically
    dates = sorted(list(set(dates)))
    breaks = 0

    if periodicity.lower() == "daily":
        for i in range(1, len(dates)):
            # If gap between consecutive dates exceeds 1 day, a streak was broken
            if (dates[i] - dates[i - 1]).days > 1:
                breaks += 1

    elif periodicity.lower() == "weekly":
        for i in range(1, len(dates)):
            year_prev, week_prev, _ = dates[i - 1].isocalendar()
            year_curr, week_curr, _ = dates[i].isocalendar()

            weeks_diff = (dates[i] - dates[i - 1]).days / 7
            if weeks_diff > 1.5:
                breaks += 1

    return breaks