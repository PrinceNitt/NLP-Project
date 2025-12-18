"""
Main entry point for Resume Parser NLP Application.
"""
import streamlit as st
from modules.users import process_user_mode
from modules.recruiters import process_recruiters_mode
from modules.admin import process_admin_mode
from modules.feedback import process_feedback_mode
from utils.logger import setup_logger
from utils.ui_components import apply_custom_css
from config import validate_config, APP_NAME, APP_VERSION

# Setup logger
logger = setup_logger(__name__)


def main() -> None:
    """
    Main application function.
    Sets up Streamlit page configuration and handles navigation.
    """
    try:
        # Page configuration MUST be first Streamlit command
        st.set_page_config(
            page_title=APP_NAME,
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': None,
                'Report a bug': None,
                'About': f"# {APP_NAME}\n\nVersion {APP_VERSION}\n\nAI-Powered Resume Parser"
            }
        )
        
        # Apply custom CSS after page config
        apply_custom_css()
        
        # Validate configuration
        try:
            validate_config()
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            st.error(f"❌ Configuration Error: {e}. Please check your .env file.")
            return
        
        # Sidebar navigation with premium styling
        st.sidebar.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            background-size: 200% 200%;
            padding: 2.5rem 1.5rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4), 0 0 0 1px rgba(255,255,255,0.1) inset;
            position: relative;
            overflow: hidden;
            animation: sidebar-hero 8s ease infinite;
        ">
            <style>
            @keyframes sidebar-hero {{
                0%, 100% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
            }}
            </style>
            <div style="position: relative; z-index: 1;">
                <h2 style="
                    color: white; 
                    margin: 0; 
                    font-size: 1.75rem; 
                    font-weight: 800;
                    text-shadow: 0 4px 15px rgba(0,0,0,0.2);
                    letter-spacing: -0.01em;
                ">🚀 {APP_NAME}</h2>
                <p style="
                    color: rgba(255,255,255,0.95); 
                    margin: 0.75rem 0 0 0;
                    font-size: 1rem;
                    font-weight: 500;
                    text-shadow: 0 2px 8px rgba(0,0,0,0.15);
                ">v{APP_VERSION}</p>
            </div>
            <div style="
                position: absolute;
                top: -50%;
                right: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
                animation: sidebar-float 6s ease-in-out infinite;
            "></div>
            <style>
            @keyframes sidebar-float {{
                0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
                50% {{ transform: translate(-25px, -25px) rotate(180deg); }}
            }}
            </style>
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown("### 🧭 Navigation")
        
        app_mode = st.sidebar.selectbox(
            "Choose an option",
            ["Users", "Recruiters", "Feedback", "Admin"],
            help="Select the mode you want to use"
        )
        
        # Route to appropriate module
        if app_mode == "Users":
            process_user_mode()
        elif app_mode == "Recruiters":
            process_recruiters_mode()
        elif app_mode == "Admin":
            process_admin_mode()
        elif app_mode == "Feedback":
            process_feedback_mode()
            
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        st.error("❌ An unexpected error occurred. Please refresh the page.")


if __name__ == "__main__":
    main()
