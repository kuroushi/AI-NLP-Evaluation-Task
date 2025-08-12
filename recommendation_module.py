RECOMMENDATIONS = {
    "Basic": [
        {
            "title": "The 5-Minute Rule",
            "description": "If a task takes less than 5 minutes, do it immediately. This helps beat procrastination on small items.",
            "for_tags": ["procrastination", "planning"]
        },
        {
            "title": "Single-Task List",
            "description": "Start your day by identifying the ONE most important task. Focus on finishing only that task before moving to others.",
            "for_profile": ["Burnout Risk", "Moderately Distracted"]
        },
        {
            "title": "Mindful Break",
            "description": "Take a 5-minute break every hour to stretch, walk, or just look away from your screen. Helps reduce mental fatigue.",
            "for_profile": ["Burnout Risk"],
            "for_tags": ["burnout", "time anxiety"]
        },
        {
            "title": "Turn Off Notifications",
            "description": "Disable non-essential notifications on your phone and computer for a 1-hour block of deep work.",
            "for_tags": ["distraction"]
        }
    ],
    "Premium": [
        {
            "title": "Advanced Time Blocking",
            "description": "Access our guided module to plan your entire week using time blocks, ensuring a balance between deep work, meetings, and breaks.",
            "for_profile": ["Moderately Distracted", "Burnout Risk"]
        },
        {
            "title": "Guided Calming Audio",
            "description": "Listen to our 3-minute calming audio session before starting a stressful task to reduce anxiety and improve focus.",
            "for_tags": ["time anxiety", "burnout"]
        },
        {
            "title": "Procrastination Coach Chatbot",
            "description": "Engage with our AI coach to identify the root causes of your procrastination and get personalized strategies.",
            "for_tags": ["procrastination"]
        }
    ]
}

def get_recommendations(profile, tags):
    """Filters and returns recommendations based on user profile and behavioral tags."""
    
    personalized_recs = {"Basic (Free)": [], "Premium (Advanced)": []}
    
    # Flatten the tags for easier checking
    all_tags = set(tags)
    
    # Check Basic recommendations
    for rec in RECOMMENDATIONS["Basic"]:
        # Check if recommendation is for the user's profile
        profile_match = "for_profile" not in rec or profile in rec.get("for_profile", [])
        # Check if recommendation matches any of the user's tags
        tag_match = "for_tags" not in rec or any(tag in all_tags for tag in rec.get("for_tags", []))
        
        if profile_match and tag_match:
            personalized_recs["Basic (Free)"].append(f"{rec['title']}: {rec['description']}")

    # Check Premium recommendations
    for rec in RECOMMENDATIONS["Premium"]:
        profile_match = "for_profile" not in rec or profile in rec.get("for_profile", [])
        tag_match = "for_tags" not in rec or any(tag in all_tags for tag in rec.get("for_tags", []))
        
        if profile_match and tag_match:
            personalized_recs["Premium (Advanced)"].append(f"{rec['title']}: {rec['description']}")
            
    return personalized_recs