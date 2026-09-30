# resources.py

PREDEFINED_HABITS = [
    {"name": "Drink Water", "periodicity": "daily", "desc": "Drink at least 2 liters of water every day"},
    {"name": "Morning Run", "periodicity": "daily", "desc": "Run for 20 minutes in the morning"},
    {"name": "Read 10 Pages", "periodicity": "daily", "desc": "Read 10 pages of a book"},
    {"name": "Workout Session", "periodicity": "weekly", "desc": "Go to the gym or do home workout"},
    {"name": "Clean Room", "periodicity": "weekly", "desc": "Tidy up your room/apartment"}
]

PREDEFINED_4_WEEK_DATA = {
    # Daily Habit 1: Continuous 28-day streak
    "Drink Water": {
        "periodicity": "daily",
        "expected_current_streak": 28,
        "expected_longest_streak": 28,
        "completions": [
            "2026-08-01 08:30:00", "2026-08-02 09:15:00", "2026-08-03 08:00:00",
            "2026-08-04 10:00:00", "2026-08-05 08:45:00", "2026-08-06 09:00:00",
            "2026-08-07 08:15:00", "2026-08-08 11:00:00", "2026-08-09 10:30:00",
            "2026-08-10 08:20:00", "2026-08-11 09:10:00", "2026-08-12 08:05:00",
            "2026-08-13 08:50:00", "2026-08-14 09:30:00", "2026-08-15 10:15:00",
            "2026-08-16 11:20:00", "2026-08-17 08:10:00", "2026-08-18 08:40:00",
            "2026-08-19 09:05:00", "2026-08-20 08:25:00", "2026-08-21 09:15:00",
            "2026-08-22 10:00:00", "2026-08-23 10:45:00", "2026-08-24 08:30:00",
            "2026-08-25 08:55:00", "2026-08-26 09:05:00", "2026-08-27 08:15:00",
            "2026-08-28 09:10:00"
        ]
    },

    # Daily Habit 2: Broken streak midway (12 days active, 2 missed, 14 days active)
    "Morning Run": {
        "periodicity": "daily",
        "expected_current_streak": 14,
        "expected_longest_streak": 14,
        "completions": [
            "2026-08-01 07:00:00", "2026-08-02 07:15:00", "2026-08-03 07:05:00",
            "2026-08-04 07:20:00", "2026-08-05 06:55:00", "2026-08-06 07:10:00",
            "2026-08-07 07:30:00", "2026-08-08 08:00:00", "2026-08-09 08:15:00",
            "2026-08-10 07:00:00", "2026-08-11 07:10:00", "2026-08-12 07:05:00",
            # Missed Aug 13 & 14
            "2026-08-15 07:45:00", "2026-08-16 08:10:00", "2026-08-17 07:00:00",
            "2026-08-18 07:15:00", "2026-08-19 07:05:00", "2026-08-20 07:20:00",
            "2026-08-21 07:00:00", "2026-08-22 08:00:00", "2026-08-23 08:30:00",
            "2026-08-24 07:10:00", "2026-08-25 07:05:00", "2026-08-26 07:15:00",
            "2026-08-27 07:00:00", "2026-08-28 07:25:00"
        ]
    },

    # Daily Habit 3: Sparse completion history
    "Read 10 Pages": {
        "periodicity": "daily",
        "expected_current_streak": 2,
        "expected_longest_streak": 3,
        "completions": [
            "2026-08-01 21:00:00", "2026-08-02 21:30:00", "2026-08-03 22:00:00",
            "2026-08-06 20:45:00", "2026-08-07 21:15:00",
            "2026-08-12 22:10:00",
            "2026-08-18 21:00:00", "2026-08-19 21:20:00",
            "2026-08-24 20:30:00",
            "2026-08-27 21:00:00", "2026-08-28 21:40:00"
        ]
    },

    # Weekly Habit 1: Perfect 4-week streak
    "Workout Session": {
        "periodicity": "weekly",
        "expected_current_streak": 4,
        "expected_longest_streak": 4,
        "completions": [
            "2026-08-03 18:00:00", # W1
            "2026-08-12 18:30:00", # W2
            "2026-08-20 17:45:00", # W3
            "2026-08-27 19:00:00"  # W4
        ]
    },

    # Weekly Habit 2: Broken weekly streak
    "Clean Room": {
        "periodicity": "weekly",
        "expected_current_streak": 1,
        "expected_longest_streak": 2,
        "completions": [
            "2026-08-02 14:00:00", # W1
            "2026-08-09 15:30:00", # W2
            # Missed Week 3
            "2026-08-25 11:00:00"  # W4 -> Reset auf 1
        ]
    }
}

HELP_CONTENT = {
    "1. What are habits?": (
        "A habit is a routine or behavior that is performed regularly.\n"
        "In this tracker, you can create two types of habits:\n"
        "  - Daily habits (to be done every single day, e.g., 'Drink water')\n"
        "  - Weekly habits (to be done once per calendar week, e.g., 'Clean the house')"
    ),
    "2. What is a streak?": (
        "A streak represents how many times in a row you have completed your habit\n"
        "without breaking the periodicity.\n"
        "  - For Daily habits: You must complete it today or yesterday to keep the streak alive.\n"
        "  - For Weekly habits: You must complete it this week or last week.\n"
        "If you miss a period, your current streak resets to 0, but your 'longest streak' record remains!"
    ),
    "3. How do I complete a habit?": (
        "1. Select 'Complete a habit' from the Main Menu.\n"
        "2. Choose the habit you just completed from the list.\n"
        "3. The tracker will log the time and automatically calculate your new streaks!"
    ),
    "4. General functionality & Tips": (
        "  - Manage Habits: You can delete habits or edit their descriptions here.\n"
        "  - Show Habits: Check your active streaks or filter your habits by daily/weekly.\n"
        "  - Avoid Cheating: Try to log your completions honestly to keep your records genuine!"
    )
}
