"""
Resume parser utilities for Resume Parser NLP Application.
Handles PDF parsing and information extraction from resumes.
"""
import re
import fitz
import streamlit as st
import spacy
import csv
import nltk
from typing import Tuple, List, Dict, Any, Optional, Set
from pathlib import Path

from config import SKILLS_CSV, MAJORS_CSV, POSITION_CSV, SUGGESTED_SKILLS_CSV, TRAINED_MODEL_PATH, SPACY_MODEL
from utils.logger import setup_logger, log_error

# Setup logger
logger = setup_logger(__name__)

# Download NLTK data (only if not already downloaded)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        # Try downloading with SSL verification
        nltk.download('punkt', quiet=True)
        logger.info("NLTK punkt tokenizer downloaded successfully")
    except Exception as download_error:
        # Handle SSL certificate errors (common on macOS)
        error_str = str(download_error).lower()
        if 'ssl' in error_str or 'certificate' in error_str:
            logger.warning("SSL certificate error when downloading NLTK data. Using workaround...")
            try:
                # Workaround for macOS SSL certificate issues
                import ssl
                original_ssl_context = ssl._create_default_https_context
                ssl._create_default_https_context = ssl._create_unverified_context
                try:
                    nltk.download('punkt', quiet=True)
                    logger.info("NLTK punkt tokenizer downloaded (SSL verification disabled)")
                finally:
                    ssl._create_default_https_context = original_ssl_context
            except Exception as e:
                logger.warning(f"Could not download NLTK punkt tokenizer: {e}")
                logger.info("Application will continue. Some NLP features may be limited.")
                logger.info("To fix manually, run: python -c \"import nltk; nltk.download('punkt')\"")
        else:
            logger.warning(f"Could not download NLTK punkt: {download_error}")
            logger.info("Application will continue. Some NLP features may be limited.")

# Load the spaCy model for English
try:
    nlp = spacy.load(SPACY_MODEL)
    logger.info(f"Loaded spaCy model: {SPACY_MODEL}")
except OSError as e:
    logger.error(f"Failed to load spaCy model {SPACY_MODEL}: {e}")
    raise

def load_keywords(file_path: Path) -> Set[str]:
    """
    Load keywords from CSV file.
    Skips header row if present.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Set of keywords
    """
    try:
        keywords = set()
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            
            # Check if first row looks like a header (common header words)
            header_keywords = {'major', 'skill', 'position', 'keywords', 'name', 'title'}
            start_idx = 0
            if rows and rows[0] and rows[0][0].lower() in header_keywords:
                start_idx = 1  # Skip header row
            
            # Extract keywords from remaining rows
            for row in rows[start_idx:]:
                if row and row[0].strip():  # Check if row has data and first column is not empty
                    keywords.add(row[0].strip())
        
        return keywords
    except FileNotFoundError:
        logger.error(f"Keywords file not found: {file_path}")
        return set()
    except Exception as e:
        log_error(logger, e, {'operation': 'load_keywords', 'file': str(file_path)})
        return set()

