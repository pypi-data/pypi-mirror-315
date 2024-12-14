import requests
import logging
from typing import Any
from ..exceptions.errors import KeycloakError

logger = logging.getLogger(__name__)

class BaseKeyCloakClient:
  """Base class for Keycloak clients"""

  def __init__(self, 
      server_url: str, 
      timeout: int = 10,
      verify_ssl: bool = True
    ):
    self.server_url = server_url.rstrip('/')
    self.timeout = timeout
    self.session = self._setup_session(verify_ssl)

  def _setup_session(self, verify_ssl: bool) -> requests.Session:
    session = requests.Session()
    session.verify = verify_ssl
    return session
  
  async def _request(
      self,
      method: str,
      url: str,
      **kwargs: Any
  ):
    try:
      kwargs['timeout'] = self.timeout
      response = self.session.request(method, url, **kwargs)
      if not response.content and response.status_code < 400:
        return {
          "success": True,
        }
      
      if response.status_code > 400:
        error_data = response.json() if response.content else {}
        raise KeycloakError(
          error_data.get('error_description', 'Unknown error'),
          status_code=response.status_code
        )

      return response.json() if response.content else {}
    except requests.exceptions.RequestException as e:
      logger.error(f"Error making request to {url}: {e}")
      raise KeycloakError(
        f"Request failed: {str(e)}"
      )


