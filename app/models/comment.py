from sqlalchemy import Column, Integer, Text, DateTime, Index, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base

import uuid

class Comment(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    reviewer_name = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    
    # Campos para análisis de sentimiento (opcionales)
    sentiment_score = Column(Float, nullable=True, comment="Confianza de la predicción de sentimiento (0-1)")
    sentiment_label = Column(Text, nullable=True, comment="Etiqueta de sentimiento: positive o negative")
    sentiment_model_version = Column(Text, nullable=True, comment="Versión del modelo que realizó la predicción: v1, v2, etc.")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_reviews_product_id', 'product_id'),
        Index('idx_reviews_user_id', 'user_id'),
        Index('idx_reviews_created_at', 'created_at'),
        Index('idx_reviews_sentiment', 'sentiment_label'),  # Índice para consultas por sentimiento
    )