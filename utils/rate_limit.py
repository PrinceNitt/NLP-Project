"""
Rate limiting utilities for Resume Parser NLP Application.
Prevents abuse and ensures fair resource usage.
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
from collections import defaultdict
import streamlit as st

from config import SESSION_TIMEOUT
from utils.logger import setup_logger

logger = setup_logger(__name__)

# In-memory rate limit storage (for single-instance deployment)
# For production with multiple instances, use Redis
_rate_limit_store: Dict[str, Dict] = defaultdict(dict)


def check_rate_limit(
    identifier: str,
    max_requests: int = 10,
    window_seconds: int = 60
) -> tuple[bool, Optional[int]]:
    """
    Check if request is within rate limit.
    
    Args:
        identifier: Unique identifier (IP, user ID, etc.)
        max_requests: Maximum requests allowed
        window_seconds: Time window in seconds
        
    Returns:
        Tuple of (is_allowed, remaining_requests)
    """
    try:
        now = datetime.now()
        window_start = now - timedelta(seconds=window_seconds)
        
        # Get or initialize rate limit data
        if identifier not in _rate_limit_store:
            _rate_limit_store[identifier] = {
                'requests': [],
                'last_reset': now
            }
        
        rate_data = _rate_limit_store[identifier]
        
        # Clean old requests outside the window
        rate_data['requests'] = [
            req_time for req_time in rate_data['requests']
            if req_time > window_start
        ]
        
        # Check if limit exceeded
        request_count = len(rate_data['requests'])
        
        if request_count >= max_requests:
            # Limit exceeded
            oldest_request = min(rate_data['requests']) if rate_data['requests'] else now
            reset_time = oldest_request + timedelta(seconds=window_seconds)
            remaining_seconds = (reset_time - now).total_seconds()
            
            logger.warning(
                f"Rate limit exceeded for {identifier}: "
                f"{request_count}/{max_requests} requests in {window_seconds}s"
            )
            return False, int(remaining_seconds)
        
        # Add current request
        rate_data['requests'].append(now)
        
        remaining = max_requests - request_count - 1
        return True, remaining
        
    except Exception as e:
        logger.error(f"Rate limit check error: {e}")
        # On error, allow the request (fail open)
        return True, None


def get_rate_limit_info(identifier: str) -> Dict:
    """
    Get rate limit information for an identifier.
    
    Args:
        identifier: Unique identifier
        
    Returns:
        Dictionary with rate limit information
    """
    try:
        if identifier not in _rate_limit_store:
            return {
                'requests': 0,
                'limit': 10,
                'window': 60,
                'remaining': 10
            }
        
        rate_data = _rate_limit_store[identifier]
        request_count = len(rate_data['requests'])
        
        return {
            'requests': request_count,
            'limit': 10,  # Default limit
            'window': 60,  # Default window
            'remaining': max(0, 10 - request_count)
        }
    except Exception:
        return {
            'requests': 0,
            'limit': 10,
            'window': 60,
            'remaining': 10
        }


def reset_rate_limit(identifier: str) -> None:
    """
    Reset rate limit for an identifier.
    
    Args:
        identifier: Unique identifier
    """
    try:
        if identifier in _rate_limit_store:
            del _rate_limit_store[identifier]
            logger.info(f"Rate limit reset for {identifier}")
    except Exception as e:
        logger.error(f"Error resetting rate limit: {e}")

