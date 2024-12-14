import jwt
from typing import Dict, Any, Optional
from datetime import datetime
import requests
from ..exceptions.errors import TokenError, ConfigError, ValidationError
from ..base.config import ClientConfig

class TokenVerifier:
    """Handles token verification with public key caching"""
    
    def __init__(self, config: ClientConfig, cache_handler=None):
        self.config = config
        self.cache = cache_handler
        self._public_key = None
        self._public_key_expiry = None

    async def get_public_key(self) -> str:
        """
        Fetch and cache Keycloak public key.
        Uses provided cache handler if available, otherwise uses in-memory cache.
        """
        if self.cache:
            # Try to get from external cache first
            cached_key = await self.cache.get('keycloak_public_key')
            if cached_key:
                return cached_key

        if self._public_key and self._public_key_expiry and \
           datetime.utcnow().timestamp() < self._public_key_expiry:
            return self._public_key

        # Fetch new public key
        url = f"{self.config.server_url}/realms/{self.config.realm_name}"
        try:
            response = await requests.get(url)
            response.raise_for_status()
            data = response.json()
            public_key = f"-----BEGIN PUBLIC KEY-----\n{data['public_key']}\n-----END PUBLIC KEY-----"
            
            # Cache the key
            if self.cache:
                await self.cache.set('keycloak_public_key', public_key, timeout=86400)
            
            # Update in-memory cache
            self._public_key = public_key
            self._public_key_expiry = datetime.utcnow().timestamp() + 86400  # 24 hours
            
            return public_key
        except requests.RequestException as e:
            raise ConfigError(f'Failed to fetch Keycloak public key: {str(e)}')
        except Exception as e:
            raise ConfigError(f'Failed to process Keycloak public key: {str(e)}')

    async def verify_token(self, token: str, verify_roles: Optional[list] = None) -> Dict[str, Any]:
        """
        Verify and decode JWT token with comprehensive validation.
        
        Args:
            token: JWT token string
            verify_roles: Optional list of roles to verify
            
        Returns:
            Dict containing decoded token data
            
        Raises:
            TokenError: If token validation fails
            ValidationError: If required claims are missing
        """
        try:
            # Clean token
            if token.startswith('Bearer '):
                token = token[7:]

            # Get public key
            public_key = await self.get_public_key()

            # Decode and verify token
            decoded_token = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                issuer=f"{self.config.server_url}/realms/{self.config.realm_name}",
                options={
                    'verify_exp': True,
                    'verify_aud': False,
                    'verify_iss': True,
                    'require': ['exp', 'iat', 'iss', 'sub']
                }
            )

            # Verify client ID
            if decoded_token.get('azp') != self.config.client_id:
                raise TokenError('Invalid token: Authorized party mismatch')

            # Verify roles if specified
            if verify_roles:
                token_roles = decoded_token.get('realm_access', {}).get('roles', [])
                if not any(role in token_roles for role in verify_roles):
                    raise TokenError('Invalid token: Required roles not present')

            # Extract user data
            user_data = {
                'id': decoded_token.get('sub'),
                'email': decoded_token.get('email'),
                'email_verified': decoded_token.get('email_verified', False),
                'username': decoded_token.get('preferred_username'),
                'first_name': decoded_token.get('given_name', decoded_token.get('first_name')),
                'last_name': decoded_token.get('family_name', decoded_token.get('last_name')),
                'name': decoded_token.get('name'),
                'roles': decoded_token.get('realm_access', {}).get('roles', []),
                'scope': decoded_token.get('scope', '').split(),
                'session_state': decoded_token.get('session_state'),
            }

            # Filter out None values
            return {k: v for k, v in user_data.items() if v is not None}

        except jwt.ExpiredSignatureError:
            raise TokenError('Token has expired')
        except jwt.InvalidTokenError as e:
            raise TokenError(f'Invalid token format: {str(e)}')
        except (TokenError, ValidationError):
            raise
        except Exception as e:
            raise TokenError(f'Token validation failed: {str(e)}')
