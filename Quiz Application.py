# Quiz Application
# Author: Muhammad Abdullah Farooq
# Language: Python
# Level: Beginner

print ("============ Welcome to Quiz Application =============")

# ------------------------------------------ Quiz Application -------------------------------------------------------

easy_questions= [
{"Question":"What does CPU stand for?","Options":["A. Central Process Unit","B. Central Processing Unit","C. Computer Personal Unit","D. Central Program Unit"],"Answer":"B"},
{"Question":"Which language are we learning?","Options":["A. Java","B. Python","C. C++","D. PHP"],"Answer":"B"},
{"Question":"Which keyword is used to define a function?","Options":["A. function","B. define","C. def","D. func"],"Answer":"C"},
{"Question":"Which data type stores True or False?","Options":["A. int","B. bool","C. str","D. float"],"Answer":"B"},
{"Question":"Which symbol starts a comment in Python?","Options":["A. //","B. <!--","C. #","D. **"],"Answer":"C"},
{"Question":"What is 15 + 10?","Options":["A. 20","B. 25","C. 30","D. 35"],"Answer":"B"},
{"Question":"Which loop runs while a condition is True?","Options":["A. for","B. while","C. do","D. repeat"],"Answer":"B"},
{"Question":"Which function is used to take input?","Options":["A. print()","B. input()","C. read()","D. scan()"],"Answer":"B"},
{"Question":"Which keyword returns a value from a function?","Options":["A. stop","B. end","C. return","D. break"],"Answer":"C"},
{"Question":"Which collection uses curly braces {}?","Options":["A. List","B. Tuple","C. Dictionary","D. String"],"Answer":"C"},
{"Question":"Which operator checks equality?","Options":["A. =","B. ==","C. !=","D. >"],"Answer":"B"},
{"Question":"Which keyword handles exceptions?","Options":["A. error","B. except","C. catch","D. handle"],"Answer":"B"},
{"Question":"Which block is written before except?","Options":["A. test","B. try","C. raise","D. finally"],"Answer":"B"},
{"Question":"Which method adds an item to a list?","Options":["A. add()","B. insert()","C. append()","D. push()"],"Answer":"C"},
{"Question":"Python is a...?","Options":["A. Low-level language","B. Machine language","C. High-level language","D. Assembly language"],"Answer":"C"},
{"Question":"Which keyword creates a class?","Options":["A. object","B. class","C. new","D. define"],"Answer":"B"},
{"Question":"Which loop is commonly used to iterate through a list?","Options":["A. while","B. for","C. repeat","D. loop"],"Answer":"B"},
{"Question":"Which function displays output?","Options":["A. show()","B. display()","C. print()","D. output()"],"Answer":"C"},
{"Question":"Python files end with which extension?","Options":["A. .exe","B. .java","C. .py","D. .cpp"],"Answer":"C"},
{"Question":"Git is mainly used for?","Options":["A. Video Editing","B. Version Control","C. Database","D. Networking"],"Answer":"B"}
]

medium_questions= [
{"Question":"Which data structure follows the FIFO principle?","Options":["A. Stack","B. Queue","C. Tree","D. Graph"],"Answer":"B"},
{"Question":"Which keyword is used to create an object in Python?","Options":["A. object","B. class","C. No keyword","D. new"],"Answer":"C"},
{"Question":"Which SQL command retrieves data?","Options":["A. GET","B. SELECT","C. FETCH","D. OPEN"],"Answer":"B"},
{"Question":"Which protocol is used to browse websites?","Options":["A. FTP","B. SMTP","C. HTTP","D. SSH"],"Answer":"C"},
{"Question":"Which device forwards data packets between networks?","Options":["A. Switch","B. Router","C. Hub","D. Modem"],"Answer":"B"},
{"Question":"Which Python collection stores unique values?","Options":["A. List","B. Tuple","C. Dictionary","D. Set"],"Answer":"D"},
{"Question":"Which sorting algorithm repeatedly swaps adjacent elements?","Options":["A. Merge Sort","B. Bubble Sort","C. Quick Sort","D. Heap Sort"],"Answer":"B"},
{"Question":"Which loop is best when the number of iterations is known?","Options":["A. while","B. do-while","C. for","D. repeat"],"Answer":"C"},
{"Question":"Which function converts a string to an integer?","Options":["A. float()","B. str()","C. int()","D. bool()"],"Answer":"C"},
{"Question":"Which symbol is used for floor division in Python?","Options":["A. /","B. %","C. //","D. **"],"Answer":"C"},
{"Question":"Which operating system is open source?","Options":["A. Windows","B. Linux","C. macOS","D. DOS"],"Answer":"B"},
{"Question":"Which database is relational?","Options":["A. MongoDB","B. MySQL","C. Redis","D. Cassandra"],"Answer":"B"},
{"Question":"Which HTML tag creates a hyperlink?","Options":["A. <link>","B. <a>","C. <href>","D. <url>"],"Answer":"B"},
{"Question":"Which CSS property changes text color?","Options":["A. font-color","B. text-color","C. color","D. background"],"Answer":"C"},
{"Question":"Which Git command uploads commits to GitHub?","Options":["A. git add","B. git commit","C. git push","D. git clone"],"Answer":"C"},
{"Question":"Which Python keyword skips the current loop iteration?","Options":["A. break","B. continue","C. return","D. pass"],"Answer":"B"},
{"Question":"Which memory is volatile?","Options":["A. SSD","B. HDD","C. RAM","D. ROM"],"Answer":"C"},
{"Question":"Which company developed Python?","Options":["A. Google","B. Microsoft","C. Python Software Foundation","D. Apple"],"Answer":"C"},
{"Question":"Which command creates a new Git repository?","Options":["A. git clone","B. git init","C. git push","D. git status"],"Answer":"B"},
{"Question":"Which operator is used for exponentiation in Python?","Options":["A. ^","B. **","C. //","D. %%"],"Answer":"B"}
]

