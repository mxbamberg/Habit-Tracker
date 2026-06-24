# habit.py

class Habit:

    def __init__(self, name: str, desc: str, start_date: datetime, end_date: datetime,
        periodicity: str, completion_list, current_streak: int, longest_streak: int):

        self.name = name
        self.desc = desc
        self.start_date = start_date
        self.end_date = end_date  #optional, default = None
        self.periodicity = periodicity   # daily or weekly
        self.completion_list = completion_list
        self.total_completions = len(self.completion_list)
        self.current_streak = current_streak
        self.longest_streak = longest_streak
