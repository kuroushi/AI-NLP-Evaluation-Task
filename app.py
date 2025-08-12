import streamlit as st
import time
from mcq_module import QUESTIONS, get_productivity_profile
from nlp_module import analyze_descriptive_answers
from recommendation_module import get_recommendations

# --- Page Configuration ---
st.set_page_config(
    page_title="Productivity Coach AI",
    page_icon="🚀"
)

st.title("🚀 :rainbow[Productivity Coach AI]")
# --- Descriptive Questions ---
DESCRIPTIVE_QUESTIONS = [
    "Describe your biggest productivity challenge in a few sentences.",
    "When do you feel most focused and energized during the day?"
]

# --- Session State Initialization ---
if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm here to help you understand your productivity patterns. Let's start with a few questions. Type 'start' or anything else to begin."}]
    st.session_state.mcq_answers = []
    st.session_state.desc_answers = {}
    st.session_state.q_index = 0
    st.session_state.results = {}

# --- Helper Functions ---
def ask_question():
    """Determines which question to ask based on the current stage."""
    if st.session_state.stage == "mcq":
        q_data = QUESTIONS[st.session_state.q_index]
        question_text = f"**Question {st.session_state.q_index + 1}/{len(QUESTIONS)}:**\n\n{q_data['question']}"
        options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(q_data['options'])])
        prompt = f"{question_text}\n\n{options_text}\n\nPlease type a number from 1 to 4."
    
    elif st.session_state.stage == "descriptive":
        question = DESCRIPTIVE_QUESTIONS[st.session_state.q_index]
        prompt = f"**Follow-up Question {st.session_state.q_index + 1}/{len(DESCRIPTIVE_QUESTIONS)}:**\n\n{question}"
    
    else:
        return

    st.session_state.messages.append({"role": "assistant", "content": prompt})

def calculate_and_display_results():
    """Calculates final results and saves them to the chat history for display."""
    with st.spinner("Analyzing your responses..."):
        # 1. Calculate MCQ Score and Profile
        total_score = sum(st.session_state.mcq_answers)
        profile = get_productivity_profile(total_score, len(QUESTIONS))
        
        # 2. Analyze Descriptive Answers
        nlp_analysis = analyze_descriptive_answers(st.session_state.desc_answers)
        tags = nlp_analysis.get('all_tags', [])
        
        # 3. Generate Summary
        summary_text = f"Your results show you're in the **'{profile}'** category. "
        if tags:
            summary_text += f"We noticed patterns related to **{', '.join(tags)}**. Based on this, here are some personalized recommendations."
        else:
            summary_text += "You seem to have a solid foundation. Here are some general tips."

        # 4. Get Recommendations
        recommendations = get_recommendations(profile, tags)
        
        # 5. Build the final results markdown string
        results_md = f"""
        Great, thank you! I've analyzed your responses. Here is your personalized productivity analysis:

        ### 👤 Your Productivity Profile: {profile}
        
        *{summary_text}*
        """
        
        if recommendations['Basic (Free)']:
            basic_recs = "\n".join([f"- {rec}" for rec in recommendations['Basic (Free)']])
            results_md += f"\n\n#### Basic (Free) Recommendations\n{basic_recs}"
            
        if recommendations['Premium (Advanced)']:
            premium_recs = "\n".join([f"- {rec}" for rec in recommendations['Premium (Advanced)']])
            results_md += f"\n\n#### Premium (Advanced) Recommendations\n{premium_recs}"
    
    # Add final results to chat history and set stage to finished
    st.session_state.messages.append({"role": "assistant", "content": results_md})
    st.session_state.stage = "finished"

# --- Main App Logic ---

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main conversation flow
if st.session_state.stage != "finished":
    # Ask the next question if it hasn't been asked yet
    if st.session_state.messages[-1]["role"] == "user":
        with st.spinner("Thinking..."):
            time.sleep(0.5)
            if st.session_state.stage == "mcq" and st.session_state.q_index < len(QUESTIONS):
                ask_question()
            elif st.session_state.stage == "descriptive" and st.session_state.q_index < len(DESCRIPTIVE_QUESTIONS):
                ask_question()
            elif st.session_state.stage == "calculating":
                calculate_and_display_results()
        st.rerun()

    # Handle user input
    if prompt := st.chat_input("Your response..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # --- STAGE: START ---
        if st.session_state.stage == "start":
            st.session_state.stage = "mcq"

        # --- STAGE: MCQ ---
        elif st.session_state.stage == "mcq":
            try:
                choice = int(prompt)
                if not 1 <= choice <= 4: raise ValueError
                
                q_data = QUESTIONS[st.session_state.q_index]
                score = choice - 1
                if q_data.get("reversed", False): score = 3 - score
                st.session_state.mcq_answers.append(score)
                
                st.session_state.q_index += 1
                if st.session_state.q_index == len(QUESTIONS):
                    st.session_state.stage = "descriptive"
                    st.session_state.q_index = 0
            except (ValueError, IndexError):
                st.session_state.messages.append({"role": "assistant", "content": "⚠️ Please enter a valid number from 1 to 4."})

        # --- STAGE: DESCRIPTIVE ---
        elif st.session_state.stage == "descriptive":
            q_key = f"desc_q_{st.session_state.q_index}"
            st.session_state.desc_answers[q_key] = prompt
            
            st.session_state.q_index += 1
            if st.session_state.q_index == len(DESCRIPTIVE_QUESTIONS):
                st.session_state.stage = "calculating"
        
        st.rerun()

# --- STAGE: FINISHED ---
if st.session_state.stage == "finished":
    if st.button("Start Over 🔁"):
        # Clear session state and rerun
        st.session_state.clear()
        st.rerun()