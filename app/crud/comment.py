from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate, CommentFilter
from typing import List, Optional
import uuid

class CommentCRUD:
    def create(self, db: Session, comment_data: CommentCreate) -> Comment:
        db_comment = Comment(**comment_data.dict())
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    
    def get(self, db: Session, comment_id: uuid.UUID) -> Optional[Comment]:
        return db.query(Comment).filter(Comment.id == comment_id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Comment]:
        return db.query(Comment).offset(skip).limit(limit).all()
    
    def get_by_product(self, db: Session, product_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
        return db.query(Comment).filter(Comment.product_id == product_id).offset(skip).limit(limit).all()
    
    def get_by_user(self, db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
        return db.query(Comment).filter(Comment.user_id == user_id).offset(skip).limit(limit).all()
    
    def get_with_filters(self, db: Session, filters: CommentFilter, skip: int = 0, limit: int = 100) -> List[Comment]:
        query = db.query(Comment)
        
        if filters.product_id:
            query = query.filter(Comment.product_id == filters.product_id)
        if filters.user_id:
            query = query.filter(Comment.user_id == filters.user_id)
        if filters.rating:
            query = query.filter(Comment.rating == filters.rating)
            
        return query.offset(skip).limit(limit).all()
    
    def update(self, db: Session, comment_id: uuid.UUID, comment_data: CommentUpdate) -> Optional[Comment]:
        db_comment = self.get(db, comment_id)
        if not db_comment:
            return None
        
        update_data = comment_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_comment, key, value)
        
        db.commit()
        db.refresh(db_comment)
        return db_comment
    
    def delete(self, db: Session, comment_id: uuid.UUID) -> bool:
        """Hard delete - elimina permanentemente el comentario"""
        db_comment = self.get(db, comment_id)
        if not db_comment:
            return False
        
        db.delete(db_comment)
        db.commit()
        return True
    
    def soft_delete(self, db: Session, comment_id: uuid.UUID) -> bool:
        """Soft delete - como no tenemos campo is_active, implementamos como hard delete"""
        return self.delete(db, comment_id)
    
    def get_average_rating(self, db: Session, product_id: uuid.UUID) -> Optional[float]:
        """Obtiene el rating promedio de un producto"""
        from sqlalchemy import func
        result = db.query(func.avg(Comment.rating)).filter(
            Comment.product_id == product_id
        ).scalar()
        return float(result) if result else None
    
    def get_comment_count(self, db: Session, product_id: uuid.UUID) -> int:
        """Obtiene el número total de comentarios de un producto"""
        return db.query(Comment).filter(Comment.product_id == product_id).count()
    
    def get_sentiment_stats(self, db: Session, product_id: Optional[uuid.UUID] = None) -> dict:
        """Obtiene estadísticas de sentimiento para positive/negative únicamente"""
        from sqlalchemy import func, case
        
        query = db.query(Comment)
        if product_id:
            query = query.filter(Comment.product_id == product_id)
        
        # Contar sentimientos y calcular promedio de confianza
        sentiment_stats = db.query(
            func.count(case([(Comment.sentiment_label == 'positive', 1)])).label('positive'),
            func.count(case([(Comment.sentiment_label == 'negative', 1)])).label('negative'),
            func.count(case([(Comment.sentiment_label.isnot(None), 1)])).label('total_with_sentiment'),
            func.count(Comment.id).label('total_comments'),
            func.avg(case([(Comment.sentiment_score.isnot(None), Comment.sentiment_score)])).label('avg_confidence')
        )
        
        if product_id:
            sentiment_stats = sentiment_stats.filter(Comment.product_id == product_id)
        
        result = sentiment_stats.first()
        
        total_comments = result.total_comments if result.total_comments else 0
        total_with_sentiment = result.total_with_sentiment if result.total_with_sentiment else 0
        positive = result.positive if result.positive else 0
        negative = result.negative if result.negative else 0
        avg_confidence = result.avg_confidence if result.avg_confidence else 0.0
        
        return {
            "total_comments": total_comments,
            "comments_with_sentiment": total_with_sentiment,
            "comments_without_sentiment": total_comments - total_with_sentiment,
            "positive": positive,
            "negative": negative,
            "positive_percentage": round((positive / total_with_sentiment) * 100, 2) if total_with_sentiment > 0 else 0,
            "negative_percentage": round((negative / total_with_sentiment) * 100, 2) if total_with_sentiment > 0 else 0,
            "average_confidence": round(avg_confidence, 3)
        }