# Quiz Application
# Author: Muhammad Abdullah Farooq
# Language: Python

import json
import sys
from datetime import datetime


class Question:
    def __init__(self, level, question, options, answer):
        self.level = level
        self.question = question
        self.options = options
        self.answer = answer

    def to_dict(self):
        return {
            "Level": self.level,
            "Question": self.question,
            "Options": self.options,
            "Answer": self.answer,
        }

    @classmethod
    def from_dict(cls, question_data):
        return cls(
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
        self.score = 0

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

    def select_level(self):
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

        # Filter questions matching the selected level
        self.selected_questions = [
            q for q in self.questions if q.level.lower() == self.selected_level.lower()
        ]

        if not self.selected_questions:
            print(f"No questions found for '{self.selected_level}' level in {self.questions_file}.")
            return False

        return True

    def quiz_game_instruction(self):
        print("\n================= INSTRUCTIONS =================")
        print(f"- Total Questions Loaded: {len(self.questions)}")
        print("- Each question carries one mark.")
        print("- Enter only A, B, C, or D.")
        print("- No negative marking.")
        print("==================================================")

    def start_quiz(self):
        if not self.select_level():
            return

        while True:
            self.score = 0
            total_q = len(self.selected_questions)

            print("---------------------------------------------------")
            print(f"Selected Level: {self.selected_level}")
            print(f"Number of Questions: {total_q}")
            print("The quiz will begin now.")
            print("---------------------------------------------------")

            for i, question in enumerate(self.selected_questions, start=1):
                print(f"\nQuestion {i}/{total_q}")
                self.show_question(question)
                self.check_answer(question)
                print("---------------------------------------------------")

            self.show_result()

            # Record and save history
            self.history.append({
                "Level": self.selected_level,
                "Score": self.score,
                "Total": total_q,
                "Date": datetime.now().strftime("%d-%m-%Y %H:%M")
            })
            self.save_history()

            # Prompt replay
            while True:
                replay = input("Do you want to play again? (Yes/No): ").strip().lower()
                if replay in ["yes", "y"]:
                    if not self.select_level():
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
            answer = input("Enter Answer (A/B/C/D): ").strip().upper()
            if answer in ["A", "B", "C", "D"]:
                break
            print("Invalid option! Choose A, B, C, or D.")

        if answer == question.answer.strip().upper():
            print("Correct Answer!")
            self.score += 1
        else:
            print(f"Wrong Answer! The correct answer was: {question.answer}")

    def show_result(self):
        total = len(self.selected_questions)
        print("\n================ QUIZ RESULT ================")
        if total == 0:
            print("No questions were answered.")
            return

        print(f"Correct Answers: {self.score}")
        print(f"Wrong Answers: {total - self.score}")
        print(f"Your final score is: {self.score}/{total}")

        percentage = (self.score / total) * 100
        print(f"Percentage: {percentage:.2f}%")

        if percentage >= 90:
            print("Status: EXCELLENT!")
        elif percentage >= 80:
            print("Status: VERY GOOD!")
        elif percentage >= 70:
            print("Status: GOOD!")
        elif percentage >= 60:
            print("Status: AVERAGE!")
        elif percentage >= 50:
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

        print("\n" + "=" * 60)
        print(f"{'SCORE HISTORY':^60}")
        print("=" * 60)
        print(f"{'Date & Time':<22} {'Level':<18} {'Score':<15}")
        print("=" * 60)
        for record in self.history:
            score_str = f"{record['Score']}/{record['Total']}"
            print(f"{record['Date']:<22} {record['Level']:<18} {score_str:<15}")
        print("=" * 60)

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
        print("4. Restart Quiz")
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
        elif choice == 4:
            manager.restart_quiz()
        elif choice == 0:
            manager.exit_system()
        else:
            print("Invalid Choice! Choose between 0 to 4")


if __name__ == "__main__":
    main()