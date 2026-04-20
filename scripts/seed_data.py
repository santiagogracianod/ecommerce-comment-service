#!/usr/bin/env python3
"""
Script para poblar la base de datos con comentarios de ejemplo con análisis de sentimiento
"""
import sys
import os
import uuid
from datetime import datetime, timedelta, timezone
import random

# Agregar el directorio raíz al path para importar módulos de la app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.comment import Comment

def seed_comments():
    """Seed the database with sample comments with sentiment analysis."""
    # Sample product UUIDs
    sample_product_ids = [
        uuid.UUID("f438b2e8-54c4-47f4-b9c4-ba9ce7bbe5cf"),  # iPhone 15 Pro Max
        uuid.UUID("641d925d-ab4e-4380-9140-76381aecab95"),  # MacBook Pro 14" M3
        uuid.UUID("2c54705e-998b-473f-b96f-c6620bfbccdb"),  # AirPods Pro (3ª generación)
        uuid.UUID("1f0ae883-d3d1-4b0b-ad0c-61b9dd6ec0e0"),  # Samsung Galaxy S24 Ultra
        uuid.UUID("964e8b17-7576-4d36-975e-91dae13beb79"),  # Sony WH-1000XM5
        uuid.UUID("d913db4b-12b8-4605-b3cf-b68c4d319197"),  # Dell XPS 13 Plus
        uuid.UUID("ec7581bf-d5e5-4945-85b0-9ad169438d45"),  # iPad Pro 12.9" M2
    ]
    
    sample_user_ids = [
        uuid.UUID("a0234567-89ab-cdef-0123-456789abcdef"),  # María González
        uuid.UUID("a1234567-89ab-cdef-0123-456789abcdef"),  # Carlos Rodríguez
        uuid.UUID("a2234567-89ab-cdef-0123-456789abcdef"),  # Ana López
        uuid.UUID("a3234567-89ab-cdef-0123-456789abcdef"),  # David Martín
        uuid.UUID("a4234567-89ab-cdef-0123-456789abcdef"),  # Laura Fernández
        uuid.UUID("a5234567-89ab-cdef-0123-456789abcdef"),  # Roberto Sánchez
    ]
    
    comments_data = [
        # Comentarios POSITIVOS con alta confianza
        {
            "comment": "¡Excelente teléfono! La cámara es increíble y la batería dura todo el día. Muy recomendado.",
            "rating": 5,
            "product_id": sample_product_ids[0],
            "user_id": sample_user_ids[0],
            "reviewer_name": "María González",
            "sentiment_score": 0.95,  # Alta confianza
            "sentiment_label": "positive"
        },
        {
            "comment": "El mejor iPhone hasta ahora. El titanio se siente premium y el rendimiento es sobresaliente.",
            "rating": 5,
            "product_id": sample_product_ids[0],
            "user_id": sample_user_ids[2],
            "reviewer_name": "Ana López",
            "sentiment_score": 0.92,
            "sentiment_label": "positive"
        },
        {
            "comment": "Perfecto para desarrollo de software. El chip M3 es una bestia y la pantalla es hermosa.",
            "rating": 5,
            "product_id": sample_product_ids[1],
            "user_id": sample_user_ids[3],
            "reviewer_name": "David Martín",
            "sentiment_score": 0.89,
            "sentiment_label": "positive"
        },
        {
            "comment": "La cancelación de ruido es impresionante. Perfectos para viajar y trabajar.",
            "rating": 5,
            "product_id": sample_product_ids[2],
            "user_id": sample_user_ids[5],
            "reviewer_name": "Roberto Sánchez",
            "sentiment_score": 0.87,
            "sentiment_label": "positive"
        },
        {
            "comment": "Los mejores audífonos over-ear que he probado. La cancelación de ruido es excepcional.",
            "rating": 5,
            "product_id": sample_product_ids[4],
            "user_id": sample_user_ids[3],
            "reviewer_name": "Alejandro Vega",
            "sentiment_score": 0.94,
            "sentiment_label": "positive"
        },
        # Comentarios NEGATIVOS con alta confianza
        {
            "comment": "No me gustó para nada. Se calienta mucho y la batería no dura lo prometido. Muy decepcionante.",
            "rating": 2,
            "product_id": sample_product_ids[0],
            "user_id": sample_user_ids[3],
            "reviewer_name": "Pedro Molina",
            "sentiment_score": 0.93,  # Alta confianza negativa
            "sentiment_label": "negative"
        },
        {
            "comment": "Terrible experiencia. El producto llegó defectuoso y el servicio al cliente fue pésimo.",
            "rating": 1,
            "product_id": sample_product_ids[1],
            "user_id": sample_user_ids[0],
            "reviewer_name": "Carmen Ruiz",
            "sentiment_score": 0.97,
            "sentiment_label": "negative"
        },
        # Comentarios sin análisis de sentimiento (opcional)
        {
            "comment": "Producto estándar, cumple con las especificaciones básicas. Nada especial.",
            "rating": 3,
            "product_id": sample_product_ids[3],
            "user_id": sample_user_ids[4],
            "reviewer_name": "Roberto Silva",
            # Sin sentiment_score ni sentiment_label (opcionales)
        },
        {
            "comment": "Lo compré hace una semana, aún estoy probándolo. Por ahora todo bien.",
            "rating": 4,
            "product_id": sample_product_ids[5],
            "user_id": sample_user_ids[3],
            "reviewer_name": "Ana Torres",
            # Sin análisis de sentimiento
        }
    ]
    
    return comments_data

