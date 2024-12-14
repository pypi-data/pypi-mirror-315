from typing import Dict, Optional
from ..base.base_client import BaseKeyCloakClient
from ..base.config import ClientConfig
from .urls import ClientUrls
from .responses import TokenResponse, LogoutResponse
from ..exceptions.errors import AuthenticationError, TokenError, KeycloakError

class KeycloakClient(BaseKeyCloakClient):
    """Client for regular Keycloak operations"""
    
    def __init__(self, config: ClientConfig):
        super().__init__(config.server_url, config.verify_ssl, config.timeout)
        self.config = config
        self.urls = ClientUrls(config.server_url, config.realm_name)

    async def login_with_password(self, username: str, password: str, grant_type: str) -> TokenResponse:
        """Password-based authentication"""
        data = {
            'grant_type': grant_type,
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret,
            'username': username,
            'password': password
        }
        
        try:
            return await self._request('POST', self.urls.token, data=data)
        except KeycloakError as e:
            raise AuthenticationError(f"Password login failed: {str(e)}")

    async def login_with_social(self, subject_token: str, subject_issuer: str) -> TokenResponse:
        """Social login authentication"""
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret,
            'subject_token': subject_token,
            'subject_issuer': subject_issuer
        }
        
        try:
            return await self._request('POST', self.urls.token, data=data)
        except KeycloakError as e:
            raise AuthenticationError(f"Social login failed: {str(e)}")

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Refresh access token"""
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret,
            'refresh_token': refresh_token
        }
        
        try:
            return await self._request('POST', self.urls.token, data=data)
        except KeycloakError as e:
            raise TokenError(f"Token refresh failed: {str(e)}")

    async def logout(self, refresh_token: str, session_state: Optional[str] = None) -> LogoutResponse:
        """Handle user logout"""
        data = {
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret,
            'refresh_token': refresh_token
        }
        
        if session_state:
            data['session_state'] = session_state
            
        try:
            await self._request('POST', self.urls.logout, data=data)
            return {
                "success": True,
                "message": "Logged out successfully"
            }
        except KeycloakError as e:
            raise AuthenticationError(f"Logout failed: {str(e)}")