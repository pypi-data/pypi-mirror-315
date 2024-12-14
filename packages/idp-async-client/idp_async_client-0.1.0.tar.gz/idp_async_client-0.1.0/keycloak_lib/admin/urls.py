# admin/urls.py
class AdminUrls:
  """URLs for admin operations"""
  def __init__(self, server_url: str, realm_name: str):
      self.master_token = f"{server_url}/realms/master/protocol/openid-connect/token"
      self.users = f"{server_url}/admin/realms/{realm_name}/users"
      self.roles = f"{server_url}/admin/realms/{realm_name}/roles"
      self.groups = f"{server_url}/admin/realms/{realm_name}/groups"