import re
import string
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# --- Keyword Dictionaries ---

POSITIVE_WORDS = [
    "focused", "productive", "energized", "motivated", "accomplished",
    "clear", "organized", "efficient", "great", "good", "calm", "ready"
]

NEGATIVE_WORDS = [
    "distracted", "overwhelmed", "procrastinating", "anxious", "stressed",
    "tired", "exhausted", "stuck", "unmotivated", "messy", "late", "pressure"
]

BEHAVIORAL_TAG_MAP = {
    "procrastination": ["procrastinate", "delay", "put off", "avoid", "can't start"],
    "time anxiety": ["deadline", "pressure", "no time", "rushed", "late"],
    "distraction": ["notifications", "social media", "phone", "distracted", "interruptions"],
    "burnout": ["exhausted", "overwhelmed", "tired", "drained", "no energy"],
    "planning": ["plan", "schedule", "list", "organize", "morning routine"]
}

def analyze_sentiment(text):
    """A simple keyword-based sentiment analysis."""
    text_lower = text.lower()
    pos_count = sum(1 for word in POSITIVE_WORDS if word in text_lower)
    neg_count = sum(1 for word in NEGATIVE_WORDS if word in text_lower)

    if neg_count > pos_count:
        return "Negative"
    elif pos_count > neg_count:
        return "Positive"
    else:
        return "Neutral"

def extract_keywords(text):
    """Extracts significant keywords by removing stopwords and punctuation."""
    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text) # Remove punctuation
    tokens = word_tokenize(text)
    
    keywords = [word for word in tokens if word.isalpha() and word not in stop_words]
    # Return the 5 most common keywords
    return [word for word, count in Counter(keywords).most_common(5)]

def get_behavioral_tags(text):
    """Assigns behavioral tags based on keyword matches."""
    text_lower = text.lower()
    tags = set() # Use a set to avoid duplicate tags
    for tag, keywords in BEHAVIORAL_TAG_MAP.items():
        if any(keyword in text_lower for keyword in keywords):
            tags.add(tag)
    return list(tags)

def analyze_descriptive_answers(answers_dict):
    """
    Runs full NLP analysis on a dictionary of descriptive answers.
    
    Args:
        answers_dict (dict): A dictionary where keys are questions and values are user answers.
        
    Returns:
        A dictionary containing the combined analysis results.
    """
    full_analysis = {}
    combined_text = " ".join(answers_dict.values())
    
    full_analysis['all_tags'] = get_behavioral_tags(combined_text)
    full_analysis['all_keywords'] = extract_keywords(combined_text)
    
    full_analysis['individual_analysis'] = {}
    for question, answer in answers_dict.items():
        analysis = {
            "sentiment": analyze_sentiment(answer),
            "keywords": extract_keywords(answer),
            "tags": get_behavioral_tags(answer),
        }
        full_analysis['individual_analysis'][question] = analysis
        
    return full_analysis