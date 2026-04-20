#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inicializar la base de datos y crear todas las tablas
"""
import sys
import os

# Agregar el directorio raiz al path para importar modulos de la app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base
from app.db.session import engine
from app.models.comment import Comment  # Importar todos los modelos para que se registren

def init_db():
    """Crear todas las tablas en la base de datos"""
    print("Iniciando creacion de tablas en la base de datos...")

    try:
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas exitosamente")

        # Mostrar las tablas creadas
        print(f"\nTablas creadas: {list(Base.metadata.tables.keys())}")

    except Exception as e:
        print(f"Error al crear tablas: {e}")
        raise

def main():
    """Funcion principal"""
    init_db()
    print("Proceso completado!")

if __name__ == "__main__":
    main()
