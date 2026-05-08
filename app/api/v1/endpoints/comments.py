from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.schemas.comment import CommentSchema, CommentCreate, CommentUpdate, CommentFilter
from app.services.comment_service import CommentService
from app.db.session import get_db

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo comentario"""
    service = CommentService(db)
    return service.add_comment(comment)

@router.get("/", response_model=List[CommentSchema])
def list_comments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Listar todos los comentarios activos"""
    service = CommentService(db)
    return service.get_all_comments(skip, limit)

@router.get("/product/{product_id}", response_model=List[CommentSchema])
def get_comments_by_product(
    product_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener todos los comentarios de un producto específico"""
    service = CommentService(db)
    return service.get_comments_by_product(product_id, skip, limit)

@router.get("/user/{user_id}", response_model=List[CommentSchema])
def get_comments_by_user(
    user_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener todos los comentarios de un usuario específico"""
    service = CommentService(db)
    return service.get_comments_by_user(user_id, skip, limit)

@router.get("/search", response_model=List[CommentSchema])
def search_comments(
    product_id: Optional[uuid.UUID] = Query(None),
    user_id: Optional[uuid.UUID] = Query(None),
    rating: Optional[int] = Query(None, ge=1, le=5),
    sentiment_label: Optional[str] = Query(None, description="Filtrar por sentimiento: positive o negative"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Buscar comentarios con filtros específicos incluyendo sentimiento"""
    filters = CommentFilter(
        product_id=product_id,
        user_id=user_id,
        rating=rating,
        sentiment_label=sentiment_label
    )
    service = CommentService(db)
    return service.search_comments(filters, skip, limit)

@router.get("/{comment_id}", response_model=CommentSchema)
def get_comment(
    comment_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Obtener un comentario específico por ID"""
    service = CommentService(db)
    return service.get_comment(comment_id)

@router.get("/product/{product_id}/stats")
def get_product_rating_stats(
    product_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de rating de un producto"""
    service = CommentService(db)
    return service.get_product_rating_stats(product_id)

@router.get("/product/{product_id}/sentiment-stats")
def get_product_sentiment_stats(
    product_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de sentimiento de un producto"""
    service = CommentService(db)
    return service.get_product_sentiment_stats(product_id)

@router.get("/sentiment-stats/global")
def get_global_sentiment_stats(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas globales de sentimiento"""
    service = CommentService(db)
    return service.get_global_sentiment_stats()

@router.put("/{comment_id}", response_model=CommentSchema)
def update_comment(
    comment_id: uuid.UUID,
    comment: CommentUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un comentario existente"""
    service = CommentService(db)
    return service.update_comment(comment_id, comment)

@router.patch("/{comment_id}/verify", response_model=CommentSchema)
def verify_comment(
    comment_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Marcar un comentario como verificado"""
    service = CommentService(db)
    return service.verify_comment(comment_id)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: uuid.UUID,
    soft_delete: bool = Query(True, description="Si es True, hace soft delete; si es False, elimina permanentemente"),
    db: Session = Depends(get_db)
):
    """Eliminar un comentario (soft delete por defecto)"""
    service = CommentService(db)
    service.delete_comment(comment_id, soft_delete)