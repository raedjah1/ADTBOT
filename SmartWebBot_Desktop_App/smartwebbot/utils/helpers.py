"""
Helper utilities for SmartWebBot.

Common utility functions used across the system.
"""

import os
import time
import random
from typing import Any, Dict, List, Optional


def generate_timestamp() -> str:
    """Generate a timestamp string."""
    return str(int(time.time()))


def generate_random_delay(min_delay: float = 0.5, max_delay: float = 2.0) -> float:
    """Generate a random delay for human-like behavior."""
    return random.uniform(min_delay, max_delay)


def safe_filename(filename: str) -> str:
    """Create a safe filename by removing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def ensure_directory(directory: str) -> bool:
    """Ensure a directory exists."""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception:
        return False


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string."""
    if seconds < 1:
        return f"{seconds:.2f}s"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def truncate_string(text: str, max_length: int = 100) -> str:
    """Truncate a string to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def deep_merge_dict(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries."""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dict(result[key], value)
        else:
            result[key] = value
    
    return result


def sanitize_text(text: str) -> str:
    """Sanitize text by removing extra whitespace and special characters."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove non-printable characters
    text = ''.join(char for char in text if char.isprintable())
    
    return text.strip()


def validate_url(url: str) -> bool:
    """Validate if a string is a valid URL."""
    from urllib.parse import urlparse
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    from urllib.parse import urlparse
    
    try:
        return urlparse(url).netloc
    except Exception:
        return ""


def is_element_visible(element) -> bool:
    """Check if a web element is visible."""
    try:
        return element.is_displayed() and element.is_enabled()
    except Exception:
        return False
