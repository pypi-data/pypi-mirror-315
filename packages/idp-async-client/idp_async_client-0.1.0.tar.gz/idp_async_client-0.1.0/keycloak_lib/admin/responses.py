from typing import TypedDict, List, Dict

class UserResponse(TypedDict):
    id: str
    username: str
    email: str
    firstName: str
    lastName: str
    enabled: bool
    attributes: Dict[str, List[str]]

class RegistrationResponse(TypedDict):
    id: str
    status: str
    message: str