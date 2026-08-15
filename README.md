# Quiz Application

A console-based Quiz Application built with Python using Object-Oriented Programming (OOP) principles. It goes well beyond a basic Q&A loop — timed questions, randomized question sampling, user accounts with performance analytics, a global leaderboard, and a full admin question-bank manager — all backed by JSON persistence and a modular package structure.

---

## Features

* **Accounts & Access:**
  * Admin Login (3-attempt lockout with a 10-second cooldown)
  * User Login (3-attempt lockout with a 10-second cooldown)
  * New User Registration (with age and phone validation)
  * SHA-256 password hashing for all accounts

* **Quiz Experience:**
  * Category and difficulty selection (Easy / Medium / Hard)
  * Up to 20 questions per attempt, **randomly sampled** from the full question pool (not always the same first 20)
  * Options shuffled per question, so the correct answer's letter changes each time
  * 15-second timer per question (cross-platform: `msvcrt` on Windows, `select` on Unix), with "Time's Up!" handling
  * Quit mid-quiz at any time (`Q`)
  * Review Incorrect Answers from the last attempt
  * Score history, performance badges (🏆 Quiz Master down to 🔰 Beginner)

* **User Analytics:**
  * Score History
  * Performance Analytics (total quizzes, average %, best category, highest badge)
  * Category-Wise Progress
  * Global Leaderboard (top 10 by best score)
  * Profile view and update (password, phone, age)

* **Admin Question Bank Management:**
  * Add Questions (with duplicate-question protection)
  * Edit Questions (with duplicate-question protection on the new text too)
  * View All Questions (grouped by category)
  * Delete Questions
  * Add New Category (persisted independently, not just derived from existing questions)
  * View All Users' Quiz History
  * View All Users' Profiles
  * Reset History

* **Data & Reliability Features:**
  * Persistent JSON storage for Users, Questions, Categories, and History — each in its own file
  * Strict validation on load: malformed question/user/history records are silently dropped rather than crashing the app
  * A guaranteed default Admin account always exists, even if the users file is corrupted or emptied
  * Data directory resolved relative to the project root, so the app works regardless of which folder it's run from

---

## Technologies Used

* **Python 3** (Object-Oriented Programming)
* **JSON Module** (Data persistence)
* **hashlib** (SHA-256 password hashing)
* **random** (Question sampling and option shuffling)
* **msvcrt / select** (Cross-platform timed input)
* **Datetime Module** (Timestamps for quiz history)
* **OS Module** (Path resolution, directory handling)

---

## Project Structure

```text
Quiz-Application/
│
├── data/
│   ├── questions.json         # Persistent question bank (gitignored)
│   ├── categories.json        # Persistent category list (gitignored)
│   ├── users.json             # Persistent user accounts (gitignored)
│   └── quiz_history.json      # Persistent quiz attempt history (gitignored)
│
├── src/                        # Source code package
│   ├── __init__.py
│   ├── models.py                 # Question class — validation and serialization
│   ├── manager.py                  # QuizManager class — all persistence logic
│   └── UI.py                       # QuizUI class — login, menus, quiz flow, analytics display
│
├── .gitignore                  # Excludes __pycache__ and local data
├── main.py                     # Application entry point
└── README.md
```

> **Note:** All `data/*.json` files are created automatically on first run, seeded with a default Admin account (`admin` / `0000`). They are excluded from the repository via `.gitignore`.

---

## How to Run

Clone the repository

```bash
git clone https://github.com/osaid400/Quiz-Application.git
```

Move into the project folder

```bash
cd Quiz-Application
```

Run the program

```bash
python main.py
```

---

## Example Outputs

### Main Menu

```text
============ Welcome to Quiz Application =============

=============== MAIN MENU ===============
1. Admin Login
2. User Login
3. New User Registration
0. Exit
```

### New User Registration

```text
=============== New User Registration ===============
Choose Username: osaid
Choose Password: pass1234
Enter Age: 18
Enter Phone Number (11 digits): 03001234567
Registration Successful! Your User ID is: 1
```

### User Login with Lockout

```text
================== User Login ==================
Username: osaid
Password: wrongpass
Invalid Username or Password! (2 attempt(s) remaining)

Username: osaid
Password: wrongpass
Invalid Username or Password! (1 attempt(s) remaining)

Username: osaid
Password: wrongpass
Too many failed attempts! Cooldown active for 10 seconds.
```

### Starting a Quiz

```text
--- Select Category ---
1. General Knowledge
2. Science
3. Programming

Select Category Number: 3

--- Select Level ---
1. Easy | 2. Medium | 3. Hard
Select Level (1-3): 2

---------------------------------------------------
Selected Category: Programming
Selected Level: Medium
Number of Questions: 15
Timer: 15 Seconds per question!
---------------------------------------------------

Question 1/15
What does OOP stand for?
A. Object-Oriented Programming
B. Order Of Precedence
C. Output Operation Protocol
D. Open Object Platform
Enter Answer (A/B/C/D) or Q to Quit [15s]: A
Correct Answer!
---------------------------------------------------
```

### Quiz Result

```text
================ QUIZ RESULT ================
Your Category    : Programming
Your Level       : Medium
Correct Answers  : 13
Wrong Answers    : 2
Final Score      : 13/15
Percentage       : 86.67%
Status: VERY GOOD! (Badge: ⭐ Pro Player)
---------------------------------------------------
Do you want to play again? (Yes/No): no
```

### Review Incorrect Answers

