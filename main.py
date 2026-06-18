import questionary
from db import get_db
from counter import Counter
from analyse import calculate_count


def cli():
    db = get_db()
    questionary.confirm("Are you ready?").ask()

    stop = False
    while not stop:

        choice = questionary.select(
            "What do you want to do?",
            choices=["Create", "Increment", "Analyse", "Exit"]
        ).ask()

        name = questionary.text("Whats the name of your counter?").ask()

        if choice == "Create":
            desc = questionary.text("What is the description of your counter?").ask()
            counter = Counter(name, desc)
            counter.store(db)
        elif choice == "Increment":
            counter = Counter(name, None)
            counter.increment()
            counter.add_event(db)
        elif choice == "Analyse":
            count = calculate_count(db, name)
            print(f"{name}: has been incremented {count} times.")
        else:
            print("Thanks for using my program.")
            stop = True

if __name__ == "__main__":
    cli()
