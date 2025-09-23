"""
Dynamic Credential Manager for SmartWebBot

Securely manages credentials that are requested dynamically during workflow execution.
Supports temporary storage, encryption, and automatic cleanup.
"""

import json
import base64
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import secrets

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

from ..core.base_component import BaseComponent


class CredentialType(Enum):
    USERNAME_PASSWORD = "username_password"
    API_KEY = "api_key"
    OAUTH_TOKEN = "oauth_token"
    TWO_FACTOR_CODE = "two_factor_code"
    CUSTOM = "custom"


class StorageType(Enum):
    MEMORY = "memory"           # In-memory only (most secure, lost on restart)
    TEMPORARY = "temporary"     # Encrypted temp file (cleared after session)
    SESSION = "session"         # Persists for session duration


@dataclass
class CredentialEntry:
    """Represents a stored credential entry"""
    credential_id: str
    session_id: str
    platform: str
    credential_type: CredentialType
    encrypted_data: str
    created_at: datetime
    expires_at: Optional[datetime]
    usage_count: int
    max_usage: Optional[int]
    metadata: Dict[str, Any]


@dataclass
class CredentialRequest:
    """Represents a request for credentials"""
    request_id: str
    session_id: str
    platform: str
    credential_types: List[CredentialType]
    required_fields: List[str]
    optional_fields: List[str]
    prompt_message: str
    timeout_seconds: int
    auto_cleanup: bool


