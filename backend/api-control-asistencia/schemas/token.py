# Importaciones
from sqlmodel import SQLModel

class Token(SQLModel):
    """
    Esquema para Token que contiene el access_token y el token_type
    """
    access_token: str
    token_type: str

class TokenData(SQLModel):
    """
    Esquema para TokenData que contiene el ID del usuario
    """
    id: int | None = None