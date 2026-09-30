# My Habit Tracker App


## What is it

The objective of this project is to design and implement a backend for a Habit Tracking
application. As we are focusing on backend engineering, the application is designed to operate
entirely with a modern Command Line Interface (CLI). The application will be built using Python
version 3.14 and will use the object-oriented programming paradigm.

## Project structure

```text
habittracker/
├── main.py    # Interactive CLI menu
├── habit.py    # Habit class
├── tracker.py    # Controller layer that manages habit lifecycle (creation, completion, edits, deletion)
├── analyse.py    # Functional analytics module
├── db.py    # SQLite database
├── resources.py    # 5 predefined habits + help content
├── seed.py      # 4 weeks of sample data
└── test_tracker.py    # Unit test
```

## Requirements

- python 3.10+ or later
- pip
- External dependencies listed in `requirements.txt` (`typer`, `questionary`, `pytest`)

## Installation
1. Ensure Python 3.10+ is installed:
```shell
python --version
```
2. Clone or download this repository

3. Install the requirements
```shell
pip install -r requirements.txt
```

## Usage

Run
```shell
python main.py
```

and use the interactive menu to interact with the app:

```shell
1. Create a habit
2. Manage habits
3. Complete a habit
4. Analyse
5. Help
0. Exit
```
To reset all data in the database, simply delete the database file:
```shell
rm main.db
```

## Predefined habits

The user can create custom habits or choose one of five predefined habits:

| Habit | Periodicity    | Description    |
| :---:   | :---: | :---: |
| Drink Water | daily   | Drink at least 2 liters of water every day   |
| Morning Run | daily   | Run for 20 minutes in the morning   |
| Read 10 Pages | daily   | Read 10 pages of a book   |
| Workout Session | weekly   | Go to the gym or do home workout   |
| Clean Room | weekly   | Tidy up your room/apartment   |

## Seed the database with example data
This inserts 5 predefined habits (3 daily, 2 weekly) and 4 weeks of completion history into the database.
```shell
python seed.py
```


## Unit Test
The test suite uses Pytest
```shell
pytest test_tracker.py
```
