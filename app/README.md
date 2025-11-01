# Influencers Platform - Backend API MVP

## 🚀 INICIO RÁPIDO

### Opción 1: Script Automático (Windows)
```bash
# Doble clic en:
start.bat
```

### Opción 2: Manual
```bash
# 1. Iniciar Backend
docker-compose up -d

# 2. Verificar estado
docker-compose ps

# 3. Ver documentación API
# http://localhost:8000/docs
```

### Frontend
```bash
cd "C:\Users\yoiner.castillo\Downloads\New folder\InfluencersFront"
npm run dev
# http://localhost:3000
```

### 👥 Usuarios de Prueba
- **Admin**: admin@influencers.com / admin123
- **Influencer (con insights)**: gaby@gmail.com / gaby123
- **Empresa**: empresa@test.com / empresa123

📖 **Guía completa**: Ver [START_APP.md](./START_APP.md)

---

## 🎯 Visión General

Plataforma de dos lados que conecta **Empresas** con **Influencers/Microinfluencers** para campañas de marketing. El backend está construido con **FastAPI**, **PostgreSQL**, y **Docker**, implementando una arquitectura limpia y escalable.

### Características Principales del MVP

- ✅ **Sistema de Roles**: EMPRESA, INFLUENCER, ADMIN
- ✅ **Free Trial de 24 Horas**: Las empresas pueden ver 1 perfil gratis
- ✅ **Gestión de Campañas**: Propuestas, negociación, aceptación/rechazo
- ✅ **Sistema de Pagos**: Integración con Stripe y comisiones de plataforma
- ✅ **Notificaciones**: Alertas en tiempo real para eventos importantes
- ✅ **Mensajería Interna**: Comunicación entre empresas e influencers

---

## 🏗️ Arquitectura

```
app/
├── api/                    # Routers de FastAPI
│   ├── auth.py            # Autenticación y registro
│   ├── users.py           # Gestión de usuarios
│   ├── profiles.py        # Perfiles de influencers (con lógica de trial)
│   ├── campaigns.py       # Gestión de campañas
│   ├── payments.py        # Procesamiento de pagos
│   ├── notifications.py   # Sistema de notificaciones
│   └── dependencies.py    # Dependencias de FastAPI (auth, trial)
├── core/                  # Configuración central
│   ├── config.py          # Settings con Pydantic
│   ├── database.py        # Configuración de SQLAlchemy async
│   └── security.py        # JWT y hashing de contraseñas
├── models/                # Modelos de SQLAlchemy
│   ├── user.py            # Usuario (con roles)
│   ├── profile.py         # Perfil de influencer
│   ├── campaign.py        # Campañas
│   ├── payment.py         # Pagos
│   ├── notification.py    # Notificaciones
│   ├── message.py         # Mensajes
│   └── subscription.py    # Suscripciones
├── schemas/               # Schemas de Pydantic
├── repositories/          # Patrón Repository para acceso a datos
├── services/              # Lógica de negocio
│   ├── auth_service.py
│   ├── trial_service.py   # ⭐ LÓGICA CRÍTICA DEL TRIAL
│   ├── campaign_service.py
│   ├── payment_service.py
│   └── notification_service.py
└── main.py                # Punto de entrada de FastAPI
```

---

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose
- Python 3.11+ (para desarrollo local)

### 1. Clonar y Configurar

```bash
# Clonar el repositorio
cd Influencers

# Copiar variables de entorno
cp .env.example .env

# Editar .env con tus configuraciones
# IMPORTANTE: Cambiar SECRET_KEY y configurar Stripe keys
```

### 2. Levantar con Docker

```bash
# Construir y levantar todos los servicios
docker-compose up --build

# La API estará disponible en:
# http://localhost:8000
# Documentación interactiva: http://localhost:8000/docs
```

### 3. Ejecutar Migraciones

```bash
# Dentro del contenedor
docker-compose exec api alembic upgrade head

# O crear una nueva migración
docker-compose exec api alembic revision --autogenerate -m "descripción"
```

---

## 🧪 Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
docker-compose exec api pytest

# Solo pruebas unitarias
docker-compose exec api pytest tests/unit/

# Solo pruebas de integración
docker-compose exec api pytest tests/integration/

