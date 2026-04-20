# 🚀 Makefile para E-commerce Comment Service
.PHONY: help install init clean seed server test

# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

help: ## 📋 Mostrar ayuda
	@echo "🚀 E-commerce Comment Service - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## 📦 Instalar dependencias
	@echo "📦 Instalando dependencias..."
	$(PIP) install -r requirements-dev.txt

init: ## 🔧 Inicializar proyecto completo (DB + datos)
	@echo "🚀 Inicializando proyecto..."
	$(PYTHON) scripts/init_project.py

clean: ## 🗑️ Limpiar base de datos
	@echo "🗑️ Limpiando base de datos..."
	$(PYTHON) -c "import psycopg2; conn = psycopg2.connect(host='localhost', port=5432, database='app', user='app_user', password='app_password'); cursor = conn.cursor(); cursor.execute('DELETE FROM comments;'); conn.commit(); conn.close(); print('✅ Base de datos limpiada')"

seed: ## 🌱 Poblar base de datos con comentarios
	@echo "🌱 Poblando base de datos..."
	$(PYTHON) scripts/seed_data.py

migrate: ## 🔄 Aplicar migraciones de base de datos
	@echo "🔄 Aplicando migraciones..."
	alembic upgrade head

server: ## 🚀 Iniciar servidor de desarrollo
	@echo "🚀 Iniciando servidor..."
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

server-bg: ## 🚀 Iniciar servidor en background
	@echo "🚀 Iniciando servidor en background..."
	nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > app.log 2>&1 &
	@echo "📋 Logs disponibles en: app.log"

test: ## 🧪 Ejecutar tests
	@echo "🧪 Ejecutando tests..."
	$(PYTHON) -m pytest tests/ -v

status: ## 📊 Mostrar estado del proyecto
	@echo "📊 Estado del proyecto:"
	@echo "  🗄️  Base de datos:"
	@$(PYTHON) -c "import psycopg2; conn = psycopg2.connect(host='localhost', port=5432, database='app', user='app_user', password='app_password'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM comments;'); print(f'     Comentarios: {cursor.fetchone()[0]}'); conn.close()" 2>/dev/null || echo "     ❌ No conectada"
	@echo "  🌐 API:"
	@curl -s http://localhost:8000/api/v1/comments/ > /dev/null 2>&1 && echo "     ✅ Funcionando (http://localhost:8000)" || echo "     ❌ No disponible"

# Comando por defecto
.DEFAULT_GOAL := help