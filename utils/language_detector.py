"""
Language detection utilities for multi-language resume parsing.
"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)

try:
    from langdetect import detect, DetectorFactory
    # Set seed for consistent results
    DetectorFactory.seed = 0
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    logger.warning("langdetect not installed. Install with: pip install langdetect")


def detect_language(text: str) -> str:
    """
    Detect language of text.
    
    Args:
        text: Text to detect language for
        
    Returns:
        Language code (e.g., 'en', 'hi', 'es', 'fr')
    """
    if not LANGDETECT_AVAILABLE:
        logger.warning("langdetect not available, defaulting to English")
        return 'en'
    
    if not text or len(text.strip()) < 10:
        return 'en'  # Default for short text
    
    try:
        lang = detect(text)
        return lang
    except Exception as e:
        logger.warning(f"Language detection failed: {e}, defaulting to English")
        return 'en'  # Default to English on error


def is_english(text: str) -> bool:
    """
    Check if text is in English.
    
    Args:
        text: Text to check
        
    Returns:
        True if English, False otherwise
    """
    detected = detect_language(text)
    return detected == 'en'

