"""
Unit tests for validators module.
"""
import pytest
from io import BytesIO
from utils.validators import (
    validate_email,
    validate_phone,
    validate_file_upload,
    sanitize_input,
    validate_skills_input
)


class TestEmailValidation:
    """Test email validation."""
    
    def test_valid_email(self):
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@domain.co.uk") is True
    
    def test_invalid_email(self):
        assert validate_email("invalid") is False
        assert validate_email("@domain.com") is False
        assert validate_email("") is False


class TestPhoneValidation:
    """Test phone validation."""
    
    def test_valid_phone(self):
        assert validate_phone("+1234567890") is True
        assert validate_phone("1234567890") is True
        assert validate_phone("+1-234-567-8900") is True
    
    def test_invalid_phone(self):
        assert validate_phone("123") is False  # Too short
        assert validate_phone("") is False


class TestFileUploadValidation:
    """Test file upload validation."""
    
    def test_valid_pdf(self):
        file = BytesIO(b"PDF content")
        file.name = "test.pdf"
        is_valid, error = validate_file_upload(file)
        assert is_valid is True
        assert error is None
    
    def test_invalid_extension(self):
        file = BytesIO(b"content")
        file.name = "test.txt"
        is_valid, error = validate_file_upload(file)
        assert is_valid is False
        assert error is not None
    
    def test_empty_file(self):
        file = BytesIO(b"")
        file.name = "test.pdf"
        is_valid, error = validate_file_upload(file)
        assert is_valid is False


class TestSanitizeInput:
    """Test input sanitization."""
    
    def test_sanitize_html(self):
        result = sanitize_input("<script>alert('xss')</script>")
        assert "<script>" not in result
    
    def test_truncate_long_input(self):
        long_input = "a" * 2000
        result = sanitize_input(long_input, max_length=100)
        assert len(result) <= 100


class TestSkillsValidation:
    """Test skills input validation."""
    
    def test_valid_skills(self):
        skills = "Python, Java, SQL"
        result = validate_skills_input(skills)
        assert len(result) == 3
        assert "Python" in result
    
    def test_empty_skills(self):
        result = validate_skills_input("")
        assert result == []

