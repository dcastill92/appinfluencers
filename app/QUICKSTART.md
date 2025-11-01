# 🚀 Quick Start Guide

Esta guía te llevará de 0 a tener la API corriendo en **menos de 5 minutos**.

---

## Paso 1: Prerrequisitos

Asegúrate de tener instalado:
- ✅ Docker Desktop (Windows/Mac) o Docker Engine (Linux)
- ✅ Docker Compose

Verifica la instalación:
```bash
docker --version
docker-compose --version
```

---

## Paso 2: Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env (opcional para desarrollo local)
# Los valores por defecto funcionan para desarrollo
```

**Importante**: Para producción, debes cambiar:
- `SECRET_KEY`: Genera uno seguro
- `STRIPE_SECRET_KEY`: Usa tus keys reales de Stripe
- Credenciales de email

---

## Paso 3: Levantar los Servicios

```bash
# Construir y levantar todos los servicios
docker-compose up --build

# O en modo detached (background)
docker-compose up -d --build
```

**Espera a ver**:
```
✅ influencers_db    | database system is ready to accept connections
✅ influencers_api   | Uvicorn running on http://0.0.0.0:8000
```

---

## Paso 4: Ejecutar Migraciones

En otra terminal:

```bash
# Ejecutar migraciones de base de datos
docker-compose exec api alembic upgrade head

# Inicializar datos (crear admin user)
docker-compose exec api python scripts/init_db.py
```

---

## Paso 5: ¡Probar la API!

### Opción A: Documentación Interactiva (Swagger)

Abre en tu navegador:
```
http://localhost:8000/docs
```

### Opción B: Usando cURL

**1. Registrar un usuario EMPRESA:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "empresa@test.com",
    "password": "password123",
    "full_name": "Mi Empresa",
    "role": "EMPRESA"
  }'
```

**2. Login:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "empresa@test.com",
    "password": "password123"
  }'
```

Guarda el `access_token` de la respuesta.

**3. Ver estado del trial:**
```bash
curl -X GET "http://localhost:8000/users/trial-status" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

---

## Paso 6: Ejecutar Pruebas (Opcional)

```bash
# Ejecutar todas las pruebas
docker-compose exec api pytest

# Solo pruebas del trial (las más importantes)
docker-compose exec api pytest tests/unit/test_trial_logic.py -v

# Con cobertura
docker-compose exec api pytest --cov=app --cov-report=html
```

---

## 🎯 Endpoints Principales

Una vez corriendo, puedes probar:

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/docs` | GET | Documentación interactiva |
| `/health` | GET | Health check |
| `/auth/register` | POST | Registrar usuario |
| `/auth/login` | POST | Login |
| `/users/me` | GET | Info del usuario actual |
| `/users/trial-status` | GET | Estado del trial |
| `/profiles/` | GET | Listar perfiles de influencers |
| `/profiles/{id}` | GET | Ver perfil (⭐ con lógica de trial) |
| `/campaigns/` | POST | Crear campaña |
| `/notifications/` | GET | Ver notificaciones |

---

## 🛑 Detener los Servicios

```bash
# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (⚠️ borra la base de datos)
docker-compose down -v
```

---

## 🐛 Troubleshooting

### Puerto 8000 ya en uso
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # Usar 8001 en lugar de 8000
```

### Base de datos no conecta
```bash
# Ver logs
docker-compose logs db

# Reiniciar servicios
docker-compose restart
```

### Errores de permisos (Linux)
```bash
# Dar permisos a scripts
chmod +x scripts/*.sh
```

---

## 📚 Siguiente Paso

Lee el [README.md](README.md) completo para entender:
- Arquitectura del sistema
- Lógica de negocio del trial
- Todos los endpoints disponibles
- Cómo contribuir

---

## 🎓 Credenciales por Defecto

Después de ejecutar `init_db.py`:

**Admin User:**
- Email: `admin@influencers.com`
- Password: `admin123`
- ⚠️ **CAMBIAR EN PRODUCCIÓN**

---

## ✅ Checklist de Verificación

- [ ] Docker corriendo
- [ ] `docker-compose up` exitoso
- [ ] Migraciones ejecutadas (`alembic upgrade head`)
- [ ] Admin user creado (`init_db.py`)
- [ ] `/docs` accesible en navegador
- [ ] Registro de usuario funciona
- [ ] Login funciona y retorna token
- [ ] Pruebas pasan (`pytest`)

---

**¡Listo! Ahora tienes el backend del MVP corriendo. 🎉**
