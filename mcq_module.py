# A list of dictionaries, each representing a question.
QUESTIONS = [
    {
        "question": "How often do you plan your day in the morning?",
        "options": ["Rarely", "Sometimes", "Often", "Almost Always"],
    },
    {
        "question": "How often do you get distracted by social media or notifications at work?",
        "options": ["Rarely", "Sometimes", "Often", "Almost Always"],
    },
    {
        "question": "How often do you finish your most important task of the day?",
        "options": ["Almost Always", "Often", "Sometimes", "Rarely"], # Note: Reversed scoring
        "reversed": True
    },
    {
        "question": "How often do you feel overwhelmed by your to-do list?",
        "options": ["Rarely", "Sometimes", "Often", "Almost Always"],
    },
    {
        "question": "How often do you take scheduled breaks (like the Pomodoro Technique)?",
        "options": ["Almost Always", "Often", "Sometimes", "Rarely"], # Note: Reversed scoring
        "reversed": True
    },
    {
        "question": "How often do you feel mentally exhausted at the end of the day?",
        "options": ["Rarely", "Sometimes", "Often", "Almost Always"],
    },
    {
        "question": "How often do you work late or on weekends to catch up?",
        "options": ["Rarely", "Sometimes", "Often", "Almost Always"],
    },
    {
        "question": "How often do you feel a sense of accomplishment from your work?",
        "options": ["Almost Always", "Often", "Sometimes", "Rarely"], # Note: Reversed scoring
        "reversed": True
    },
    {
        "question": "How often do you struggle to start a new task (procrastinate)?",
        "options": ["Rarely", "Sometimes", "Often", "Almost Always"],
    },
    {
        "question": "How often do you feel you have your energy levels under control?",
        "options": ["Almost Always", "Often", "Sometimes", "Rarely"], # Note: Reversed scoring
        "reversed": True
    },
]

def run_mcq_test():
    """
    Presents the MCQ test to the user and calculates the total score.
    A higher score indicates a higher risk of burnout/distraction.
    """
    total_score = 0
    user_mcq_answers = {}

    print("--- Part 1: Multiple Choice Productivity Test ---\n")
    for i, q in enumerate(QUESTIONS):
        print(f"Q{i+1}: {q['question']}")
        for j, option in enumerate(q['options']):
            print(f"  {j+1}. {option}")

        while True:
            try:
                choice = int(input("Enter your choice (1-4): "))
                if 1 <= choice <= 4:
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Scoring: 0 for best, 3 for worst.
        # Some questions are reversed, where "Almost Always" is a good thing.
        score = choice - 1
        if q.get("reversed"):
            score = 3 - score
        
        total_score += score
        user_mcq_answers[f"Q{i+1}"] = {"answer": q['options'][choice-1], "score": score}
        print("-" * 20)

    return total_score, user_mcq_answers


def get_productivity_profile(score, num_questions=len(QUESTIONS)):
    """
    Categorizes the user into a productivity profile based on their score.
    The max score is num_questions * 3.
    """
    max_score = num_questions * 3
    
    if score <= max_score / 3:
        return "Focused Achiever"
    elif score <= (max_score / 3) * 2:
        return "Moderately Distracted"
    else:
        return "Burnout Risk"