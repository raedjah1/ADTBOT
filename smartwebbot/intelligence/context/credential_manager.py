"""
Secure Credential Manager for Intelligent Chat System.

Manages secure storage and retrieval of user credentials
with encryption and secure handling practices.
"""

import json
import base64
import time
from cryptography.fernet import Fernet
from typing import Dict, Optional, Any
from ..core.base_chat_component import BaseChatComponent
from ..core.interfaces import ICredentialManager, CredentialType


class SecureCredentialManager(BaseChatComponent, ICredentialManager):
    """
    Secure credential manager with encryption and secure practices.
    
    Features:
    - Encrypted credential storage
    - Session-based credential management
    - Automatic credential expiration
    - Secure key management
    - Audit logging
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("secure_credential_manager", config)
        
        # Credential storage (encrypted)
        self.credentials: Dict[str, Dict] = {}
        
        # Encryption setup
        self.encryption_key = self._get_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)
        
        # Configuration
        self.credential_timeout = self.get_config_value("credential_timeout", 3600)  # 1 hour
        self.max_credentials_per_session = self.get_config_value("max_credentials_per_session", 10)
    
    def initialize(self) -> bool:
        """Initialize the credential manager."""
        try:
            self.logger.info("Initializing Secure Credential Manager...")
            
            # Test encryption
            test_data = b"test_encryption"
            encrypted = self.fernet.encrypt(test_data)
            decrypted = self.fernet.decrypt(encrypted)
            
            if decrypted != test_data:
                raise Exception("Encryption test failed")
            
            self.is_initialized = True
            self.is_healthy = True
            
            self.logger.info("Secure Credential Manager initialized successfully")
            return True
            
        except Exception as e:
            self.log_error(e, "Credential manager initialization")
            return False
    
    async def store_credentials(self, session_id: str, platform: str, credentials: Dict[str, Any]) -> bool:
        """Securely store credentials for session."""
        
        try:
            # Validate input
            if not session_id or not platform or not credentials:
                raise ValueError("Invalid parameters for credential storage")
            
            # Check session credential limit
            session_key = f"{session_id}:{platform}"
            
            if session_id in self.credentials:
                if len(self.credentials[session_id]) >= self.max_credentials_per_session:
                    raise Exception(f"Maximum credentials per session ({self.max_credentials_per_session}) reached")
            else:
                self.credentials[session_id] = {}
            
            # Encrypt credentials
            credentials_json = json.dumps(credentials)
            encrypted_credentials = self.fernet.encrypt(credentials_json.encode())
            
            # Store encrypted credentials with metadata
            credential_record = {
                "platform": platform,
                "encrypted_data": base64.b64encode(encrypted_credentials).decode(),
                "stored_at": time.time(),
                "expires_at": time.time() + self.credential_timeout,
                "access_count": 0
            }
            
            self.credentials[session_id][platform] = credential_record
            
            # Audit log (without sensitive data)
            self.logger.info(f"Stored credentials for {platform} in session {session_id}")
            self.increment_metric("credentials_stored")
            
            return True
            
        except Exception as e:
            self.log_error(e, f"Failed to store credentials for {platform}")
            return False
    
    async def get_credentials(self, session_id: str, platform: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored credentials."""
        
        try:
            # Check if session and platform exist
            if session_id not in self.credentials:
                return None
            
            if platform not in self.credentials[session_id]:
                return None
            
            credential_record = self.credentials[session_id][platform]
            
            # Check expiration
            if time.time() > credential_record["expires_at"]:
                # Remove expired credentials
                del self.credentials[session_id][platform]
                self.logger.info(f"Removed expired credentials for {platform}")
                return None
            
            # Decrypt credentials
            encrypted_data = base64.b64decode(credential_record["encrypted_data"])
            decrypted_data = self.fernet.decrypt(encrypted_data)
            credentials = json.loads(decrypted_data.decode())
            
            # Update access count
            credential_record["access_count"] += 1
            credential_record["last_accessed"] = time.time()
            
            # Audit log
            self.logger.debug(f"Retrieved credentials for {platform}")
            self.increment_metric("credentials_retrieved")
            
            return credentials
            
        except Exception as e:
            self.log_error(e, f"Failed to retrieve credentials for {platform}")
            return None
    
    async def has_credentials(self, session_id: str, platform: str, cred_type: CredentialType) -> bool:
        """Check if credentials are available."""
        
        try:
            credentials = await self.get_credentials(session_id, platform)
            
            if not credentials:
                return False
            
            # Check for specific credential type
            if cred_type == CredentialType.USERNAME_PASSWORD:
                return "username" in credentials and "password" in credentials
            elif cred_type == CredentialType.API_KEY:
                return "api_key" in credentials
            elif cred_type == CredentialType.OAUTH:
                return "access_token" in credentials
            elif cred_type == CredentialType.TWO_FACTOR:
                return "two_factor_code" in credentials
            
            return True
            
        except Exception as e:
            self.log_error(e, f"Failed to check credentials for {platform}")
            return False
    
    async def clear_credentials(self, session_id: str, platform: Optional[str] = None) -> bool:
        """Clear stored credentials."""
        
        try:
            if session_id not in self.credentials:
                return True
            
            if platform:
                # Clear specific platform credentials
                if platform in self.credentials[session_id]:
                    del self.credentials[session_id][platform]
                    self.logger.info(f"Cleared credentials for {platform}")
                    self.increment_metric("credentials_cleared")
            else:
                # Clear all credentials for session
                platforms_count = len(self.credentials[session_id])
                del self.credentials[session_id]
                self.logger.info(f"Cleared all credentials for session {session_id} ({platforms_count} platforms)")
                self.update_metrics("credentials_cleared", platforms_count)
            
            return True
            
        except Exception as e:
            self.log_error(e, f"Failed to clear credentials")
            return False
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key."""
        
        # In production, this should be loaded from a secure key management system
        # For now, we'll use a simple approach
        
        key_file = self.get_config_value("encryption_key_file", ".credential_key")
        
        try:
            # Try to load existing key
            with open(key_file, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            # Generate new key
            key = Fernet.generate_key()
            
            # Save key (in production, this should be done more securely)
            with open(key_file, 'wb') as f:
                f.write(key)
            
            self.logger.warning("Generated new encryption key for credentials")
            return key
    
    def get_credential_statistics(self) -> Dict[str, Any]:
        """Get credential storage statistics."""
        
        total_sessions = len(self.credentials)
        total_platforms = sum(len(platforms) for platforms in self.credentials.values())
        
        # Platform distribution
        platform_counts = {}
        expired_count = 0
        current_time = time.time()
        
        for session_creds in self.credentials.values():
            for platform, cred_record in session_creds.items():
                platform_counts[platform] = platform_counts.get(platform, 0) + 1
                
                if current_time > cred_record["expires_at"]:
                    expired_count += 1
        
        return {
            "total_sessions_with_credentials": total_sessions,
            "total_credential_records": total_platforms,
            "expired_credentials": expired_count,
            "platform_distribution": platform_counts,
            "memory_usage_estimate_mb": self._estimate_memory_usage()
        }
    
    def _estimate_memory_usage(self) -> float:
        """Estimate memory usage of credential storage."""
        
        total_size = 0
        
        for session_creds in self.credentials.values():
            for cred_record in session_creds.values():
                # Estimate size of encrypted data + metadata
                encrypted_size = len(cred_record["encrypted_data"])
                metadata_size = 200  # Rough estimate for metadata
                total_size += encrypted_size + metadata_size
        
        return total_size / (1024 * 1024)  # Convert to MB
    
    async def cleanup_expired_credentials(self) -> int:
        """Clean up expired credentials."""
        
        expired_count = 0
        current_time = time.time()
        
        # Find expired credentials
        sessions_to_clean = []
        
        for session_id, session_creds in self.credentials.items():
            expired_platforms = []
            
            for platform, cred_record in session_creds.items():
                if current_time > cred_record["expires_at"]:
                    expired_platforms.append(platform)
            
            # Remove expired platforms
            for platform in expired_platforms:
                del session_creds[platform]
                expired_count += 1
            
            # If session has no credentials left, mark for removal
            if not session_creds:
                sessions_to_clean.append(session_id)
        
        # Remove empty sessions
        for session_id in sessions_to_clean:
            del self.credentials[session_id]
        
        if expired_count > 0:
            self.logger.info(f"Cleaned up {expired_count} expired credentials")
            self.update_metrics("credentials_expired", expired_count)
        
        return expired_count