def seed_comments_data():
    """Función principal para poblar la base de datos con comentarios de ejemplo"""
    db = SessionLocal()
    try:
        # Verificar si ya existen comentarios
        existing_comments = db.query(Comment).first()
        if existing_comments:
            print("❌ Ya existen reseñas en la base de datos. Saltando la creación de datos de ejemplo.")
            return
        
        print("🌱 Creando reseñas de ejemplo con análisis de sentimiento...")
        
        # Crear comentarios
        comments_data = seed_comments()
        created_count = 0
        
        for comment_data in comments_data:
            # Añadir timestamps realistas (comentarios de los últimos 6 meses)
            days_ago = random.randint(1, 180)
            created_at = datetime.now(timezone.utc) - timedelta(days=days_ago)
            
            comment = Comment(
                **comment_data,
                created_at=created_at
            )
            
            db.add(comment)
            created_count += 1
        
        db.commit()
        print(f"✅ Se crearon {created_count} reseñas de ejemplo exitosamente.")
        
        # Mostrar estadísticas
        total_comments = db.query(Comment).count()
        avg_rating = db.query(func.avg(Comment.rating)).scalar()
        
        # Estadísticas de sentimiento
        positive_count = db.query(Comment).filter(Comment.sentiment_label == 'positive').count()
        negative_count = db.query(Comment).filter(Comment.sentiment_label == 'negative').count()
        comments_without_sentiment = db.query(Comment).filter(Comment.sentiment_label.is_(None)).count()
        avg_confidence = db.query(func.avg(Comment.sentiment_score)).filter(Comment.sentiment_score.isnot(None)).scalar()
        
        print(f"\n📊 Estadísticas de la base de datos:")
        print(f"   • Total de reseñas: {total_comments}")
        print(f"   • Calificación promedio: {avg_rating:.2f}/5.0" if avg_rating else "   • Calificación promedio: N/A")
        print(f"   • Confianza promedio: {avg_confidence:.3f}" if avg_confidence else "   • Confianza promedio: N/A")
        print(f"   • Comentarios positivos: {positive_count}")
        print(f"   • Comentarios negativos: {negative_count}")
        print(f"   • Comentarios sin análisis: {comments_without_sentiment}")
        
    except Exception as e:
        print(f"❌ Error al crear comentarios de ejemplo: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando creación de datos de ejemplo para el servicio de reseñas...")
    seed_comments_data()
    print("🎉 Proceso completado.")
