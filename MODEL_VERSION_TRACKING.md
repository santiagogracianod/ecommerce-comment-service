# 🏷️ Tracking de Versión del Modelo de Sentimiento

## Descripción

El servicio de comentarios ahora guarda en la base de datos qué versión del modelo de análisis de sentimiento se utilizó para cada predicción.

## Campo Agregado

### `sentiment_model_version`

- **Tipo**: Text (String)
- **Nullable**: Sí
- **Valores**: `v1`, `v2`, `blue`, `green`, etc.
- **Descripción**: Identifica qué modelo realizó el análisis de sentimiento

## Modelo de Datos Actualizado

```python
class Comment(Base):
    __tablename__ = "reviews"

    id = Column(UUID)
    product_id = Column(UUID)
    user_id = Column(UUID)
    reviewer_name = Column(Text)
    rating = Column(Integer)
    comment = Column(Text)

    # Campos de sentimiento
    sentiment_score = Column(Float)              # Confianza 0-1
    sentiment_label = Column(Text)               # positive/negative
    sentiment_model_version = Column(Text)       # 🆕 NUEVO: v1, v2, etc.

    created_at = Column(DateTime)
```

## Uso

### Crear Comentario con Versión del Modelo

```python
# Ejemplo con modelo V1
comment_data = {
    "product_id": "123e4567-e89b-12d3-a456-426614174000",
    "user_id": "223e4567-e89b-12d3-a456-426614174001",
    "reviewer_name": "Juan Pérez",
    "rating": 5,
    "comment": "Excelente producto!",
    "sentiment_score": 0.98,
    "sentiment_label": "positive",
    "sentiment_model_version": "v1"  # 🆕 Indica que V1 hizo la predicción
}
```

### Ejemplo con API REST

```bash
# Crear comentario indicando qué modelo analizó
curl -X POST "http://localhost:8001/api/v1/comments/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "123e4567-e89b-12d3-a456-426614174000",
    "user_id": "223e4567-e89b-12d3-a456-426614174001",
    "reviewer_name": "María García",
    "rating": 4,
    "comment": "Muy buena calidad",
    "sentiment_score": 0.95,
    "sentiment_label": "positive",
    "sentiment_model_version": "v2"
  }'
```

### Consultar Comentarios por Versión del Modelo

```sql
-- Ver qué modelo analizó cada comentario
SELECT
    id,
    comment,
    sentiment_label,
    sentiment_score,
    sentiment_model_version,
    created_at
FROM reviews
WHERE sentiment_model_version IS NOT NULL
ORDER BY created_at DESC
LIMIT 10;

-- Comparar distribución de sentimientos por modelo
SELECT
    sentiment_model_version,
    sentiment_label,
    COUNT(*) as total,
    AVG(sentiment_score) as avg_confidence
FROM reviews
WHERE sentiment_model_version IS NOT NULL
GROUP BY sentiment_model_version, sentiment_label
ORDER BY sentiment_model_version, sentiment_label;
```

## Integración con API Gateway

### Flujo Completo

```
┌─────────────────┐
│  Cliente        │
└────────┬────────┘
         │ 1. POST /comments
         v
┌─────────────────┐
│ Comments        │
│ Service         │
└────────┬────────┘
         │ 2. Analizar sentimiento
         v
┌─────────────────┐      ┌──────────────┐
│  API Gateway    │◄─────│ Detecta      │
│  (Port 8888)    │      │ modelo activo│
└────────┬────────┘      └──────────────┘
         │ 3. Envía a modelo activo
         ├─────────────┬─────────────┐
         │             │             │
         v             v             v
   ┌─────────┐   ┌─────────┐
   │ V1 (Blue)│   │ V2 (Green)│
   │ :8002   │   │ :8005   │
   └────┬────┘   └────┬────┘
        │             │
        └──────┬──────┘
               │ 4. Respuesta con predicción
               v
      ┌─────────────────┐
      │ {               │
      │   sentiment: +, │
      │   score: 0.98,  │
      │   version: "v1" │ ◄── Info del modelo
      │ }               │
      └────────┬────────┘
               │ 5. Guardar en DB con versión
               v
      ┌─────────────────┐
      │ Database        │
      │ reviews table   │
      └─────────────────┘
```

## Estadísticas y Análisis

### Comparar Performance de Modelos

```python
# Obtener estadísticas por modelo
def get_model_comparison():
    """Compara performance de diferentes versiones de modelos"""

    query = """
    SELECT
        sentiment_model_version as model,
        COUNT(*) as total_predictions,
        AVG(sentiment_score) as avg_confidence,
        COUNT(CASE WHEN sentiment_label = 'positive' THEN 1 END) as positive_count,
        COUNT(CASE WHEN sentiment_label = 'negative' THEN 1 END) as negative_count
    FROM reviews
    WHERE sentiment_model_version IS NOT NULL
    GROUP BY sentiment_model_version
    """

    return execute_query(query)

# Resultado esperado:
# {
#   "v1": {
#     "total_predictions": 1000,
#     "avg_confidence": 0.92,
#     "positive_count": 750,
#     "negative_count": 250
#   },
#   "v2": {
#     "total_predictions": 500,
#     "avg_confidence": 0.95,
#     "positive_count": 400,
#     "negative_count": 100
#   }
# }
```

### Monitorear Calidad por Modelo

```python
# Detectar si un modelo tiene baja confianza
def check_model_quality(threshold=0.8):
    """Identifica modelos con predicciones de baja confianza"""

    query = """
    SELECT
        sentiment_model_version,
        AVG(sentiment_score) as avg_score,
        MIN(sentiment_score) as min_score,
        MAX(sentiment_score) as max_score,
        STDDEV(sentiment_score) as std_dev
    FROM reviews
    WHERE sentiment_model_version IS NOT NULL
    GROUP BY sentiment_model_version
    HAVING AVG(sentiment_score) < :threshold
    """

    return execute_query(query, {'threshold': threshold})
```

