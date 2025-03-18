"""
Security utilities for data encryption and decryption.
"""

import os
from base64 import b64encode, b64decode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Load encryption key from environment or generate one
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
fernet = Fernet(ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    """
    Encrypt data using AES-256 (via Fernet).
    
    Args:
        data: String data to encrypt
        
    Returns:
        Base64 encoded encrypted string
    """
    if not data:
        return ""
    encrypted = fernet.encrypt(data.encode())
    return b64encode(encrypted).decode()

def decrypt_data(encrypted_data: str) -> str:
    """
    Decrypt data using AES-256 (via Fernet).
    
    Args:
        encrypted_data: Base64 encoded encrypted string
        
    Returns:
        Decrypted string
    """
    if not encrypted_data:
        return ""
    try:
        decrypted = fernet.decrypt(b64decode(encrypted_data))
        return decrypted.decode()
    except Exception:
        return ""  # Return empty string if decryption fails 