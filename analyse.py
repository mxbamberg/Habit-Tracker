
from typing import List
from habit import Habit
from datetime import datetime, timedelta


def get_habits(habits: List[Habit]) -> List[Habit]:
    '''
    Return all habits sorted alphabetically

    :param habits: a list of habits
    :return: a list of habits sorted alphabetically
    '''

    return sorted(habits, key=lambda h: h.current_streak, reverse=True)


def get_habits_by_periodicity(habits: List[Habit], periodicity:str) -> List[Habit]:
    '''
    Return all habits with same periodicity

    :param habits:
    :param periodicity:
    :return: list of habits with same periodicity
    '''
    return [h for h in habits if h.periodicity.lower() == periodicity.lower()]


def calc_current_streak(completions: List[datetime], periodicity: str) -> int:

    if not completions:
        return 0 # Fallback: if list is empty, streak = 0

    if periodicity.lower() == "daily":
        if completion_date[0] < today - timedelta(days=1):
            return 0    # streak is over

    elif periodicity.lower() == "weekly":
        pass


def calc_longest_streak_habit(habits:List[Habit]) -> int:
    pass

def calc_longest_streak_all_habits():
    '''
    :return: the habit wih the longest streak
    :param habits: a list of habits
    :return: the habit wih the longest streak all time
    '''

    if not habits:
        return None # Fallback: if list is empty, streak = 0

    longest_streak_alltime = max(habits, key=calc_longest_streak_habit)

    return longest_streak_alltime

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