"""
Utilidades y funciones auxiliares para el servicio
"""
import uuid
from typing import Optional
from datetime import datetime, timezone

def generate_uuid() -> str:
    """Genera un UUID4 como string"""
    return str(uuid.uuid4())

def is_valid_uuid(uuid_string: str) -> bool:
    """Verifica si una string es un UUID válido"""
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False

def utc_now() -> datetime:
    """Retorna la fecha/hora actual en UTC"""
    return datetime.now(timezone.utc)

def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Formatea datetime a string ISO"""
    if dt is None:
        return None
    return dt.isoformat()