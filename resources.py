# resources.py

HELP_CONTENT = {
    "What are habits?": (
        "A habit is a routine or behavior that is performed regularly.\n"
        "In this tracker, you can create two types of habits:\n"
        "  - Daily habits (to be done every single day, e.g., 'Drink water')\n"
        "  - Weekly habits (to be done once per calendar week, e.g., 'Clean the house')"
    ),
    "What is a streak?": (
        "A streak (🔥) represents how many times in a row you have completed your habit\n"
        "without breaking the periodicity.\n"
        "  - For Daily habits: You must complete it today or yesterday to keep the streak alive.\n"
        "  - For Weekly habits: You must complete it this week or last week.\n"
        "If you miss a period, your current streak resets to 0, but your 'longest streak' record remains!"
    ),
    "How do I complete a habit?": (
        "1. Select 'Complete a habit' from the Main Menu.\n"
        "2. Choose the habit you just completed from the list.\n"
        "3. The tracker will log the time and automatically calculate your new streaks!"
    ),
    "General functionality & Tips": (
        "  - Manage Habits: You can delete habits or edit their descriptions here.\n"
        "  - Show Habits: Check your active streaks or filter your habits by daily/weekly.\n"
        "  - Avoid Cheating: Try to log your completions honestly to keep your records genuine!"
    )
}

# --- NEU: Motivationssprüche, wenn ein Streak reißt ---
STREAK_BROKEN_MOTIVATION = [
    "Don't sweat it! Every master was once a beginner. Start fresh today!",
    "Failure is not the opposite of success; it's part of success. You got this!",
    "Tomorrow is a new day and a clean slate. Let's build that streak again!",
    "The only bad workout (or habit) is the one that didn't happen. Dust yourself off! ️",
    "Falling down is an accident. Staying down is a choice. Rise up!"
]

# --- NEU: Glückwünsche bei einem neuen Rekord (Longest Streak gebrochen) ---
RECORD_BREAKER_CONGRATS = [
    "UNBELIEVABLE! You just broke your personal high score!",
    "Look at you go! New record achieved! Keep pushing!",
    "Legendary! Your dedication is paying off. New personal best!",
    "You are officially unstoppable. Record broken!"
]

""" -----  Logik zum einfügen der sätze in main.py -------

import random
from resources import STREAK_BROKEN_MOTIVATION, RECORD_BREAKER_CONGRATS

# ... irgendwo in deiner Logik, wenn ein Streak reißt ...
random_motivation = random.choice(STREAK_BROKEN_MOTIVATION)
typer.secho(f"\n😔 Oh no, your streak broke... but remember:\n{random_motivation}", fg=typer.colors.YELLOW)

# ... oder wenn ein Rekord gebrochen wurde ...
random_congrats = random.choice(RECORD_BREAKER_CONGRATS)
typer.secho(f"\n🎉 {random_congrats}", fg=typer.colors.GREEN, bold=True)
"""