hard_questions = [
{"Question":"What is the average time complexity of Binary Search?","Options":["A. O(n)","B. O(log n)","C. O(n log n)","D. O(1)"],"Answer":"B"},
{"Question":"Which traversal visits Left, Root, Right?","Options":["A. Preorder","B. Postorder","C. Inorder","D. Level Order"],"Answer":"C"},
{"Question":"Which normal form removes transitive dependency?","Options":["A. 1NF","B. 2NF","C. 3NF","D. BCNF"],"Answer":"C"},
{"Question":"Which protocol is used for secure web browsing?","Options":["A. HTTP","B. HTTPS","C. FTP","D. SMTP"],"Answer":"B"},
{"Question":"Which OS scheduling algorithm may cause starvation?","Options":["A. FCFS","B. Round Robin","C. Priority Scheduling","D. FIFO"],"Answer":"C"},
{"Question":"Which data structure is used in recursion?","Options":["A. Queue","B. Stack","C. Tree","D. Graph"],"Answer":"B"},
{"Question":"Which SQL JOIN returns only matching rows?","Options":["A. LEFT JOIN","B. RIGHT JOIN","C. INNER JOIN","D. FULL JOIN"],"Answer":"C"},
{"Question":"Which algorithm finds the shortest path in a weighted graph?","Options":["A. DFS","B. BFS","C. Dijkstra","D. Kruskal"],"Answer":"C"},
{"Question":"Which port is used by HTTPS?","Options":["A. 21","B. 25","C. 80","D. 443"],"Answer":"D"},
{"Question":"Which Python keyword is used to handle exceptions?","Options":["A. catch","B. except","C. error","D. raise"],"Answer":"B"},
{"Question":"Which algorithm divides the array around a pivot?","Options":["A. Merge Sort","B. Bubble Sort","C. Quick Sort","D. Selection Sort"],"Answer":"C"},
{"Question":"Which layer of the OSI model handles routing?","Options":["A. Data Link","B. Network","C. Session","D. Transport"],"Answer":"B"},
{"Question":"Which SQL clause filters grouped records?","Options":["A. WHERE","B. GROUP BY","C. HAVING","D. ORDER BY"],"Answer":"C"},
{"Question":"Which protocol translates domain names into IP addresses?","Options":["A. DHCP","B. DNS","C. FTP","D. SMTP"],"Answer":"B"},
{"Question":"Which Git command combines another branch into the current branch?","Options":["A. git add","B. git merge","C. git push","D. git pull"],"Answer":"B"},
{"Question":"Which tree is always height-balanced?","Options":["A. Binary Tree","B. AVL Tree","C. Heap","D. Trie"],"Answer":"B"},
{"Question":"Which complexity represents Merge Sort?","Options":["A. O(n²)","B. O(log n)","C. O(n log n)","D. O(n)"],"Answer":"C"},
{"Question":"Which attack attempts to guess passwords repeatedly?","Options":["A. Phishing","B. Brute Force","C. Spoofing","D. Sniffing"],"Answer":"B"},
{"Question":"Which Python module is commonly used for working with JSON?","Options":["A. csv","B. pickle","C. json","D. os"],"Answer":"C"},
{"Question":"Which database command permanently removes a table?","Options":["A. DELETE","B. DROP","C. REMOVE","D. ERASE"],"Answer":"B"}
]

