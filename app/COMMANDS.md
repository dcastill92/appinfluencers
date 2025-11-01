# 🛠️ Comandos Útiles - Cheat Sheet

Referencia rápida de comandos para desarrollo, testing y despliegue.

---

## 🐳 Docker Commands

### Básicos
```bash
# Construir y levantar
docker-compose up --build

# Levantar en background
docker-compose up -d

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (⚠️ borra DB)
docker-compose down -v

# Ver logs
docker-compose logs -f

# Ver logs solo de API
docker-compose logs -f api

# Reiniciar servicios
docker-compose restart

# Ver estado de servicios
docker-compose ps
```

### Ejecutar Comandos en Contenedor
```bash
# Shell interactivo
docker-compose exec api bash

# Python shell
docker-compose exec api python

# Ejecutar script
docker-compose exec api python scripts/init_db.py
```

---

## 🗄️ Database Commands

### Migraciones con Alembic
```bash
# Ejecutar migraciones
docker-compose exec api alembic upgrade head

# Crear nueva migración
docker-compose exec api alembic revision --autogenerate -m "descripción"

# Ver historial de migraciones
docker-compose exec api alembic history

# Revertir última migración
docker-compose exec api alembic downgrade -1

# Revertir a versión específica
docker-compose exec api alembic downgrade abc123

# Ver migración actual
docker-compose exec api alembic current
```

### PostgreSQL Directo
```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U influencer_user -d influencers_platform

# Backup de base de datos
docker-compose exec db pg_dump -U influencer_user influencers_platform > backup.sql

# Restaurar backup
docker-compose exec -T db psql -U influencer_user influencers_platform < backup.sql

# Ver tablas
docker-compose exec db psql -U influencer_user -d influencers_platform -c "\dt"

# Ver usuarios
docker-compose exec db psql -U influencer_user -d influencers_platform -c "SELECT * FROM users;"
```

---

## 🧪 Testing Commands

### Ejecutar Pruebas
```bash
# Todas las pruebas
docker-compose exec api pytest

# Con output verbose
docker-compose exec api pytest -v

# Solo unit tests
docker-compose exec api pytest tests/unit/

# Solo integration tests
docker-compose exec api pytest tests/integration/

# Pruebas específicas del trial
docker-compose exec api pytest tests/unit/test_trial_logic.py -v

# Ejecutar un test específico
docker-compose exec api pytest tests/unit/test_trial_logic.py::TestTrialLogic::test_second_profile_view_blocked -v

# Con cobertura
docker-compose exec api pytest --cov=app --cov-report=term-missing

# Generar reporte HTML de cobertura
docker-compose exec api pytest --cov=app --cov-report=html

# Ejecutar solo tests marcados
docker-compose exec api pytest -m unit
docker-compose exec api pytest -m integration

# Detener en primer fallo
docker-compose exec api pytest -x

# Mostrar print statements
docker-compose exec api pytest -s
```

### Usando Scripts
```bash
# Windows PowerShell
.\scripts\run_tests.ps1

# Linux/Mac
./scripts/run_tests.sh
```

---

## 🔧 Development Commands

### Formateo y Linting
```bash
# Formatear código con black
docker-compose exec api black app/ tests/

# Verificar formato sin cambiar
docker-compose exec api black --check app/ tests/

# Lint con flake8
docker-compose exec api flake8 app/ tests/

# Type checking con mypy
docker-compose exec api mypy app/
```

### Inicialización
```bash
# Inicializar base de datos con admin
docker-compose exec api python scripts/init_db.py

# Crear datos de prueba (si existe script)
docker-compose exec api python scripts/seed_data.py
```

---

## 📡 API Testing Commands

### Usando cURL

#### Autenticación
```bash
# Registrar EMPRESA
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "empresa@test.com",
    "password": "password123",
    "full_name": "Mi Empresa",
    "role": "EMPRESA"
  }'

# Registrar INFLUENCER
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "influencer@test.com",
    "password": "password123",
    "full_name": "Mi Influencer",
    "role": "INFLUENCER"
  }'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "empresa@test.com",
    "password": "password123"
  }'

# Guardar token en variable (Linux/Mac)
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"empresa@test.com","password":"password123"}' \
  | jq -r '.access_token')

# Windows PowerShell
$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" -Method POST -Body (@{email="empresa@test.com";password="password123"} | ConvertTo-Json) -ContentType "application/json"
$TOKEN = $response.access_token
```

#### Endpoints Protegidos
```bash
# Ver mi usuario
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer $TOKEN"

# Ver estado del trial
curl -X GET "http://localhost:8000/users/trial-status" \
  -H "Authorization: Bearer $TOKEN"

# Listar perfiles
curl -X GET "http://localhost:8000/profiles/" \
  -H "Authorization: Bearer $TOKEN"

# Ver perfil específico (⭐ con lógica de trial)
curl -X GET "http://localhost:8000/profiles/1" \
  -H "Authorization: Bearer $TOKEN"

# Crear campaña
curl -X POST "http://localhost:8000/campaigns/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "influencer_id": 2,
    "title": "Campaña de Prueba",
    "description": "Descripción de la campaña",
    "proposed_budget": 1000.0
  }'

# Ver mis notificaciones
curl -X GET "http://localhost:8000/notifications/" \
  -H "Authorization: Bearer $TOKEN"
```