def extract_name(doc) -> Tuple[str, str]:
    """
    Extract first and last name from resume using multiple strategies.
    Improved to prioritize names at the top of resume and filter false positives.
    
    Args:
        doc: spaCy document object
        
    Returns:
        Tuple of (first_name, last_name)
    """
    try:
        doc_text = doc.text if hasattr(doc, 'text') else str(doc)
        
        # Words that indicate organization/educational institution (not person names)
        org_keywords = {
            'college', 'university', 'institute', 'school', 'academy', 
            'corporation', 'company', 'ltd', 'inc', 'llc', 'pvt', 'limited',
            'department', 'faculty', 'campus', 'technologies', 'solutions',
            'systems', 'services', 'group', 'industries', 'enterprises'
        }
        
        # Common job titles that might be mistaken for names
        job_titles = {
            'engineer', 'developer', 'manager', 'director', 'analyst', 'consultant',
            'specialist', 'coordinator', 'assistant', 'executive', 'officer',
            'lead', 'senior', 'junior', 'intern', 'trainee', 'associate'
        }
        
        # Place name suffixes (common in Indian addresses/locations)
        place_suffixes = {
            'ganj', 'nagar', 'pur', 'abad', 'garh', 'pura', 'nagar', 'vihar',
            'colony', 'road', 'street', 'lane', 'avenue', 'marg', 'path',
            'village', 'town', 'city', 'state', 'district', 'taluka', 'tehsil'
        }
        
        # Common prefixes/titles to skip
        name_prefixes = {'mr', 'mrs', 'miss', 'ms', 'dr', 'professor', 'prof', 'sir', 'madam', 'mr.', 'mrs.', 'ms.', 'dr.'}
        
        # Get first 200 characters (where name typically appears)
        first_part = doc_text[:200].lower()
        
        # Strategy 1: Use spaCy NER to find PERSON entities, prioritizing those at the top
        person_entities = []
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                names = ent.text.split()
                # Filter out common false positives
                if len(names) >= 2:
                    # CRITICAL: Check if this entity is actually a location (GPE, LOC, FAC)
                    # Check surrounding context for location indicators
                    ent_text_lower = ent.text.lower()
                    
                    # Skip if contains place name suffixes
                    if any(suffix in ent_text_lower for suffix in place_suffixes):
                        continue
                    
                    # Skip if contains job titles
                    if any(title in ent_text_lower for title in job_titles):
                        continue
                    
                    # Check if any word ends with place suffix
                    if any(word.lower().endswith(tuple(place_suffixes)) for word in names):
                        continue
                    
                    # Check if it's identified as location in the document
                    # Look for nearby entities that might indicate it's a location
                    skip_this = False
                    for other_ent in doc.ents:
                        if other_ent.start <= ent.end + 50 and other_ent.start >= ent.start - 50:
                            # If nearby entity is GPE, LOC, or FAC, this might be a location too
                            if other_ent.label_ in ['GPE', 'LOC', 'FAC'] and other_ent.text.lower() in ent_text_lower:
                                skip_this = True
                                break
                    if skip_this:
                        continue
                    
                    # Check if it looks like a name (all words are title case, not all caps)
                    if all(name.istitle() or name.isupper() for name in names):
                        # Skip if it's too long (probably not a name)
                        if len(names) <= 4:
                            # Skip common non-name words and prefixes
                            if not any(word.lower() in name_prefixes for word in names):
                                # CRITICAL: Check if any word is an organization keyword
                                if not any(word.lower() in org_keywords for word in names):
                                    # Check if first name is not just an initial (like "S.")
                                    first_name = names[0]
                                    if len(first_name) > 1 or (len(first_name) == 1 and first_name.isalpha()):
                                        # Verify it's not an organization by checking context
                                        if not any(keyword in ent_text_lower for keyword in org_keywords):
                                            # Check position - prioritize names at the top (first 200 chars)
                                            ent_position = ent.start_char
                                            is_at_top = ent_position < 200
                                            person_entities.append({
                                                'names': names,
                                                'position': ent_position,
                                                'is_at_top': is_at_top,
                                                'text': ent.text
                                            })
        
        # Sort person entities: prioritize those at the top
        person_entities.sort(key=lambda x: (not x['is_at_top'], x['position']))
        
        # Return the first valid person entity (preferably at the top)
        for entity in person_entities:
            names = entity['names']
            # Additional validation: check if it appears before email/phone/address
            entity_text_lower = entity['text'].lower()
            context_after = doc_text[entity['position']:min(len(doc_text), entity['position']+100)].lower()
            
            # If name is at top and followed by contact info, it's likely the candidate name
            # Contact info (email, phone) usually comes right after name in resumes
            if entity['is_at_top']:
                # Check if followed by contact info - this is a good sign it's the candidate name
                has_contact_info = any(indicator in context_after[:80] for indicator in ['@', 'email', 'phone', 'mobile', 'address'])
                # Also check if it's NOT followed by job title or company name
                has_job_info = any(indicator in context_after[:80] for indicator in job_titles.union(org_keywords))
                
                # If at top and has contact info but no job info, it's likely the name
                if has_contact_info and not has_job_info:
                    return names[0], ' '.join(names[1:])
                # If at top and no job info nearby, also likely the name
                elif not has_job_info:
                    return names[0], ' '.join(names[1:])
            else:
                # Not at top, but if no job/org keywords nearby, might still be valid
                if not any(keyword in context_after[:50] for keyword in job_titles.union(org_keywords)):
                    return names[0], ' '.join(names[1:])
        
        # Strategy 2: Extract from first few lines (where name typically appears)
        lines = doc_text.split('\n')
        first_lines = lines[:3]  # Check only first 3 lines (name is usually at the very top)
        
        for line in first_lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip lines that are clearly not names
            skip_patterns = ['email', 'phone', 'address', 'resume', 'cv', '@', 'www.', 'http', 'linkedin', 'github', 'portfolio']
            if any(skip in line.lower() for skip in skip_patterns):
                continue
            
            # Skip if line contains job title keywords
            if any(title in line.lower() for title in job_titles):
                continue
            
            # CRITICAL: Skip lines with organization keywords
            if any(keyword in line.lower() for keyword in org_keywords):
                continue
            
            # CRITICAL: Skip lines with place name suffixes
            place_suffixes = {
                'ganj', 'nagar', 'pur', 'abad', 'garh', 'pura', 'nagar', 'vihar',
                'colony', 'road', 'street', 'lane', 'avenue', 'marg', 'path',
                'village', 'town', 'city', 'state', 'district', 'taluka', 'tehsil'
            }
            if any(suffix in line.lower() for suffix in place_suffixes):
                continue
            
            # Check if line looks like a name (2-4 words, all title case)
            words = line.split()
            if 2 <= len(words) <= 4:
                # Check if all words are title case or proper nouns
                if all(word.istitle() or word.isupper() for word in words):
                    # Additional validation: should not contain numbers or special chars (except hyphens and periods)
                    if all(re.match(r'^[A-Za-z\-\.]+$', word) for word in words):
                        # Skip if any word ends with place suffix
                        if any(word.lower().endswith(tuple(place_suffixes)) for word in words):
                            continue
                        
                        # Skip if first word is just an initial (like "S.") without a full name
                        if len(words[0]) > 1 or (len(words) >= 3):  # Allow initial if there are 3+ words
                            # Process with spaCy to verify it's a person and not an org/location
                            line_doc = nlp(line)
                            is_person = False
                            is_org = False
                            is_location = False
                            
                            for ent in line_doc.ents:
                                if ent.label_ == 'PERSON':
                                    is_person = True
                                elif ent.label_ == 'ORG':
                                    is_org = True
                                elif ent.label_ in ['GPE', 'LOC', 'FAC']:  # Location entities
                                    is_location = True
                            
                            # Only accept if it's identified as PERSON and NOT as ORG or LOCATION
                            if is_person and not is_org and not is_location:
                                names = words
                                # Remove any prefixes
                                names = [n for n in names if n.lower() not in name_prefixes]
                                if len(names) >= 2:
                                    return names[0], ' '.join(names[1:])
                            # If NER doesn't catch it but pattern matches and no org/location keywords, use it
                            elif not is_org and not is_location and not any(keyword in line.lower() for keyword in org_keywords):
                                # Additional check: first name should be at least 2 chars (not just "S.")
                                # Remove prefixes
                                words = [w for w in words if w.lower() not in name_prefixes]
                                if len(words) >= 2 and len(words[0]) >= 2:
                                    return words[0], ' '.join(words[1:])
        
        # Strategy 3: Pattern matching for common name patterns
        # Look for patterns like "First Last" or "First Middle Last"
        name_pattern = r'^([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]+){1,3})$'  # First name must be at least 3 chars
        for line in first_lines[:3]:
            line = line.strip()
            # Skip if contains org keywords
            if any(keyword in line.lower() for keyword in org_keywords):
                continue
            match = re.match(name_pattern, line)
            if match:
                names = match.group(1).split()
                if 2 <= len(names) <= 4:
                    return names[0], ' '.join(names[1:])
        
        return "", ""
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_name'})
        return "", ""