class DynamicCredentialManager(BaseComponent):
    """
    Manages credentials that are requested dynamically during automation workflows.
    
    Features:
    - Secure encryption of sensitive data
    - Temporary storage with automatic cleanup
    - Session-based credential sharing
    - Usage tracking and limits
    - Multiple storage backends
    """
    
    def __init__(self, config: Dict = None):
        super().__init__("dynamic_credential_manager", config)
        
        # Configuration
        self.default_expiry_hours = config.get("default_expiry_hours", 24) if config else 24
        self.max_credentials_per_session = config.get("max_credentials_per_session", 10) if config else 10
        self.encryption_enabled = config.get("encryption_enabled", True) if config else True
        self.default_storage_type = StorageType(config.get("default_storage_type", "memory")) if config else StorageType.MEMORY
        
        # Storage
        self.memory_store: Dict[str, CredentialEntry] = {}
        self.active_requests: Dict[str, CredentialRequest] = {}
        self.session_credentials: Dict[str, List[str]] = {}  # session_id -> [credential_ids]
        
        # Encryption
        self.encryption_key = None
        self.cipher_suite = None
        
        # Cleanup tracking
        self.last_cleanup = datetime.now()
        self.cleanup_interval = timedelta(hours=1)
    
    def initialize(self) -> bool:
        """Initialize the credential manager"""
        try:
            self.logger.info("Initializing Dynamic Credential Manager...")
            
            # Initialize encryption if available and enabled
            if self.encryption_enabled and CRYPTO_AVAILABLE:
                self._initialize_encryption()
                self.logger.info("Encryption initialized successfully")
            elif self.encryption_enabled:
                self.logger.warning("Encryption requested but cryptography library not available")
                self.encryption_enabled = False
            
            self.is_initialized = True
            self.logger.info("Dynamic Credential Manager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Dynamic Credential Manager: {e}")
            return False
    
    def _initialize_encryption(self):
        """Initialize encryption system"""
        # Generate a key from a master password (in production, this should be more secure)
        master_password = secrets.token_urlsafe(32).encode()
        salt = secrets.token_bytes(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(master_password))
        self.cipher_suite = Fernet(key)
    
    async def request_credentials(self, 
                                session_id: str,
                                platform: str,
                                credential_types: List[CredentialType],
                                required_fields: List[str],
                                optional_fields: List[str] = None,
                                prompt_message: str = None,
                                timeout_seconds: int = 300) -> CredentialRequest:
        """
        Create a credential request that can be fulfilled by the user.
        
        Args:
            session_id: Session requesting credentials
            platform: Target platform (Instagram, Facebook, etc.)
            credential_types: Types of credentials needed
            required_fields: Required credential fields
            optional_fields: Optional credential fields
            prompt_message: Custom message to show user
            timeout_seconds: Request timeout
            
        Returns:
            CredentialRequest object
        """
        
        request_id = f"req_{secrets.token_urlsafe(8)}"
        
        # Generate appropriate prompt message
        if not prompt_message:
            prompt_message = self._generate_credential_prompt(platform, required_fields)
        
        request = CredentialRequest(
            request_id=request_id,
            session_id=session_id,
            platform=platform,
            credential_types=credential_types,
            required_fields=required_fields,
            optional_fields=optional_fields or [],
            prompt_message=prompt_message,
            timeout_seconds=timeout_seconds,
            auto_cleanup=True
        )
        
        self.active_requests[request_id] = request
        
        self.logger.info(f"Created credential request {request_id} for {platform}")
        return request
    
    async def fulfill_credential_request(self,
                                       request_id: str,
                                       credentials: Dict[str, str],
                                       storage_type: StorageType = None) -> Dict[str, Any]:
        """
        Fulfill a credential request with provided credentials.
        
        Args:
            request_id: ID of the credential request
            credentials: Dictionary of credential fields and values
            storage_type: How to store the credentials
            
        Returns:
            Result dictionary with credential_id and status
        """
        
        if request_id not in self.active_requests:
            return {"success": False, "error": "Request not found or expired"}
        
        request = self.active_requests[request_id]
        
        # Validate required fields
        missing_fields = [field for field in request.required_fields if field not in credentials]
        if missing_fields:
            return {"success": False, "error": f"Missing required fields: {missing_fields}"}
        
        # Store the credentials
        credential_id = await self._store_credentials(
            session_id=request.session_id,
            platform=request.platform,
            credential_type=request.credential_types[0],  # Use first type for now
            credentials=credentials,
            storage_type=storage_type or self.default_storage_type
        )
        
        # Clean up the request
        del self.active_requests[request_id]
        
        self.logger.info(f"Fulfilled credential request {request_id}, stored as {credential_id}")
        
        return {
            "success": True,
            "credential_id": credential_id,
            "platform": request.platform,
            "fields_stored": list(credentials.keys())
        }
    
    async def _store_credentials(self,
                               session_id: str,
                               platform: str,
                               credential_type: CredentialType,
                               credentials: Dict[str, str],
                               storage_type: StorageType) -> str:
        """Store credentials securely"""
        
        credential_id = f"cred_{secrets.token_urlsafe(8)}"
        
        # Encrypt credentials if encryption is enabled
        if self.encryption_enabled and self.cipher_suite:
            credential_data = json.dumps(credentials)
            encrypted_data = self.cipher_suite.encrypt(credential_data.encode()).decode()
        else:
            # Store as base64 for basic obfuscation
            credential_data = json.dumps(credentials)
            encrypted_data = base64.b64encode(credential_data.encode()).decode()
        
        # Create credential entry
        entry = CredentialEntry(
            credential_id=credential_id,
            session_id=session_id,
            platform=platform,
            credential_type=credential_type,
            encrypted_data=encrypted_data,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=self.default_expiry_hours),
            usage_count=0,
            max_usage=None,
            metadata={"storage_type": storage_type.value}
        )
        
        # Store based on storage type
        if storage_type == StorageType.MEMORY:
            self.memory_store[credential_id] = entry
        
        # Track session credentials
        if session_id not in self.session_credentials:
            self.session_credentials[session_id] = []
        self.session_credentials[session_id].append(credential_id)
        
        return credential_id
    
    async def get_credentials(self, credential_id: str, session_id: str = None) -> Optional[Dict[str, str]]:
        """
        Retrieve and decrypt stored credentials.
        
        Args:
            credential_id: ID of stored credentials
            session_id: Session requesting credentials (for validation)
            
        Returns:
            Dictionary of credential fields or None if not found
        """
        
        # Find credential entry
        entry = self.memory_store.get(credential_id)
        if not entry:
            return None
        
        # Validate session if provided
        if session_id and entry.session_id != session_id:
            self.logger.warning(f"Session mismatch for credential {credential_id}")
            return None
        
        # Check expiration
        if entry.expires_at and datetime.now() > entry.expires_at:
            self.logger.info(f"Credential {credential_id} expired, removing")
            await self._remove_credential(credential_id)
            return None
        
        # Check usage limits
        if entry.max_usage and entry.usage_count >= entry.max_usage:
            self.logger.info(f"Credential {credential_id} usage limit reached")
            return None
        
        # Decrypt credentials
        try:
            if self.encryption_enabled and self.cipher_suite:
                decrypted_data = self.cipher_suite.decrypt(entry.encrypted_data.encode()).decode()
            else:
                decrypted_data = base64.b64decode(entry.encrypted_data.encode()).decode()
            
            credentials = json.loads(decrypted_data)
            
            # Update usage count
            entry.usage_count += 1
            
            self.logger.info(f"Retrieved credentials for {entry.platform} (usage: {entry.usage_count})")
            return credentials
            
        except Exception as e:
            self.logger.error(f"Failed to decrypt credentials {credential_id}: {e}")
            return None
    
    async def get_session_credentials(self, session_id: str, platform: str = None) -> List[Dict[str, Any]]:
        """
        Get all credentials for a session, optionally filtered by platform.
        
        Args:
            session_id: Session ID
            platform: Optional platform filter
            
        Returns:
            List of credential info (without actual credential data)
        """
        
        if session_id not in self.session_credentials:
            return []
        
        credential_ids = self.session_credentials[session_id]
        results = []
        
        for cred_id in credential_ids:
            entry = self.memory_store.get(cred_id)
            if entry and (not platform or entry.platform.lower() == platform.lower()):
                results.append({
                    "credential_id": cred_id,
                    "platform": entry.platform,
                    "credential_type": entry.credential_type.value,
                    "created_at": entry.created_at.isoformat(),
                    "expires_at": entry.expires_at.isoformat() if entry.expires_at else None,
                    "usage_count": entry.usage_count
                })
        
        return results
    
    async def _remove_credential(self, credential_id: str):
        """Remove a credential entry"""
        
        if credential_id in self.memory_store:
            entry = self.memory_store[credential_id]
            
            # Remove from session tracking
            if entry.session_id in self.session_credentials:
                if credential_id in self.session_credentials[entry.session_id]:
                    self.session_credentials[entry.session_id].remove(credential_id)
            
            # Remove from store
            del self.memory_store[credential_id]
            
            self.logger.info(f"Removed credential {credential_id}")
    
    async def cleanup_expired_credentials(self):
        """Clean up expired credentials"""
        
        current_time = datetime.now()
        expired_ids = []
        
        for cred_id, entry in self.memory_store.items():
            if entry.expires_at and current_time > entry.expires_at:
                expired_ids.append(cred_id)
        
        for cred_id in expired_ids:
            await self._remove_credential(cred_id)
        
        if expired_ids:
            self.logger.info(f"Cleaned up {len(expired_ids)} expired credentials")
        
        self.last_cleanup = current_time
    
    async def cleanup_session_credentials(self, session_id: str):
        """Clean up all credentials for a session"""
        
        if session_id not in self.session_credentials:
            return
        
        credential_ids = self.session_credentials[session_id].copy()
        
        for cred_id in credential_ids:
            await self._remove_credential(cred_id)
        
        del self.session_credentials[session_id]
        
        self.logger.info(f"Cleaned up {len(credential_ids)} credentials for session {session_id}")
    
    def _generate_credential_prompt(self, platform: str, required_fields: List[str]) -> str:
        """Generate user-friendly credential prompt"""
        
        field_names = {
            "username": "username",
            "password": "password",
            "email": "email address",
            "api_key": "API key",
            "token": "access token",
            "code": "verification code"
        }
        
        friendly_fields = [field_names.get(field, field) for field in required_fields]
        
        if len(friendly_fields) == 1:
            return f"Please provide your {friendly_fields[0]} for {platform}."
        else:
            return f"Please provide your {', '.join(friendly_fields[:-1])} and {friendly_fields[-1]} for {platform}."
    
    async def get_active_requests(self) -> List[Dict[str, Any]]:
        """Get all active credential requests"""
        
        return [
            {
                "request_id": req.request_id,
                "session_id": req.session_id,
                "platform": req.platform,
                "required_fields": req.required_fields,
                "prompt_message": req.prompt_message,
                "created_at": datetime.now().isoformat()  # Approximate
            }
            for req in self.active_requests.values()
        ]
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        
        return {
            "total_credentials": len(self.memory_store),
            "active_sessions": len(self.session_credentials),
            "active_requests": len(self.active_requests),
            "encryption_enabled": self.encryption_enabled,
            "last_cleanup": self.last_cleanup.isoformat()
        }
    
    def cleanup(self) -> bool:
        """Clean up all resources"""
        
        try:
            # Clear all stored data
            self.memory_store.clear()
            self.active_requests.clear()
            self.session_credentials.clear()
            
            # Clear encryption keys
            self.encryption_key = None
            self.cipher_suite = None
            
            self.logger.info("Dynamic Credential Manager cleanup completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")
            return False
