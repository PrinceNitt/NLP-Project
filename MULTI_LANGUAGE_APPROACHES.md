# Multi-Language Resume Extraction - Approaches (हिंदी में) 🌍

## Overview

Aapka current application **sirf English** ke liye optimized hai. Multi-language support ke liye yeh approaches use kar sakte hain:

---

## 🎯 Approach 1: Language Detection + Multi-Language spaCy Models ⭐ **RECOMMENDED**

### Concept:
1. Resume ka language detect karo
2. Us language ka spaCy model load karo
3. Us model se information extract karo

### Advantages:
- ✅ Native language mein accurate extraction
- ✅ Language-specific patterns handle karta hai
- ✅ Best accuracy

### Disadvantages:
- ⚠️ Har language ke liye model download karna padega
- ⚠️ Memory usage zyada

### Implementation:

**Step 1: Language Detection Library Install**
```bash
pip install langdetect
# Ya
pip install polyglot
```

**Step 2: Code Implementation**

```python
# utils/language_detector.py (new file)
from langdetect import detect, DetectorFactory
import spacy
from typing import Optional

# Set seed for consistent results
DetectorFactory.seed = 0

# Language to spaCy model mapping
LANGUAGE_MODELS = {
    'en': 'en_core_web_sm',      # English
    'hi': 'xx_ent_wiki_sm',      # Hindi (multilingual model)
    'es': 'es_core_news_sm',      # Spanish
    'fr': 'fr_core_news_sm',     # French
    'de': 'de_core_news_sm',     # German
    'zh': 'zh_core_web_sm',      # Chinese
    'ja': 'ja_core_news_sm',     # Japanese
    'ru': 'ru_core_news_sm',     # Russian
    'pt': 'pt_core_news_sm',     # Portuguese
    'it': 'it_core_news_sm',     # Italian
    'nl': 'nl_core_news_sm',     # Dutch
    'pl': 'pl_core_news_sm',     # Polish
}

# Fallback to multilingual model
FALLBACK_MODEL = 'xx_ent_wiki_sm'  # Multilingual model

def detect_language(text: str) -> str:
    """Detect language of text."""
    try:
        lang = detect(text)
        return lang
    except:
        return 'en'  # Default to English

def get_spacy_model(language_code: str):
    """Get appropriate spaCy model for language."""
    try:
        model_name = LANGUAGE_MODELS.get(language_code, FALLBACK_MODEL)
        return spacy.load(model_name)
    except OSError:
        # If model not installed, use fallback
        logger.warning(f"Model for {language_code} not found, using fallback")
        return spacy.load(FALLBACK_MODEL)
```

**Step 3: Update resume_parser.py**

```python
# utils/resume_parser.py mein add karein
from utils.language_detector import detect_language, get_spacy_model

def extract_resume_info_from_pdf(uploaded_file):
    """Extract text and process with language-specific spaCy model."""
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        
        if not text.strip():
            return nlp("")  # Default English model
        
        # Detect language
        detected_lang = detect_language(text)
        logger.info(f"Detected language: {detected_lang}")
        
        # Load appropriate model
        nlp_model = get_spacy_model(detected_lang)
        
        # Process with language-specific model
        return nlp_model(text)
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_resume_info_from_pdf'})
        return nlp("")  # Fallback to English
```

### Required Models Download:

```bash
# English (already installed)
python -m spacy download en_core_web_sm

# Hindi/Multilingual
python -m spacy download xx_ent_wiki_sm

# Spanish
python -m spacy download es_core_news_sm

# French
python -m spacy download fr_core_news_sm

# German
python -m spacy download de_core_news_sm

# Chinese
python -m spacy download zh_core_web_sm

# Japanese
python -m spacy download ja_core_news_sm

# Russian
python -m spacy download ru_core_news_sm

# Portuguese
python -m spacy download pt_core_news_sm
```

---

## 🎯 Approach 2: Translation to English (Simple & Effective) ⭐ **EASY**

### Concept:
1. Resume ka language detect karo
2. English mein translate karo
3. English model se extract karo

### Advantages:
- ✅ Sirf English model chahiye
- ✅ Implementation easy
- ✅ Existing code reuse kar sakte hain

### Disadvantages:
- ⚠️ Translation quality par depend karta hai
- ⚠️ Some information loss possible
- ⚠️ Translation API cost (agar paid use karein)

### Implementation:

**Step 1: Translation Library Install**

**Option A: Google Translate (Free)**
```bash
pip install googletrans==4.0.0-rc1
```

**Option B: DeepL (Better quality, paid)**
```bash
pip install deepl
```