def extract_email(doc) -> str:
    """
    Extract email address from resume.
    
    Args:
        doc: spaCy document object
        
    Returns:
        Email address or empty string
    """
    try:
        matcher = spacy.matcher.Matcher(nlp.vocab)
        email_pattern = [{'LIKE_EMAIL': True}]
        matcher.add('EMAIL', [email_pattern])

        matches = matcher(doc)
        for match_id, start, end in matches:
            if match_id == nlp.vocab.strings['EMAIL']:
                return doc[start:end].text
        return ""
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_email'})
        return ""

def extract_contact_number_from_resume(doc) -> Optional[str]:
    """
    Extract contact number from resume.
    
    Args:
        doc: spaCy document object
        
    Returns:
        Contact number or None
    """
    try:
        text = doc.text if hasattr(doc, 'text') else str(doc)
        pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
        match = re.search(pattern, text)
        if match:
            return match.group()
        return None
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_contact_number'})
        return None

def extract_education_from_resume(doc) -> List[str]:
    """
    Extract education information from resume.
    
    Args:
        doc: spaCy document object or text string
        
    Returns:
        List of educational institutions
    """
    try:
        universities = []
        
        # Process the document with spaCy if it's a string
        if isinstance(doc, str):
            processed_doc = nlp(doc)
        else:
            processed_doc = doc

        # Iterate through entities and check for organizations (universities)
        for entity in processed_doc.ents:
            if entity.label_ == "ORG":
                entity_lower = entity.text.lower()
                if any(keyword in entity_lower for keyword in ["university", "college", "institute"]):
                    universities.append(entity.text)

        return universities
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_education'})
        return []

