# Quiz Application
# Author: Muhammad Abdullah Farooq
# Language: Python

import json
import sys
from datetime import datetime


class Question:
    def __init__(self, category, level, question, options, answer):
        self.category = category
        self.level = level
        self.question = question
        self.options = options
        self.answer = answer

    def to_dict(self):
        return {
            "Category": self.category,
            "Level": self.level,
            "Question": self.question,
            "Options": self.options,
            "Answer": self.answer,
        }

    @classmethod
    def from_dict(cls, question_data):
        return cls(
            category = question_data.get("Category"),
            level=question_data["Level"],
            question=question_data["Question"],
            options=question_data["Options"],
            answer=question_data["Answer"]
        )


class QuizManager:

    def __init__(self, questions_file="questions.json", history_file="quiz_history.json"):
        self.questions_file = questions_file
        self.history_file = history_file

        self.questions = []
        self.selected_questions = []
        self.history = []

        self.selected_level = ""
        self.selected_category = None
        self.score = 0
        self.quiz_stopped = False

        self.load_questions()
        self.load_history()

    def load_questions(self):
        try:
            with open(self.questions_file, "r") as file:
                data = json.load(file)
                self.questions = [Question.from_dict(q) for q in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.questions = []

    def load_history(self):
        try:
            with open(self.history_file, "r") as file:
                self.history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []
        return self.history

    def save_history(self):
        with open(self.history_file, "w") as file:
            json.dump(self.history, file, indent=4)

    def select_category(self):
        categories = sorted(set(q.category for q in self.questions))
        if not categories:
            print("No categories available in the questions file.")
            return False

        print("\n--- Select Category ---")
        for idx, category in enumerate(categories, start=1):
            print(f"{idx}. {category}")

        try:
            choice_category = int(input("Select Category: "))
            if 1 <= choice_category <= len(categories):
                self.selected_category = list(categories)[choice_category - 1]
                # Filter questions matching the selected category
                self.selected_questions = [
                    q for q in self.questions if q.category == self.selected_category
                ]
                return True
            else:
                print("Invalid Choice! Please select a valid category number.")
                return False
        except ValueError:
            print("Invalid input! Please enter a number corresponding to the category.")
            return False

    def select_level(self):
        if self.selected_category is None:
            print("Please select a category first.")
            return False

        print("\n--- Select Difficulty Level ---")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")

        try:
            choice_level = int(input("Select Level: "))
        except ValueError:
            print("Invalid input! Please enter 1, 2, or 3.")
            return False

        if choice_level == 1:
            self.selected_level = "Easy"
        elif choice_level == 2:
            self.selected_level = "Medium"
        elif choice_level == 3:
            self.selected_level = "Hard"
        else:
            print("Invalid Choice! Please enter 1, 2, or 3.")
            return False

        # Filter questions matching both the selected category and level
        self.selected_questions = [
            q for q in self.questions
            if q.category == self.selected_category and q.level.lower() == self.selected_level.lower()
        ]

        # Keep only the first 20 questions for the selected category/level
        self.selected_questions = self.selected_questions[:20]

        if not self.selected_questions:
            print(f"No questions found for '{self.selected_level}' level in category '{self.selected_category}'.")
            return False

        return True

    def quiz_game_instruction(self):
        print("\n================= INSTRUCTIONS =================")
        print("- Welcome to the Quiz Application!")
        print("- There are 5 categories of questions available.")
        print("- You can select a category and difficulty level to start the quiz.")
        print(f"- Each category has 20 questions for each level (Easy, Medium, Hard).")
        print("- Each question carries one mark.")
        print("- Enter only A, B, C, or D.")
        print("- No negative marking.")
        print("==================================================")

    def start_quiz(self):
        if not self.select_category():
            return

        if not self.select_level():
            return

        while True:
            self.score = 0
            self.quiz_stopped = False
            total_q = len(self.selected_questions)

            print("---------------------------------------------------")
            print(f"Selected Category: {self.selected_category}")
            print(f"Selected Level: {self.selected_level}")
            print(f"Number of Questions: {total_q}")
            print("The quiz will begin now.")
            print("---------------------------------------------------")

            for i, question in enumerate(self.selected_questions, start=1):
                print(f"\nQuestion {i}/{total_q}")
                self.show_question(question)
                if not self.check_answer(question):
                    break
                print("---------------------------------------------------")

            self.show_result()

            # Record and save history
            self.history.append({
                "Category": self.selected_category,
                "Level": self.selected_level,
                "Score": self.score,
                "Total": total_q,
                "Percentage": self.percentage,
                "Date and Time": datetime.now().strftime("%d-%m-%Y %H:%M")
            })
            self.save_history()

            if self.quiz_stopped:
                print("You quit the quiz. Returning to the main menu.")
                return

            # Prompt replay
            while True:
                replay = input("Do you want to play again? (Yes/No): ").strip().lower()
                if replay in ["yes", "y"]:
                    if not self.select_category():
                        return
                    break
                elif replay in ["no", "n"]:
                    return
                else:
                    print("Invalid Input! Please enter Yes or No.")

    def show_question(self, question):
        print(question.question)
        for option in question.options:
            print(option)

    def check_answer(self, question):
        while True:
            answer = input("Enter Answer (A/B/C/D) or Q to Quit: ").strip().upper()
            if answer in ["Q", "QUIT"]:
                print("You chose to quit the quiz.")
                self.quiz_stopped = True
                return False
            if answer in ["A", "B", "C", "D"]:
                break
            print("Invalid option! Choose A, B, C, or D.")

        if answer == question.answer.strip().upper():
            print("Correct Answer!")
            self.score += 1
        else:
            print(f"Wrong Answer! The correct answer was: {question.answer}")

        return True

    def show_result(self):
        total = len(self.selected_questions)

        print("\n================ QUIZ RESULT ================")

        if total == 0:
            print("No questions were answered.")
            return

        self.percentage = (self.score / total) * 100

        print(f"Your Category    : {self.selected_category}")
        print(f"Your Level       : {self.selected_level}")
        print(f"Correct Answers : {self.score}")
        print(f"Wrong Answers   : {total - self.score}")
        print(f"Final Score     : {self.score}/{total}")
        print(f"Percentage      : {self.percentage:.2f}%")

        if self.quiz_stopped:
            print("Status: Quit EARLY")
        elif self.percentage >= 90:
            print("Status: EXCELLENT!")
        elif self.percentage >= 80:
            print("Status: VERY GOOD!")
        elif self.percentage >= 70:
            print("Status: GOOD!")
        elif self.percentage >= 60:
            print("Status: AVERAGE!")
        elif self.percentage >= 50:
            print("Status: PASS!")
        else:
            print("Status: FAIL!\nBetter Luck Next Time")

        print("---------------------------------------------------")

    def view_history(self):
        self.load_history()

        if not self.history:
            print("============================")
            print("No history found.")
            print("============================")
            return

        print("\n" + "=" * 80)
        print(f"{'SCORE HISTORY':^80}")
        print("=" * 80)

        print(
            f"{'Date and Time':<20}"
            f"{'Category':<25}"
            f"{'Level':<12}"
            f"{'Score':<10}"
            f"{'Percentage':<12}"
        )

        print("=" * 80)

        for record in self.history:
            score = f"{record['Score']}/{record['Total']}"

            print(
                f"{record['Date and Time']:<20}"
                f"{record['Category']:<25}"
                f"{record['Level']:<12}"
                f"{score:<10}"
                f"{str(record['Percentage']) + '%':<12}"
            )

        print("=" * 80)

    def restart_quiz(self):
        self.score = 0
        self.start_quiz()

    def exit_system(self):
        print("\n==============================================")
        print("Thank you for using the Quiz Application!")
        print("Good Bye! Have a nice day!")
        print("Exiting the Quiz Application...")
        print("==============================================")
        sys.exit()


def main():
    print("============ Welcome to Quiz Application =============")
    manager = QuizManager()

    while True:
        print("\n=============== Select the Option (0-4) ===============")
        print("1. Start New Quiz")
        print("2. Game Instructions")
        print("3. View Score History")
        print("0. Exit")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid Choice! Please enter a number.")
            continue

        if choice == 1:
            manager.start_quiz()
        elif choice == 2:
            manager.quiz_game_instruction()
        elif choice == 3:
            manager.view_history()
        elif choice == 0:
            manager.exit_system()
        else:
            print("Invalid Choice! Choose between 0 to 3")


if __name__ == "__main__":
    main()