from datetime import datetime
from typing import List


class Habit:

    def __init__(self,
                 name: str,
                 periodicity: str,
                 start_date: datetime,
                 desc: str = "",
                 end_date: Optional[datetime] = None,
                 completion_list: List[datetime] = None,
                 current_streak: int = 0,
                 longest_streak: int = 0):
        '''
        :param name: Name of the habit
        :param periodicity: Daily or weekly
        :param start_date: Start of the habit
        :param desc: Description of the habit
        :param end_date: Optional end of the habit
        :param completion_list: All completions of the habit
        :param current_streak: Current streak of the habit
        :param longest_streak: Longest streak of the habit
        '''

        self.name = name
        self.desc = desc
        self.start_date = start_date
        self.end_date = end_date  #optional, default = None
        self.periodicity = periodicity   # daily or weekly
        self.completion_list = completion_list if completion_list is not None else [] # empty list, if no completions made
        self.total_completions = len(self.completion_list)
        self.current_streak = current_streak
        self.longest_streak = longest_streak
