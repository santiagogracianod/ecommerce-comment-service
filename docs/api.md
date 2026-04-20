# API Documentation - Ecommerce Comment Service

## Descripción General

El microservicio de comentarios proporciona una API RESTful para gestionar comentarios y reseñas de productos en un sistema de e-commerce.

## Base URL

```
http://localhost:8000/api/v1
```

## Autenticación

*En desarrollo - actualmente no requiere autenticación*

## Endpoints

### 1. Crear Comentario

**POST** `/comments/`

Crea un nuevo comentario para un producto.

**Request Body:**
```json
{
  "content": "Excelente producto, muy buena calidad",
  "rating": 5,
  "product_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440001",
  "author_name": "Juan Pérez"
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "content": "Excelente producto, muy buena calidad",
  "rating": 5,
  "product_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440001",
  "author_name": "Juan Pérez",
  "is_verified": false,
  "is_active": true,
  "created_at": "2025-09-15T10:30:00Z",
  "updated_at": "2025-09-15T10:30:00Z"
}
```

### 2. Listar Comentarios

**GET** `/comments/`

Obtiene una lista paginada de comentarios activos.

**Query Parameters:**
- `skip` (int, optional): Número de registros a omitir (default: 0)
- `limit` (int, optional): Límite de registros a retornar (default: 100, max: 1000)

**Response (200):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "content": "Excelente producto, muy buena calidad",
    "rating": 5,
    "product_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "550e8400-e29b-41d4-a716-446655440001",
    "author_name": "Juan Pérez",
    "is_verified": false,
    "is_active": true,
    "created_at": "2025-09-15T10:30:00Z",
    "updated_at": "2025-09-15T10:30:00Z"
  }
]
```

### 3. Obtener Comentario por ID

**GET** `/comments/{comment_id}`

Obtiene un comentario específico por su ID.

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "content": "Excelente producto, muy buena calidad",
  "rating": 5,
  "product_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440001",
  "author_name": "Juan Pérez",
  "is_verified": false,
  "is_active": true,
  "created_at": "2025-09-15T10:30:00Z",
  "updated_at": "2025-09-15T10:30:00Z"
}
```

### 4. Comentarios por Producto

**GET** `/comments/product/{product_id}`

Obtiene todos los comentarios de un producto específico.

**Query Parameters:**
- `skip` (int, optional): Número de registros a omitir (default: 0)
- `limit` (int, optional): Límite de registros a retornar (default: 100, max: 1000)

### 5. Comentarios por Usuario

**GET** `/comments/user/{user_id}`

Obtiene todos los comentarios de un usuario específico.

**Query Parameters:**
- `skip` (int, optional): Número de registros a omitir (default: 0)
- `limit` (int, optional): Límite de registros a retornar (default: 100, max: 1000)

### 6. Búsqueda con Filtros

**GET** `/comments/search`

Busca comentarios con filtros avanzados.

**Query Parameters:**
- `product_id` (UUID, optional): Filtrar por producto
- `user_id` (UUID, optional): Filtrar por usuario
- `rating` (int, optional): Filtrar por rating (1-5)
- `is_verified` (boolean, optional): Filtrar por estado de verificación
- `is_active` (boolean, optional): Filtrar por estado activo (default: true)
- `skip` (int, optional): Número de registros a omitir (default: 0)
- `limit` (int, optional): Límite de registros a retornar (default: 100, max: 1000)

### 7. Estadísticas de Rating

**GET** `/comments/product/{product_id}/stats`

Obtiene estadísticas de rating para un producto.

**Response (200):**
```json
{
  "product_id": "550e8400-e29b-41d4-a716-446655440000",
  "average_rating": 4.5,
  "total_comments": 25
}
```

### 8. Actualizar Comentario

**PUT** `/comments/{comment_id}`

Actualiza un comentario existente.

**Request Body:**
```json
{
  "content": "Producto actualizado, ahora es aún mejor",
  "rating": 5,
  "author_name": "Juan Pérez Actualizado"
}
```

### 9. Verificar Comentario

**PATCH** `/comments/{comment_id}/verify`

Marca un comentario como verificado (indica que la compra fue confirmada).

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "content": "Excelente producto, muy buena calidad",
  "rating": 5,
  "product_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "550e8400-e29b-41d4-a716-446655440001",
  "author_name": "Juan Pérez",
  "is_verified": true,
  "is_active": true,
  "created_at": "2025-09-15T10:30:00Z",
  "updated_at": "2025-09-15T11:00:00Z"
}
```

### 10. Eliminar Comentario

**DELETE** `/comments/{comment_id}`

Elimina un comentario (soft delete por defecto).

**Query Parameters:**
- `soft_delete` (boolean, optional): Si es true hace soft delete, si es false elimina permanentemente (default: true)

**Response (204):** No content

## Códigos de Error

### 400 - Bad Request
Datos de entrada inválidos o mal formateados.

```json
{
  "detail": "Validation error message"
}
```

### 404 - Not Found
Comentario no encontrado.

```json
{
  "detail": "Comentario no encontrado"
}
```

### 422 - Unprocessable Entity
Error de validación de datos.

```json
{
  "detail": [
    {
      "loc": ["body", "rating"],
      "msg": "El rating debe estar entre 1 y 5",
      "type": "value_error"
    }
  ]
}
```

## Validaciones

### Rating
- Debe ser un entero entre 1 y 5 (inclusive)
- Es opcional al crear un comentario

### Content
- Debe tener entre 1 y 2000 caracteres
- Es obligatorio

### UUIDs
- Todos los IDs deben ser UUIDs válidos
- `product_id` y `user_id` son obligatorios al crear

### Author Name
- Máximo 255 caracteres
- Es opcional

## Ejemplos de Uso

### Crear un comentario sin rating
```bash
curl -X POST "http://localhost:8000/api/v1/comments/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Buen producto, llegó rápido",
    "product_id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "550e8400-e29b-41d4-a716-446655440001"
  }'
```

### Buscar comentarios de 5 estrellas de un producto
```bash
curl "http://localhost:8000/api/v1/comments/search?product_id=550e8400-e29b-41d4-a716-446655440000&rating=5"
```

### Obtener estadísticas de un producto
```bash
curl "http://localhost:8000/api/v1/comments/product/550e8400-e29b-41d4-a716-446655440000/stats"
```