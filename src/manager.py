# src/UI.py

import os
import json
import hashlib
from datetime import datetime
from src.models import Question

class QuizManager:
    def __init__(self, data_dir="data"):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, data_dir)
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)

        self.users_file = os.path.join(self.data_dir, "users.json")
        self.questions_file = os.path.join(self.data_dir, "questions.json")
        self.history_file = os.path.join(self.data_dir, "quiz_history.json")
        self.categories_file = os.path.join(self.data_dir, "categories.json")

        self.users = []
        self.questions = []
        self.history = []
        self.categories = []
        
        self.current_user = None
        self.selected_category = None
        self.selected_level = None
        self.selected_questions = []
        self.score = 0
        self.percentage = 0.0
        self.quiz_stopped = False
        self.last_incorrect_answers = []

        self.load_users()
        self.load_questions()
        self.load_categories()
        self.load_history()

    def safe_load_json(self, file_path, default_data):
        if not os.path.exists(file_path):
            return default_data
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return default_data

    def load_users(self):
        default_admin = [{
            "id": 0, 
            "username": "admin", 
            "password": hashlib.sha256("0000".encode()).hexdigest(),
            "role": "Admin", 
            "age": 30, 
            "phone": "03123456789"
        }]
        
        raw_users = self.safe_load_json(self.users_file, default_admin)
        valid_users = []
        
        required_keys = {"id", "username", "password", "role", "age", "phone"}
        if isinstance(raw_users, list):
            for u in raw_users:
                if isinstance(u, dict) and required_keys.issubset(u.keys()):
                    valid_users.append(u)

        self.users = valid_users if valid_users else default_admin

        has_admin = any(u.get("role") == "Admin" for u in self.users)
        if not has_admin:
            self.users.extend(default_admin)
            self.save_users()

    def save_users(self):
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(self.users, f, indent=4)

    def load_categories(self):
        raw_cats = self.safe_load_json(self.categories_file, [])
        if isinstance(raw_cats, list):
            self.categories = [str(c).strip() for c in raw_cats if isinstance(c, str)]
        else:
            self.categories = []

        q_cats = {q.category for q in self.questions if hasattr(q, 'category')}
        for cat in q_cats:
            if cat not in self.categories:
                self.categories.append(cat)
        self.save_categories()

    def save_categories(self):
        with open(self.categories_file, "w", encoding="utf-8") as f:
            json.dump(sorted(list(set(self.categories))), f, indent=4)

    def add_category(self, category_name):
        category_name = category_name.strip()
        if category_name and category_name not in self.categories:
            self.categories.append(category_name)
            self.save_categories()

    def load_questions(self):
        raw_questions = self.safe_load_json(self.questions_file, [])
        self.questions = []
        if isinstance(raw_questions, list):
            for q_data in raw_questions:
                if isinstance(q_data, dict):
                    q_obj = Question.from_dict(q_data)
                    if q_obj:
                        self.questions.append(q_obj)

    def save_questions(self):
        questions_dict = [q.to_dict() for q in self.questions]
        with open(self.questions_file, "w", encoding="utf-8") as f:
            json.dump(questions_dict, f, indent=4)

    def load_history(self):
        raw_history = self.safe_load_json(self.history_file, [])
        valid_history = []
        required_keys = {"Date and Time", "User", "Category", "Level", "Score", "Total", "Percentage"}
        
        if isinstance(raw_history, list):
            for h in raw_history:
                if isinstance(h, dict) and required_keys.issubset(h.keys()):
                    valid_history.append(h)
                    
        self.history = valid_history

    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4)

    def add_question_obj(self, category, level, question_text, options, answer):
        new_q = Question(category, level, question_text, options, answer)
        self.questions.append(new_q)
        self.add_category(category)
        self.save_questions()

    def delete_question_by_idx(self, idx):
        deleted_q = self.questions.pop(idx)
        self.save_questions()
        return deleted_q

    def record_quiz_history(self, total_questions):
        if total_questions == 0:
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "Date and Time": now,
            "User": self.current_user if self.current_user else "Guest",
            "Category": self.selected_category,
            "Level": self.selected_level,
            "Score": self.score,
            "Total": total_questions,
            "Percentage": round(self.percentage, 2)
        }
        self.history.append(record)
        self.save_history()