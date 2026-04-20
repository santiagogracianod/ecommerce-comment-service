# Este archivo permite que la carpeta 'services' sea reconocida como un módulo de Python.
from app.services.comment_service import CommentService

__all__ = ["CommentService"]