### Usando HTTPie (más amigable)
```bash
# Instalar httpie
pip install httpie

# Login
http POST http://localhost:8000/auth/login email=empresa@test.com password=password123

# Con token
http GET http://localhost:8000/users/me Authorization:"Bearer $TOKEN"

# Ver perfiles
http GET http://localhost:8000/profiles/ Authorization:"Bearer $TOKEN"
```

---

## 🔍 Debugging Commands

### Ver Logs
```bash
# Logs en tiempo real
docker-compose logs -f api

# Últimas 100 líneas
docker-compose logs --tail=100 api

# Buscar errores
docker-compose logs api | grep ERROR

# Buscar warnings
docker-compose logs api | grep WARNING

# Ver logs de base de datos
docker-compose logs -f db
```

### Inspeccionar Contenedores
```bash
# Ver procesos en contenedor
docker-compose exec api ps aux

# Ver uso de recursos
docker stats

# Inspeccionar contenedor
docker inspect influencers_api

# Ver variables de entorno
docker-compose exec api env
```

### Database Debugging
```bash
# Contar usuarios
docker-compose exec db psql -U influencer_user -d influencers_platform \
  -c "SELECT COUNT(*) FROM users;"

# Ver últimos usuarios registrados
docker-compose exec db psql -U influencer_user -d influencers_platform \
  -c "SELECT id, email, role, created_at FROM users ORDER BY created_at DESC LIMIT 5;"

# Ver campañas activas
docker-compose exec db psql -U influencer_user -d influencers_platform \
  -c "SELECT id, title, status FROM campaigns WHERE status = 'ACTIVA';"

# Ver usuarios en trial
docker-compose exec db psql -U influencer_user -d influencers_platform \
  -c "SELECT id, email, trial_start_time, trial_profile_viewed_id FROM users WHERE role = 'EMPRESA' AND has_active_subscription = false;"
```

---

## 📊 Monitoring Commands

### Health Checks
```bash
# Health check endpoint
curl http://localhost:8000/health

# Ver documentación
curl http://localhost:8000/docs

# Ver OpenAPI schema
curl http://localhost:8000/openapi.json
```

### Performance Testing
```bash
# Instalar Apache Bench
# Ubuntu: sudo apt-get install apache2-utils
# Mac: brew install httpd

# Test de carga simple
ab -n 1000 -c 10 http://localhost:8000/health

# Con autenticación
ab -n 1000 -c 10 -H "Authorization: Bearer $TOKEN" http://localhost:8000/users/me
```

---

## 🚀 Deployment Commands

### Build para Producción
```bash
# Build imagen de producción
docker build -t influencers-api:latest .

# Tag para registry
docker tag influencers-api:latest your-registry.com/influencers-api:v1.0.0

# Push a registry
docker push your-registry.com/influencers-api:v1.0.0
```

### Heroku
```bash
# Login
heroku login

# Crear app
heroku create influencers-api-prod

# Deploy
git push heroku main

# Ver logs
heroku logs --tail

# Ejecutar migraciones
heroku run alembic upgrade head

# Abrir app
heroku open
```

---

## 🧹 Cleanup Commands

### Limpiar Docker
```bash
# Detener y eliminar todo
docker-compose down -v

# Eliminar imágenes no usadas
docker image prune -a

# Eliminar volúmenes no usados
docker volume prune

# Eliminar todo (⚠️ cuidado)
docker system prune -a --volumes

# Ver espacio usado
docker system df
```

### Limpiar Python
```bash
# Eliminar __pycache__
find . -type d -name __pycache__ -exec rm -r {} +

# Eliminar .pyc
find . -type f -name "*.pyc" -delete

# Eliminar coverage reports
rm -rf htmlcov/ .coverage
```

---

## 🎯 Makefile Shortcuts

Si usas el Makefile incluido:

```bash
# Ver comandos disponibles
make help

# Setup completo
make setup

# Levantar servicios
make up

# Detener servicios
make down

# Ver logs
make logs

# Ejecutar tests
make test

# Tests con cobertura
make test-coverage

# Ejecutar migraciones
make migrate

# Crear nueva migración
make migrate-create MSG="add_new_field"

# Inicializar DB
make init

# Shell de Python
make shell

# Shell de PostgreSQL
make db-shell

# Formatear código
make format

# Limpiar todo
make clean
```

---

## 💡 Tips y Trucos

### Alias Útiles (agregar a .bashrc o .zshrc)
```bash
# Alias para docker-compose
alias dc='docker-compose'
alias dce='docker-compose exec'
alias dcl='docker-compose logs -f'

# Alias para la API
alias api-shell='docker-compose exec api bash'
alias api-logs='docker-compose logs -f api'
alias api-test='docker-compose exec api pytest'

# Alias para DB
alias db-shell='docker-compose exec db psql -U influencer_user -d influencers_platform'
```

### Variables de Entorno Rápidas
```bash
# Exportar token para usar en múltiples comandos
export API_TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@influencers.com","password":"admin123"}' \
  | jq -r '.access_token')

# Usar en requests
curl -H "Authorization: Bearer $API_TOKEN" http://localhost:8000/users/me
```

---

## 📚 Recursos Adicionales

- **Documentación API**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **README**: [README.md](README.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)

---

**¡Guarda este archivo como referencia rápida! 📌**