**Option C: Microsoft Translator**
```bash
pip install azure-cognitiveservices-language-translator
```

**Step 2: Code Implementation**

```python
# utils/translator.py (new file)
from googletrans import Translator
from typing import Optional

translator = Translator()

def translate_to_english(text: str, source_lang: Optional[str] = None) -> str:
    """Translate text to English."""
    try:
        if source_lang and source_lang == 'en':
            return text  # Already English
        
        # Detect language if not provided
        if not source_lang:
            detected = translator.detect(text)
            source_lang = detected.lang
        
        # Translate to English
        if source_lang != 'en':
            translated = translator.translate(text, src=source_lang, dest='en')
            return translated.text
        return text
    except Exception as e:
        logger.warning(f"Translation failed: {e}, using original text")
        return text  # Return original if translation fails
```

**Step 3: Update resume_parser.py**

```python
# utils/resume_parser.py mein
from utils.translator import translate_to_english
from utils.language_detector import detect_language

def extract_resume_info_from_pdf(uploaded_file):
    """Extract text, translate if needed, and process."""
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        
        if not text.strip():
            return nlp("")
        
        # Detect language
        detected_lang = detect_language(text)
        
        # Translate to English if needed
        if detected_lang != 'en':
            logger.info(f"Translating from {detected_lang} to English")
            text = translate_to_english(text, detected_lang)
        
        # Process with English model
        return nlp(text)
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_resume_info_from_pdf'})
        return nlp("")
```

---

## 🎯 Approach 3: Hybrid Approach (Best of Both) ⭐⭐⭐ **BEST**

### Concept:
1. Language detect karo
2. Agar English hai → directly process
3. Agar non-English hai → translate karke process
4. Important fields (name, email, phone) directly extract (language-independent)

### Advantages:
- ✅ Best accuracy for English
- ✅ Works for all languages
- ✅ Language-independent fields directly extract
- ✅ Balanced approach

### Implementation:

```python
# utils/multi_language_parser.py (new file)
import re
from typing import Dict, Any
from utils.language_detector import detect_language
from utils.translator import translate_to_english

def extract_language_independent_fields(text: str) -> Dict[str, Any]:
    """Extract fields that don't depend on language."""
    result = {}
    
    # Email (language-independent)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        result['email'] = email_match.group()
    
    # Phone (language-independent)
    phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        result['phone'] = phone_match.group()
    
    # URLs (language-independent)
    url_pattern = r'https?://[^\s]+|www\.[^\s]+'
    url_matches = re.findall(url_pattern, text)
    if url_matches:
        result['urls'] = url_matches
    
    return result

def extract_resume_multi_language(text: str) -> Dict[str, Any]:
    """Extract resume info with multi-language support."""
    # Step 1: Extract language-independent fields
    lang_independent = extract_language_independent_fields(text)
    
    # Step 2: Detect language
    detected_lang = detect_language(text)
    
    # Step 3: Process based on language
    if detected_lang == 'en':
        # Direct processing for English
        doc = nlp(text)
        extracted = extract_resume_info(doc)
    else:
        # Translate and process for non-English
        translated_text = translate_to_english(text, detected_lang)
        doc = nlp(translated_text)
        extracted = extract_resume_info(doc)
    
    # Merge results
    result = {**lang_independent, **extracted}
    result['detected_language'] = detected_lang
    
    return result
```

---

## 🎯 Approach 4: Pattern-Based Extraction (Language-Agnostic)

### Concept:
- Regular expressions use karke language-independent patterns extract karo
- Skills, emails, phones, etc. patterns se extract karo

### Advantages:
- ✅ No language detection needed
- ✅ Fast
- ✅ Works for most languages

### Disadvantages:
- ⚠️ Limited accuracy
- ⚠️ Context understanding nahi

### Implementation:

```python
# utils/pattern_extractor.py (new file)
import re
from typing import List, Set

def extract_email_pattern(text: str) -> str:
    """Extract email using pattern."""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(pattern, text)
    return match.group() if match else ""

def extract_phone_pattern(text: str) -> str:
    """Extract phone using pattern."""
    patterns = [
        r'\+\d{1,3}[-.\s]?\d{10}',  # International format
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
        r'\d{10}',  # Simple 10 digits
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return ""

def extract_skills_pattern(text: str, skills_list: List[str]) -> Set[str]:
    """Extract skills by matching against known skills list."""
    found_skills = set()
    text_lower = text.lower()
    
    for skill in skills_list:
        if skill.lower() in text_lower:
            found_skills.add(skill)
    
    return found_skills
```

---

## 📊 Comparison Table

