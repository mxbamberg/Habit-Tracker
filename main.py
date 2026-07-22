import questionary
from questionary import Style
import typer
from tracker import *
from db import get_db
from resources import *
import re
from analyse import count_broken_streaks, get_longest_active_streak
# import random   # Zufällige Tipps und Motivation

app = typer.Typer()


def show_welcome_screen():
    """Zeigt ein Willkommens-Banner nur mit Typer-Bordmitteln."""

    # 1. Optional: Das Terminal vorher leeren, damit es sauber aussieht


    # 2. Ein paar Leerzeilen für den Abstand von oben
    print("\n" * 10)

    # 3. Der obere Rand der Box
    typer.secho("  " + "=" * 40, fg=typer.colors.CYAN, bold=True)

    # 4. Der Titel (zentriert durch Leerzeichen)
    typer.secho("           HABIT TRACKER ", fg=typer.colors.MAGENTA, bold=True)

    # 5. Der untere Rand der Box
    typer.secho("  " + "=" * 40, fg=typer.colors.CYAN, bold=True)

    # 6. Der Untertitel
    typer.secho("      Build good habits. Break bad ones.\n", fg=typer.colors.YELLOW)

    questionary.press_any_key_to_continue("\nPress key to start").ask()

# in ui.py packen, damit übersichtlicher
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),       # Fragezeichen-Farbe
    ('question', 'bold'),               # Fragetext
    ('answer', 'fg:#f44336 bold'),      # Eingegebene Antwort
    ('pointer', 'fg:#673ab7 bold'),     # Der Zeiger (z.B. "»")
    ('highlighted', 'fg:#673ab7 bold'), # Die aktuell markierte Auswahl
    ('selected', 'fg:#cc5454'),         # Ausgewählte Option
])