## Casos de Uso

### 1. Auditoría de Predicciones

Saber qué modelo hizo cada predicción permite:
- Rastrear errores a versiones específicas
- Identificar cuándo se hizo cada predicción
- Validar resultados históricos

```python
# Encontrar todas las predicciones incorrectas de V1
SELECT * FROM reviews
WHERE sentiment_model_version = 'v1'
  AND sentiment_label = 'positive'
  AND rating <= 2  -- Rating bajo pero sentimiento positivo (posible error)
```

### 2. A/B Testing de Modelos

Comparar resultados de diferentes modelos:

```python
# Comparar mismo texto analizado por V1 y V2
SELECT
    comment,
    MAX(CASE WHEN sentiment_model_version = 'v1' THEN sentiment_score END) as v1_score,
    MAX(CASE WHEN sentiment_model_version = 'v2' THEN sentiment_score END) as v2_score,
    MAX(CASE WHEN sentiment_model_version = 'v1' THEN sentiment_label END) as v1_label,
    MAX(CASE WHEN sentiment_model_version = 'v2' THEN sentiment_label END) as v2_label
FROM reviews
WHERE comment IN (
    SELECT comment
    FROM reviews
    GROUP BY comment
    HAVING COUNT(DISTINCT sentiment_model_version) > 1
)
GROUP BY comment
```

### 3. Rollback de Modelo

Si V2 produce malos resultados:

```python
# Identificar comentarios analizados por V2
SELECT COUNT(*) FROM reviews
WHERE sentiment_model_version = 'v2'
  AND created_at > '2025-11-10 00:00:00'

# Re-analizar con V1
UPDATE reviews
SET sentiment_score = NULL,
    sentiment_label = NULL,
    sentiment_model_version = NULL
WHERE sentiment_model_version = 'v2'
  AND created_at > '2025-11-10 00:00:00'
```

### 4. Análisis de Drift

Detectar si un modelo está degradándose:

```python
# Ver evolución de confianza por modelo a lo largo del tiempo
SELECT
    DATE(created_at) as date,
    sentiment_model_version,
    AVG(sentiment_score) as avg_confidence,
    COUNT(*) as predictions
FROM reviews
WHERE sentiment_model_version IS NOT NULL
GROUP BY DATE(created_at), sentiment_model_version
ORDER BY date DESC, sentiment_model_version
```

## Migración Aplicada

```sql
-- Migración: 38fbae3e45e2
ALTER TABLE reviews
ADD COLUMN sentiment_model_version TEXT;

COMMENT ON COLUMN reviews.sentiment_model_version IS
'Versión del modelo que realizó la predicción: v1, v2, etc.';
```

## API Endpoints Actualizados

### POST /api/v1/comments/

**Request Body:**
```json
{
  "product_id": "uuid",
  "user_id": "uuid",
  "reviewer_name": "string",
  "rating": 5,
  "comment": "string",
  "sentiment_score": 0.98,           // Opcional
  "sentiment_label": "positive",     // Opcional
  "sentiment_model_version": "v1"    // 🆕 NUEVO - Opcional
}
```

**Response:**
```json
{
  "id": "uuid",
  "product_id": "uuid",
  "user_id": "uuid",
  "reviewer_name": "string",
  "rating": 5,
  "comment": "string",
  "sentiment_score": 0.98,
  "sentiment_label": "positive",
  "sentiment_model_version": "v1",   // 🆕 NUEVO
  "created_at": "2025-11-11T00:00:00Z"
}
```

## Mejores Prácticas

### 1. Siempre Incluir la Versión

Cuando guardes un comentario con análisis de sentimiento, SIEMPRE incluye la versión:

```python
# ✅ CORRECTO
comment = {
    "comment": "Great product!",
    "sentiment_label": "positive",
    "sentiment_score": 0.95,
    "sentiment_model_version": "v2"  # Siempre incluir
}

# ❌ INCORRECTO
comment = {
    "comment": "Great product!",
    "sentiment_label": "positive",
    "sentiment_score": 0.95
    # Falta sentiment_model_version
}
```

### 2. Nomenclatura Consistente

Usa un formato consistente para versiones:
- `v1`, `v2`, `v3` - Para versiones numéricas
- `blue`, `green` - Para ambientes de deployment
- `v1.0.0`, `v1.1.0` - Para semantic versioning

### 3. Auditoría Regular

Revisa periódicamente qué modelos están siendo usados:

```bash
# Ver distribución de modelos
curl "http://localhost:8001/api/v1/comments/?skip=0&limit=100" | \
  jq -r '.[].sentiment_model_version' | \
  sort | uniq -c
```

## Troubleshooting

### Comentarios sin versión de modelo

```python
# Encontrar comentarios con sentimiento pero sin versión
SELECT COUNT(*) FROM reviews
WHERE sentiment_label IS NOT NULL
  AND sentiment_model_version IS NULL
```

### Actualizar comentarios antiguos

```python
# Marcar comentarios antiguos con versión desconocida
UPDATE reviews
SET sentiment_model_version = 'unknown'
WHERE sentiment_label IS NOT NULL
  AND sentiment_model_version IS NULL
  AND created_at < '2025-11-11'
```

## Referencias

- [Modelo de Comment](./app/models/comment.py)
- [Schemas de Comment](./app/schemas/comment.py)
- [Migración](./alembic/versions/38fbae3e45e2_add_sentiment_model_version_column.py)