def csv_skills(doc) -> Set[str]:
    """
    Extract skills from resume using CSV keyword matching.
    
    Args:
        doc: spaCy document object
        
    Returns:
        Set of extracted skills
    """
    try:
        skills_keywords = load_keywords(SKILLS_CSV)
        skills = set()
        doc_text = doc.text if hasattr(doc, 'text') else str(doc)
        doc_text_lower = doc_text.lower()

        for keyword in skills_keywords:
            if keyword.lower() in doc_text_lower:
                skills.add(keyword)

        return skills
    except Exception as e:
        log_error(logger, e, {'operation': 'csv_skills'})
        return set()

# Try to load the trained NER model for skills, fallback to None if not available
nlp_skills: Optional[Any] = None
try:
    if TRAINED_MODEL_PATH.exists() and TRAINED_MODEL_PATH.is_dir():
        # Check if model directory has required files
        meta_json = TRAINED_MODEL_PATH / 'meta.json'
        if meta_json.exists():
            nlp_skills = spacy.load(str(TRAINED_MODEL_PATH))
            logger.info("✅ Loaded trained skill extraction model successfully")
        else:
            logger.info("ℹ️ Trained model directory exists but is incomplete. Using CSV-based skill extraction.")
    else:
        logger.info("ℹ️ Trained skill model not found. Using CSV-based skill extraction (this is normal if model hasn't been trained yet).")
except (OSError, Exception) as e:
    logger.warning(f"⚠️ Could not load trained skill model. Using CSV-based skill extraction only. Error: {e}")
    logger.info("💡 To train the model, run: python scripts/train_model.py")

def extract_skills_from_ner(doc) -> Set[str]:
    """
    Extract skills using trained NER model if available.
    
    Args:
        doc: spaCy document object
        
    Returns:
        Set of extracted skills
    """
    if nlp_skills is None:
        return set()
    
    try:
        non_skill_labels = {'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL', 'EMAIL'}
        doc_text = doc.text if hasattr(doc, 'text') else str(doc)
        
        skills = set()
        for ent in nlp_skills(doc_text).ents:
            if ent.label_ == 'SKILL':
                if ent.label_ not in non_skill_labels and not ent.text.isdigit():
                    skill_text = ''.join(filter(str.isalpha, ent.text))
                    if skill_text:
                        skills.add(skill_text)
        return skills
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_skills_from_ner'})
        return set()


def is_valid_skill(skill_text: str) -> bool:
    """
    Validate if a skill text is valid.
    
    Args:
        skill_text: Skill text to validate
        
    Returns:
        True if valid, False otherwise
    """
    return len(skill_text) > 1 and not any(char.isdigit() for char in skill_text)


def extract_skills(doc) -> List[str]:
    """
    Extract skills from resume using both CSV and NER methods.
    
    Args:
        doc: spaCy document object
        
    Returns:
        List of extracted skills
    """
    try:
        skills_csv = csv_skills(doc)
        skills_ner = extract_skills_from_ner(doc)
        
        filtered_skills_csv = {skill for skill in skills_csv if is_valid_skill(skill)}
        filtered_skills_ner = {skill for skill in skills_ner if is_valid_skill(skill)}
        
        combined_skills = filtered_skills_csv.union(filtered_skills_ner)
        
        return list(combined_skills)
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_skills'})
        return []

# --------------------------------------------------------------------------------

