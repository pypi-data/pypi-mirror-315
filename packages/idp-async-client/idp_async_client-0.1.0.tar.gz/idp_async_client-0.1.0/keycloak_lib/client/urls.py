class ClientUrls:
  """URLs for regular client operations"""
  def __init__(
      self,
      server_url: str,
      realm_name: str
  ):
    base_url = f"{server_url}/realms/{realm_name}"
    self.token = f"{base_url}/protocol/openid-connect/token"
    self.auth = f"{base_url}/protocol/openid-connect/auth"
    self.logout = f"{base_url}/protocol/openid-connect/logout"
    self.user_info = f"{base_url}/protocol/openid-connect/userinfo"