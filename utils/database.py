"""
Database utilities for Resume Parser NLP Application.
Provides connection management and database operations.
"""
import sqlite3
from contextlib import contextmanager
from typing import Optional, List, Tuple, Any
from pathlib import Path

from config import DATABASE_PATH, DATABASE_DIR
from utils.logger import setup_logger, log_error

logger = setup_logger(__name__)


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Ensures proper connection handling and cleanup.
    
    Yields:
        Database connection object
    """
    conn = None
    try:
        # Ensure database directory exists
        Path(DATABASE_DIR).mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        log_error(logger, e, {'operation': 'database_connection'})
        raise
    finally:
        if conn:
            conn.close()


def init_database() -> None:
    """
    Initialize database tables if they don't exist.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Create user_uploaded_pdfs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_uploaded_pdfs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    data BLOB NOT NULL,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    file_size INTEGER
                )
            ''')
            
            # Create feedback table (migrate from CSV)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    feedback_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create index for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_uploaded_at 
                ON user_uploaded_pdfs(uploaded_at)
            ''')
            
            conn.commit()
            logger.info("Database initialized successfully")
            
    except sqlite3.Error as e:
        log_error(logger, e, {'operation': 'database_init'})
        raise


def insert_pdf(name: str, data: bytes) -> Optional[int]:
    """
    Insert PDF into database.
    
    Args:
        name: PDF file name
        data: PDF file data as bytes
        
    Returns:
        Inserted record ID, or None if failed
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO user_uploaded_pdfs (name, data, file_size) VALUES (?, ?, ?)',
                (name, data, len(data))
            )
            record_id = cursor.lastrowid
            logger.info(f"PDF inserted successfully: {name} (ID: {record_id})")
            return record_id
    except sqlite3.Error as e:
        log_error(logger, e, {'operation': 'insert_pdf', 'file_name': name})
        return None


def get_pdf_by_id(pdf_id: int) -> Optional[Tuple[str, bytes]]:
    """
    Retrieve PDF by ID.
    
    Args:
        pdf_id: PDF record ID
        
    Returns:
        Tuple of (name, data) or None if not found
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT name, data FROM user_uploaded_pdfs WHERE id = ?',
                (pdf_id,)
            )
            result = cursor.fetchone()
            if result:
                return result['name'], result['data']
            return None
    except sqlite3.Error as e:
        log_error(logger, e, {'operation': 'get_pdf_by_id', 'pdf_id': pdf_id})
        return None


def get_all_pdfs() -> List[Tuple[int, str]]:
    """
    Get all uploaded PDFs.
    
    Returns:
        List of tuples (id, name)
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM user_uploaded_pdfs ORDER BY uploaded_at DESC')
            return [(row['id'], row['name']) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        log_error(logger, e, {'operation': 'get_all_pdfs'})
        return []


def insert_feedback(user_name: str, feedback_text: str) -> Optional[int]:
    """
    Insert feedback into database.
    
    Args:
        user_name: Name of the user providing feedback
        feedback_text: Feedback text
        
    Returns:
        Inserted record ID, or None if failed
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO feedback (user_name, feedback_text) VALUES (?, ?)',
                (user_name, feedback_text)
            )
            record_id = cursor.lastrowid
            logger.info(f"Feedback inserted successfully (ID: {record_id})")
            return record_id
    except sqlite3.Error as e:
        log_error(logger, e, {'operation': 'insert_feedback'})
        return None


def get_feedback(limit: int = 10) -> List[dict]:
    """
    Get feedback records.
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        List of feedback dictionaries
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, user_name, feedback_text, created_at FROM feedback ORDER BY created_at DESC LIMIT ?',
                (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        log_error(logger, e, {'operation': 'get_feedback'})
        return []


def get_all_pdfs_with_details() -> List[dict]:
    """
    Get all PDFs with detailed information.
    
    Returns:
        List of dictionaries with PDF details
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, uploaded_at, file_size 
                FROM user_uploaded_pdfs 
                ORDER BY uploaded_at DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        log_error(logger, e, {'operation': 'get_all_pdfs_with_details'})
        return []


def get_statistics() -> dict:
    """
    Get overall statistics.
    
    Returns:
        Dictionary with statistics
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Total resumes
            cursor.execute('SELECT COUNT(*) as count FROM user_uploaded_pdfs')
            total_resumes = cursor.fetchone()['count']
            
            # Total feedback
            cursor.execute('SELECT COUNT(*) as count FROM feedback')
            total_feedback = cursor.fetchone()['count']
            
            # Total file size
            cursor.execute('SELECT SUM(file_size) as total_size FROM user_uploaded_pdfs')
            result = cursor.fetchone()
            total_size = result['total_size'] if result['total_size'] else 0
            
            # Resumes by date (last 7 days)
            cursor.execute('''
                SELECT date(uploaded_at) as date, COUNT(*) as count
                FROM user_uploaded_pdfs
                WHERE uploaded_at >= datetime('now', '-7 days')
                GROUP BY date(uploaded_at)
                ORDER BY date DESC
            ''')
            recent_uploads = [dict(row) for row in cursor.fetchall()]
            
            # Average file size
            avg_size = total_size / total_resumes if total_resumes > 0 else 0
            
            return {
                'total_resumes': total_resumes,
                'total_feedback': total_feedback,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'avg_size_mb': round(avg_size / (1024 * 1024), 2),
                'recent_uploads': recent_uploads,
                'recent_7_days': sum(row['count'] for row in recent_uploads)
            }
    except sqlite3.Error as e:
        log_error(logger, e, {'operation': 'get_statistics'})
        return {
            'total_resumes': 0,
            'total_feedback': 0,
            'total_size_mb': 0,
            'avg_size_mb': 0,
            'recent_uploads': [],
            'recent_7_days': 0
        }

