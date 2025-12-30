"""
Translation utilities for multi-language resume parsing.
Translates non-English resumes to English for processing.
"""
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Try to import translation libraries
TRANSLATOR_AVAILABLE = False
translator = None

try:
    from googletrans import Translator
    translator = Translator()
    TRANSLATOR_AVAILABLE = True
except ImportError:
    try:
        # Try alternative: deep-translator
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator
        TRANSLATOR_AVAILABLE = True
    except ImportError:
        logger.warning(
            "Translation library not installed. "
            "Install with: pip install googletrans==4.0.0-rc1 "
            "or pip install deep-translator"
        )


def translate_to_english(text: str, source_lang: Optional[str] = None) -> str:
    """
    Translate text to English.
    
    Args:
        text: Text to translate
        source_lang: Source language code (optional, will detect if not provided)
        
    Returns:
        Translated text in English, or original text if translation fails
    """
    if not TRANSLATOR_AVAILABLE:
        logger.warning("Translation not available, returning original text")
        return text
    
    if not text or len(text.strip()) < 5:
        return text  # Too short to translate
    
    try:
        # If using googletrans
        if hasattr(translator, 'translate'):
            if source_lang:
                if source_lang == 'en':
                    return text  # Already English
                translated = translator.translate(text, src=source_lang, dest='en')
                return translated.text
            else:
                # Auto-detect language
                detected = translator.detect(text)
                if detected.lang == 'en':
                    return text  # Already English
                translated = translator.translate(text, src=detected.lang, dest='en')
                return translated.text
        
        # If using deep-translator
        elif hasattr(translator, 'translate'):
            if source_lang and source_lang != 'en':
                trans = translator(source=source_lang, target='en')
                return trans.translate(text)
            else:
                # Auto-detect and translate
                trans = translator(source='auto', target='en')
                return trans.translate(text)
        
        return text
        
    except Exception as e:
        logger.warning(f"Translation failed: {e}, returning original text")
        return text  # Return original if translation fails


def translate_text(text: str, target_lang: str = 'en', source_lang: Optional[str] = None) -> str:
    """
    Translate text to target language.
    
    Args:
        text: Text to translate
        target_lang: Target language code (default: 'en')
        source_lang: Source language code (optional)
        
    Returns:
        Translated text
    """
    if target_lang == 'en':
        return translate_to_english(text, source_lang)
    
    if not TRANSLATOR_AVAILABLE:
        return text
    
    try:
        if hasattr(translator, 'translate'):
            if source_lang:
                translated = translator.translate(text, src=source_lang, dest=target_lang)
                return translated.text
            else:
                translated = translator.translate(text, dest=target_lang)
                return translated.text
        return text
    except Exception as e:
        logger.warning(f"Translation to {target_lang} failed: {e}")
        return text

