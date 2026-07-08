# Quiz Application

A console-based Quiz Application built with Python that allows users to test their knowledge through multiple-choice questions across three difficulty levels. The project demonstrates modular programming, input validation, score calculation, and menu-driven application design.

## Features

* Three difficulty levels (Easy, Medium, Hard)
* 20 questions for each level
* Multiple-choice questions (A, B, C, D)
* Input validation
* Automatic score calculation
* Percentage calculation
* Performance grading
* View last quiz result
* Restart quiz
* Replay with another difficulty level
* Menu-driven interface

## Technologies Used

* Python 3

## Concepts Covered

* Functions
* Lists
* Dictionaries
* Loops
* Conditional Statements
* Exception Handling
* Global Variables
* Input Validation
* Menu-Driven Programming
* Modular Programming

## Project Structure

```text
Quiz-Application-Python/
│
├── Quiz Application.py
└── README.md
```

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

```text
============ Welcome to Quiz Application ============

=============== Select the Option (0-4) ===============

1. Start New Quiz
2. Game Instructions
3. View Last Game Result
4. Restart Quiz
0. Exit

Enter the number: 1

Select Difficulty

1. Easy
2. Medium
3. Hard

Select Level: 2

---------------------------------------------------
Selected Level      : Medium
Total Questions     : 20
Marks Per Question  : 1
Maximum Score       : 20
---------------------------------------------------
Good Luck!
The quiz is starting...
---------------------------------------------------

Question 1/20

Which SQL command retrieves data?

A. GET
B. SELECT
C. FETCH
D. OPEN

Enter Answer (A/B/C/D): B

Correct Answer!

...

================ QUIZ RESULT ================

Correct Answers : 18
Wrong Answers   : 2
Final Score     : 18/20
Percentage      : 90.00%

Status : EXCELLENT!
```

## Future Improvements

* Randomize question order
* Randomize answer options
* Add countdown timer
* Save quiz history using file handling
* Maintain leaderboard
* Load questions from external files
* Add category-wise quizzes
* Build a GUI version using Tkinter

## Learning Outcomes

This project helped me practice:

* Writing modular Python programs
* Organizing code using functions
* Managing structured data using lists and dictionaries
* Building menu-driven applications
* Validating user input
* Implementing scoring systems
* Calculating percentages and performance grades
* Improving problem-solving and debugging skills

## Author

**Muhammad Abdullah Farooq**

GitHub: https://github.com/osaid400