score = 0
questions = []

def select_level():
    global questions, selected_level

    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    try:
        choice_level = int(input("Select Level: "))
    except ValueError:
        print("Invalid input! Please enter 1, 2, or 3.")
        return False

    if choice_level == 1:
        questions = easy_questions
        selected_level = "Easy"
    elif choice_level == 2:
        questions = medium_questions
        selected_level = "Medium"
    elif choice_level == 3:
        questions = hard_questions
        selected_level = "Hard"
    else:
        print("Invalid Choice! Please enter 1, 2, or 3.")
        return False
    return True

def quiz_game_instruction():
    print("=================INSTRUCTIONS=================")
    total = len(questions) if questions else 20
    print(f"- Total Questions: {total}")
    print("- Each question carries one mark")
    print("- Enter only A, B, C, D")
    print("- No negative marking.")
    print("==============================================")

def start_quiz():
    if not select_level():
        return

    print("---------------------------------------------------")
    print(f"Selected Level: {selected_level}")
    print(f"Number of Questions: {len(questions)}")
    print("The quiz will begin now.")
    print("---------------------------------------------------")

    while True:
        print("Starting the Quiz...")
        for i, question in enumerate(questions, start=1):
            print(f"Question {i}/{len(questions)}")
            show_question(question)
            check_answer(question)
            print("---------------------------------------------------")

        print()
        show_result()

        while True:
            replay = input("Do you want to play again? Yes/No: ").strip().lower()
            if replay in ["yes", "y"]:
                global score
                score = 0
                if not select_level():
                    return
                break
            elif replay in ["no", "n"]:
                return
            else:
                print("Invalid Input! Please enter Yes or No.")
        print()

def show_question(question):
    print(question["Question"])
    for option in question["Options"]:
        print(option)

def check_answer(question):
    global score
    while True:
        answer = input("Enter Answer (A/B/C/D): ").upper()
        if answer in ["A", "B", "C", "D"]:
            break
        print("Invalid option! Choose A, B, C or D.")

    if answer == question["Answer"]:
        print("Correct Answer!", answer)
        score += 1
    else:
        print(f"Wrong Answer! The correct answer is: {question['Answer']}")

def show_result():
    print("================ QUIZ RESULT ================")
    if not questions:
        print("No quiz has been played yet.")
        print("---------------------------------------------------")
        return
    print("Correct Answers: ", score)
    print("Wrong Answers: ", len(questions) - score)
    print(f"Your final score is: {score}/{len(questions)}")
    percentage = (score / len(questions) * 100)
    print(f"Percentage: {percentage:.2f}%")    
    if percentage >=90:
        print("Status: EXCELLENT!")
    elif percentage >=80:
        print("Status: VERY GOOD!")
    elif percentage >= 70:
        print("Status: GOOD!")
    elif percentage >=60:
        print("Status: AVERAGE!")
    elif percentage >=50:
        print("Status: PASS!")
    else:
        print("Status: FAIL! \nBetter Luck Next Time")
    print("---------------------------------------------------")

def restart_quiz():
    global score
    score = 0
    start_quiz()

def last_game_score():
    if not questions:
        print("No quiz has been played yet. Start a quiz first.")
        return
    show_result()

def exit_system():
    print("Thank you for using the Quiz Application!")
    print("Good Bye! Have a nice day!")
    print("Exiting the Quiz Application...")
    input("Press Enter to close window!")
    import sys
    sys.exit()

while True:
    print()
    print("=============== Select the Option (0-4) ===============")
    print("1. Start New Quiz")
    print("2. Game Instructions")
    print("3. View Last Game Result")
    print("4. Restart Quiz")
    print("0. Exit")

    try:
        choice = int(input("Enter the number: "))
    except ValueError:
        print("Invalid Choice! Please enter a number.")
        continue
    except Exception as e:
        print(f"An error occurred: {e}")
        continue

    if choice == 1:
        start_quiz()
    elif choice == 2:
        quiz_game_instruction()
    elif choice == 3:
        last_game_score()
    elif choice == 4:
        restart_quiz()
    elif choice == 0:
        exit_system()
    else:
        print("Invalid Choice! Choose between 0 to 4")