```text
================ REVIEW INCORRECT ANSWERS ================

1. Question: What is the time complexity of binary search?
   A. O(n)
   B. O(log n)
   C. O(n^2)
   D. O(1)
   Your Answer   : A
   Correct Answer: B
==========================================================
```

### Performance Analytics

```text
============================================================
                   PERFORMANCE ANALYTICS
============================================================
Total Quizzes Played : 6
Total Correct Answers: 71/90
Average Percentage   : 79.83%
Best Category        : Programming
Highest Score        : 93.33%
Highest Badge        : ⭐ Pro Player
============================================================
```

### Category-Wise Progress

```text
======================================================================
                     CATEGORY-WISE PROGRESS
======================================================================
Category                 Quizzes     Score          Avg Score %
======================================================================
Programming               3           38/45          84.44%
Science                   2           22/30          73.33%
General Knowledge         1           11/15          73.33%
======================================================================
```

### Global Leaderboard

```text
======================================================================
                 GLOBAL LEADERBOARD (TOP SCORERS)
======================================================================
Rank    Username                 Best Percentage     Badge
======================================================================
1       osaid                    93.33%              ⭐ Pro Player
2       hamza                    86.67%              ⭐ Pro Player
3       fatima                   80.00%              ⭐ Pro Player
======================================================================
```

### Admin Menu

```text
=============== ADMIN MENU ===============
1. Add Questions
2. Edit Questions
3. View All Questions
4. Delete Questions
5. View All Users Quiz History
6. View All Users Profile
7. Reset History
8. Add New Category
0. Logout
```

### Admin: Add New Category

```text
--------------- Add New Category ---------------
Enter New Category Name: Finance
Category 'Finance' created and saved successfully!
```

### Admin: Add Question

```text
---------------- Add Questions ----------------

Existing Categories:
1. General Knowledge
2. Science
3. Programming
4. Finance
5. Add New Category
Select Category Number: 4

----------- Select Difficulty Level -----------
1. Easy | 2. Medium | 3. Hard
Select Level (1-3): 1

Enter Question: What does ROI stand for?
Enter Option A: Return On Investment
Enter Option B: Rate Of Interest
Enter Option C: Revenue Over Income
Enter Option D: Ratio Of Investment
Enter Correct Answer [A/B/C/D]: A

Question Added Successfully!
```

---

## Concepts Covered

* **Object-Oriented Programming (OOP):** Class design (`Question`, `QuizManager`, `QuizUI`), with strict `from_dict()` validation that rejects malformed records instead of crashing.
* **CRUD Operations:** Full question lifecycle (add, edit, view, delete), plus category and user management.
* **JSON Data Serialization:** Four independent persistent stores (questions, categories, users, history), each validated on load.
* **Security:** SHA-256 password hashing, with a login lockout (3 attempts, 10-second cooldown) applied consistently to both Admin and User logins.
* **Randomization:** `random.sample()` for fair question selection from the full pool, and `random.shuffle()` for per-question option ordering, with careful tracking of which shuffled letter is now correct.
* **Cross-Platform I/O:** A custom timed-input function using `msvcrt` on Windows and `select` on Unix-like systems, so the timer works either way.
* **Data Aggregation:** Performance analytics, category-wise progress, and a leaderboard all computed by aggregating quiz history records per user.
* **Modules & Packages:** Code organized into a `src/` package (`models.py`, `manager.py`, `UI.py`), separating data, persistence, and presentation/business logic, with `main.py` as the entry point outside the package.
* **Defensive Programming:** Input validation and exception handling across all menus, plus resilient JSON loading that degrades gracefully instead of crashing on bad data.

---

## How Random Question Selection Works

* When a category and level are chosen, every matching question in the pool is collected first.
* `random.sample()` then picks up to 20 of them at random — so two attempts at the same category/level can present a different set of questions, not just a different order of the same first 20.
* Within that selected set, both the question order (`random.shuffle`) and each question's option order are further randomized, with the correct answer's new shuffled letter tracked correctly.

## How Categories Are Persisted

* Categories live in their own `categories.json`, independent of the question bank.
* Adding a category via the Admin Menu immediately saves it — it will still exist even if no question has been added to it yet, and survives an app restart.
* On load, any category referenced by an existing question that isn't already in the category list is automatically added, so the two stay in sync.

---

## Future Improvements

* Negative marking option (currently explicitly "No negative marking")
* Difficulty-based scoring (harder questions worth more)
* Category and question bank import/export (e.g. from CSV)
* Admin ability to delete or rename categories
* SQLite integration replacing JSON persistence
* Graphical User Interface (Tkinter)

---

## Learning Outcomes

This project helped me practice and solidify key software engineering concepts:

* **Getting randomization genuinely right:** Fixing a real bug where question selection always used the same first 20 questions instead of a fair random sample — a good lesson in testing what a feature actually does, not just whether it runs without errors.
* **Designing for data integrity:** Building strict `from_dict()` validation and `required_keys` checks so that corrupted or malformed JSON records are dropped safely instead of crashing the whole application.
* **Consistent security patterns:** Applying the same login-lockout logic to both Admin and User authentication, rather than only protecting one.
* **Cross-platform considerations:** Writing timed input that works differently under the hood on Windows versus Unix-like systems, while presenting the same behavior to the user.
* **Modular project structure:** Splitting a feature-rich single-file project into a `models` / `manager` / `UI` / `main` package as its scope grew from a simple quiz to a full account-and-analytics system.

---

## Author

**Muhammad Abdullah Farooq**

GitHub: [https://github.com/osaid400](https://github.com/osaid400)