def extract_major(doc) -> str:
    """
    Extract major/degree from resume.
    Uses multiple strategies: exact match, partial match, and common degree patterns.
    
    Args:
        doc: spaCy document object
        
    Returns:
        Major/degree name or empty string
    """
    try:
        major_keywords = load_keywords(MAJORS_CSV)
        doc_text = doc.text if hasattr(doc, 'text') else str(doc)
        doc_text_lower = doc_text.lower()
        
        # Strategy 1: Exact match (case-insensitive)
        for keyword in major_keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in doc_text_lower:
                return keyword
        
        # Strategy 2: Partial match (for cases like "Computer Science" matching "COMPUTER SCIENCE")
        # Split major keywords and check if all significant words appear
        for keyword in major_keywords:
            keyword_lower = keyword.lower()
            # Split into words and check if all significant words (length > 3) appear
            keyword_words = [w for w in keyword_lower.split() if len(w) > 3]
            if keyword_words and all(word in doc_text_lower for word in keyword_words):
                return keyword
        
        # Strategy 3: Common degree patterns (B.Tech, B.E., M.Tech, etc.)
        degree_patterns = {
            r'\b(b\.?tech|bachelor.*technology)\b': 'ENGINEERING',
            r'\b(b\.?e\.?|bachelor.*engineering)\b': 'ENGINEERING',
            r'\b(m\.?tech|master.*technology)\b': 'ENGINEERING',
            r'\b(b\.?sc|bachelor.*science)\b': 'SCIENCE',
            r'\b(m\.?sc|master.*science)\b': 'SCIENCE',
            r'\b(b\.?com|bachelor.*commerce)\b': 'COMMERCE',
            r'\b(mba|master.*business)\b': 'BUSINESS ADMINISTRATION',
            r'\b(b\.?a\.?|bachelor.*arts)\b': 'ARTS',
            r'\b(m\.?a\.?|master.*arts)\b': 'ARTS',
        }
        
        for pattern, degree_type in degree_patterns.items():
            if re.search(pattern, doc_text_lower):
                # Try to find a more specific major from keywords
                for keyword in major_keywords:
                    if degree_type.lower() in keyword.lower() or keyword.lower() in degree_type.lower():
                        return keyword
                # If no specific match, return the degree type
                return degree_type
        
        return ""
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_major'})
        return ""

def extract_experience(doc) -> Dict[str, str]:
    """
    Extract experience level from resume.
    
    Args:
        doc: spaCy document object
        
    Returns:
        Dictionary with level_of_experience and suggested_position
    """
    try:
        verbs = [token.text.lower() for token in doc if token.pos_ == 'VERB']

        senior_keywords = ['lead', 'manage', 'direct', 'oversee', 'supervise', 'orchestrate', 'govern']
        mid_senior_keywords = ['develop', 'design', 'analyze', 'implement', 'coordinate', 'execute', 'strategize']
        mid_junior_keywords = ['assist', 'support', 'collaborate', 'participate', 'aid', 'facilitate', 'contribute']
        
        if any(keyword in verbs for keyword in senior_keywords):
            level_of_experience = "Senior"
        elif any(keyword in verbs for keyword in mid_senior_keywords):
            level_of_experience = "Mid-Senior"
        elif any(keyword in verbs for keyword in mid_junior_keywords):
            level_of_experience = "Mid-Junior"
        else:
            level_of_experience = "Entry Level"

        suggested_position = suggest_position(verbs)

        return {
            'level_of_experience': level_of_experience,
            'suggested_position': suggested_position
        }
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_experience'})
        return {
            'level_of_experience': "Unknown",
            'suggested_position': "Not Identified"
        }


def load_positions_keywords(file_path: Path) -> Dict[str, List[str]]:
    """
    Load position keywords from CSV file.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Dictionary mapping positions to keywords
    """
    try:
        positions_keywords = {}
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                position = row.get('position', '')
                keywords_str = row.get('keywords', '')
                keywords = [keyword.strip().lower() for keyword in keywords_str.split(',') if keyword.strip()]
                if position:
                    positions_keywords[position] = keywords
        return positions_keywords
    except FileNotFoundError:
        logger.error(f"Positions file not found: {file_path}")
        return {}
    except Exception as e:
        log_error(logger, e, {'operation': 'load_positions_keywords', 'file': str(file_path)})
        return {}


def suggest_position(verbs: List[str]) -> str:
    """
    Suggest position based on verbs found in resume.
    
    Args:
        verbs: List of verb tokens from resume
        
    Returns:
        Suggested position name
    """
    try:
        positions_keywords = load_positions_keywords(POSITION_CSV)
        verbs_lower = [verb.lower() for verb in verbs]
        
        for position, keywords in positions_keywords.items():
            if any(keyword in verbs_lower for keyword in keywords):
                return position

        return "Position Not Identified"
    except Exception as e:
        log_error(logger, e, {'operation': 'suggest_position'})
        return "Position Not Identified"


