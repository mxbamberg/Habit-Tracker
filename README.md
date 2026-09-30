# My Habit Tracker App

A little description

## What is it

The objective of this project is to design and implement a backend for a Habit Tracking
application. As we are focusing on backend engineering, the application is designed to operate
entirely with a modern Command Line Interface (CLI). The application will be built using Python
version 3.14 and will use the object-oriented programming paradigm.

## Project structure

```text
habittracker/
├── main.py
├── habit.py
├── tracker.py
├── analyse.py
├── db.py
├── resources.py
├── seed.py
└── test_tracker.py
```

## Requirements

- python 3.14 or later
- pip

## Installation

```shell
pip install -r requirements.txt
```

## Usage

Run

```shell
python main.py
```

and use the interactive menu to interact with the app.

```shell
1. Create a habit
2. Manage habits
3. Complete a habit
4. Analyse
5. Help
0. Exit
```

## Predefined habits

The user can create custom habits or choose one of five predefined habits:

| Habit | periodicity    | description    |
| :---:   | :---: | :---: |
| Drink Water | daily   | Drink at least 2 liters of water every day   |
| Morning Run | daily   | Run for 20 minutes in the morning   |
| Read 10 Pages | daily   | Read 10 pages of a book   |
| Workout Session | weekly   | Go to the gym or do home workout   |
| Clean Room | weekly   | Tidy up your room/apartment   |

## Unit Test

```shell
pytest test_tracker.py
```
