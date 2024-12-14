# exceptions/errors.py
from typing import Optional

class KeycloakError(Exception):
    """Base exception for all Keycloak errors"""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AuthenticationError(KeycloakError):
    """Authentication-related errors"""
    pass

class TokenError(KeycloakError):
    """Token-related errors"""
    pass

class AdminError(KeycloakError):
    """Admin operation errors"""
    pass

class ValidationError(KeycloakError):
    """Validation errors"""
    pass

class ConfigError(KeycloakError):
    """Configuration errors"""
    pass

class SessionError(KeycloakError):
    """Session management errors"""
    pass

class RegistrationError(KeycloakError):
    """User registration errors"""
    pass