# src/models.py

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

        if not isinstance(data.get("Options"), list) or len(data["Options"]) != 4:
            return None

        if str(data.get("Answer")).upper() not in ["A", "B", "C", "D"]:
            return None

        return cls(
            category=data["Category"],
            level=data["Level"],
            question=data["Question"],
            options=data["Options"],
            answer=str(data["Answer"]).upper()
        )
    
    def to_dict(self):
        return {
            "Category": self.category,
            "Level": self.level,
            "Question": self.question,
            "Options": self.options,
            "Answer": self.answer
        }