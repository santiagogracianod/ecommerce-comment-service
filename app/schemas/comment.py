from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import uuid

class ReviewBase(BaseModel):
    product_id: uuid.UUID = Field(..., description="ID del producto reseñado")
    user_id: uuid.UUID = Field(..., description="ID del usuario que hace la reseña")
    reviewer_name: Optional[str] = Field(None, description="Nombre del reseñador")
    rating: int = Field(..., ge=1, le=5, description="Calificación de 1 a 5 estrellas")
    comment: str = Field(..., min_length=1, max_length=2000, description="Texto del comentario")
    
    @validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('El rating debe estar entre 1 y 5')
        return v

class ReviewCreate(ReviewBase):
    # Campos opcionales para análisis de sentimiento
    sentiment_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confianza de la predicción (0-1)")
    sentiment_label: Optional[str] = Field(None, description="Etiqueta de sentimiento: positive, negative o neutral")
    sentiment_model_version: Optional[str] = Field(None, description="Versión del modelo: v1, v2, etc.")

    @validator('sentiment_label')
    def validate_sentiment_label(cls, v):
        if v is not None and v not in ['positive', 'negative', 'neutral']:
            raise ValueError('La etiqueta de sentimiento debe ser positive, negative o neutral')
        return v

class ReviewUpdate(BaseModel):
    reviewer_name: Optional[str] = Field(None, description="Nombre del reseñador")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Calificación de 1 a 5 estrellas")
    comment: Optional[str] = Field(None, min_length=1, max_length=2000, description="Texto del comentario")
    sentiment_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confianza de la predicción (0-1)")
    sentiment_label: Optional[str] = Field(None, description="Etiqueta de sentimiento: positive, negative o neutral")
    sentiment_model_version: Optional[str] = Field(None, description="Versión del modelo: v1, v2, etc.")

    @validator('rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('El rating debe estar entre 1 y 5')
        return v

    @validator('sentiment_label')
    def validate_sentiment_label(cls, v):
        if v is not None and v not in ['positive', 'negative', 'neutral']:
            raise ValueError('La etiqueta de sentimiento debe ser positive, negative o neutral')
        return v

class ReviewInDB(ReviewBase):
    id: uuid.UUID
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    sentiment_model_version: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ReviewSchema(ReviewInDB):
    pass

# Schema para filtros de búsqueda
class ReviewFilter(BaseModel):
    product_id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    sentiment_label: Optional[str] = Field(None, description="Filtrar por sentimiento: positive, negative o neutral")

# Mantener alias para compatibilidad
CommentBase = ReviewBase
CommentCreate = ReviewCreate
CommentUpdate = ReviewUpdate
CommentInDB = ReviewInDB
CommentSchema = ReviewSchema
CommentFilter = ReviewFilter