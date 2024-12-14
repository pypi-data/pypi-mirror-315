from typing import Dict, Any
from ..base.base_client import BaseKeyCloakClient
from ..exceptions.errors import SessionError

class SessionManager(BaseKeyCloakClient):
    """Manages user sessions in Keycloak"""
    
    def __init__(self, admin_client):
        self.admin_client = admin_client
        super().__init__(admin_client.config.server_url, 
                        admin_client.config.verify_ssl,
                        admin_client.config.timeout)

    async def get_user_sessions(self, user_id: str) -> Dict[str, Any]:
        """Get all active sessions for a user"""
        admin_token = await self.admin_client._get_admin_token()
        headers = {'Authorization': admin_token}
        
        try:
            url = f"{self.admin_client.urls.users}/{user_id}/sessions"
            return await self._request('GET', url, headers=headers)
        except Exception as e:
            raise SessionError(f"Failed to get user sessions: {str(e)}")

    async def revoke_session(self, session_id: str) -> Dict[str, str]:
        """Revoke a specific session"""
        admin_token = await self.admin_client._get_admin_token()
        headers = {'Authorization': admin_token}
        
        try:
            url = f"{self.admin_client.config.server_url}/admin/realms/{self.admin_client.config.realm_name}/sessions/{session_id}"
            await self._request('DELETE', url, headers=headers)
            return {"status": "success", "message": "Session revoked successfully"}
        except Exception as e:
            raise SessionError(f"Failed to revoke session: {str(e)}")
