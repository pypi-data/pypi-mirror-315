from typing import TypedDict, Optional, Dict

class TokenResponse(TypedDict):
    access_token: str
    refresh_token: str
    expires_in: int
    refresh_expires_in: int
    token_type: str

class LogoutResponse(TypedDict):
    success: bool
    message: str

