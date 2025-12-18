"""
Unit tests for database module.
"""
import pytest
import os
import tempfile
from pathlib import Path
from utils.database import (
    init_database,
    insert_pdf,
    get_pdf_by_id,
    get_all_pdfs,
    insert_feedback,
    get_feedback,
    get_db_connection
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        os.environ['DATABASE_PATH'] = db_path
        yield db_path
        if os.path.exists(db_path):
            os.remove(db_path)


def test_init_database(temp_db):
    """Test database initialization."""
    init_database()
    assert os.path.exists(temp_db)


def test_insert_and_get_pdf(temp_db):
    """Test PDF insertion and retrieval."""
    init_database()
    pdf_id = insert_pdf("test.pdf", b"PDF content")
    assert pdf_id is not None
    
    result = get_pdf_by_id(pdf_id)
    assert result is not None
    name, data = result
    assert name == "test.pdf"
    assert data == b"PDF content"


def test_insert_feedback(temp_db):
    """Test feedback insertion."""
    init_database()
    feedback_id = insert_feedback("Test User", "Test feedback")
    assert feedback_id is not None
    
    feedback_list = get_feedback(limit=1)
    assert len(feedback_list) == 1
    assert feedback_list[0]['user_name'] == "Test User"

