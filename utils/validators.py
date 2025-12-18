"""
Input validation utilities for Resume Parser NLP Application.
"""
import re
from pathlib import Path
from typing import Optional, List, Tuple
from utils.logger import default_logger

from config import MAX_UPLOAD_SIZE, ALLOWED_EXTENSIONS


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not phone:
        return False
    
    # Remove common separators
    cleaned = re.sub(r'[-.\s()]', '', phone)
    # Check if it's a valid phone number (7-15 digits)
    return bool(re.match(r'^\+?\d{7,15}$', cleaned))


def validate_file_upload(file, max_size: Optional[int] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate uploaded file.
    
    Args:
        file: Uploaded file object
        max_size: Maximum file size in bytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if file is None:
        return False, "No file provided"
    
    # Check file extension
    file_extension = Path(file.name).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return False, f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check file size
    file_size = len(file.getvalue())
    max_file_size = max_size or MAX_UPLOAD_SIZE
    
    if file_size > max_file_size:
        size_mb = max_file_size / (1024 * 1024)
        return False, f"File size exceeds maximum allowed size of {size_mb}MB"
    
    if file_size == 0:
        return False, "File is empty"
    
    return True, None


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize user input to prevent XSS attacks.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    sanitized = re.sub(r'[^\w\s\-.,!?@#%&*()]', '', sanitized)  # Keep only safe characters
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
        default_logger.warning(f"Input truncated to {max_length} characters")
    
    return sanitized.strip()


def validate_skills_input(skills: str) -> List[str]:
    """
    Validate and parse skills input.
    
    Args:
        skills: Comma-separated skills string
        
    Returns:
        List of validated skill names
    """
    if not skills:
        return []
    
    # Split by comma and clean
    skill_list = [sanitize_input(skill.strip(), max_length=50) for skill in skills.split(',')]
    
    # Remove empty strings
    skill_list = [skill for skill in skill_list if skill]
    
    # Limit number of skills
    if len(skill_list) > 50:
        default_logger.warning(f"Too many skills provided, limiting to 50")
        skill_list = skill_list[:50]
    
    return skill_list

