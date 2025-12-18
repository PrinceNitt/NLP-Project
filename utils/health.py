"""
Health check utilities for Resume Parser NLP Application.
Provides system health monitoring and status checks.
"""
from typing import Dict, Any
from pathlib import Path
import sqlite3

from config import DATABASE_PATH, DATA_DIR, SKILLS_CSV, MAJORS_CSV, POSITION_CSV
from utils.logger import setup_logger

logger = setup_logger(__name__)


def check_database_health() -> Dict[str, Any]:
    """
    Check database health and connectivity.
    
    Returns:
        Dictionary with database health status
    """
    try:
        if not Path(DATABASE_PATH).exists():
            return {
                'status': 'error',
                'message': 'Database file does not exist',
                'details': {'path': str(DATABASE_PATH)}
            }
        
        # Try to connect and query
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['user_uploaded_pdfs', 'feedback']
        missing_tables = [t for t in required_tables if t not in tables]
        
        conn.close()
        
        if missing_tables:
            return {
                'status': 'warning',
                'message': f'Missing tables: {", ".join(missing_tables)}',
                'details': {'existing_tables': tables, 'missing_tables': missing_tables}
            }
        
        return {
            'status': 'healthy',
            'message': 'Database is healthy',
            'details': {'tables': tables, 'path': str(DATABASE_PATH)}
        }
        
    except sqlite3.Error as e:
        return {
            'status': 'error',
            'message': f'Database error: {str(e)}',
            'details': {'error_type': type(e).__name__}
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            'status': 'error',
            'message': f'Unexpected error: {str(e)}',
            'details': {}
        }


def check_data_files_health() -> Dict[str, Any]:
    """
    Check if required data files exist.
    
    Returns:
        Dictionary with data files health status
    """
    required_files = {
        'skills': SKILLS_CSV,
        'majors': MAJORS_CSV,
        'positions': POSITION_CSV,
    }
    
    missing_files = []
    existing_files = []
    
    for name, file_path in required_files.items():
        if file_path.exists():
            existing_files.append(name)
        else:
            missing_files.append(name)
    
    if missing_files:
        return {
            'status': 'error',
            'message': f'Missing required files: {", ".join(missing_files)}',
            'details': {
                'existing': existing_files,
                'missing': missing_files
            }
        }
    
    return {
        'status': 'healthy',
        'message': 'All required data files exist',
        'details': {'files': existing_files}
    }


def check_system_health() -> Dict[str, Any]:
    """
    Perform comprehensive system health check.
    
    Returns:
        Dictionary with overall system health status
    """
    db_health = check_database_health()
    files_health = check_data_files_health()
    
    # Determine overall status
    if db_health['status'] == 'error' or files_health['status'] == 'error':
        overall_status = 'error'
    elif db_health['status'] == 'warning' or files_health['status'] == 'warning':
        overall_status = 'warning'
    else:
        overall_status = 'healthy'
    
    return {
        'status': overall_status,
        'timestamp': str(Path(__file__).stat().st_mtime),  # Simple timestamp
        'components': {
            'database': db_health,
            'data_files': files_health
        }
    }


def get_system_stats() -> Dict[str, Any]:
    """
    Get system statistics for monitoring.
    
    Returns:
        Dictionary with system statistics
    """
    try:
        from utils.database import get_statistics
        
        stats = get_statistics()
        
        return {
            'total_resumes': stats.get('total_resumes', 0),
            'total_feedback': stats.get('total_feedback', 0),
            'total_storage_mb': stats.get('total_size_mb', 0),
            'recent_uploads_7_days': stats.get('recent_7_days', 0),
        }
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        return {
            'total_resumes': 0,
            'total_feedback': 0,
            'total_storage_mb': 0,
            'recent_uploads_7_days': 0,
            'error': str(e)
        }

