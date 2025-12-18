"""
Recruiters module for Resume Parser NLP Application.
Handles recruiter functionality for bulk resume processing and skill matching.
"""
import streamlit as st
import spacy
from spacy.matcher import Matcher
import csv
import fitz  # PyMuPDF
from typing import List, Set, Optional

from config import UPDATED_SKILLS_CSV, MAX_FILES_PER_UPLOAD, MAX_UPLOAD_SIZE
from utils.validators import validate_file_upload, validate_skills_input
from utils.logger import setup_logger, log_error
from utils.resume_parser import extract_name, extract_name_from_filename
from utils.ui_components import (
    create_hero_section,
    create_info_card,
    create_success_card,
    display_skill_tags,
    create_metric_card
)

# Load the SpaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError as e:
    st.error("❌ Error loading spaCy model. Please ensure 'en_core_web_sm' is installed.")
    nlp = None

logger = setup_logger(__name__)


def process_recruiters_mode() -> None:
    """
    Main function to process recruiters mode.
    Handles bulk resume upload, skill matching, and candidate evaluation.
    """
    try:
        if nlp is None:
            st.error("❌ NLP model not available. Please check installation.")
            return
        
        # Modern hero section
        create_hero_section(
            "👥 Recruiter's Panel",
            "Upload multiple resumes and find the perfect candidates"
        )
        
        # Configuration
        MAX_FILE_SIZE_MB = MAX_UPLOAD_SIZE / (1024 * 1024)  # Convert bytes to MB
        
        # File upload section
        st.markdown("### 📤 Upload Resumes")
        create_info_card(
            "Upload Limit",
            f"Maximum {MAX_FILES_PER_UPLOAD} files, {MAX_FILE_SIZE_MB:.0f}MB per file"
        )
        
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            accept_multiple_files=True,
            type="pdf",
            help=f"You can upload up to {MAX_FILES_PER_UPLOAD} PDF files at once. Each file should be less than {MAX_FILE_SIZE_MB:.0f}MB.",
            label_visibility="collapsed"
        )
        
        # Check file count limit
        if uploaded_files and len(uploaded_files) > MAX_FILES_PER_UPLOAD:
            st.error(f"❌ Too many files! Maximum {MAX_FILES_PER_UPLOAD} files allowed. Please upload fewer files.")
            uploaded_files = uploaded_files[:MAX_FILES_PER_UPLOAD]  # Limit to max files
            st.info(f"⚠️ Processing first {MAX_FILES_PER_UPLOAD} files only.")
        
        # Show upload summary
        if uploaded_files:
            total_size = sum(len(file.getvalue()) for file in uploaded_files)
            total_size_mb = total_size / (1024 * 1024)
            st.info(f"📊 **Upload Summary:** {len(uploaded_files)} file(s), Total size: {total_size_mb:.2f} MB")
        
        # Input for required skills
        st.markdown("### 🎯 Required Skills")
        required_skills_input = st.text_input(
            "Enter required skills (comma-separated)",
            key="required_skills",
            help="Example: Python, Java, Machine Learning, SQL",
            placeholder="Python, Java, Machine Learning, SQL, React..."
        )
        
        # Validate and parse skills
        required_skills = validate_skills_input(required_skills_input) if required_skills_input else []
        
        # Button to save required skills
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("💾 Save Required Skills", type="primary") and required_skills:
                try:
                    save_required_skills(required_skills)
                    create_success_card("Skills Saved!", f"Successfully saved {len(required_skills)} skills to database")
                except Exception as e:
                    log_error(logger, e, {'operation': 'save_skills'})
                    st.error("❌ Error saving skills. Please try again.")
        
        # Process uploaded files
        if uploaded_files:
            if not required_skills:
                st.warning("⚠️ Please enter required skills to match against resumes.")
            
            process_resumes(uploaded_files, required_skills)
            
    except Exception as e:
        log_error(logger, e, {'operation': 'process_recruiters_mode'})
        st.error("❌ An error occurred. Please try again.")


