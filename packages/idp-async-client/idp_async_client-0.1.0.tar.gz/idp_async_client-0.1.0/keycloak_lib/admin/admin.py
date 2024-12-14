# admin/admin.py
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
import logging
from ..base.base_client import BaseKeycloakClient
from ..base.config import AdminConfig
from .urls import AdminUrls
from .responses import UserResponse, RegistrationResponse
from ..exceptions.errors import AdminError, KeycloakError, RegistrationError
from ..utils.token_utils import is_token_expired

logger = logging.getLogger(__name__)

class KeycloakAdmin(BaseKeycloakClient):
    """Client for Keycloak admin operations"""
    
    def __init__(self, config: AdminConfig):
        super().__init__(config.server_url, config.verify_ssl, config.timeout)
        self.config = config
        self.urls = AdminUrls(config.server_url, config.realm_name)
        self._admin_token = None
        self._admin_token_expires = None

    async def _get_admin_token(self, grant_type: str = 'password') -> str:
        """Get and cache admin token"""
        if not self._admin_token or is_token_expired(self._admin_token):
            try:
                data = {
                    'username': self.config.admin_username,
                    'password': self.config.admin_password,
                    'grant_type': grant_type,
                    'client_id': self.config.client_id
                }
                
                response = await self._request('POST', self.urls.master_token, data=data)
                self._admin_token = response['access_token']
                
            except Exception as e:
                logger.error(f"Admin token acquisition failed: {str(e)}")
                raise AdminError(f"Failed to get admin token: {str(e)}")
                
        return f"Bearer {self._admin_token}"

    async def create_user(self, user_data: Dict[str, Any]) -> RegistrationResponse:
        """Create new user"""
        admin_token = await self._get_admin_token()
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': admin_token
        }
        
        payload = {
            "enabled": True,
            "username": user_data['username'],
            "email": user_data['email'],
            "firstName": user_data.get('firstName', ''),
            "lastName": user_data.get('lastName', ''),
            "attributes": user_data.get('attributes', {}),
            "credentials": [{
                "type": "password",
                "value": user_data['password'],
                "temporary": False
            }]
        }
        
        try:
            response = await self._request('POST', self.urls.users, headers=headers, json=payload)
            return {
                "id": response.get('id', ''),
                "status": "success",
                "message": "User created successfully"
            }
        except KeycloakError as e:
            raise RegistrationError(f"User creation failed: {str(e)}")

    async def get_user(self, user_id: str) -> UserResponse:
        """Get user details"""
        admin_token = await self._get_admin_token()
        headers = {'Authorization': admin_token}
        
        try:
            return await self._request('GET', f"{self.urls.users}/{user_id}", headers=headers)
        except KeycloakError as e:
            raise AdminError(f"Failed to get user: {str(e)}")

    async def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, str]:
        """Update user details"""
        admin_token = await self._get_admin_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': admin_token
        }
        
        try:
            await self._request('PUT', f"{self.urls.users}/{user_id}", headers=headers, json=user_data)
            return {"status": "success", "message": "User updated successfully"}
        except KeycloakError as e:
            raise AdminError(f"Failed to update user: {str(e)}")

    async def delete_user(self, user_id: str) -> Dict[str, str]:
        """Delete user"""
        admin_token = await self._get_admin_token()
        headers = {'Authorization': admin_token}
        
        try:
            await self._request('DELETE', f"{self.urls.users}/{user_id}", headers=headers)
            return {"status": "success", "message": "User deleted successfully"}
        except KeycloakError as e:
            raise AdminError(f"Failed to delete user: {str(e)}")