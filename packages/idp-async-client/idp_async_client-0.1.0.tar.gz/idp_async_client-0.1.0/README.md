# IdP Async Client Documentation

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [Token Management](#token-management)
- [Role-Based Access](#role-based-access)
- [Session Management](#session-management)
- [Web Integration](#web-integration)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [API Reference](#api-reference)
- [FAQ](#faq)

## Overview

IdP Async Client is a Python library that provides a unified interface for interacting with Identity Providers (IdPs). It currently supports Keycloak with plans to expand to other IdP solutions.

### Key Features
- Async/await support
- Token verification & management
- Session handling
- Role-based access control
- Web framework integration
- Extensible IdP support

## Installation

```bash
pip install idp-async-client
```

## Getting Started

### Basic Setup

```python
from idp_async_client import IdPClient, IdPConfig

# Configure the client
config = IdPConfig(
    provider="keycloak",
    server_url="http://localhost:8080",
    realm_name="my-realm",
    client_id="my-client",
    client_secret="my-secret"
)

# Create client instance
client = IdPClient(config)
```

### Initial Test

```python
# Test connection
async def test_connection():
    is_available = await client.test_connection()
    print(f"IdP server is {'available' if is_available else 'unavailable'}")
```

## Authentication

### Password-Based Login

```python
# Login with username and password
async def login():
    try:
        tokens = await client.login_with_password(
            username="user@example.com",
            password="secure_password"
        )
        return tokens
    except AuthenticationError as e:
        print(f"Login failed: {e}")
```

### Social Login

```python
# Login with social provider
async def social_login():
    tokens = await client.login_with_social(
        subject_token="social-provider-token",
        subject_issuer="google"
    )
    return tokens
```

## Token Management

### Token Verification

```python
# Verify token
async def verify_token(token: str):
    try:
        user_data = await client.verify_token(token)
        print(f"Token valid for user: {user_data['username']}")
        return user_data
    except TokenError as e:
        print(f"Token invalid: {e}")
```

### Token Refresh

```python
# Refresh access token
async def refresh_token(refresh_token: str):
    try:
        new_tokens = await client.refresh_token(refresh_token)
        return new_tokens
    except TokenError as e:
        print(f"Token refresh failed: {e}")
```

## Role-Based Access

### Role Verification

```python
# Check user roles
async def verify_user_access(token: str, required_roles: list):
    try:
        user_data = await client.verify_token(
            token=token,
            verify_roles=required_roles
        )
        return True
    except AuthenticationError:
        return False
```

### Protected Route Decorator

```python
from idp_async_client.auth import require_auth

@require_auth(roles=['admin'])
async def protected_route(request):
    return {"status": "accessed by admin"}
```

## Session Management

### Managing User Sessions

```python
# Get user sessions
async def get_sessions(user_id: str):
    sessions = await client.get_user_sessions(user_id)
    return sessions

# Revoke session
async def revoke_session(session_id: str):
    await client.revoke_session(session_id)
```

### Logout

```python
# Logout user
async def logout(refresh_token: str):
    try:
        await client.logout(refresh_token)
        return {"status": "logged out"}
    except Exception as e:
        print(f"Logout failed: {e}")
```

## Web Integration

### Middleware Setup

```python
from idp_async_client.middleware import IdPMiddleware

# FastAPI example
app = FastAPI()
app.add_middleware(
    IdPMiddleware,
    idp_client=client,
    required_roles=['user']
)

# Django example
MIDDLEWARE = [
    'idp_async_client.middleware.DjangoIdPMiddleware',
]
```

### Custom Cache Implementation

```python
from idp_async_client.cache import BaseCache

class RedisCache(BaseCache):
    def __init__(self, redis_client):
        self.redis = redis_client

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, timeout: int = None):
        await self.redis.set(key, value, ex=timeout)
```

## Configuration

### Configuration Options

```python
config = IdPConfig(
    # Required settings
    provider="keycloak",
    server_url="http://localhost:8080",
    realm_name="my-realm",
    client_id="my-client",
    client_secret="my-secret",
    
    # Optional settings
    verify_ssl=True,
    timeout=30,
    token_expires_in=300,
    refresh_expires_in=1800,
    cache_timeout=86400
)
```

### Environment Variables

```bash
export IDP_SERVER_URL="http://localhost:8080"
export IDP_REALM_NAME="my-realm"
export IDP_CLIENT_ID="my-client"
export IDP_CLIENT_SECRET="my-secret"
```

## Error Handling

### Exception Types

```python
from idp_async_client.exceptions import (
    IdPError,
    AuthenticationError,
    TokenError,
    ConfigError
)

async def handle_auth():
    try:
        tokens = await client.login_with_password(
            "username",
            "password"
        )
    except AuthenticationError as e:
        # Handle authentication failure
        print(f"Authentication failed: {e}")
    except TokenError as e:
        # Handle token-related errors
        print(f"Token error: {e}")
    except ConfigError as e:
        # Handle configuration issues
        print(f"Configuration error: {e}")
    except IdPError as e:
        # Handle general IdP errors
        print(f"IdP error: {e}")
```

## API Reference

### Main Classes

- `IdPClient`: Main client interface
- `IdPConfig`: Configuration class
- `TokenVerifier`: Token verification utilities
- `SessionManager`: Session management utilities

### Utilities

- `token_utils`: Token handling utilities
- `cache_utils`: Caching utilities
- `crypto_utils`: Cryptographic utilities

## FAQ

### Common Issues

**Q: Why am I getting token verification errors?**
A: Ensure your server's clock is synchronized and the token hasn't expired.

**Q: How do I handle token expiration?**
A: Use the refresh token to get a new access token before it expires.

**Q: Can I use multiple IdP providers?**
A: Yes, create separate client instances with different configurations.

### Best Practices

1. Always use HTTPS in production
2. Implement proper error handling
3. Use role-based access control
4. Regularly rotate client secrets
5. Implement token refresh logic
6. Use secure session storage