def process_resumes(uploaded_files: List, required_skills: List[str]) -> None:
    """
    Process multiple resumes and match against required skills.
    
    Args:
        uploaded_files: List of uploaded file objects
        required_skills: List of required skills to match
    """
    try:
        st.markdown("---")
        st.subheader(f"📄 Processing {len(uploaded_files)} resume(s)...")
        
        all_skills_found = set()
        processed_count = 0
        
        # Progress bar for bulk processing
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, file in enumerate(uploaded_files):
            # Update progress
            progress = (idx + 1) / len(uploaded_files)
            progress_bar.progress(progress)
            status_text.text(f"Processing file {idx + 1} of {len(uploaded_files)}: {file.name}")
            try:
                # Validate file
                is_valid, error_message = validate_file_upload(file)
                if not is_valid:
                    st.warning(f"⚠️ Skipping {file.name}: {error_message}")
                    continue
                
                with st.spinner(f"Processing {file.name}..."):
                    # Extract text from PDF
                    text = extract_text_from_pdf(file)
                    if not text:
                        st.warning(f"⚠️ Could not extract text from {file.name}")
                        continue
                    
                    # Process with spaCy
                    doc = nlp(text)
                    
                    # Extract candidate information using improved name extraction
                    # Pass filename for better fallback
                    first_name, last_name = extract_name(doc)
                    
                    # Fallback to filename if name not found in document
                    if not first_name or len(first_name.strip()) == 0:
                        first_name, last_name = extract_name_from_filename(file.name)
                        if first_name:
                            logger.info(f"Extracted name from filename: {first_name} {last_name} (file: {file.name})")
                    
                    # Format candidate name
                    if first_name and last_name:
                        candidate_name = f"{first_name} {last_name}"
                    elif first_name:
                        candidate_name = first_name
                    else:
                        candidate_name = "Candidate name not found"
                    
                    display_candidate_info(candidate_name, file.name)
                    
                    # Extract and display all skills
                    parsed_skills = extract_all_skills(doc)
                    display_parsed_skills(parsed_skills)
                    
                    # Match required skills
                    if required_skills:
                        skills_found = extract_skills(doc, required_skills)
                        display_skills_found(required_skills, skills_found)
                        all_skills_found.update(skills_found)
                    
                    processed_count += 1
                    st.markdown("---")
                    
            except Exception as e:
                log_error(logger, e, {'operation': 'process_resume', 'file': file.name})
                st.error(f"❌ Error processing {file.name}. Skipping...")
                continue
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Summary
        if processed_count > 0:
            st.success(f"✅ Successfully processed {processed_count} resume(s)")
            if required_skills and all_skills_found:
                st.info(f"📊 Found {len(all_skills_found)} out of {len(required_skills)} required skills across all resumes")
                
    except Exception as e:
        log_error(logger, e, {'operation': 'process_resumes'})
        st.error("❌ Error processing resumes. Please try again.")