| Approach | Accuracy | Complexity | Cost | Speed | Best For |
|----------|----------|------------|------|-------|----------|
| **Multi-Language Models** | ⭐⭐⭐⭐⭐ | High | Medium | Medium | Production |
| **Translation** | ⭐⭐⭐⭐ | Low | Low/Medium | Fast | Quick Implementation |
| **Hybrid** | ⭐⭐⭐⭐⭐ | Medium | Low | Fast | **Recommended** |
| **Pattern-Based** | ⭐⭐⭐ | Low | None | Very Fast | Simple Use Cases |

---

## 🚀 Recommended Implementation Plan

### Phase 1: Quick Start (Translation Approach)
1. Install `langdetect` and `googletrans`
2. Add language detection
3. Add translation to English
4. Test with Hindi/other language resumes

**Time:** 2-3 hours

### Phase 2: Enhanced (Hybrid Approach)
1. Add language-independent field extraction
2. Optimize translation (cache, batch)
3. Add language-specific models for major languages
4. Improve accuracy

**Time:** 1-2 days

### Phase 3: Production (Multi-Language Models)
1. Install language-specific spaCy models
2. Implement model switching
3. Add language detection UI
4. Performance optimization

**Time:** 3-5 days

---

## 💻 Complete Implementation Example

### Step 1: Install Dependencies

```bash
pip install langdetect googletrans==4.0.0-rc1
```

### Step 2: Create Language Detector

```python
# utils/language_detector.py
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0

def detect_language(text: str) -> str:
    """Detect language of text."""
    try:
        lang = detect(text)
        return lang
    except:
        return 'en'
```

### Step 3: Create Translator

```python
# utils/translator.py
from googletrans import Translator

translator = Translator()

def translate_to_english(text: str) -> str:
    """Translate text to English."""
    try:
        detected = translator.detect(text)
        if detected.lang == 'en':
            return text
        
        translated = translator.translate(text, src=detected.lang, dest='en')
        return translated.text
    except:
        return text
```

### Step 4: Update resume_parser.py

```python
# utils/resume_parser.py mein modify karein
from utils.language_detector import detect_language
from utils.translator import translate_to_english

def extract_resume_info_from_pdf(uploaded_file):
    """Extract text with multi-language support."""
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
        doc.close()
        
        if not text.strip():
            return nlp("")
        
        # Detect language
        detected_lang = detect_language(text)
        logger.info(f"Detected language: {detected_lang}")
        
        # Translate if not English
        if detected_lang != 'en':
            text = translate_to_english(text)
            logger.info("Translated to English for processing")
        
        # Process with English model
        return nlp(text)
    except Exception as e:
        log_error(logger, e, {'operation': 'extract_resume_info_from_pdf'})
        return nlp("")
```

### Step 5: Test

```python
# Test script
from utils.language_detector import detect_language
from utils.translator import translate_to_english

# Hindi text
hindi_text = "मेरा नाम राज कुमार है। मैं Python developer हूं।"

# Detect
lang = detect_language(hindi_text)
print(f"Detected: {lang}")

# Translate
english = translate_to_english(hindi_text)
print(f"Translated: {english}")
```

---

## 🎯 Specific Language Support

### Hindi (हिंदी)

**Option 1: Translation (Easy)**
```python
# Hindi text ko English mein translate karo
hindi_text = "मेरा नाम राज है"
english = translate_to_english(hindi_text)
# Result: "My name is Raj"
```

**Option 2: Multilingual Model**
```bash
python -m spacy download xx_ent_wiki_sm
```

### Other Indian Languages

- **Marathi, Gujarati, Tamil, Telugu, etc.**
- Translation approach best hai
- Ya multilingual model use karo

---

## ⚠️ Important Considerations

### 1. **Translation Quality**
- Google Translate free hai but quality variable
- DeepL better hai but paid
- Test karke decide karo

### 2. **Performance**
- Translation API calls slow ho sakte hain
- Caching implement karo
- Batch processing consider karo

### 3. **Cost**
- Free APIs: Rate limits hain
- Paid APIs: Better quality but cost
- Self-hosted: Best but complex

### 4. **Accuracy**
- Translation mein some loss possible
- Important fields (email, phone) directly extract karo
- Skills list ko multiple languages mein maintain karo

---

## 📝 Next Steps

1. **Quick Test:** Translation approach try karo
2. **Evaluate:** Accuracy check karo different languages mein
3. **Optimize:** Based on results, best approach choose karo
4. **Implement:** Full implementation karo

---

**Recommendation:** Start with **Translation Approach** (Approach 2) - Easy, fast, effective! 🚀

Agar koi specific language ke liye help chahiye, to batao!

