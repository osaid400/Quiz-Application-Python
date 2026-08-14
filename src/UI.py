# src/UI.py

import sys
import time
import select
import hashlib
import random

class QuizUI:
    def __init__(self, manager):
        self.manager = manager

    def timed_input(self, prompt, timeout=15):
        print(prompt, end="", flush=True)
        if sys.platform == "win32":
            import msvcrt
            start_time = time.time()
            input_chars = []
            while True:
                if msvcrt.kbhit():
                    char = msvcrt.getwche()
                    if char in ['\r', '\n']:
                        print()
                        return ''.join(input_chars)
                    elif char == '\b':
                        if input_chars:
                            input_chars.pop()
                            sys.stdout.write('\b \b')
                            sys.stdout.flush()
                    else:
                        input_chars.append(char)
                if time.time() - start_time > timeout:
                    print("\n\n⏰ Time's Up!")
                    return None
                time.sleep(0.05)
        else:
            ready, _, _ = select.select([sys.stdin], [], [], timeout)
            if ready:
                return sys.stdin.readline().rstrip('\r\n')
            else:
                print("\n\n⏰ Time's Up!")
                return None

    def main_menu(self):
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
                self.admin_login()
            elif choice == 2:
                self.user_login()
            elif choice == 3:
                self.register_user()
            elif choice == 0:
                print("=========================================")
                print("THANKS FOR USING QUIZ APPLICATION!")
                print("=========================================")
                sys.exit()
            else:
                print("Invalid Choice! Choose between 0 to 3")

    def admin_login(self):
        print("\n=================== Admin Login ===================")
        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            username = input("Admin Username: ").strip()
            password = input("Admin Password: ").strip()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            for user in self.manager.users:
                if (user.get("username", "").lower() == username.lower() and 
                    user.get("password") == hashed_password and 
                    user.get("role") == "Admin"):
                    print(f"\nWelcome {user['username']}!")
                    self.manager.current_user = user["username"]
                    self.admin_menu()
                    return
            
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"Invalid Admin Credentials! ({remaining} attempt(s) remaining)\n")
            else:
                print("Too many failed attempts! Account temporarily locked for 10 seconds.")
                time.sleep(10)

    def user_login(self):
        print("\n================== User Login ==================")
        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            for user in self.manager.users:
                if (user.get("username", "").lower() == username.lower() and 
                    user.get("password") == hashed_password and 
                    user.get("role") == "User"):
                    print(f"\nWelcome {user['username']}!")
                    self.manager.current_user = user["username"]
                    self.user_menu()
                    return

            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"Invalid Username or Password! ({remaining} attempt(s) remaining)\n")
            else:
                print("Too many failed attempts! Cooldown active for 10 seconds.")
                time.sleep(10)

    def register_user(self):
        print("\n=============== New User Registration ===============")
        username = input("Choose Username: ").strip()
        if not username:
            print("Error: Username cannot be empty!")
            return
        if any(u.get("username", "").lower() == username.lower() for u in self.manager.users):
            print("Error: Username already exists!")
            return
    
        password = input("Choose Password: ").strip()
        if len(password) < 4:
            print("Error: Password must be at least 4 characters long!")
            return
        hashed_password = hashlib.sha256(password.encode()).hexdigest() 

        age = input("Enter Age: ").strip()
        if not age.isdigit() or int(age) <= 0:
            print("Error: Invalid Age!")
            return

        phone = input("Enter Phone Number (11 digits): ").strip()
        if not phone.isdigit() or len(phone) != 11:
            print("Error: Invalid Phone number!")
            return

        new_id = max([u.get("id", 0) for u in self.manager.users], default=0) + 1
        new_user = {
            "id": new_id,
            "username": username,
            "password": hashed_password, 
            "role": "User",
            "age": int(age),
            "phone": phone
        }
        self.manager.users.append(new_user)
        self.manager.save_users()
        print(f"Registration Successful! Your User ID is: {new_id}")

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
                print("Invalid Choice!")
                continue

            if choice == 1: self.add_questions_ui()
            elif choice == 2: self.edit_questions_ui()
            elif choice == 3: self.view_all_questions_ui()
            elif choice == 4: self.delete_questions_ui()
            elif choice == 5: self.view_all_users_history_ui()
            elif choice == 6: self.view_all_users_profile_ui()
            elif choice == 7: self.reset_history_ui()
            elif choice == 8: self.add_new_category_ui()
            elif choice == 0:
                print("Logging out...")
                self.manager.current_user = None
                return
            else:
                print("Invalid Choice! Choose between 0 to 8")

    def user_menu(self):
        while True:
            self.manager.load_history()
            user_recs = [r for r in self.manager.history if r.get("User") == self.manager.current_user]
            
            print("\n=============== USER MENU ===============")
            if user_recs:
                last = user_recs[-1]
                print(f"Logged in as: {self.manager.current_user} | Last Score: {last['Score']}/{last['Total']} ({last['Percentage']}%)")
            else:
                print(f"Logged in as: {self.manager.current_user}")
                
            print("1. Start New Quiz")
            print("2. Review Incorrect Answers (Last Quiz)")
            print("3. View Score History")
            print("4. Performance Analytics")
            print("5. Category-Wise Progress")
            print("6. Global Leaderboard")
            print("7. View My Profile")
            print("8. Update Profile / Password")
            print("9. Game Instructions")
            print("0. Logout")

            try:
                choice = int(input("Enter choice: "))
            except ValueError:
                print("Invalid Choice!")
                continue

            if choice == 1: self.start_quiz_ui()
            elif choice == 2: self.review_incorrect_answers_ui()
            elif choice == 3: self.view_history_ui()
            elif choice == 4: self.view_performance_analytics_ui()
            elif choice == 5: self.view_category_progress_ui()
            elif choice == 6: self.view_leaderboard_ui()
            elif choice == 7: self.view_my_profile_ui()
            elif choice == 8: self.update_profile_ui()
            elif choice == 9: self.quiz_game_instruction_ui()
            elif choice == 0:
                print("Logging out...")
                self.manager.current_user = None
                return
            else:
                print("Invalid Choice! Choose between 0 to 9")

    def start_quiz_ui(self):
        if not self.select_category_ui() or not self.select_level_ui():
            return

        while True:
            self.manager.score = 0
            self.manager.quiz_stopped = False
            self.manager.last_incorrect_answers = []
            total_q = len(self.manager.selected_questions)

            random.shuffle(self.manager.selected_questions)  

            print("---------------------------------------------------")
            print(f"Selected Category: {self.manager.selected_category}")
            print(f"Selected Level: {self.manager.selected_level}")
            print(f"Number of Questions: {total_q}")
            print("Timer: 15 Seconds per question!")
            print("---------------------------------------------------")

            for i, question in enumerate(self.manager.selected_questions, start=1):
                print(f"\nQuestion {i}/{total_q}")
                
                raw_texts = [opt.split(". ", 1)[1] if ". " in opt else opt for opt in question.options]
                correct_idx = ["A", "B", "C", "D"].index(question.answer)
                correct_text = raw_texts[correct_idx]

                random.shuffle(raw_texts)

                labels = ["A", "B", "C", "D"]
                shuffled_options = [f"{labels[idx]}. {txt}" for idx, txt in enumerate(raw_texts)]
                new_correct_label = labels[raw_texts.index(correct_text)]

                print(question.question)
                for opt in shuffled_options:
                    print(opt)

                if not self.check_answer_ui(question, shuffled_options, new_correct_label):
                    break
                print("---------------------------------------------------")

            self.show_result_ui()  
            self.manager.record_quiz_history(total_q)

            if self.manager.quiz_stopped:
                print("You quit the quiz. Returning to main menu.")
                return

            replay = input("Do you want to play again? (Yes/No): ").strip().lower()
            if replay not in ["yes", "y"]:
                return

    def check_answer_ui(self, question, shuffled_options, correct_label):
        while True:
            user_input = self.timed_input("Enter Answer (A/B/C/D) or Q to Quit [15s]: ", 15)
            
            if user_input is None:
                print(f"Correct answer was: {correct_label}")
                self.manager.last_incorrect_answers.append({
                    "Question": question.question,
                    "Options": shuffled_options,
                    "Correct": correct_label,
                    "User": "Time Out"
                })
                return True

            answer = user_input.strip().upper()
            if answer in ["Q", "QUIT"]:
                self.manager.quiz_stopped = True
                return False
            if answer in ["A", "B", "C", "D"]:
                break
            print("Invalid option! Choose A, B, C, or D.")

        if answer == correct_label:
            print("Correct Answer!")
            self.manager.score += 1
        else:
            print(f"Wrong Answer! Correct answer was: {correct_label}")
            self.manager.last_incorrect_answers.append({
                "Question": question.question,
                "Options": shuffled_options,
                "Correct": correct_label,
                "User": answer
            })

        return True

    def show_result_ui(self):
        total = len(self.manager.selected_questions)
        self.manager.percentage = (self.manager.score / total) * 100 if total > 0 else 0.0

        print("\n================ QUIZ RESULT ================")
        if total == 0:
            print("No questions were answered.")
            return

        print(f"Your Category    : {self.manager.selected_category}")
        print(f"Your Level       : {self.manager.selected_level}")
        print(f"Correct Answers  : {self.manager.score}")
        print(f"Wrong Answers    : {total - self.manager.score}")
        print(f"Final Score      : {self.manager.score}/{total}")

        if self.manager.quiz_stopped:
            print(f"Attempted        : {total}")
            print("Status: QUIT EARLY")
        else:
            print(f"Percentage       : {self.manager.percentage:.2f}%")
            if self.manager.percentage >= 90:
                print("Status: EXCELLENT! (Badge: 🏆 Quiz Master)")
            elif self.manager.percentage >= 80:
                print("Status: VERY GOOD! (Badge: ⭐ Pro Player)")
            elif self.manager.percentage >= 70:
                print("Status: GOOD! (Badge: 🎖️ Scholar)")
            elif self.manager.percentage >= 60:
                print("Status: AVERAGE! (Badge: 📘 Learner)")
            elif self.manager.percentage >= 50:
                print("Status: PASS! (Badge: 🔰 Beginner)")
            else:
                print("Status: FAIL!\nBetter Luck Next Time")

        print("---------------------------------------------------")

    def select_category_ui(self):
        categories = sorted(self.manager.categories)
        if not categories:
            print("No categories available.")
            return False

        print("\n--- Select Category ---")
        for idx, category in enumerate(categories, start=1):
            print(f"{idx}. {category}")

        try:
            choice = int(input("Select Category Number: "))
            if 1 <= choice <= len(categories):
                self.manager.selected_category = categories[choice - 1]
                return True
        except ValueError:
            pass
        print("Invalid Choice! Please select a valid category number.")
        return False

    def select_level_ui(self):
        print("\n--- Select Level ---")
        print("1. Easy | 2. Medium | 3. Hard")
        choice = input("Select Level (1-3): ").strip()
        levels = {"1": "Easy", "2": "Medium", "3": "Hard"}
        
        if choice in levels:
            self.manager.selected_level = levels[choice]
            matching_questions = [
                q for q in self.manager.questions
                if q.category == self.manager.selected_category and q.level.strip().lower() == self.manager.selected_level.lower()
            ]
            
            if matching_questions:
                # FIX: Random sampling over the entire Pool instead of hardcoded [:20]
                sample_size = min(20, len(matching_questions))
                self.manager.selected_questions = random.sample(matching_questions, sample_size)
                return True
            print(f"No questions found for '{self.manager.selected_level}' level in category '{self.manager.selected_category}'.")
            return False
        print("Invalid Selection!")
        return False

    def add_questions_ui(self):
        print("\n---------------- Add Questions ----------------")
        categories = sorted(self.manager.categories)
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
        print("1. Easy | 2. Medium | 3. Hard")
        level_map = {"1": "Easy", "2": "Medium", "3": "Hard"}
        lvl_choice = input("Select Level (1-3): ").strip()
        if lvl_choice not in level_map:
            print("Invalid Choice!")
            return
        level = level_map[lvl_choice]

        question_text = input("\nEnter Question: ").strip()
        if not question_text:
            print("Error: Question cannot be empty!")
            return

        if any(q.question.strip().lower() == question_text.lower() for q in self.manager.questions):
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

        self.manager.add_question_obj(category, level, question_text, options, answer)
        print("\nQuestion Added Successfully!")

    def edit_questions_ui(self):
        print("\n---------------- Edit Question ----------------")
        if not self.manager.questions:
            print("No questions available to edit.")
            return

        self.view_all_questions_ui()
        try:
            q_num = int(input("\nEnter Question Number to Edit: "))
            if not (1 <= q_num <= len(self.manager.questions)):
                print("Invalid Question Number!")
                return
        except ValueError:
            print("Invalid Input! Please enter a number.")
            return

        target_q = self.manager.questions[q_num - 1]
        print(f"\nEditing Question #{q_num}: {target_q.question}")

        new_q_text = input("Enter New Question Text (Press Enter to keep current): ").strip()
        
        # FIX: Duplicate question check during edit
        if new_q_text and new_q_text.lower() != target_q.question.lower():
            if any(q.question.strip().lower() == new_q_text.lower() for idx, q in enumerate(self.manager.questions) if idx != (q_num - 1)):
                print("Error: Another question with this exact text already exists! Edit cancelled.")
                return
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

        self.manager.save_questions()
        print("\nQuestion Updated Successfully!")

    def delete_questions_ui(self):
        print("\n--------------- Delete Question ---------------")
        if not self.manager.questions:
            print("No questions available to delete.")
            return

        self.view_all_questions_ui()
        try:
            q_num = int(input("\nEnter Question Number to Delete: "))
            if not (1 <= q_num <= len(self.manager.questions)):
                print("Invalid Question Number!")
                return
        except ValueError:
            print("Invalid Input! Please enter a number.")
            return

        deleted_q = self.manager.delete_question_by_idx(q_num - 1)
        print(f"\nQuestion '{deleted_q.question}' Deleted Successfully!")

    def view_all_questions_ui(self):
        print("\n----------- View All Questions Category Wise -----------")
        if not self.manager.questions: 
            print("=============================")
            print("       No Questions Found    ")
            print("=============================")
            return
        
        categories = sorted(list(set(q.category for q in self.manager.questions)))
        count = 1
        for cat in categories:
            print(f"\n{'='*20} Category: {cat} {'='*20}")
            cat_questions = [q for q in self.manager.questions if q.category == cat]
            for q in cat_questions:
                print(f"\n{count}. {q.question}  [{q.level}]")
                for opt in q.options: 
                    print(f"   {opt}")
                print(f"   Ans: {q.answer}")
                count += 1
        print(f"\nTotal Questions: {len(self.manager.questions)}")

    def view_all_users_profile_ui(self):
        print("\n" + "=" * 80)
        print(f"{'ALL USERS PROFILE':^80}")
        print("=" * 80)
        if not self.manager.users:
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
        for u in self.manager.users:
            print(
                f"{u.get('id', 'N/A'):<6}"
                f"{u.get('username', 'N/A'):<20}"
                f"{u.get('role', 'N/A'):<12}"
                f"{u.get('age', 'N/A'):<10}"
                f"{u.get('phone', 'N/A'):<20}"
            )
        print("=" * 80)

    def view_all_users_history_ui(self):
        self.manager.load_history()
        print("\n" + "=" * 95)
        print(f"{'ALL USERS QUIZ HISTORY':^95}")
        print("=" * 95)
        if not self.manager.history:
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
        for record in self.manager.history:
            score = f"{record.get('Score', 0)}/{record.get('Total', 0)}"
            pct_str = f"{record.get('Percentage', 0.0):.2f}%"
            user_name = record.get("User", "Guest")
            print(
                f"{record.get('Date and Time', 'N/A'):<20}"
                f"{user_name:<15}"
                f"{record.get('Category', 'N/A'):<22}"
                f"{record.get('Level', 'N/A'):<10}"
                f"{score:<10}"
                f"{pct_str:<12}"
            )
        print("=" * 95)

    def reset_history_ui(self):
        print("\n---------------- Reset History ----------------")
        confirm = input("Are you sure you want to clear all history? (Yes/No): ").strip().lower()
        if confirm in ["yes", "y"]:
            self.manager.history = []
            self.manager.save_history()
            print("Quiz History cleared successfully!")
        else:
            print("Reset operation cancelled.")

    def add_new_category_ui(self):
        print("\n--------------- Add New Category ---------------")
        new_cat = input("Enter New Category Name: ").strip()
        if not new_cat:
            print("Error: Category name cannot be empty!")
            return

        if new_cat.lower() in [c.lower() for c in self.manager.categories]:
            print("Category already exists!")
            return

        self.manager.add_category(new_cat)
        print(f"Category '{new_cat}' created and saved successfully!")

    def review_incorrect_answers_ui(self):
        print("\n================ REVIEW INCORRECT ANSWERS ================")
        if not self.manager.last_incorrect_answers:
            print("No incorrect answers to review from your last quiz attempt!")
            print("==========================================================")
            return

        for idx, item in enumerate(self.manager.last_incorrect_answers, start=1):
            print(f"\n{idx}. Question: {item['Question']}")
            for opt in item["Options"]:
                print(f"   {opt}")
            print(f"   Your Answer   : {item['User']}")
            print(f"   Correct Answer: {item['Correct']}")
        print("==========================================================")

    def view_history_ui(self):
        self.manager.load_history()
        user_history = [
            r for r in self.manager.history 
            if r.get("User") == self.manager.current_user or self.manager.current_user is None
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
            score = f"{record.get('Score', 0)}/{record.get('Total', 0)}"
            pct_str = f"{record.get('Percentage', 0.0):.2f}%"

            print(
                f"{record.get('Date and Time', 'N/A'):<20}"
                f"{record.get('Category', 'N/A'):<25}"
                f"{record.get('Level', 'N/A'):<12}"
                f"{score:<10}"
                f"{pct_str:<12}"        
            )
        print("=" * 80)

    def view_performance_analytics_ui(self):
        self.manager.load_history()
        user_recs = [r for r in self.manager.history if r.get("User") == self.manager.current_user]
        
        print("\n" + "=" * 60)
        print(f"{'PERFORMANCE ANALYTICS':^60}")
        print("=" * 60)

        if not user_recs:
            print("No quiz records found to calculate performance.")
            print("=" * 60)
            return

        total_quizzes = len(user_recs)
        total_score = sum(r.get("Score", 0) for r in user_recs)
        total_possible = sum(r.get("Total", 0) for r in user_recs)
        avg_pct = sum(r.get("Percentage", 0.0) for r in user_recs) / total_quizzes

        cats = {}
        for r in user_recs:
            c = r.get("Category", "N/A")
            cats[c] = cats.get(c, 0) + r.get("Score", 0)
        top_cat = max(cats, key=cats.get) if cats else "N/A"

        print(f"Total Quizzes Played : {total_quizzes}")
        print(f"Total Correct Answers: {total_score}/{total_possible}")
        print(f"Average Percentage   : {avg_pct:.2f}%")
        print(f"Best Category        : {top_cat}")

        best_score = max(r.get("Percentage", 0.0) for r in user_recs)
        print(f"Highest Score        : {best_score:.2f}%")
        
        if best_score >= 90: badge = "🏆 Quiz Master"
        elif best_score >= 80: badge = "⭐ Pro Player"
        elif best_score >= 70: badge = "🎖️ Scholar"
        elif best_score >= 60: badge = "📘 Learner"
        elif best_score >= 50: badge = "🔰 Beginner"
        else: badge = "No Badge Unlocked"

        print(f"Highest Badge        : {badge}")
        print("=" * 60)

    def view_category_progress_ui(self):
        self.manager.load_history()
        user_recs = [r for r in self.manager.history if r.get("User") == self.manager.current_user]

        print("\n" + "=" * 70)
        print(f"{'CATEGORY-WISE PROGRESS':^70}")
        print("=" * 70)

        if not user_recs:
            print("No records found.")
            print("=" * 70)
            return

        cat_stats = {}
        for r in user_recs:
            c = r.get("Category", "N/A")
            if c not in cat_stats:
                cat_stats[c] = {"Played": 0, "Score": 0, "Total": 0}
            cat_stats[c]["Played"] += 1
            cat_stats[c]["Score"] += r.get("Score", 0)
            cat_stats[c]["Total"] += r.get("Total", 0)

        print(
            f"{'Category':<25}"
            f"{'Quizzes':<12}"
            f"{'Score':<15}"
            f"{'Avg Score %':<15}"
        )
        print("=" * 70)

        for cat, stat in cat_stats.items():
            pct = (stat["Score"] / stat["Total"]) * 100 if stat["Total"] > 0 else 0
            score_str = f"{stat['Score']}/{stat['Total']}"
            pct_str = f"{pct:.2f}%"
            print(
                f"{cat:<25}"
                f"{stat['Played']:<12}"
                f"{score_str:<15}"
                f"{pct_str:<15}"
            )
        print("=" * 70)

    def view_leaderboard_ui(self):
        self.manager.load_history()
        print("\n" + "=" * 70)
        print(f"{'GLOBAL LEADERBOARD (TOP SCORERS)':^70}")
        print("=" * 70)

        if not self.manager.history:
            print("No history records found.")
            print("=" * 70)
            return

        user_bests = {}
        for r in self.manager.history:
            u = r.get("User", "Guest")
            pct = r.get("Percentage", 0.0)
            if u not in user_bests or pct > user_bests[u]:
                user_bests[u] = pct

        sorted_users = sorted(user_bests.items(), key=lambda x: x[1], reverse=True)[:10]

        print(
            f"{'Rank':<8}"
            f"{'Username':<25}"
            f"{'Best Percentage':<20}"
            f"{'Badge':<15}"
        )
        print("=" * 70)

        for rank, (uname, pct) in enumerate(sorted_users, start=1):
            if pct >= 90: badge = "🏆 Quiz Master"
            elif pct >= 80: badge = "⭐ Pro Player"
            elif pct >= 70: badge = "🎖️ Scholar"
            elif pct >= 60: badge = "📘 Learner"
            elif pct >= 50: badge = "🔰 Beginner"
            else: badge = "Unranked"

            pct_str = f"{pct:.2f}%"
            print(
                f"{rank:<8}"
                f"{uname:<25}"
                f"{pct_str:<20}"
                f"{badge:<15}"
            )
        print("=" * 70)

    def view_my_profile_ui(self):
        print("\n================= MY PROFILE =================")
        user_info = next((u for u in self.manager.users if u.get("username", "").lower() == self.manager.current_user.lower()), None)
        if user_info:
            print(f"User ID   : {user_info.get('id', 'N/A')}")
            print(f"Username  : {user_info.get('username', 'N/A')}")
            print(f"Role      : {user_info.get('role', 'N/A')}")
            print(f"Age       : {user_info.get('age', 'N/A')}")
            print(f"Phone     : {user_info.get('phone', 'N/A')}")
        else:
            print("User profile not found!")
        print("==============================================")

    def update_profile_ui(self):
        print("\n================ UPDATE PROFILE ================")
        user_info = next((u for u in self.manager.users if u.get("username", "").lower() == self.manager.current_user.lower()), None)
        if not user_info:
            print("User profile not found!")
            return

        print("1. Change Password")
        print("2. Update Phone Number")
        print("3. Update Age")
        print("0. Back")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid Choice!")
            return

        if choice == 1:
            curr_pass = input("Enter Current Password: ").strip()
            if hashlib.sha256(curr_pass.encode()).hexdigest() != user_info["password"]:
                print("Incorrect Current Password!")
                return
            new_pass = input("Enter New Password: ").strip()
            if len(new_pass) < 4:
                print("Password must be at least 4 characters!")
                return
            user_info["password"] = hashlib.sha256(new_pass.encode()).hexdigest()
            self.manager.save_users()
            print("Password Updated Successfully!")

        elif choice == 2:
            new_phone = input("Enter New Phone Number (11 digits): ").strip()
            if not new_phone.isdigit() or len(new_phone) != 11:
                print("Invalid Phone Number!")
                return
            user_info["phone"] = new_phone
            self.manager.save_users()
            print("Phone Number Updated Successfully!")

        elif choice == 3:
            new_age = input("Enter New Age: ").strip()
            if not new_age.isdigit() or int(new_age) <= 0:
                print("Invalid Age!")
                return
            user_info["age"] = int(new_age)
            self.manager.save_users()
            print("Age Updated Successfully!")

        elif choice == 0:
            return

    def quiz_game_instruction_ui(self):
        print("\n================= INSTRUCTIONS =================")
        print("- Welcome to the Quiz Application!")
        print("- Select category and difficulty level to start.")
        print("- Each category has up to 20 questions per level.")
        print("- Each question carries 1 mark.")
        print("- You have 15 seconds to answer each question!")
        print("- Enter only A, B, C, or D (or Q to Quit).")
        print("- No negative marking.")
        print("==================================================")