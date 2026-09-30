import sqlite3
from datetime import date, datetime, timedelta
import pytest

from habit import Habit
from tracker import Tracker
import db
import analyse
from resources import PREDEFINED_4_WEEK_DATA


class TestTrackerApp:
    """Test suite covering habit storage, completions, and analytics calculations"""

    def setup_method(self):
        """Prepares an isolated in-memory SQLite database before each test execution"""
        self.db_conn = sqlite3.connect(":memory:")
        db.create_tables(self.db_conn)
        self.tracker = Tracker(self.db_conn)

    def teardown_method(self):
        """Closes the in-memory database connection after each test execution"""
        self.db_conn.close()

    # -------------------------------------------------------------------------
    # Tests für das Erstellen und Verwalten von Habits (OOP & Backend)
    # -------------------------------------------------------------------------

    def test_create_habit_success(self):
        """Tests successful creation and storage of a new habit"""
        test_habit = Habit(
            name="Read Books",
            periodicity="daily",
            desc="Read 10 pages a day",
            start_date=datetime(2026, 7, 1)
        )
        success, message = self.tracker.store_new_habit(test_habit)

        assert success is True

        habit_names = self.tracker.get_habit_names()
        assert "Read Books" in habit_names

    def test_duplicate_habit_prevention(self):
        """Tests that creating duplicate habit names is prevented"""
        habit1 = Habit(name="Drink Water", periodicity="daily", desc="Drink 5 glasses", start_date=datetime(2026, 7, 1))
        habit2 = Habit(name="Drink Water", periodicity="daily", desc="Drink 5 glasses", start_date=datetime(2026, 7, 1))

        self.tracker.store_new_habit(habit1)
        success, message = self.tracker.store_new_habit(habit2)

        assert success is False
        assert "already exists" in message.lower() or "duplikat" in message.lower()

    # -------------------------------------------------------------------------
    # Tests für Editing und Delete Habits
    # -------------------------------------------------------------------------

    def test_delete_habit_success(self):
        """Tests deleting an existing habit from the database and verifies its removal."""
        # Setup test habit
        test_habit = Habit(
            name="Read Books",
            periodicity="daily",
            desc="Read 10 pages daily",
            start_date=datetime(2026, 7, 1)
        )
        self.tracker.store_new_habit(test_habit)
        assert "Read Books" in self.tracker.get_habit_names()

        # Delete habit via tracker
        success, message = self.tracker.delete_habit("Read Books")

        assert success is True
        assert "deleted" in message.lower()
        assert "Read Books" not in self.tracker.get_habit_names()

    def test_edit_habit_success(self):
        """Tests updating an existing habit's name, description, and periodicity."""
        # Setup test habit
        test_habit = Habit(
            name="Drink Water",
            periodicity="daily",
            desc="Drink 1L water",
            start_date=datetime(2026, 7, 1)
        )
        self.tracker.store_new_habit(test_habit)

        # Execute edit_habit passing the current name as old_name
        self.tracker.edit_habit(
            old_name="Drink Water",
            new_name="Drink 2L Water",
            new_desc="Updated description",
            new_periodicity="weekly"
        )

        # Retrieve all habits and verify updated values
        habit_names = self.tracker.get_habit_names()
        assert "Drink Water" not in habit_names
        assert "Drink 2L Water" in habit_names

        weekly_habits = self.tracker.get_habits_by_periodicity("weekly")
        assert len(weekly_habits) == 1
        assert weekly_habits[0].name == "Drink 2L Water"
        assert weekly_habits[0].desc == "Updated description"

    # -------------------------------------------------------------------------
    # Tests für das Abhaken / Complete & Event-Log
    # -------------------------------------------------------------------------

    def test_complete_habit(self):
        """Tests logging a completion entry for a stored habit"""
        test_habit = Habit(name="Workout", periodicity="daily", desc="Do a workout", start_date=datetime(2026, 7, 1))
        self.tracker.store_new_habit(test_habit)

        success, msg = self.tracker.complete_habit("Workout")
        assert success is True

        habit_id = db.get_habit_id_by_name(self.db_conn, "Workout")
        history = db.get_latest_completions(self.db_conn, habit_id, limit=10)

        assert len(history) == 1

    def test_daily_streak_calculation(self):
        """Tests daily streak evaluation logic using consecutive date inputs"""

        today = date.today()
        dates = [
            today - timedelta(days=2),
            today - timedelta(days=1),
            today
        ]

        current_streak, longest_streak = analyse.calc_streaks(dates, "daily")

        assert current_streak == 3
        assert longest_streak == 3

    def test_broken_streak_reset(self):
        """Tests that streak counters reset properly when dates contain gaps"""
        today = date.today()

        dates = [
            today - timedelta(days=5),
            today
        ]

        current_streak, longest_streak = analyse.calc_streaks(dates, "daily")

        assert current_streak == 1
        assert longest_streak == 1

    def test_filter_by_periodicity(self):
        """Tests habit list filtering based on periodicity"""
        self.tracker.store_new_habit(Habit(name="Daily Run", periodicity="daily", desc="Do a run", start_date=datetime(2026, 7, 1)))
        self.tracker.store_new_habit(Habit(name="Weekly Report", periodicity="weekly", desc="Do a report", start_date=datetime(2026, 7, 1)))


        daily_habits = self.tracker.get_habits_by_periodicity("daily")

        assert len(daily_habits) == 1
        assert daily_habits[0].name == "Daily Run"

    def test_get_longest_streak_alltime(self):
        """Tests identifying the habit with the maximum historical streak across all habits."""
        # Create test habit instances with differing historical streak records
        habit1 = Habit(name="Read Books", periodicity="daily", desc="Read 10 pages daily", start_date=datetime(2026, 7, 1))
        habit1.longest_streak = 5

        habit2 = Habit(name="Drink Water", periodicity="daily", desc="Drink 2L water daily", start_date=datetime(2026, 7, 1))
        habit2.longest_streak = 15

        habit3 = Habit(name="Workout", periodicity="weekly", desc="Gym session weekly", start_date=datetime(2026, 7, 1))
        habit3.longest_streak = 8

        habits_list = [habit1, habit2, habit3]

        # Execute analytical calculation
        top_habit_name, max_streak = analyse.get_longest_streak_alltime(habits_list)

        assert top_habit_name == "Drink Water"
        assert max_streak == 15

    def test_get_longest_active_streak(self):
        """Tests identifying the habit with the highest currently active streak."""
        # Create test habit instances with differing current active streaks
        habit1 = Habit(name="Read Books", periodicity="daily", desc="Read 10 pages daily", start_date=datetime(2026, 7, 1))
        habit1.current_streak = 12

        habit2 = Habit(name="Drink Water", periodicity="daily", desc="Drink 2L water daily", start_date=datetime(2026, 7, 1))
        habit2.current_streak = 3

        habit3 = Habit(name="Workout", periodicity="weekly", desc="Gym session weekly", start_date=datetime(2026, 7, 1))
        habit3.current_streak = 7

        habits_list = [habit1, habit2, habit3]

        # Execute analytical calculation
        top_habit_name, max_active_streak = analyse.get_longest_active_streak(habits_list)

        assert top_habit_name == "Read Books"
        assert max_active_streak == 12

    def test_count_broken_streaks(self):
        """Tests counting broken streak gaps for daily and weekly completion histories."""
        # Daily habit test: 2 gaps larger than 1 day (Aug 1-2, gap to Aug 5, gap to Aug 8)
        daily_dates = [
            date(2026, 8, 1),
            date(2026, 8, 2),
            date(2026, 8, 5),  # Break 1 (> 1 day gap)
            date(2026, 8, 8)  # Break 2 (> 1 day gap)
        ]
        daily_breaks = analyse.count_broken_streaks(daily_dates, "daily")
        assert daily_breaks == 2

        # Weekly habit test: 1 gap larger than 1.5 weeks (Aug 1 to Aug 8, gap to Aug 25)
        weekly_dates = [
            date(2026, 8, 1),
            date(2026, 8, 8),
            date(2026, 8, 25)  # Break 1 (> 1.5 weeks gap)
        ]
        weekly_breaks = analyse.count_broken_streaks(weekly_dates, "weekly")
        assert weekly_breaks == 1