

import json
import random
import sys
import hashlib
from datetime import datetime

class Question:
    def __init__(self, category, level, question, options, answer):
        self.category = category
        self.level = level
        self.question = question
        self.options = options
        self.answer = answer

    @classmethod
    def from_dict(cls, data):
        required_keys = ["Category", "Level", "Question", "Options", "Answer"]
        if not all(key in data for key in required_keys):
            return None

        if not isinstance(data["Options"], list) or len(data["Options"]) != 4:
            return None

        if data["Answer"].upper() not in ["A", "B", "C", "D"]:
            return None

        return cls(
            category=data["Category"],
            level=data["Level"],
            question=data["Question"],
            options=data["Options"],
            answer=data["Answer"].upper()
        )
    
    def to_dict(self):
        return {
            "Category": self.category,
            "Level": self.level,
            "Question": self.question,
            "Options": self.options,
            "Answer": self.answer
        }

class QuizManager:
    def __init__(self, questions_file="questions.json", history_file="quiz_history.json", users_file="users.json"):
        self.questions_file = questions_file
        self.history_file = history_file
        self.users_file = users_file 

        self.questions = []
        self.selected_questions = []
        self.history = []
        self.users = [] 

        self.selected_level = ""
        self.selected_category = None
        self.score = 0
        self.percentage = 0.0
        self.quiz_stopped = False
        self.current_user = None

        self.load_questions()
        self.load_history()
        self.load_users() 

    def load_questions(self):
        try:
            with open(self.questions_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            loaded_questions = [Question.from_dict(q) for q in data]
            self.questions = [q for q in loaded_questions if q is not None]
        except (FileNotFoundError, json.JSONDecodeError):
            self.questions = []

    def save_questions(self):
        with open(self.questions_file, "w", encoding="utf-8") as f:
            json.dump([q.to_dict() for q in self.questions], f, indent=4, ensure_ascii=False)

    def load_history(self):
        try:
            with open(self.history_file, "r", encoding="utf-8") as file:
                self.history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []
        return self.history

    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as file:
            json.dump(self.history, file, indent=4)

    def load_users(self):
        try:
            with open(self.users_file, "r", encoding="utf-8") as file:
                self.users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = [{
                "id": 0, 
                "username": "admin", 
                "password": hashlib.sha256("0000".encode()).hexdigest(),
                "role": "Admin", 
                "age": 30, 
                "phone": "0312-3456789"
            }]
            self.save_users()

    def save_users(self):
        with open(self.users_file, "w", encoding="utf-8") as file:
            json.dump(self.users, file, indent=4)

    def add_questions(self):
        print("\n---------------- Add Questions ----------------")
        categories = sorted(set(q.category for q in self.questions))
        if categories:
            print("\nExisting Categories:")
            for idx, cat in enumerate(categories, start=1):
                print(f"{idx}. {cat}")
            print(f"{len(categories)+1}. Add New Category")

        try:
            cat_choice = int(input("Select Category Number: "))
        except ValueError:
            print("Invalid Input!")
            return

        if cat_choice == len(categories) + 1:
            category = input("Enter New Category Name: ").strip()
        elif 1 <= cat_choice <= len(categories):
            category = categories[cat_choice - 1]
        else:
            print("Invalid Choice!")
            return

        if not category:
            print("Error: Category cannot be empty!")
            return

        print("\n----------- Select Difficulty Level -----------")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
    
        try:
            level_choice = int(input("Select Level: "))
        except ValueError:
            print("Invalid Input!")
            return
    
        if level_choice == 1: level = "Easy"
        elif level_choice == 2: level = "Medium"
        elif level_choice == 3: level = "Hard"
        else:
            print("Invalid Choice!")
            return

        question_text = input("\nEnter Question: ").strip()
        if not question_text:
            print("Error: Question cannot be empty!")
            return

        if any(q.question.strip().lower() == question_text.lower() for q in self.questions):
            print("Error: Duplicate question already exists!")
            return

        options = []
        for i in ['A','B','C','D']:
            opt = input(f"Enter Option {i}: ").strip()
            if not opt: 
                print("Error: All 4 options are required! Question not added.")
                return
            options.append(f"{i}. {opt}")
    
        answer = input("Enter Correct Answer [A/B/C/D]: ").strip().upper()
        if answer not in ["A", "B", "C", "D"]:
            print("Error: Answer must be A, B, C or D!")
            return

        new_q = Question(category, level, question_text, options, answer)
        self.questions.append(new_q)
        self.save_questions() 
        print("\nQuestion Added Successfully!")

    def edit_questions(self):
        print("\n---------------- Edit Question ----------------")
        if not self.questions:
            print("No questions available to edit.")
            return

        self.view_all_questions()
        try:
            q_num = int(input("\nEnter Question Number to Edit: "))
            if not (1 <= q_num <= len(self.questions)):
                print("Invalid Question Number!")
                return
        except ValueError:
            print("Invalid Input! Please enter a number.")
            return

        target_q = self.questions[q_num - 1]
        print(f"\nEditing Question #{q_num}: {target_q.question}")

        new_q_text = input("Enter New Question Text (Press Enter to keep current): ").strip()
        if new_q_text:
            target_q.question = new_q_text

        print("\nUpdate Options (Press Enter to keep current):")
        new_options = []
        for idx, opt_label in enumerate(['A', 'B', 'C', 'D']):
            curr_opt = target_q.options[idx]
            user_opt = input(f"Option {opt_label} [{curr_opt}]: ").strip()
            if user_opt:
                new_options.append(f"{opt_label}. {user_opt}")
            else:
                new_options.append(curr_opt)
        target_q.options = new_options

        new_ans = input(f"Enter New Correct Answer [A/B/C/D] [{target_q.answer}]: ").strip().upper()
        if new_ans in ["A", "B", "C", "D"]:
            target_q.answer = new_ans

        self.save_questions()
        print("\nQuestion Updated Successfully!")

    def delete_questions(self):
        print("\n--------------- Delete Question ---------------")
        if not self.questions:
            print("No questions available to delete.")
            return

        self.view_all_questions()
        try:
            q_num = int(input("\nEnter Question Number to Delete: "))
            if not (1 <= q_num <= len(self.questions)):
                print("Invalid Question Number!")
                return
        except ValueError:
            print("Invalid Input! Please enter a number.")
            return

        deleted_q = self.questions.pop(q_num - 1)
        self.save_questions()
        print(f"\nQuestion '{deleted_q.question}' Deleted Successfully!")

    def view_all_questions(self):
        print("\n----------- View All Questions Category Wise -----------")
        if not self.questions: 
            print("=============================")
            print("       No Questions Found    ")
            print("=============================")
            return
        
        categories = sorted(set(q.category for q in self.questions))
        count = 1
        for cat in categories:
            print(f"\n{'='*20} Category: {cat} {'='*20}")
            cat_questions = [q for q in self.questions if q.category == cat]
            for q in cat_questions:
                print(f"\n{count}. {q.question}  [{q.level}]")
                for opt in q.options: 
                    print(f"   {opt}")
                print(f"   Ans: {q.answer}")
                count += 1
        print(f"\nTotal Questions: {len(self.questions)}")

    def view_all_users_profile(self):
        print("\n" + "=" * 80)
        print(f"{'ALL USERS PROFILE':^80}")
        print("=" * 80)
        if not self.users:
            print("No users registered.")
            print("=" * 80)
            return

        print(
            f"{'ID':<6}"
            f"{'Username':<20}"
            f"{'Role':<12}"
            f"{'Age':<10}"
            f"{'Phone':<20}"
        )
        print("=" * 80)
        for u in self.users:
            print(
                f"{u['id']:<6}"
                f"{u['username']:<20}"
                f"{u['role']:<12}"
                f"{u['age']:<10}"
                f"{u['phone']:<20}"
            )
        print("=" * 80)

    def view_all_users_history(self):
        self.load_history()
        print("\n" + "=" * 95)
        print(f"{'ALL USERS QUIZ HISTORY':^95}")
        print("=" * 95)
        if not self.history:
            print("No history found.")
            print("=" * 95)
            return

        print(
            f"{'Date and Time':<20}"
            f"{'User':<15}"
            f"{'Category':<22}"
            f"{'Level':<10}"
            f"{'Score':<10}"
            f"{'Percentage':<12}"
        )
        print("=" * 95)
        for record in self.history:
            score = f"{record['Score']}/{record['Total']}"
            pct_str = f"{record['Percentage']:.2f}%"
            user_name = record.get("User", "Guest")
            print(
                f"{record['Date and Time']:<20}"
                f"{user_name:<15}"
                f"{record['Category']:<22}"
                f"{record['Level']:<10}"
                f"{score:<10}"
                f"{pct_str:<12}"
            )
        print("=" * 95)

    def reset_history(self):
        print("\n---------------- Reset History ----------------")
        confirm = input("Are you sure you want to clear all history? (Yes/No): ").strip().lower()
        if confirm in ["yes", "y"]:
            self.history = []
            self.save_history()
            print("Quiz History cleared successfully!")
        else:
            print("Reset operation cancelled.")

    def add_new_category(self):
        print("\n--------------- Add New Category ---------------")
        new_cat = input("Enter New Category Name: ").strip()
        if not new_cat:
            print("Error: Category name cannot be empty!")
            return

        categories = set(q.category for q in self.questions)
        if new_cat.lower() in [c.lower() for c in categories]:
            print("Category already exists!")
            return

        print(f"Category '{new_cat}' created and available for questions.")

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

        self.selected_questions = [
            q for q in self.questions
            if q.category == self.selected_category and q.level.strip().lower() == self.selected_level.strip().lower()
        ]

        self.selected_questions = self.selected_questions[:20]

        if not self.selected_questions:
            print(f"No questions found for '{self.selected_level}' level in category '{self.selected_category}'.")
            return False

        return True

    def quiz_game_instruction(self):
        print("\n================= INSTRUCTIONS =================")
        print("- Welcome to the Quiz Application!")
        print("- There are various categories of questions available.")
        print("- You can select a category and difficulty level to start the quiz.")
        print("- Each category has up to 20 questions for each level (Easy, Medium, Hard).")
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

            random.shuffle(self.selected_questions)  

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

            user_name = self.current_user if self.current_user else "Guest"
            self.history.append({
                "User": user_name,  
                "Category": self.selected_category,
                "Level": self.selected_level,
                "Score": self.score,
                "Total": total_q,
                "Percentage": round(self.percentage, 2),
                "Date and Time": datetime.now().strftime("%d-%m-%Y %H:%M")
            })
            self.save_history()

            if self.quiz_stopped:
                print("You quit the quiz. Returning to the main menu.")
                return

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
        self.percentage = (self.score / total) * 100 if total > 0 else 0.0

        print("\n================ QUIZ RESULT ================")

        if total == 0:
            print("No questions were answered.")
            return

        print(f"Your Category    : {self.selected_category}")
        print(f"Your Level       : {self.selected_level}")
        print(f"Correct Answers  : {self.score}")
        print(f"Wrong Answers    : {total - self.score}")
        print(f"Final Score      : {self.score}/{total}")

        if self.quiz_stopped:
            print(f"Attempted        : {total}")
            print("Status: QUIT EARLY")
        else:
            print(f"Percentage       : {self.percentage:.2f}%")
            if self.percentage >= 90:
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
        user_history = [
            r for r in self.history 
            if r.get("User") == self.current_user or self.current_user is None
        ]

        if not user_history:
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

        for record in user_history:
            score = f"{record['Score']}/{record['Total']}"
            pct_str = f"{record['Percentage']:.2f}%"

            print(
                f"{record['Date and Time']:<20}"
                f"{record['Category']:<25}"
                f"{record['Level']:<12}"
                f"{score:<10}"
                f"{pct_str:<12}"        
            )

        print("=" * 80)

    def admin_menu(self):
        while True:
            print("\n=============== ADMIN MENU ===============")
            print("1. Add Questions")
            print("2. Edit Questions")
            print("3. View All Questions")
            print("4. Delete Questions")
            print("5. View All Users Quiz History")
            print("6. View All Users Profile")
            print("7. Reset History")
            print("8. Add New Category")
            print("0. Logout")

            try:
                choice = int(input("Enter choice: "))
            except ValueError:
                print("Invalid Choice! Please enter a number.")
                continue

            if choice == 1:
                self.add_questions()
            elif choice == 2:
                self.edit_questions()
            elif choice == 3:
                self.view_all_questions()
            elif choice == 4:
                self.delete_questions()
            elif choice == 5:
                self.view_all_users_history()
            elif choice == 6:
                self.view_all_users_profile()
            elif choice == 7:
                self.reset_history()
            elif choice == 8:
                self.add_new_category()
            elif choice == 0:
                print("Logging out...")
                self.current_user = None
                return
            else:
                print("Invalid Choice! Choose between 0 to 8")

    def admin_login(self):
        print("\n=================== Admin Login ===================")
        username = input("Admin Username: ").strip()
        password = input("Admin Password: ").strip()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        for user in self.users:
            if user["username"].lower() == username.lower() and user["password"] == hashed_password and user["role"] == "Admin":
                print(f"\nWelcome {user['username']}!")
                self.current_user = user["username"]
                self.admin_menu()
                return
    
        print("Invalid Admin Credentials!")

    def user_menu(self):
        while True:
            self.load_history()
            user_recs = [r for r in self.history if r.get("User") == self.current_user]
            
            print("\n=============== USER MENU ===============")
            if user_recs:
                last = user_recs[-1]
                print(f"Logged in as: {self.current_user} | Last Score: {last['Score']}/{last['Total']} ({last['Percentage']}%)")
            else:
                print(f"Logged in as: {self.current_user}")
            print("1. Start New Quiz")
            print("2. Game Instructions")
            print("3. View Score History")
            print("0. Logout")

            try:
                choice = int(input("Enter choice: "))
            except ValueError:
                print("Invalid Choice! Please enter a number.")
                continue

            if choice == 1:
                self.start_quiz()
            elif choice == 2:
                self.quiz_game_instruction()
            elif choice == 3:
                self.view_history()
            elif choice == 0:
                print("Logging out...")
                self.current_user = None
                return
            else:
                print("Invalid Choice! Choose between 0 to 3")

    def register_user(self):
        print("\n=============== New User Registration ===============")
        username = input("Choose Username: ").strip()
        if not username:
            print("Error: Username cannot be empty!")
            return
        if any(u["username"].lower() == username.lower() for u in self.users):
            print("Error: Username already exists!")
            return
    
        password = input("Choose Password: ").strip()
        if len(password) < 4:
            print("Error: Password must be at least 4 characters long!")
            return
        hashed_password = hashlib.sha256(password.encode()).hexdigest() 

        age = input("Enter Age: ").strip()
        if not age.isdigit():
            print("Error: Age must be a whole number!")
            return
        age = int(age)
        if age <= 0:
            print("Error: Age must be greater than 0!")
            return

        phone = input("Enter Phone Number: ").strip()
        if not phone.isdigit():
            print("Error: Phone number must contain only digits!")
            return
        if len(phone) != 11:
            print("Error: Phone number must be exactly 11 digits!")
            return

        new_id = max([u["id"] for u in self.users], default=0) + 1

        new_user = {
            "id": new_id,
            "username": username,
            "password": hashed_password, 
            "role": "User",
            "age": age,
            "phone": phone
        }
    
        self.users.append(new_user)
        self.save_users()
        print(f"Registration Successful! Your User ID is: {new_id}")

    def user_login(self):
        print("\n================== User Login ==================")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        for user in self.users:
            if user["username"].lower() == username.lower() and user["password"] == hashed_password and user["role"] == "User":
                print(f"\nWelcome {user['username']}!")
                self.current_user = user["username"]
                self.user_menu()
                return
    
        print("Invalid Username or Password!")

def main():
    print("============ Welcome to Quiz Application =============")
    manager = QuizManager()

    while True:
        print("\n=============== MAIN MENU ===============")
        print("1. Admin Login")
        print("2. User Login")
        print("3. New User Registration")
        print("0. Exit")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid Choice! Please enter a number.")
            continue

        if choice == 1:
            manager.admin_login()
        elif choice == 2:
            manager.user_login()
        elif choice == 3:
            manager.register_user()
        elif choice == 0:
            print("=========================================")
            print("THANKS FOR USING QUIZ APPLICATION!")
            print("=========================================")
            sys.exit()
        else:
            print("Invalid Choice! Choose between 0 to 3")

if __name__ == "__main__":
    main()