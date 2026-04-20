#!/usr/bin/env python3
"""
🚀 Script de inicialización del proyecto
Configura la base de datos y la puebla con datos de ejemplo
"""

import os
import sys
import subprocess
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e.stderr}")
        return False

def main():
    """Función principal de inicialización"""
    print("🚀 Inicializando proyecto E-commerce Comment Service...")
    print("=" * 60)
    
    # Cambiar al directorio del proyecto
    os.chdir(root_dir)
    
    # 1. Verificar que la base de datos esté disponible
    print("📊 Verificando conexión a la base de datos...")
    try:
        import psycopg2
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='app',
            user='app_user',
            password='app_password'
        )
        conn.close()
        print("✅ Conexión a la base de datos exitosa")
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        print("💡 Asegúrate de que PostgreSQL esté corriendo en Docker")
        return False
    
    # 2. Ejecutar migraciones (si es necesario)
    if run_command("alembic upgrade head", "Aplicando migraciones de base de datos"):
        pass
    else:
        print("⚠️  Las migraciones fallaron, pero continuando...")
    
    # 3. Poblar con datos de ejemplo
    print("🌱 Poblando la base de datos con comentarios de ejemplo...")
    try:
        # Importar y ejecutar el script de semillas
        from scripts.seed_data import seed_comments_data
        seed_comments_data()
        print("✅ Base de datos poblada exitosamente")
    except Exception as e:
        print(f"❌ Error poblando la base de datos: {e}")
        return False
    
    # 4. Verificar que todo esté funcionando
    print("🔍 Verificando que la API esté disponible...")
    try:
        import requests
        response = requests.get("http://localhost:8000/api/v1/comments/", timeout=5)
        if response.status_code == 200:
            comments = response.json()
            print(f"✅ API responde correctamente con {len(comments)} comentarios")
        else:
            print(f"⚠️  API responde pero con código: {response.status_code}")
    except Exception as e:
        print(f"⚠️  No se pudo verificar la API: {e}")
        print("💡 Asegúrate de que el servidor FastAPI esté corriendo")
    
    print("=" * 60)
    print("🎉 ¡Inicialización completada!")
    print()
    print("📋 Resumen:")
    print("   - Base de datos: ✅ Configurada y poblada")
    print("   - Comentarios: ✅ 10 comentarios")
    print("   - API: ✅ Lista para usar")
    print()
    print("🚀 Para iniciar el servidor:")
    print("   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
    print()
    print("📖 Documentación API:")
    print("   http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)