# Con cobertura
docker-compose exec api pytest --cov=app --cov-report=html
```

### Pruebas Críticas del Trial

Las pruebas más importantes están en `tests/unit/test_trial_logic.py`:

- ✅ `test_trial_expiration`: Verifica expiración después de 24 horas
- ✅ `test_first_profile_view_allowed`: Primera vista permitida
- ✅ `test_second_profile_view_blocked`: Segunda vista bloqueada ⭐
- ✅ `test_same_profile_can_be_viewed_multiple_times`: Mismo perfil OK
- ✅ `test_subscription_allows_unlimited_access`: Suscripción sin límites

---

## 📋 Lógica de Negocio Crítica

### 1. Free Trial de 24 Horas (EMPRESA)

**Implementación**: `app/services/trial_service.py` + `app/api/dependencies.py`

#### Reglas de Negocio:

1. Al registrarse, una EMPRESA recibe 24 horas de trial
2. Durante el trial, puede ver **1 perfil completo** de influencer
3. Intentar ver un segundo perfil → **HTTP 403 Forbidden**
4. Después de 24 horas → **HTTP 402 Payment Required**
5. Con suscripción activa → Acceso ilimitado

#### Endpoints Afectados:

```
GET /profiles/{profile_id}  # ⭐ Aplica middleware check_trial_access
```

#### Códigos de Estado:

- `200 OK`: Acceso permitido
- `403 Forbidden`: Límite de perfil gratuito alcanzado
- `402 Payment Required`: Trial expirado, requiere suscripción

### 2. Flujo de Propuesta y Notificación

**Implementación**: `app/services/campaign_service.py`

1. EMPRESA crea propuesta → Estado: `PENDIENTE`
2. INFLUENCER recibe notificación
3. INFLUENCER puede:
   - **Aceptar** → Estado: `ACTIVA` (habilita mensajería)
   - **Rechazar** → Estado: `RECHAZADA`
   - **Negociar** → Estado: `NEGOCIACION` (con contra-oferta)

### 3. Pagos y Comisiones

**Implementación**: `app/services/payment_service.py`

1. EMPRESA paga campaña → Pago capturado
2. Comisión de plataforma calculada (15% por defecto)
3. Estado: `RETENIDO` hasta completar campaña
4. Al finalizar campaña → ADMIN libera pago
5. Estado: `COMPLETADO` → Payout a influencer

---

## 🔐 Autenticación y Autorización

### Registro

```bash
POST /auth/register
{
  "email": "empresa@example.com",
  "password": "securepassword",
  "full_name": "Mi Empresa",
  "role": "EMPRESA"  # EMPRESA | INFLUENCER | ADMIN
}
```

### Login

```bash
POST /auth/login
{
  "email": "empresa@example.com",
  "password": "securepassword"
}

# Respuesta:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Uso del Token

