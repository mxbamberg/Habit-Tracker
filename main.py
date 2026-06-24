import questionary
import typer

from db import get_db
from habit import *
from analyse import *


def cli():
    db = get_db()
    questionary.confirm("Welcome to your Habit Tracker!").ask()

    stop = False
    while not stop:

        choice = questionary.select(
            "Main Menu:\nWhat do you want to do?",
            choices=["Create habits", "Manage habits", "Track a habit", "Analyse", "Exit"]
        ).ask()

        # name = questionary.text("Whats the name of the habit?").ask()

        if choice == "Create habits":
            name = questionary.text("Whats the name of the habit?").ask()
            desc = questionary.text("What is the description of your habit?").ask()
            habit = Habit(name, desc)
            tracker.store(db)       # Richtig verbunden zum speichern???


        elif choice == "Manage habits":
            ''' User can edit or delete the selected habit '''

            habit_names = get_all_habit_names()     # show all habits

            if not habit_names:
                typer.secho("There are no habits to manage yet. Create one first!", fg=typer.colors.YELLOW)
                continue    # Back to main menu

            habit_choices = habit_names + ["< Back"]
            action = questionary.select("Which habit do you want to edit or delete?", choices=habit_choices).ask()

            if action == "< Back>" or selected_habit is None:
                continue    # Back to main menu

            if action == "Edit a habit":
                # edit the habit
                pass
            elif action == "Delete a habit":
                # delete the habit
                pass

        elif choice == "Track a habit":
            pass

        elif choice == "Analyse":

            app = typer.Typer()

            def handle_show_periodicity():
                # User selects if he wants to see all habits or filter them by periodicity
                choice = questionary.select(
                    "Which habits do you want to see?",
                    choices=["All", "Daily", "Weekly", "< Back"]
                ).ask()

                if choice == "< Back>" or choice is None:   # User wants to exit the sub menu
                    return

                # 2. Daten aus der Datenbank holen (Simuliert)
                # all_habits = get_all_habit_objects()

                # 3. Handle the "All" logic
                if choice == "All":
                    # No filtering needed, returns all habits
                    get_habits()

                    # 3. HIER nutzt du deine Funktion (Die Logik)
                    # Wir übergeben die Liste und das Wort (z.B. "Daily"), das der User gerade gewählt hat
                else:
                    selected_habits = get_habits_by_periodicity(all_habits, choice)

                # 4. Ergebnis ausgeben
                    # Hier fängt die Tabellenausgabe an:
                    if not selected_habits:
                        typer.echo("No habits found in this category.")
                    else:
                        # 1. Tabellen-Kopfzeile (Header) definieren
                        # Die Zahlen (z.B. <20) bestimmen die feste Breite der Spalte
                        header = f"{'Name':<20} | {'Periodicity':<12} | {'Description':<30}"
                        typer.secho(header, fg=typer.colors.CYAN, bold=True)

                        # Eine Trennlinie aus Bindestrichen ziehen (68 Zeichen lang)
                        typer.echo("-" * 68)

                        # 2. Die Zeilen (Rows) mit den echten Habit-Daten befüllen
                        for habit in selected_habits:
                            # Wir holen die Attribute aus dem aktuellen Habit-Objekt
                            name = habit.name
                            periodicity = habit.periodicity
                            description = habit.description if hasattr(habit, 'description') else "No description"
                            current_streak = habit.current_streak
                            longest_streak = habit.longest_streak

                            # Ausgabe der Zeile mit exakt derselben Spaltenbreite wie oben
                            typer.echo(f"{name:<20} | {periodicity:<12} | {description:<30} | {current_streak:<30} | {longest_streak:<30}")

                        typer.echo("\n")


        elif choice == "Exit":
            print("Thanks for using the Habit Tracker.")
            stop = True # while loop ends
            db.close()  # Database gets closed
            raise typer.Exit()

if __name__ == "__main__":
    cli()


'''
CREATE
DELETE
COMPLETE
ANALYSE
HELP -> kann man erklären, was ein habit ist, oder sonstige sachen erklären 
CLOSE

Nach einer Analyse: Press key to continue

'''
'''
drink_water = Habit(
    "Drink Water", "Drink two glasses of water", 1-1-2026, 1-2-2026, "weekly", "default", 10, 20
)

print(f"Name: {drink_water.name}\nDescription: {drink_water.desc}")

'''