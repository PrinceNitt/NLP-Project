"""
Feedback module for Resume Parser NLP Application.
Handles user feedback collection and storage.
"""
import streamlit as st
from typing import Optional

from utils.database import init_database, insert_feedback
from utils.validators import sanitize_input
from utils.logger import setup_logger, log_error
from utils.ui_components import (
    create_hero_section,
    create_info_card,
    create_success_card
)

logger = setup_logger(__name__)


def process_feedback_mode() -> None:
    """
    Main function to process feedback mode.
    Handles feedback form display and submission.
    """
    try:
        # Initialize database
        init_database()
        
        # Modern hero section
        create_hero_section(
            "💬 Feedback Section",
            "Your feedback helps us improve! Share your thoughts and suggestions."
        )
        
        # Feedback Form
        st.markdown("### 📝 Provide Your Feedback")
        create_info_card(
            "We Value Your Input",
            "Please share your thoughts, suggestions, or report any issues you've encountered."
        )
        
        user_name = st.text_input(
            "👤 Your Name (Optional):",
            key="feedback_name",
            max_chars=100,
            help="Enter your name (optional)",
            placeholder="John Doe"
        )
        
        feedback = st.text_area(
            "💭 Your Feedback:",
            height=150,
            key="feedback_text",
            max_chars=2000,
            help="Share your feedback, suggestions, or report issues",
            placeholder="Enter your feedback here..."
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🚀 Submit Feedback", type="primary", use_container_width=True):
                submit_feedback(user_name, feedback)
            
    except Exception as e:
        log_error(logger, e, {'operation': 'process_feedback_mode'})
        st.error("❌ An error occurred. Please try again.")


def submit_feedback(user_name: str, feedback: str) -> None:
    """
    Submit feedback to database.
    
    Args:
        user_name: Name of the user providing feedback
        feedback: Feedback text
    """
    try:
        # Validate inputs
        if not feedback or not feedback.strip():
            st.warning("⚠️ Please provide feedback before submitting.")
            return
        
        # Sanitize inputs
        user_name_clean = sanitize_input(user_name, max_length=100) if user_name else "Anonymous"
        feedback_clean = sanitize_input(feedback, max_length=2000)
        
        # Insert feedback into database
        feedback_id = insert_feedback(user_name_clean, feedback_clean)
        
        if feedback_id:
            st.success("✅ Feedback submitted successfully! Thank you for your input.")
            logger.info(f"Feedback submitted successfully (ID: {feedback_id})")
            
            # Clear form (Streamlit will rerun)
            st.session_state.feedback_name = ""
            st.session_state.feedback_text = ""
        else:
            st.error("❌ Failed to submit feedback. Please try again.")
            logger.error("Failed to insert feedback into database")
            
    except Exception as e:
        log_error(logger, e, {'operation': 'submit_feedback'})
        st.error("❌ An error occurred while submitting feedback. Please try again.")


if __name__ == "__main__":
    process_feedback_mode()
