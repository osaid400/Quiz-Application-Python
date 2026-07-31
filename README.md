# Quiz Application

A console-based Quiz Application built with Python. This project demonstrates the use of Object-Oriented Programming (OOP), JSON-based file handling, exception handling, and modular programming to create a feature-rich quiz system with multiple categories, difficulty levels, and persistent score history.

## Features

* 5 Quiz Categories:

  * IQ
  * Mathematics
  * General Knowledge
  * Computer Science
  * Current Affairs
* Three difficulty levels for every category:

  * Easy
  * Medium
  * Hard
* 20 questions per difficulty level
* Multiple-choice questions with input validation (A/B/C/D only)
* Quit the quiz anytime using **Q**
* Real-time score tracking
* Percentage calculation
* Performance grading (Excellent, Very Good, Good, Average, Pass, Fail)
* Quiz history saved automatically
* View complete score history
* Game instructions menu
* Replay quiz without restarting the application

## Technologies Used

* Python 3

## Concepts Covered

* Object-Oriented Programming (OOP)
* Classes & Objects
* Constructors (`__init__`)
* Class Methods (`@classmethod`)
* Lists
* Dictionaries
* Loops (`for`, `while`)
* Conditional Statements
* Exception Handling
* User Input Validation
* List Comprehensions
* JSON File Handling (`json.load()`, `json.dump()`)
* `datetime` Module
* File Persistence
* Menu-Driven Console Applications

## Project Structure

```text
Quiz-Application/
│
├── Quiz Application.py
├── questions.json
├── .gitignore
└── README.md
```

> **Note:** `quiz_history.json` is created automatically when the program runs. It stores quiz history locally and is excluded from the repository using `.gitignore`.

## How to Run

1. Clone the repository

```bash
git clone https://github.com/osaid400/Quiz-Application-Python.git
```

2. Navigate to the project folder

```bash
cd Quiz-Application-Python
```

3. Run the application

```bash
python "Quiz Application.py"
```

## Example Output

### Main Menu

```text
============ Welcome to Quiz Application =============

=============== Select the Option (0-4) ===============
1. Start New Quiz
2. Game Instructions
3. View Score History
4. Restart Quiz
0. Exit
```

### Category Selection

```text
--- Select Category ---

1. Computer Science
2. Current Affairs
3. General Knowledge
4. IQ
5. Mathematics

Select Category:
```

### Difficulty Selection

```text
--- Select Difficulty Level ---

1. Easy
2. Medium
3. Hard

Select Level:
```

### Quiz

```text
Question 1/20

What does CPU stand for?

A. Central Process Unit
B. Central Processing Unit
C. Computer Personal Unit
D. Central Program Unit

Enter Answer (A/B/C/D) or Q to Quit:
```

### Result

```text
================ QUIZ RESULT ================

Your Category    : Computer Science
Your Level       : Easy
Correct Answers  : 18
Wrong Answers    : 2
Final Score      : 18/20
Percentage       : 90.00%

===============================================

Status: EXCELLENT!
```

### Score History

```text
================================================================================
                                 SCORE HISTORY
================================================================================
Date and Time      Category                 Level       Score     Percentage
================================================================================
31-07-2026 10:15   Computer Science         Easy        18/20     90.00%
31-07-2026 10:45   Mathematics              Medium      15/20     75.00%
================================================================================
```

## Data Persistence

* All questions are stored in **questions.json**.
* Quiz history is stored in **quiz_history.json**.
* Every completed quiz records:

  * Category
  * Difficulty Level
  * Score
  * Percentage
  * Date & Time
* History remains available even after restarting the program.

## Future Improvements

* Add a timer for each question
* Shuffle questions randomly
* Shuffle answer options
* Add hints
* Display highest score for every category and level
* Migrate from JSON storage to SQLite
* Build a GUI version using Tkinter

## Learning Outcomes

This project helped me practice:

* Designing applications using Object-Oriented Programming
* Working with JSON-based data persistence
* Reading and writing structured data
* Managing multiple categories and difficulty levels
* Creating reusable classes and methods
* Building menu-driven console applications
* Implementing input validation
* Recording and displaying user history
* Improving code organization and readability

## Author

**Muhammad Abdullah Farooq**

GitHub: https://github.com/osaid400
