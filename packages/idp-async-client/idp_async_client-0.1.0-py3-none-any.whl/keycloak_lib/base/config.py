from dataclasses import dataclass

@dataclass
class ClientConfig:
    """Client configuration"""
    server_url: str
    realm_name: str
    client_id: str
    client_secret: str
    verify_ssl: bool = True
    timeout: int = 30

@dataclass
class AdminConfig:
    """Admin configuration"""
    server_url: str
    realm_name: str
    admin_username: str
    admin_password: str
    verify_ssl: bool = True
    timeout: int = 30
    client_id: str = 'admin-cli'