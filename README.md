# 🛒 Ecommerce Comment Microservice

Microservicio para la gestión de comentarios y reseñas en un sistema de e-commerce, desarrollado con [FastAPI](https://fastapi.tiangolo.com/).

![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-green)
![Python](https://img.shields.io/badge/Python-3.12.1-blue)
![Status](https://img.shields.io/badge/Status-En%20Desarrollo-yellow)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)

---

## 🚀 Características

- ✨ CRUD de comentarios (crear, leer, actualizar, eliminar)
- ⭐ Sistema de ratings de 1 a 5 estrellas
- 🔍 Filtros avanzados por producto, usuario, rating y estado
- 👤 Soporte para comentarios verificados y no verificados
- 🗑️ Soft delete para preservar historial
- � Estadísticas de rating por producto
- �📄 API RESTful con documentación automática (Swagger/OpenAPI)
- 🧩 Estructura modular y escalable
- 🐳 Listo para contenerización con Docker
- 🗃️ Base de datos PostgreSQL con migraciones Alembic

---

## 📁 Estructura del Proyecto

```text
/workspaces/ecommerce-comment-service/
├── app/
│   ├── __init__.py
│   ├── main.py                          # Punto de entrada de la aplicación
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                    # Configuración y variables de entorno
│   │   ├── security.py                  # Funciones de seguridad
│   │   └── exceptions.py                # Excepciones personalizadas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                      # Dependencias compartidas
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py                   # Router principal de la API
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── comments.py          # Endpoints de comentarios
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py                      # CRUD base genérico
│   │   └── comment.py                   # CRUD específico de comentarios
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py                      # Base SQLAlchemy
│   │   ├── session.py                   # Configuración de sesión DB
│   │   └── init_db.py                   # Inicialización de DB
│   ├── models/
│   │   ├── __init__.py
│   │   └── comment.py                   # Modelos SQLAlchemy
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── comment.py                   # Schemas Pydantic
│   ├── services/
│   │   ├── __init__.py
│   │   └── comment_service.py           # Lógica de negocio
│   └── utils/
│       ├── __init__.py
│       └── helpers.py                   # Utilidades generales
├── tests/
│   └── __init__.py
├── alembic/                             # Migraciones de base de datos
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── docs/                                # Documentación adicional
│   └── api.md
├── scripts/                             # Scripts de utilidad
│   ├── init_db.py
│   └── seed_data.py
├── .env                                 # Variables de entorno (local)
├── .env.example                         # Ejemplo de variables de entorno
├── .gitignore
├── alembic.ini                          # Configuración de Alembic
├── docker-compose.yml                   # Para desarrollo local
├── Dockerfile
├── pyproject.toml                       # Configuración de dependencias
├── requirements.txt
└── README.md
```

---

## 🔧 API Endpoints

### Comentarios

- `POST /api/v1/comments/` - Crear un nuevo comentario
- `GET /api/v1/comments/` - Listar todos los comentarios
- `GET /api/v1/comments/{comment_id}` - Obtener un comentario específico
- `PUT /api/v1/comments/{comment_id}` - Actualizar un comentario
- `DELETE /api/v1/comments/{comment_id}` - Eliminar un comentario
- `PATCH /api/v1/comments/{comment_id}/verify` - Verificar un comentario

### Filtros y Búsquedas

- `GET /api/v1/comments/product/{product_id}` - Comentarios por producto
- `GET /api/v1/comments/user/{user_id}` - Comentarios por usuario
- `GET /api/v1/comments/search` - Búsqueda con filtros avanzados
- `GET /api/v1/comments/product/{product_id}/stats` - Estadísticas de rating

---

## ⚙️ Instalación

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/RickContreras/ecommerce-comment-service
   cd ecommerce-comment-service
   ```

2. **Crea y activa un entorno virtual**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements-dev.txt
   ```

### 📦 Dependencias principales

- `fastapi==0.116.1` - Framework web
- `uvicorn==0.35.0` - Servidor ASGI
- `sqlalchemy==2.0.43` - ORM
- `psycopg2-binary==2.9.10` - Driver PostgreSQL
- `pydantic==2.11.8` - Validación de datos
- `alembic==1.16.5` - Migraciones de BD

---

## 🚀 Uso

### Desarrollo local

1. **Configura las variables de entorno**
   ```bash
   cp .env.example .env
   # Edita .env con tus configuraciones
   ```

2. **Ejecuta las migraciones**
   ```bash
   alembic upgrade head
   ```

3. **Inicia el servidor**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Accede a la documentación**
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker

```bash
docker-compose up -d
```

---

## 📝 Modelo de Datos

### Comment

```python
{
  "id": "uuid",
  "content": "string",           # Contenido del comentario
  "rating": "int",              # Rating 1-5 (opcional)
  "product_id": "uuid",         # ID del producto comentado
  "user_id": "uuid",           # ID del usuario que comenta
  "author_name": "string",      # Nombre del autor (opcional)
  "is_verified": "boolean",     # Si la compra está verificada
  "is_active": "boolean",       # Si el comentario está activo
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

---

## 🔐 Configuración de Seguridad

**⚠️ IMPORTANTE**: Este proyecto NO incluye credenciales reales por seguridad.

### Variables de entorno requeridas:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
API_TITLE=Ecommerce Comment Service
```

---

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app
```

---

## 📚 Documentación

- [API Docs](docs/api.md) - Documentación detallada de la API
- Swagger UI: `/docs`
- ReDoc: `/redoc`

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

1. **Genera credenciales seguras:**
   ```bash
   python scripts/generate_secrets.py template
   ```

2. **Copia y personaliza tu configuración:**
   ```bash
   cp .env.example .env
   # Edita .env con tus credenciales reales
   ```

3. **Variables de entorno requeridas:**
   - `DATABASE_URL` - Conexión a PostgreSQL## 🔐 Configuración de Seguridad

**⚠️ IMPORTANTE**: Este proyecto NO incluye credenciales reales por seguridad.

### Primera configuración:

1. **Genera credenciales seguras:**
   ```bash
   python scripts/generate_secrets.py template
   ```

2. **Copia y personaliza tu configuración:**
   ```bash
   cp .env.example .env
   # Edita .env con tus credenciales reales
   ```

3. **Variables de entorno requeridas:**
   - `DATABASE_URL` - Conexión a PostgreSQL

## 🏃 Ejecución en desarrollo

```bash
uvicorn app.main:app --reload
```

Accede a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🎯 Comandos Makefile

```bash
# Inicialización completa (migraciones + datos)
make init

# Solo poblar con datos de prueba
make seed

# Iniciar servidor en foreground
make server

# Iniciar servidor en background
make server-bg

# Ver estado del servidor
make status

# Limpiar base de datos
make clean

# Ejecutar tests
make test

# Ver todos los comandos disponibles
make help
```

---
## 🐳 Docker

1. **Construye la imagen**
   ```bash
   docker build -t ecommerce-comment-service .
   ```

2. **Ejecuta el contenedor**
   ```bash
   docker run -p 8000:8000 ecommerce-comment-service
   ```

---

## 🧪 Pruebas *(En desarrollo)*

Ejecuta las pruebas unitarias con:

```bash
pytest
```

---

## 🧹 Formateo y calidad de código *(En desarrollo)*

Formatea y verifica la calidad del código con:

```bash
black .
isort .
flake8 .
```

---

##  Requisitos

- **Python 3.12.1**
- **Docker** (opcional)
- **PostgreSQL** (para persistencia)
- **Linux, macOS o Windows**

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!  
Por favor, abre un issue o envía un pull request siguiendo las [buenas prácticas de Git y Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/).

---

> Desarrollado por [RickContreras](https://github.com/RickContreras)