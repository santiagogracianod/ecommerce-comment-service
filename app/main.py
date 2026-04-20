from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

from .monitoring.prometheus_middleware import PrometheusMiddleware, metrics_response

app = FastAPI(
    title="Ecommerce Comment Service",
    version=settings.api_version,
    description="Microservicio para gestión de comentarios y reseñas",
    debug=settings.debug
)

# Prometheus metrics middleware
app.add_middleware(PrometheusMiddleware, service_name="comment-service")

# CORS middleware - Permite solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier dominio
    allow_credentials=False,  # Deshabilitado para compatibilidad con allow_origins=["*"]
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Ecommerce Comment Service API", "version": settings.api_version}

@app.get("/metrics", include_in_schema=False)
def metrics():
    return metrics_response()

@app.get("/health")
def health_check():
    return {"status": "healthy"}