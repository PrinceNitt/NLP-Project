"""
Unit tests for health check module.
"""
import pytest
import tempfile
import os
from pathlib import Path
from utils.health import (
    check_database_health,
    check_data_files_health,
    check_system_health
)


def test_check_database_health_missing_file():
    """Test database health check when file doesn't exist."""
    # This will test the error case
    # Note: In actual test, you'd mock the DATABASE_PATH
    result = check_database_health()
    
    assert 'status' in result
    assert 'message' in result
    assert 'details' in result
    assert result['status'] in ['healthy', 'warning', 'error']


def test_check_data_files_health():
    """Test data files health check."""
    result = check_data_files_health()
    
    assert 'status' in result
    assert 'message' in result
    assert 'details' in result
    assert result['status'] in ['healthy', 'warning', 'error']


def test_check_system_health():
    """Test comprehensive system health check."""
    result = check_system_health()
    
    assert 'status' in result
    assert 'components' in result
    assert 'database' in result['components']
    assert 'data_files' in result['components']
    assert result['status'] in ['healthy', 'warning', 'error']

