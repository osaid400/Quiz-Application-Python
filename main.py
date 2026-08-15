# ======================================
# QUIZ APPLICATION 
# Author: Muhammad Abdullah Farooq  
# Language: Python 3.13
# ======================================

from src.manager import QuizManager
from src.UI import QuizUI

def main():
    
    print("============ Welcome to Quiz Application =============")

    manager = QuizManager()
    UI = QuizUI(manager)
    UI.main_menu()

if __name__ == "__main__":
    main()