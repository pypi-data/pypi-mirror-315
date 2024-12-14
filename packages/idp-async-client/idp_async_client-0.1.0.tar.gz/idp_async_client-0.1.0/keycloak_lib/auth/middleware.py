# auth/middleware.py
from typing import Optional
from ..client.client import KeycloakClient
from ..exceptions.errors import AuthenticationError

class KeycloakMiddleware:
  """Middleware for handling Keycloak authentication"""
  
  def __init__(self, keycloak_client: KeycloakClient):
      self.keycloak_client = keycloak_client

  async def __call__(self, request, call_next):
      try:
          # Check for token in cookies or headers
          token = request.cookies.get('access_token') or request.headers.get('Authorization')
          
          if token:
              # Verify and refresh token if needed
              if token.startswith('Bearer '):
                  token = token[7:]
              
              try:
                  # Attempt to validate token
                  # If invalid, try refresh
                  refresh_token = request.cookies.get('refresh_token')
                  if refresh_token:
                      new_tokens = await self.keycloak_client.refresh_token(refresh_token)
                      # Update tokens in response
                      response = await call_next(request)
                      response.set_cookie('access_token', new_tokens['access_token'])
                      response.set_cookie('refresh_token', new_tokens['refresh_token'])
                      return response
              except:
                  pass
          
          return await call_next(request)
          
      except Exception as e:
          raise AuthenticationError(f"Middleware error: {str(e)}")