```bash
# Incluir en headers de todas las peticiones protegidas
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 📊 Roles y Permisos

| Rol | Permisos |
|-----|----------|
| **EMPRESA** | - Crear campañas<br>- Ver perfiles (con restricción de trial)<br>- Realizar pagos<br>- Mensajería con influencers |
| **INFLUENCER** | - Crear/editar perfil público<br>- Recibir propuestas<br>- Aceptar/rechazar/negociar<br>- Recibir pagos |
| **ADMIN** | - Aprobar usuarios<br>- Monitorear campañas<br>- Liberar pagos<br>- Acceso total |

---

## 🔧 Configuración de Variables de Entorno

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/influencers_platform

# Security (⚠️ CAMBIAR EN PRODUCCIÓN)
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Trial
TRIAL_DURATION_HOURS=24

# Stripe (usar test keys para MVP)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
PLATFORM_COMMISSION_RATE=0.15

# Email (opcional para MVP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

## 📖 Documentación de API

### Documentación Interactiva

Una vez levantado el servidor:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

#### Autenticación
- `POST /auth/register` - Registro de usuario
- `POST /auth/login` - Login

#### Usuarios
- `GET /users/me` - Info del usuario actual
- `GET /users/trial-status` - Estado del trial (EMPRESA)
- `PATCH /users/{id}/approve` - Aprobar usuario (ADMIN)

#### Perfiles
- `POST /profiles/` - Crear perfil (INFLUENCER)
- `GET /profiles/` - Listar perfiles
- `GET /profiles/{id}` - Ver perfil detallado ⭐ (con lógica de trial)
- `PUT /profiles/me` - Actualizar mi perfil

#### Campañas
- `POST /campaigns/` - Crear propuesta (EMPRESA)
- `GET /campaigns/` - Mis campañas
- `POST /campaigns/{id}/accept` - Aceptar (INFLUENCER)
- `POST /campaigns/{id}/reject` - Rechazar (INFLUENCER)
- `POST /campaigns/{id}/negotiate` - Negociar (INFLUENCER)
- `POST /campaigns/{id}/complete` - Completar (EMPRESA/ADMIN)

#### Pagos
- `POST /payments/` - Crear pago (EMPRESA)
- `GET /payments/` - Mis pagos
- `POST /payments/{id}/complete` - Liberar pago (ADMIN)

#### Notificaciones
- `GET /notifications/` - Mis notificaciones
- `PATCH /notifications/{id}/read` - Marcar como leída

---

## 🛠️ Desarrollo Local (sin Docker)

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos PostgreSQL local
# Editar .env con DATABASE_URL local

# Ejecutar migraciones
alembic upgrade head

# Levantar servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📦 Stack Tecnológico

- **Framework**: FastAPI 0.104+
- **Base de Datos**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 (async)
- **Validación**: Pydantic 2.5+
- **Autenticación**: JWT (python-jose)
- **Hashing**: Passlib + bcrypt
- **Migraciones**: Alembic
- **Testing**: pytest + pytest-asyncio + httpx
- **Pagos**: Stripe
- **Servidor**: Uvicorn + Gunicorn
- **Containerización**: Docker + Docker Compose

---

## 🚦 Estado del Proyecto

### ✅ Completado (MVP)

- [x] Arquitectura base con FastAPI
- [x] Modelos de base de datos
- [x] Sistema de autenticación JWT
- [x] Lógica de trial de 24 horas
- [x] CRUD de perfiles de influencers
- [x] Sistema de campañas
- [x] Integración de pagos (mock Stripe)
- [x] Sistema de notificaciones
- [x] Pruebas unitarias e integración
- [x] Dockerización completa

### 🔜 Próximos Pasos (Post-MVP)

- [ ] Integración real con Stripe
- [ ] Sistema de búsqueda avanzada de influencers
- [ ] Filtros por categorías, followers, engagement
- [ ] Sistema de reviews y ratings
- [ ] Dashboard de métricas (ADMIN)
- [ ] Envío de emails transaccionales
- [ ] Webhooks de Stripe
- [ ] Rate limiting y throttling
- [ ] Logging estructurado
- [ ] Monitoreo con Prometheus/Grafana

---

## 🤝 Contribución

1. Fork el proyecto
2. Crear branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

## 📄 Licencia

Este proyecto es privado y confidencial.

---

## 📞 Soporte

Para preguntas o soporte, contactar al equipo de desarrollo.

---

## 🎓 Notas de Implementación

### Decisiones de Arquitectura

1. **Async/Await**: Todo el stack es asíncrono para máximo rendimiento
2. **Repository Pattern**: Abstracción de acceso a datos para testabilidad
3. **Service Layer**: Lógica de negocio separada de endpoints
4. **Dependency Injection**: FastAPI dependencies para auth y trial
5. **Pydantic Schemas**: Validación automática de request/response

### Consideraciones de Seguridad

- ✅ Passwords hasheados con bcrypt
- ✅ JWT tokens con expiración
- ✅ CORS configurado
- ✅ SQL injection protegido (SQLAlchemy ORM)
- ✅ Validación de inputs (Pydantic)
- ⚠️ Cambiar SECRET_KEY en producción
- ⚠️ Usar HTTPS en producción
- ⚠️ Configurar rate limiting

### Performance

- ✅ Conexiones async a base de datos
- ✅ Connection pooling configurado
- ✅ Índices en campos frecuentemente consultados
- ✅ Lazy loading de relaciones
- ✅ Paginación en listados

---

**¡Listo para desarrollar el MVP de tu plataforma de influencers! 🚀**
