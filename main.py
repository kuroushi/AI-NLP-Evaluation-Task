import json
from mcq_module import run_mcq_test, get_productivity_profile
from nlp_module import analyze_descriptive_answers
from recommendation_module import get_recommendations

def generate_summary(profile, tags):
    """Generates a 2-3 line personalized summary."""
    summary = f"Your results show you're in the '{profile}' category. "
    
    if not tags:
        summary += "You seem to have a good handle on your productivity habits."
        return summary

    if "procrastination" in tags and "distraction" in tags:
        summary += "It seems like procrastination and frequent distractions are key challenges for you. "
    elif "burnout" in tags or "time anxiety" in tags:
        summary += "We've noticed signs of potential burnout and pressure related to time management. "
    else:
        summary += f"You appear to be struggling with {tags[0]}. "
        
    summary += "Let's find some steps to help you improve."
    return summary

def main():
    """Main function to run the entire assessment flow."""
    
    # --- Part 1: MCQ Test ---
    mcq_score, mcq_answers = run_mcq_test()
    productivity_profile = get_productivity_profile(mcq_score)
    
    # --- Part 2: Descriptive NLP Analysis ---
    print("\n--- Part 2: Descriptive Questions ---\n")
    desc_q1 = "Describe your biggest productivity challenge."
    desc_q2 = "When do you feel most focused and energized during the day?"
    
    answer1 = input(f"{desc_q1}\n> ")
    answer2 = input(f"\n{desc_q2}\n> ")
    
    descriptive_answers = {
        "challenge": answer1,
        "focus_time": answer2
    }
    
    nlp_analysis = analyze_descriptive_answers(descriptive_answers)
    behavioral_tags = nlp_analysis['all_tags']
    
    # --- Part 3: Result Generation ---
    final_summary = generate_summary(productivity_profile, behavioral_tags)
    
    # --- Part 4: Recommendation Flow ---
    recommendations = get_recommendations(productivity_profile, behavioral_tags)

    # --- Final Output ---
    print("\n\n======================================")
    print("      Your Personalized Analysis      ")
    print("======================================\n")
    
    print(f"👤 PRODUCTIVITY PROFILE: {productivity_profile}\n")
    
    print("📝 SUMMARY:")
    print(f"   {final_summary}\n")
    
    print("💡 RECOMMENDED ACTIONS:\n")
    if recommendations["Basic (Free)"]:
        print("--- Basic (Free) ---")
        for rec in recommendations["Basic (Free)"]:
            print(f"  • {rec}")
    
    if recommendations["Premium (Advanced)"]:
        print("\n--- Premium (Advanced) ---")
        for rec in recommendations["Premium (Advanced)"]:
            print(f"  • {rec}")
            
    # --- Create JSON output for submission ---
    output_data = {
        "user_input": {
            "mcq_answers": mcq_answers,
            "descriptive_answers": descriptive_answers
        },
        "system_output": {
            "mcq_score": mcq_score,
            "profile": productivity_profile,
            "nlp_analysis": nlp_analysis,
            "summary": final_summary,
            "recommendations": recommendations
        }
    }
    
    with open("output_data.json", "w") as f:
        json.dump(output_data, f, indent=4)
        
    print("\n\n(A file named 'output_data.json' with your detailed results has been saved.)")


if __name__ == "__main__":
    try:
        main()
    except (ModuleNotFoundError, ImportError):
        print("\n[ERROR] NLTK not found.")
        print("Please install it by running: pip install nltk")
        print("Then, run python and type:\nimport nltk\nnltk.download('punkt')\nnltk.download('stopwords')")