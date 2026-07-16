# Quiz Application

A console-based Quiz Application built with Python. This project demonstrates the use of functions, lists, dictionaries, loops, conditional statements, exception handling, and JSON-based file persistence to run a multi-level quiz with score history tracking.

## Features

* Three difficulty levels — Easy, Medium, Hard (20 questions each)
* Multiple-choice questions with input validation (only A/B/C/D accepted)
* Real-time score tracking with correct/wrong feedback
* Final result with percentage and performance status (Excellent/Very Good/Good/Average/Pass/Fail)
* Replay option to play again without restarting the program
* Score history — every completed quiz is saved with level, score, and date
* View Score History — see all past quiz attempts
* Game instructions menu

## Technologies Used

* Python 3

## Concepts Covered

* Functions
* Lists
* Dictionaries
* Loops (`for`, `while`)
* Conditional Statements
* Exception Handling
* User Input Validation
* `enumerate()` Function
* Global Variables and Scope
* File Handling with JSON (`json.load()`, `json.dump()`)
* `os.path.exists()` for safe file loading
* `datetime` Module (`strftime()` for formatting dates)

## Project Structure

```text
Quiz-Application/
│
├── Quiz Application.py
├── .gitignore
└── README.md
```

> Note: `quiz_history.json` is created automatically when the program runs and stores your quiz score history locally. It is excluded from the repository via `.gitignore` since it holds runtime data rather than source code.

## How to Run

1. Clone the repository:
```bash
git clone https://github.com/osaid400/Quiz-Application-Python.git
```
2. Navigate to the project folder:
```bash
cd Quiz-Application-Python
```
3. Run the program:
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

### Taking a Quiz

```text
Select Level: 1
---------------------------------------------------
Selected Level: Easy
Number of Questions: 20
The quiz will begin now.
---------------------------------------------------
Question 1/20
What does CPU stand for?
A. Central Process Unit
B. Central Processing Unit
C. Computer Personal Unit
D. Central Program Unit
Enter Answer (A/B/C/D): B
Correct Answer! B
```

### Final Result

```text
================ QUIZ RESULT ================
Correct Answers:  18
Wrong Answers:  2
Your final score is: 18/20
Percentage: 90.00%
Status: EXCELLENT!
---------------------------------------------------
```

### Viewing Score History

```text
============================================================
                   SCORE HISTORY                  
============================================================
============================================================
Date                 Level                Score                
============================================================
14-07-2026          Level: Easy            18/20
14-07-2026          Level: Medium          14/20
```

## How Data Persistence Works

* Every time a quiz is completed, a record (level, score, total, date) is appended to `quiz_history.json` using `json.dump()`.
* The `view_history()` function reads the file with `json.load()` and displays all past attempts.
* History persists across program runs since it's stored on disk rather than only in memory.
* History is only saved once per completed quiz — viewing history or restarting does not create duplicate entries.

## Future Improvements

* Add a timer per question
* Add more question categories (not just difficulty-based)
* Show highest score per level
* Migrate from JSON file storage to SQLite
* Implement Object-Oriented Programming (OOP)

## Learning Outcomes

This project helped me practice:

* Writing modular code using functions
* Managing multiple datasets (three difficulty levels) with lists and dictionaries
* Implementing input validation and exception handling
* Using `enumerate()` for numbered question display
* Understanding global variable scope across functions
* Persisting data between program runs using JSON file handling
* Working with the `datetime` module to record and format dates

## Author

**Muhammad Abdullah Farooq**

GitHub: https://github.com/osaid400