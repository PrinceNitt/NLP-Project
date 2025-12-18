"""
Configuration management for Resume Parser NLP Application.
Handles environment variables and application settings.
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Database Configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', str(BASE_DIR / 'data' / 'user_pdfs.db'))
DATABASE_DIR = os.path.dirname(DATABASE_PATH)

# Ensure database directory exists
os.makedirs(DATABASE_DIR, exist_ok=True)

# Admin Configuration
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '')
ADMIN_SESSION_KEY = os.getenv('ADMIN_SESSION_KEY', 'admin_authenticated')

# File Upload Configuration
MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', '5242880'))  # 5MB default
MAX_FILES_PER_UPLOAD = int(os.getenv('MAX_FILES_PER_UPLOAD', '50'))  # Maximum files per upload
ALLOWED_EXTENSIONS = {'.pdf'}

# Data Files Configuration
DATA_DIR = BASE_DIR / 'data'
SKILLS_CSV = DATA_DIR / 'newSkills.csv'
UPDATED_SKILLS_CSV = DATA_DIR / 'UpdatedSkills.csv'
SUGGESTED_SKILLS_CSV = DATA_DIR / 'sugestedSkills.csv'
MAJORS_CSV = DATA_DIR / 'majors.csv'
POSITION_CSV = DATA_DIR / 'position.csv'
FEEDBACK_CSV = DATA_DIR / 'feedback_data.csv'

# Model Configuration
TRAINED_MODEL_PATH = BASE_DIR / 'TrainedModel' / 'skills'
SPACY_MODEL = os.getenv('SPACY_MODEL', 'en_core_web_sm')

# Logging Configuration
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = LOG_DIR / 'app.log'

# Application Configuration
APP_NAME = 'Resume Parser NLP'
APP_VERSION = '1.0.0'
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Security Configuration
SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32).hex())
SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '3600'))  # 1 hour

# Validation
def validate_config() -> bool:
    """Validate that all required configuration is present."""
    required_files = [
        SKILLS_CSV,
        MAJORS_CSV,
        POSITION_CSV,
    ]
    
    missing_files = [f for f in required_files if not f.exists()]
    if missing_files:
        raise FileNotFoundError(f"Missing required files: {missing_files}")
    
    if not ADMIN_PASSWORD and not DEBUG:
        raise ValueError("ADMIN_PASSWORD must be set in production mode")
    
    return True

