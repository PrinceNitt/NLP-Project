"""
User module for Resume Parser NLP Application.
Handles user resume upload and parsing functionality.
"""
import streamlit as st
from typing import Optional, Dict, Any

from utils.resume_parser import (
    extract_resume_info_from_pdf,
    extract_contact_number_from_resume,
    extract_education_from_resume,
    extract_experience,
    suggest_skills_for_job,
    show_colored_skills,
    calculate_resume_score,
    extract_resume_info
)
from utils.database import init_database, insert_pdf
from utils.validators import validate_file_upload, sanitize_input
from utils.logger import setup_logger, log_error
from utils.ui_components import (
    create_hero_section,
    create_info_card,
    create_success_card,
    display_skill_tags,
    create_progress_bar,
    create_metric_card
)

logger = setup_logger(__name__)


def process_user_mode() -> None:
    """
    Main function to process user mode.
    Handles resume upload, parsing, and display of extracted information.
    """
    try:
        # Initialize database
        init_database()
        
        # Modern hero section
        create_hero_section(
            "📄 Resume Parser using NLP",
            "Upload your resume and get instant insights about your profile"
        )
        
        # File uploader with better styling
        st.markdown("### 📤 Upload Your Resume")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload your resume in PDF format (max 5MB)",
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            try:
                # Validate file upload
                is_valid, error_message = validate_file_upload(uploaded_file)
                
                if not is_valid:
                    st.error(f"❌ {error_message}")
                    logger.warning(f"Invalid file upload: {error_message}")
                    return
                
                create_success_card("File Uploaded!", "Your resume has been uploaded successfully. Processing...")
                
                # Get file data
                pdf_name = uploaded_file.name
                pdf_data = uploaded_file.getvalue()
                
                # Insert PDF into database
                pdf_id = insert_pdf(pdf_name, pdf_data)
                if pdf_id:
                    logger.info(f"PDF stored successfully: {pdf_name} (ID: {pdf_id})")
                else:
                    logger.warning(f"Failed to store PDF: {pdf_name}")
                
                # Extract and parse resume
                with st.spinner("Processing resume... This may take a few seconds."):
                    try:
                        # Reset file pointer to beginning for parsing
                        uploaded_file.seek(0)
                        pdf_text = extract_resume_info_from_pdf(uploaded_file)
                        resume_info = extract_resume_info(pdf_text, filename=pdf_name)
                    except Exception as e:
                        log_error(logger, e, {'operation': 'resume_parsing', 'file': pdf_name})
                        st.error("❌ Error parsing resume. Please ensure the PDF contains readable text.")
                        return
                
                # Display extracted information
                display_resume_info(resume_info, pdf_text)
                
            except Exception as e:
                log_error(logger, e, {'operation': 'process_user_mode'})
                st.error("❌ An error occurred while processing your resume. Please try again.")
                
    except Exception as e:
        log_error(logger, e, {'operation': 'process_user_mode_init'})
        st.error("❌ Application error. Please refresh the page and try again.")


