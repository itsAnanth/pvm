import winreg
import os
import logging

logger = logging.getLogger("pvm.registry")

# Windows registry PATH value has a maximum length of 2047 characters
MAX_PATH_LENGTH = 2047

def get_user_path():
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Environment"
    ) as key:
        try:
            value, _ = winreg.QueryValueEx(key, "PATH")
            return value
        except FileNotFoundError:
            return ""

def validate_path_entry(entry: str) -> bool:
    """Validate a single PATH entry for security and correctness.
    
    Args:
        entry: A single path entry from the PATH variable
        
    Returns:
        True if the entry is valid, False otherwise
    """
    if not entry or not entry.strip():
        return False
    
    # Check for suspicious characters that could indicate path traversal
    suspicious_patterns = ['..', '<', '>', '|', '"', '?', '*']
    if any(pattern in entry for pattern in suspicious_patterns):
        logger.warning(f"Suspicious characters found in PATH entry: {entry}")
        return False
    
    # Check for null bytes
    if '\x00' in entry:
        logger.warning(f"Null byte found in PATH entry: {entry}")
        return False
    
    return True

def validate_path_value(path_value: str) -> bool:
    """Validate the entire PATH value before writing to registry.
    
    Args:
        path_value: The complete PATH string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not path_value:
        logger.error("Empty PATH value provided")
        return False
    
    # Check length to prevent registry corruption
    if len(path_value) > MAX_PATH_LENGTH:
        logger.error(f"PATH value exceeds maximum length ({len(path_value)} > {MAX_PATH_LENGTH})")
        return False
    
    # Validate individual entries
    entries = path_value.split(';')
    for entry in entries:
        if entry and not validate_path_entry(entry):
            logger.error(f"Invalid PATH entry detected: {entry}")
            return False
    
    return True
        
def set_user_path(new_path: str):
    """Set the user PATH environment variable with validation.
    
    Args:
        new_path: The new PATH value to set
        
    Raises:
        ValueError: If the PATH value is invalid
    """
    if not validate_path_value(new_path):
        raise ValueError("Invalid PATH value: failed validation checks")
    
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
            logger.debug(f"Successfully updated user PATH in registry")
    except PermissionError as e:
        logger.error(f"Permission denied when writing to registry: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to write PATH to registry: {e}")
        raise