def extract_resume_info_from_pdf(uploaded_file) -> Any:
    """
    Extract text from PDF and process with spaCy.
    
    Args:
        uploaded_file: Uploaded file object
        
    Returns:
        spaCy document object
    """
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        
        if not text.strip():
            logger.warning("No text extracted from PDF")
            return nlp("")
        
        return nlp(text)
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_resume_info_from_pdf'})
        return nlp("")


def show_colored_skills(skills: List[str]) -> None:
    """
    Display skills in Streamlit.
    
    Args:
        skills: List of skill names
    """
    if skills:
        st.write(', '.join(skills))
    else:
        st.info("No skills found")


def calculate_resume_score(resume_info: Dict[str, Any]) -> int:
    """
    Calculate resume completeness score.
    
    Args:
        resume_info: Dictionary containing resume information
        
    Returns:
        Score out of 100
    """
    try:
        score = 0
        if resume_info.get('first_name') and resume_info.get('last_name'):
            score += 25
        if resume_info.get('email'):
            score += 25
        if resume_info.get('degree_major'):
            score += 25
        if resume_info.get('skills'):
            score += 25
        return score
    except Exception as e:
        log_error(logger, e, {'operation': 'calculate_resume_score'})
        return 0


def extract_name_from_filename(filename: str) -> Tuple[str, str]:
    """
    Extract name from filename as fallback.
    Handles patterns like "111121112_ShivamKumarMishra_.pdf" or "Shivam_Kumar_Mishra.pdf"
    
    Args:
        filename: PDF filename
        
    Returns:
        Tuple of (first_name, last_name)
    """
    try:
        # Remove extension
        name_part = Path(filename).stem
        
        # Remove common prefixes/suffixes (numbers, underscores, etc.)
        # Pattern: remove leading numbers and underscores
        name_part = re.sub(r'^[\d_]+', '', name_part)
        name_part = re.sub(r'[_]+$', '', name_part)
        
        # Split by underscore or camelCase
        # Try underscore first
        if '_' in name_part:
            parts = [p for p in name_part.split('_') if p]
        else:
            # Handle camelCase: "ShivamKumarMishra" -> ["Shivam", "Kumar", "Mishra"]
            parts = re.findall(r'[A-Z][a-z]+', name_part)
            if not parts:
                # If no camelCase, try to split by capital letters
                parts = re.split(r'(?=[A-Z])', name_part)
                parts = [p for p in parts if p]
        
        if len(parts) >= 2:
            # Capitalize first letter of each part
            parts = [p.capitalize() for p in parts if p.strip()]
            if len(parts) >= 2:
                return parts[0], ' '.join(parts[1:])
        
        return "", ""
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_name_from_filename', 'filename': filename})
        return "", ""


def extract_resume_info(doc, filename: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract all resume information.
    
    Args:
        doc: spaCy document object
        filename: Optional filename to use as fallback for name extraction
        
    Returns:
        Dictionary containing all extracted information
    """
    try:
        first_name, last_name = extract_name(doc)
        
        # Fallback to filename if name not found in document
        if not first_name and filename:
            first_name, last_name = extract_name_from_filename(filename)
            if first_name:
                logger.info(f"Extracted name from filename: {first_name} {last_name}")
        
        email = extract_email(doc)
        skills = extract_skills(doc)
        degree_major = extract_major(doc)
        experience = extract_experience(doc)

        return {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'degree_major': degree_major,
            'skills': skills,
            'experience': experience
        }
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_resume_info'})
        return {
            'first_name': '',
            'last_name': '',
            'email': '',
            'degree_major': '',
            'skills': [],
            'experience': {}
        }


def suggest_skills_for_job(desired_job: str) -> List[str]:
    """
    Suggest skills for a desired job position.
    
    Args:
        desired_job: Job title
        
    Returns:
        List of suggested skills
    """
    try:
        job_skills_mapping = {}
        
        with open(SUGGESTED_SKILLS_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    job_title = row[0].lower()
                    skills = [skill.strip() for skill in row[1:] if skill.strip()]
                    job_skills_mapping[job_title] = skills
        
        desired_job_lower = desired_job.lower().strip()
        if desired_job_lower in job_skills_mapping:
            return job_skills_mapping[desired_job_lower]
        else:
            return []
    except FileNotFoundError:
        logger.error(f"Suggested skills file not found: {SUGGESTED_SKILLS_CSV}")
        return []
    except Exception as e:
        log_error(logger, e, {'operation': 'suggest_skills_for_job', 'job': desired_job})
        return []


'''
def show_pdf(uploaded_file):
    try:
        with open(uploaded_file.name, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    except AttributeError:
        base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')

    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

'''
