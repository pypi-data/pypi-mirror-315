from functools import wraps
from typing import Callable, Any
from ..exceptions.errors import AuthenticationError, ConfigError
from ..utils.token_utils import TokenVerifier

def require_auth(roles: list = None):
    """Enhanced decorator with proper token verification"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get('request')
            if not request:
                raise AuthenticationError("No request object found")

            token = request.headers.get('Authorization')
            if not token:
                raise AuthenticationError("No authorization token provided")

            try:
                config = getattr(request, 'keycloak_config', None)
                if not config:
                    raise ConfigError("Keycloak configuration not found")
                    
                verifier = TokenVerifier(config)
                user_data = await verifier.verify_token(token, verify_roles=roles)
                request.user = user_data
                return await func(*args, **kwargs)
            except Exception as e:
                raise AuthenticationError(f"Authentication failed: {str(e)}")
        return wrapper
    return decorator