@app.command()
def cli():
    db = get_db()
    tracker = Tracker(db)

    show_welcome_screen()

    stop = False
    while not stop:
        print("\n" * 10)
        typer.secho("=" * 45, fg=typer.colors.RED)
        typer.secho("            MAIN MENU         ", fg=typer.colors.RED, bold=True)
        typer.secho("=" * 45, fg=typer.colors.RED)

        choice = questionary.select(
            "",
            choices=["1. Create a habit", "2. Manage habits", "3. Complete a habit", "4. Analyse", "5. Help", "0. Exit"],
            style=custom_style
        ).ask()



        if choice == "1. Create a habit":
            """User can create a new habit:
            options: choose name, description, periodicity, start_date, end_date"""
            print("\n" * 10)
            typer.secho("=" * 45, fg=typer.colors.CYAN)
            typer.secho("    Create a new Habit", fg=typer.colors.CYAN, bold=True)
            typer.secho("=" * 45, fg=typer.colors.CYAN)

            name = questionary.text("Whats the name of the habit?").ask()
            if not name:
                typer.secho("Name cannot be empty. Habit creation cancelled.", fg=typer.colors.RED)
                questionary.press_any_key_to_continue("Press any key to continue...").ask()
                continue

            desc = questionary.text("What is the description of your habit?").ask()

            periodicity = questionary.select(
                "Do you want to complete the habit daily or weekly?",
                choices=["Daily", "Weekly"]).ask()

            start_date = datetime.now()

            end_date = None
            add_end = questionary.confirm("Do you want to set an end date for this habit?", default=False).ask()
            if add_end:
                while True:
                    date_input = questionary.text("Enter end date (Format: YYYY-MM-DD):").ask()
                    if not date_input:
                        break  # User left it empty, remains None

                    # Simple RegEx to validate format
                    if re.match(r"^\d{4}-\d{2}-\d{2}$", date_input):
                        try:
                            # Convert the string to a real datetime object for the Habit class
                            end_date = datetime.strptime(date_input, "%Y-%m-%d")

                            # Ensure end date isn't in the past
                            if end_date.date() < start_date.date():
                                print("The end date cannot be in the past!")
                                continue

                            break
                        except ValueError:
                            print("Invalid date values (e.g., check months/days).")
                    else:
                        print("Invalid format! Please use YYYY-MM-DD (e.g., 2026-12-31).")

            new_habit = Habit(
                name=name.strip(),  # removes whitespaces at beginning and end
                periodicity=periodicity.lower(),
                desc=desc.strip(),
                start_date=start_date,
                end_date=end_date,
            )

            # XXXXXXXXXXX Zusammengefasst das erstellte Habit zusammengefasst anzeigen XXXXXXXXXXXX

            success, message = tracker.store_new_habit(new_habit)  # store habit in main.db

            if success:
                typer.secho(f"\nHabit {name} was created successfully!", fg=typer.colors.GREEN, bold=True)

            else:
                typer.secho(f"\n{message}", fg=typer.colors.RED, bold=True)

            questionary.press_any_key_to_continue("Press any key to continue...").ask()



        elif choice == "2. Manage habits":
            """ User can edit and delete all created habits"""
            print("\n" * 10)

            typer.secho("=" * 45, fg=typer.colors.CYAN)
            typer.secho("    Manage habits", fg=typer.colors.CYAN, bold=True)
            typer.secho("=" * 45, fg=typer.colors.CYAN)

            habit_names = tracker.get_habit_names()     # Get habit names from db

            if not habit_names:
                # Back to main menu, if no habits in db
                typer.secho("There are no habits to manage yet. Create one first!", fg=typer.colors.YELLOW)
                questionary.press_any_key_to_continue("Press any key to continue...").ask()
                continue

            action = questionary.select(
                "Choose an option:\n",
                choices=["1. Edit a habit", "2. Delete a habit", "0. Back"],
                style=custom_style
            ).ask()

            if not action or action == "0. Back":
                # User returns to main menu
                continue


            elif action == "1. Edit a habit":
                typer.secho("=" * 45, fg=typer.colors.CYAN)
                typer.secho("    Edit a Habit", fg=typer.colors.RED, bold=True)
                typer.secho("=" * 45, fg=typer.colors.CYAN)

                # User selects the habit that he wants to edit
                selected_habit = questionary.select(
                    f"Which habit do you want to edit?",
                    choices=habit_names + ["0. Back"],
                    style=custom_style
                ).ask()

                if not selected_habit or selected_habit == "0. Back":
                    continue

                # Platzhalter für die neuen Werte (bleiben None, wenn der User Nein sagt)
                new_name = None
                new_desc = None
                new_period = None

                # 2. Schritt-für-Schritt Abfrage mit questionary.confirm
                if questionary.confirm(f"Do you want to change the name of '{selected_habit}'?").ask():
                    new_name = questionary.text("Enter new name:", style=custom_style).ask()

                if questionary.confirm("Do you want to update the description?").ask():
                    new_desc = questionary.text("Enter new description:", style=custom_style).ask()

                if questionary.confirm("Do you want to edit the periodicity?").ask():
                    new_period = questionary.select(
                        "Select new periodicity:",
                        choices=["Daily", "Weekly"],
                        style=custom_style
                    ).ask()

                # 3. Prüfen, ob überhaupt etwas geändert wurde
                if new_name is None and new_desc is None and new_period is None:
                    typer.secho("\nNo changes made.", fg=typer.colors.YELLOW)
                    continue

                # 4. Speichern!
                tracker.edit_habit(
                    old_name=selected_habit,
                    new_name=new_name,
                    new_desc=new_desc,
                    new_periodicity=new_period
                )

                typer.secho("\nHabit was updated successfully!", fg=typer.colors.GREEN, bold=True)

                questionary.press_any_key_to_continue("\nPress any key to continue...").ask()


            elif action == "2. Delete a habit":
                typer.secho("=" * 45, fg=typer.colors.CYAN)
                typer.secho("    Delete a Habit", fg=typer.colors.RED, bold=True)
                typer.secho("=" * 45, fg=typer.colors.CYAN)

                # User selects the habit that he wants to delete
                selected_habit = questionary.select(
                    f"Which habit do you want to delete?",
                    choices=habit_names + ["0. Back"],
                    style=custom_style
                ).ask()

                if not selected_habit or selected_habit == "0. Back":
                    continue

                confirm = questionary.confirm(
                    f"Are you sure you want to delete '{selected_habit}'? This will delete all progress!",
                    default=False
                ).ask()

                if confirm is True:
                    success, message = tracker.delete_habit(selected_habit)

                    color = typer.colors.GREEN if success else typer.colors.RED

                    typer.secho(f"\n{message}", fg=color, bold=True)
                else:
                    typer.secho("\nDeletion cancelled.", fg=typer.colors.CYAN)

                questionary.press_any_key_to_continue("\nPress any key to continue...").ask()



        elif choice == "3. Complete a habit":
            """User can complete a habit that he created"""
            print("\n" * 10)

            typer.secho("=" * 45, fg=typer.colors.CYAN)
            typer.secho("    Complete a Habit", fg=typer.colors.CYAN, bold=True)
            typer.secho("=" * 45, fg=typer.colors.CYAN)

            # Fetch available habit names
            habit_names = tracker.get_habit_names()

            if not habit_names:
                typer.secho("You haven't created any habits yet!", fg=typer.colors.YELLOW)
                questionary.press_any_key_to_continue("Press any key to continue...").ask()
                continue

            # User chooses which habit to complete
            selected_habit = questionary.select(
                "Which habit did you complete?",
                choices=habit_names + ["0. Back"],
                style=custom_style
            ).ask()

            if not selected_habit or selected_habit == "0. Back":
                typer.secho("Action cancelled.", fg=typer.colors.RED)
                questionary.press_any_key_to_continue("Press any key to continue...").ask()
                continue

            # Call the tracker logic to record the completion
            success, message = tracker.complete_habit(selected_habit)

            if success:
                typer.secho(f"\n{message}", fg=typer.colors.GREEN, bold=True)
            else:
                typer.secho(f"\n{message}", fg=typer.colors.RED, bold=True)

            # XXXXXXXX Anzeigen, was aktuell die streak ist XXXXXXXXXXXX
            # XXXXXXXX Wenn streak gebrochen --> User einen Hinweis geben und ggf Motivationsspruch XXXXXXXXXXXX

            questionary.press_any_key_to_continue("Press any key to continue...").ask()



        elif choice == "4. Analyse":
            """Was soll hier rein:
            - Habits anzeigen --> Liste von allen, alle aktiven, alle daily oder alle weekly
            - Streaks von einzelnem habit anzeigen (aktive streak und all-time)
            - Letzten (10) completion dates anzeigen
            - Welche streak ist am längsten von allen habits
            - Welche aktive streak ist am längsten
            - Welches habit wurde am meisten gebrochen?
                --> insgesamt am meisten oder innerhalb von zeitraum (letzte 30 Tage)
            """
            print("\n" * 10)

            while True:
                typer.secho("=" * 45, fg=typer.colors.CYAN)
                typer.secho("    Habit Analytics Dashboard", fg=typer.colors.MAGENTA, bold=True)
                typer.secho("=" * 45, fg=typer.colors.CYAN)

                analyse_choice = questionary.select(
                    "What analysis do you want to run?",
                    choices=[
                        "1. List all tracked habits",
                            "2. Filter habits by periodicity (Daily/Weekly)",
                            "3. View streaks of a specific habit",
                            "4. Show last 10 completions of a habit",
                            "5. Find longest streak of all time across all habits",
                            "6. Find longest active streak across all habits",
                            "7. Show most struggled habit (broken streaks)",
                        "0. Back"
                    ],
                    style=custom_style
                ).ask()

                if not analyse_choice or analyse_choice == "0. Back":
                    # User returns to main menu
                    break

                if analyse_choice == "1. List all tracked habits":
                    habits = tracker.get_all_habits()
                    if not habits:
                        typer.secho("No habits tracked yet.", fg=typer.colors.YELLOW)
                    else:
                        typer.secho("\n--- Your Habits ---", fg=typer.colors.CYAN, bold=True)
                        for h in habits:
                            print(
                                f"{h.name} ({h.periodicity}) - Desc: {h.desc} | Current Streak: {h.current_streak} | All-time Longest: {h.longest_streak}")
                    questionary.press_any_key_to_continue().ask()

                # 2. FILTER BY PERIODICITY
                elif analyse_choice == "2. Filter habits by periodicity (Daily/Weekly)":
                    period = questionary.select("Select periodicity:", choices=["Daily", "Weekly"]).ask()
                    if period:
                        # Utilizing functional module filter
                        filtered = tracker.get_habits_by_periodicity(period.lower())
                        if not filtered:
                            typer.secho(f"No {period.lower()} habits found.", fg=typer.colors.YELLOW)
                        else:
                            typer.secho(f"\n--- {period} Habits ---", fg=typer.colors.CYAN, bold=True)
                            for h in filtered:
                                print(f"{h.name} - Current: {h.current_streak} | Longest: {h.longest_streak}")
                    questionary.press_any_key_to_continue().ask()

                # 2. View streak of selected habit
                elif analyse_choice == "3. View streaks of a specific habit":
                    habit_names = tracker.get_habit_names()

                    if not habit_names:
                        typer.secho("No habits found.", fg=typer.colors.YELLOW)

                    else:
                        selected_habit = questionary.select(
                            "Choose a habit to view streaks:",
                            choices=habit_names,
                            style=custom_style
                        ).ask()

                        if selected_habit:
                            # 3. Das entsprechende Habit-Objekt aus der DB/Liste holen
                            all_habits = tracker.get_all_habits()
                            target_habit = next((h for h in all_habits if h.name == selected_habit), None)

                            if target_habit:
                                typer.secho(f"\n--- Streaks for '{target_habit.name}' ---", fg=typer.colors.CYAN,
                                            bold=True)
                                print(f" Periodicity:    {target_habit.periodicity.capitalize()}")
                                print(f" Current Streak: {target_habit.current_streak}")
                                print(f" Longest Streak: {target_habit.longest_streak}")
                            else:
                                typer.secho("Habit not found.", fg=typer.colors.RED)

                            questionary.press_any_key_to_continue().ask()


                elif analyse_choice == "4. Show last 10 completions of a habit":
                    habit_names = tracker.get_habit_names()

                    if not habit_names:
                        typer.secho("\nNo habits found.", fg=typer.colors.YELLOW)
                        questionary.press_any_key_to_continue().ask()

                    else:
                        # Super schlank und sauber!
                        selected_habit = questionary.select(
                            "Choose a habit to check history:",
                            choices=habit_names,
                            style=custom_style
                        ).ask()

                        # 3. Historie abrufen
                        history = tracker.get_completion_history(selected_habit)

                        if not history:
                            typer.secho(f"\nThe habit {selected_habit} has no completions recorded yet.",
                                        fg=typer.colors.YELLOW)
                        else:
                            typer.secho(f"\n--- Last 10 completions for '{selected_habit}' ---", fg=typer.colors.CYAN,
                                        bold=True)
                            for idx, dt in enumerate(history, 1):
                                date_display = dt.strftime('%Y-%m-%d') if hasattr(dt, 'strftime') else str(dt)
                                print(f" {idx}. ✅ {date_display}")

                        # Das hält den Bildschirm an, damit du das Ergebnis siehst!
                        questionary.press_any_key_to_continue().ask()


                # 5. LONGEST STREAK OF ALL TIME OVERALL
                elif analyse_choice == "5. Find longest streak of all time across all habits":
                    habits = tracker.get_all_habits()
                    name, length = get_longest_active_streak(habits)
                    if length == 0:
                        typer.secho("No records found.", fg=typer.colors.YELLOW)
                    else:
                        typer.secho(
                            f"\nAbsolute Record Holder Across All Habits: '{name}' with a historical streak of {length} periods!",
                            fg=typer.colors.GREEN, bold=True)
                    questionary.press_any_key_to_continue().ask()

                    # 6. LONGEST ACTIVE STREAK OVERALL
                elif analyse_choice == "6. Find longest active streak across all habits":
                    habits = tracker.get_all_habits()
                    name, length = get_longest_active_streak(habits)
                    if length == 0:
                        typer.secho("No active streaks found right now.", fg=typer.colors.YELLOW)
                    else:
                        typer.secho(
                            f"\nCurrent Top Leader: '{name}' with a live active streak of {length} periods!",
                            fg=typer.colors.GREEN, bold=True)
                    questionary.press_any_key_to_continue().ask()

                # 7. MOST STRUGGLED HABIT
                elif analyse_choice == "7. Show most struggled habit (broken streaks)":
                    habits = tracker.get_all_habits()
                    if not habits:
                        typer.secho("No habits tracked yet.", fg=typer.colors.YELLOW)
                    else:
                        struggle_list = []
                        for h in habits:
                            # Fetch full history dates via tracker
                            history_datetimes = tracker.get_completion_history(h.name)
                            # Convert full datetimes into simple datetime.date objects for analytics
                            history_dates = [dt.date() for dt in history_datetimes]

                            # Count breaks via our functional math engine
                            breaks = count_broken_streaks(history_dates, h.periodicity)
                            struggle_list.append((h.name, breaks))

                        # Find the habit with maximum breaks
                        worst_habit, max_breaks = max(struggle_list, key=lambda item: item[1])

                        if max_breaks == 0:
                            typer.secho("\nPhenomenal! You haven't broken any habit streaks yet!",
                                        fg=typer.colors.GREEN, bold=True)
                        else:
                            typer.secho(f"\nYour most struggled habit is '{worst_habit}'!",
                                        fg=typer.colors.RED, bold=True)
                            print(
                                f"You let this habit slip and broke your streak sequence a total of {max_breaks} times.")
                    questionary.press_any_key_to_continue().ask()


        elif choice == "5. Help":
            print("\n" * 10)


            while True:
                typer.secho("=" * 45, fg=typer.colors.CYAN)
                typer.secho("    Help & Frequently Asked Questions", fg=typer.colors.CYAN, bold=True)
                typer.secho("=" * 45, fg=typer.colors.CYAN)

                # 1. Menü mit den Fragen aus unserem Dictionary + Zurück-Option
                help_choices = list(HELP_CONTENT.keys()) + ["0. Back"]

                selected_question = questionary.select(
                    "What do you want to know?\n",
                    choices=help_choices,
                    style=custom_style
                ).ask()

                # Return to main menu
                if not selected_question or selected_question == "0. Back":
                    typer.secho("Back to main menu", fg=typer.colors.YELLOW)
                    break

                ''' Return the answer from resources'''
                answer = HELP_CONTENT[selected_question]

                typer.secho(f"\n{selected_question}", fg=typer.colors.YELLOW, bold=True)
                print("-" * len(selected_question) * 2)
                typer.secho(answer, fg=typer.colors.WHITE)
                print("-" * len(selected_question) * 2)

                # Kurze Pause, damit der User den Text lesen kann, bevor das Menü neu lädt
                questionary.press_any_key_to_continue("\nPress any key to read another topic...").ask()

        elif choice == "0. Exit":
            print("\n" * 10)
            typer.secho("=" * 45, fg=typer.colors.RED)
            print("Thanks for using the Habit Tracker.")
            typer.secho("=" * 45, fg=typer.colors.RED)
            stop = True  # while loop ends
            db.close()  # Database gets closed
            raise typer.Exit()


if __name__ == "__main__":
    app()