def display_resume_info(resume_info: Dict[str, Any], pdf_text) -> None:
    """
    Display extracted resume information.
    
    Args:
        resume_info: Dictionary containing extracted resume information
        pdf_text: Processed PDF text (spaCy doc object)
    """
    try:
        st.divider()
        st.header("📋 Extracted Information:")
        
        # Personal Information
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**First Name:** {resume_info.get('first_name', 'Not found')}")
            st.write(f"**Last Name:** {resume_info.get('last_name', 'Not found')}")
        
        with col2:
            email = resume_info.get('email', '')
            if email:
                st.write(f"**Email:** {email}")
            else:
                st.write("**Email:** Not found")
            
            # Extract and display phone number
            try:
                contact_number = extract_contact_number_from_resume(pdf_text)
                if contact_number:
                    display_number = (
                        contact_number 
                        if contact_number.startswith('+') 
                        else f"+{contact_number}"
                    )
                    st.write(f"**Phone Number:** {display_number}")
                else:
                    st.write("**Phone Number:** Not found")
            except Exception as e:
                log_error(logger, e, {'operation': 'extract_phone'})
                st.write("**Phone Number:** Error extracting")
        
        st.write(f"**Degree/Major:** {resume_info.get('degree_major', 'Not found')}")
        
        # Education Section
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 2rem 0;
            border-left: 5px solid #3498db;
        ">
            <h3 style="color: #2c3e50; margin-top: 0;">🎓 Education</h3>
        </div>
        """, unsafe_allow_html=True)
        try:
            education_info = extract_education_from_resume(pdf_text)
            if education_info:
                for edu in education_info:
                    st.markdown(f"""
                    <div style="
                        background: white;
                        padding: 1rem;
                        border-radius: 10px;
                        margin: 0.5rem 0;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        border-left: 4px solid #3498db;
                    ">
                        <p style="margin: 0; color: #2c3e50; font-weight: 500;">🎓 {edu}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                create_info_card("Education", "No education information found in resume")
        except Exception as e:
            log_error(logger, e, {'operation': 'extract_education'})
            st.warning("Error extracting education information")
        
        # Skills Section
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 2rem 0;
            border-left: 5px solid #e74c3c;
        ">
            <h3 style="color: white; margin-top: 0;">💼 Skills</h3>
        </div>
        """, unsafe_allow_html=True)
        try:
            skills = resume_info.get('skills', [])
            if skills:
                display_skill_tags(skills, color_scheme="purple")
            else:
                create_info_card("Skills", "No skills found in resume")
        except Exception as e:
            log_error(logger, e, {'operation': 'display_skills'})
            st.warning("Error displaying skills")
        
        # Experience Section
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 2rem 0;
            border-left: 5px solid #3498db;
        ">
            <h3 style="color: white; margin-top: 0;">📈 Experience</h3>
        </div>
        """, unsafe_allow_html=True)
        try:
            experience_info = extract_experience(pdf_text)
            col1, col2 = st.columns(2)
            with col1:
                create_metric_card(
                    "Experience Level",
                    experience_info.get('level_of_experience', 'Not determined'),
                    icon="📊"
                )
            with col2:
                create_metric_card(
                    "Suggested Position",
                    experience_info.get('suggested_position', 'Not identified'),
                    icon="💼"
                )
        except Exception as e:
            log_error(logger, e, {'operation': 'extract_experience'})
            st.warning("Error extracting experience information")
        
        # Resume Score
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 2rem 0;
            border-left: 5px solid #3498db;
        ">
            <h3 style="color: white; margin-top: 0;">⭐ Resume Score</h3>
        </div>
        """, unsafe_allow_html=True)
        try:
            resume_score = calculate_resume_score(resume_info)
            
            # Create attractive score display
            col1, col2 = st.columns([1, 2])
            with col1:
                create_metric_card(
                    "Score",
                    f"{resume_score}/100",
                    icon="⭐"
                )
            with col2:
                create_progress_bar(resume_score, 100, "Resume Completeness")
        except Exception as e:
            log_error(logger, e, {'operation': 'calculate_score'})
            st.warning("Error calculating resume score")
        
        # Job Suggestions
        st.divider()
        st.header("🎯 Suggested Skills for Desired Job:")
        desired_job = st.text_input("Enter the job you are looking for:", key="desired_job")
        
        if desired_job:
            try:
                # Sanitize input
                desired_job_clean = sanitize_input(desired_job, max_length=100)
                suggested_skills = suggest_skills_for_job(desired_job_clean)
                
                if suggested_skills:
                    st.write("**Recommended Skills:**")
                    for skill in suggested_skills:
                        st.write(f"- {skill}")
                else:
                    st.info(f"No specific skills found for '{desired_job_clean}'. Try a different job title.")
            except Exception as e:
                log_error(logger, e, {'operation': 'suggest_skills', 'job': desired_job})
                st.warning("Error fetching skill suggestions")
                
    except Exception as e:
        log_error(logger, e, {'operation': 'display_resume_info'})
        st.error("Error displaying resume information")


if __name__ == '__main__':
    process_user_mode()
