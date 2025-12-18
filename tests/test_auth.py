"""
Unit tests for authentication module.
"""
import pytest
import bcrypt
from utils.auth import (
    hash_password,
    verify_password,
    authenticate_admin_secure,
    get_session_remaining_time
)


def test_hash_password():
    """Test password hashing."""
    password = "test_password_123"
    hashed = hash_password(password)
    
    assert hashed is not None
    assert len(hashed) > 0
    assert hashed != password
    assert hashed.startswith('$2b$')  # bcrypt hash format


def test_verify_password_correct():
    """Test password verification with correct password."""
    password = "test_password_123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Test password verification with incorrect password."""
    password = "test_password_123"
    wrong_password = "wrong_password"
    hashed = hash_password(password)
    
    assert verify_password(wrong_password, hashed) is False


def test_hash_password_different_salts():
    """Test that same password produces different hashes (due to salt)."""
    password = "test_password_123"
    hashed1 = hash_password(password)
    hashed2 = hash_password(password)
    
    # Hashes should be different (due to different salts)
    assert hashed1 != hashed2
    
    # But both should verify correctly
    assert verify_password(password, hashed1) is True
    assert verify_password(password, hashed2) is True

