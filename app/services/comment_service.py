from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.models.comment import Comment 
from app.schemas.comment import CommentCreate, CommentUpdate, CommentSchema, CommentFilter 
from app.db.session import get_db
from app.crud.comment import CommentCRUD
from typing import List, Optional
import uuid

class CommentService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.comment_crud = CommentCRUD()

    def add_comment(self, comment: CommentCreate) -> Comment:  
        """Crear un nuevo comentario"""
        return self.comment_crud.create(self.db, comment)

    def get_comment(self, comment_id: uuid.UUID) -> Optional[Comment]:
        """Obtener un comentario por ID"""
        comment = self.comment_crud.get(self.db, comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comentario no encontrado"
            )
        return comment
    
    def get_all_comments(self, skip: int = 0, limit: int = 100) -> List[Comment]: 
        """Obtener todos los comentarios activos"""
        return self.comment_crud.get_all(self.db, skip, limit)
    
    def get_comments_by_product(self, product_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Obtener todos los comentarios de un producto específico"""
        return self.comment_crud.get_by_product(self.db, product_id, skip, limit)
    
    def get_comments_by_user(self, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Obtener todos los comentarios de un usuario específico"""
        return self.comment_crud.get_by_user(self.db, user_id, skip, limit)
    
    def search_comments(self, filters: CommentFilter, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Buscar comentarios con filtros específicos"""
        return self.comment_crud.get_with_filters(self.db, filters, skip, limit)

    def update_comment(self, comment_id: uuid.UUID, updated_comment: CommentUpdate) -> Comment:
        """Actualizar un comentario existente"""
        comment = self.comment_crud.update(self.db, comment_id, updated_comment)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comentario no encontrado"
            )
        return comment

    def delete_comment(self, comment_id: uuid.UUID, soft_delete: bool = True) -> bool:
        """Eliminar un comentario (soft delete por defecto)"""
        if soft_delete:
            success = self.comment_crud.soft_delete(self.db, comment_id)
        else:
            success = self.comment_crud.delete(self.db, comment_id)
            
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comentario no encontrado"
            )
        return success
    
    def get_product_rating_stats(self, product_id: uuid.UUID) -> dict:
        """Obtener estadísticas de rating de un producto"""
        avg_rating = self.comment_crud.get_average_rating(self.db, product_id)
        comment_count = self.comment_crud.get_comment_count(self.db, product_id)
        
        return {
            "product_id": product_id,
            "average_rating": avg_rating,
            "total_comments": comment_count
        }
    
    def get_product_sentiment_stats(self, product_id: uuid.UUID) -> dict:
        """Obtener estadísticas de sentimiento de un producto específico"""
        stats = self.comment_crud.get_sentiment_stats(self.db, product_id)
        stats["product_id"] = product_id
        return stats
    
    def get_global_sentiment_stats(self) -> dict:
        """Obtener estadísticas globales de sentimiento"""
        return self.comment_crud.get_sentiment_stats(self.db)
    
    def verify_comment(self, comment_id: uuid.UUID) -> Comment:
        """Marcar un comentario como verificado - NO IMPLEMENTADO en modelo actual"""
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Función de verificación no disponible en el modelo actual"
        )