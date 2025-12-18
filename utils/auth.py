"""
Authentication utilities for Resume Parser NLP Application.
Handles password hashing, session management, and authentication.
"""
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict
import streamlit as st

from config import ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_SESSION_KEY, SESSION_TIMEOUT
from utils.logger import setup_logger, log_error

logger = setup_logger(__name__)


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    try:
        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    except Exception as e:
        log_error(logger, e, {'operation': 'hash_password'})
        raise


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        password: Plain text password to verify
        hashed: Hashed password to compare against
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception as e:
        log_error(logger, e, {'operation': 'verify_password'})
        return False


def get_hashed_password_from_env() -> Optional[str]:
    """
    Get hashed password from environment variable.
    If ADMIN_PASSWORD_HASH is set, use it. Otherwise, hash ADMIN_PASSWORD.
    
    Returns:
        Hashed password string or None
    """
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check if hashed password is provided
    password_hash = os.getenv('ADMIN_PASSWORD_HASH', '')
    if password_hash:
        return password_hash
    
    # If plain password is provided, hash it (for backward compatibility)
    plain_password = os.getenv('ADMIN_PASSWORD', '')
    if plain_password:
        return hash_password(plain_password)
    
    return None


def authenticate_admin_secure(username: str, password: str) -> bool:
    """
    Authenticate admin user with secure password hashing.
    
    Args:
        username: Admin username
        password: Admin password
        
    Returns:
        True if authentication successful, False otherwise
    """
    try:
        from utils.validators import sanitize_input
        
        # Sanitize inputs
        username = sanitize_input(username, max_length=50)
        password = sanitize_input(password, max_length=100)
        
        # Get hashed password
        hashed_password = get_hashed_password_from_env()
        
        # Verify username
        if username != ADMIN_USERNAME:
            logger.warning(f"Failed admin authentication attempt: Invalid username: {username}")
            return False
        
        # Verify password
        if not hashed_password:
            logger.error("Admin password hash not configured")
            return False
        
        if verify_password(password, hashed_password):
            # Set session with timestamp
            st.session_state[ADMIN_SESSION_KEY] = True
            st.session_state[f'{ADMIN_SESSION_KEY}_timestamp'] = datetime.now().isoformat()
            logger.info(f"Admin authenticated successfully: {username}")
            return True
        else:
            logger.warning(f"Failed admin authentication attempt: Invalid password for user: {username}")
            return False
            
    except Exception as e:
        log_error(logger, e, {'operation': 'authenticate_admin_secure'})
        return False


def is_admin_authenticated() -> bool:
    """
    Check if admin is authenticated and session is still valid.
    
    Returns:
        True if authenticated and session valid, False otherwise
    """
    try:
        if not st.session_state.get(ADMIN_SESSION_KEY, False):
            return False
        
        # Check session timeout
        timestamp_str = st.session_state.get(f'{ADMIN_SESSION_KEY}_timestamp', '')
        if not timestamp_str:
            return False
        
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            elapsed = (datetime.now() - timestamp).total_seconds()
            
            if elapsed > SESSION_TIMEOUT:
                # Session expired
                logout_admin()
                logger.info("Admin session expired")
                return False
            
            return True
        except (ValueError, TypeError):
            # Invalid timestamp, logout
            logout_admin()
            return False
            
    except Exception as e:
        log_error(logger, e, {'operation': 'is_admin_authenticated'})
        return False


def logout_admin() -> None:
    """Logout admin user and clear session."""
    try:
        if ADMIN_SESSION_KEY in st.session_state:
            del st.session_state[ADMIN_SESSION_KEY]
        if f'{ADMIN_SESSION_KEY}_timestamp' in st.session_state:
            del st.session_state[f'{ADMIN_SESSION_KEY}_timestamp']
        logger.info("Admin logged out")
    except Exception as e:
        log_error(logger, e, {'operation': 'logout_admin'})


def get_session_remaining_time() -> Optional[int]:
    """
    Get remaining session time in seconds.
    
    Returns:
        Remaining seconds or None if not authenticated
    """
    try:
        if not is_admin_authenticated():
            return None
        
        timestamp_str = st.session_state.get(f'{ADMIN_SESSION_KEY}_timestamp', '')
        if not timestamp_str:
            return None
        
        timestamp = datetime.fromisoformat(timestamp_str)
        elapsed = (datetime.now() - timestamp).total_seconds()
        remaining = int(SESSION_TIMEOUT - elapsed)
        return max(0, remaining)
    except Exception:
        return None