def save_required_skills(required_skills: List[str]) -> None:
    """
    Save required skills to CSV file.
    
    Args:
        required_skills: List of skill names to save
    """
    try:
        with open(UPDATED_SKILLS_CSV, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for skill in required_skills:
                writer.writerow([skill])
        logger.info(f"Saved {len(required_skills)} skills to {UPDATED_SKILLS_CSV}")
    except Exception as e:
        log_error(logger, e, {'operation': 'save_required_skills'})
        raise


def extract_text_from_pdf(file) -> str:
    """
    Extract text from PDF file.
    
    Args:
        file: Uploaded file object
        
    Returns:
        Extracted text as string
    """
    try:
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        pdf_document.close()
        return text
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_text_from_pdf', 'file': file.name})
        return ""


def extract_candidate_name(doc, filename: Optional[str] = None) -> str:
    """
    Extract candidate's full name using improved extraction logic.
    Uses the same robust name extraction as the users module.
    
    Args:
        doc: spaCy document object
        filename: Optional filename for fallback extraction
        
    Returns:
        Candidate name or default message
    """
    try:
        # Use the improved extract_name function from resume_parser
        first_name, last_name = extract_name(doc)
        
        # Fallback to filename if name not found in document
        if not first_name and filename:
            first_name, last_name = extract_name_from_filename(filename)
        
        # Format candidate name
        if first_name and last_name:
            return f"{first_name} {last_name}"
        elif first_name:
            return first_name
        else:
            return "Candidate name not found"
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_candidate_name'})
        return "Error extracting name"


def extract_all_skills(doc) -> Set[str]:
    """
    Extract all skills from the resume.
    
    Args:
        doc: spaCy document object
        
    Returns:
        Set of extracted skills
    """
    try:
        all_skills = set()
        for token in doc:
            if token.pos_ == 'NOUN' and token.text.isalpha() and len(token.text) > 1:
                all_skills.add(token.text.lower())
        return all_skills
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_all_skills'})
        return set()


def extract_skills(doc, required_skills: List[str]) -> Set[str]:
    """
    Extract skills using SpaCy Matcher.
    
    Args:
        doc: spaCy document object
        required_skills: List of required skills to match
        
    Returns:
        Set of found skills
    """
    try:
        matcher = Matcher(nlp.vocab)
        skills_found = set()
        
        for skill in required_skills:
            pattern = [{"LOWER": skill.lower()}]
            matcher.add(skill, [pattern])
        
        matches = matcher(doc)
        for match_id, start, end in matches:
            matched_skill = doc[start:end].text.lower()
            skills_found.add(matched_skill)
        
        return skills_found
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_skills'})
        return set()


def display_candidate_info(candidate_name: str, file_name: str) -> None:
    """
    Display candidate information with modern UI.
    
    Args:
        candidate_name: Name of the candidate
        file_name: Name of the uploaded file
    """
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    ">
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        create_metric_card("📄 File", file_name, icon="📄")
    with col2:
        create_metric_card("👤 Candidate", candidate_name, icon="👤")


def display_parsed_skills(parsed_skills: Set[str]) -> None:
    """
    Display parsed skills from the resume with modern UI.
    
    Args:
        parsed_skills: Set of parsed skills
    """
    if parsed_skills:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border-left: 5px solid #e74c3c;
        ">
            <h4 style="color: white; margin-top: 0;">💼 All Skills Parsed from Resume</h4>
        </div>
        """, unsafe_allow_html=True)
        from utils.ui_components import display_skill_tags
        display_skill_tags(list(parsed_skills)[:30], color_scheme="pink")  # Limit to 30 for display
    else:
        create_info_card("Skills", "No skills parsed from resume")


def display_skills_found(required_skills: List[str], skills_found: Set[str]) -> None:
    """
    Display skills found or not found with modern UI.
    
    Args:
        required_skills: List of required skills
        skills_found: Set of found skills
    """
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #27ae60;
    ">
        <h4 style="color: #2c3e50; margin-top: 0;">🎯 Skills Match Results</h4>
    </div>
    """, unsafe_allow_html=True)
    
    found_count = 0
    found_skills = []
    missing_skills = []
    
    for skill in required_skills:
        if skill.lower() in skills_found:
            found_skills.append(skill)
            found_count += 1
        else:
            missing_skills.append(skill)
    
    # Display found skills
    if found_skills:
        st.markdown("### ✅ Found Skills")
        from utils.ui_components import display_skill_tags
        display_skill_tags(found_skills, color_scheme="green")
    
    # Display missing skills
    if missing_skills:
        st.markdown("### ❌ Missing Skills")
        display_skill_tags(missing_skills, color_scheme="red")
    
    # Summary metric
    match_percentage = (found_count / len(required_skills) * 100) if required_skills else 0
    col1, col2, col3 = st.columns(3)
    with col1:
        create_metric_card("Found", str(found_count), icon="✅")
    with col2:
        create_metric_card("Total", str(len(required_skills)), icon="📊")
    with col3:
        create_metric_card("Match Rate", f"{match_percentage:.1f}%", icon="🎯")


if __name__ == "__main__":
    process_recruiters_mode()
