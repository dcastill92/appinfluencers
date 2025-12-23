# 🚀 Digital Ocean Deployment - Quick Setup

## Base de Datos: `dfkj68lnvi5nki`

Esta guía asume que ya tienes una base de datos PostgreSQL en Digital Ocean con el nombre **dfkj68lnvi5nki**.

---

## 📋 Paso 1: Ejecutar Script de Inicialización

### Opción A: Desde tu máquina local

```bash
# Obtener la cadena de conexión de Digital Ocean
# Dashboard → Databases → dfkj68lnvi5nki → Connection Details

# Ejecutar el script
psql "postgresql://doadmin:YOURPASSWORD@host-xxxx.db.ondigitalocean.com:25060/dfkj68lnvi5nki?sslmode=require" \
  -f app/scripts/init_complete_db.sql
```

### Opción B: Desde la consola de Digital Ocean

1. Ve a **Databases** → **dfkj68lnvi5nki**
2. Click en **Console**
3. Copia y pega el contenido de `app/scripts/init_complete_db.sql`
4. Ejecuta

---

## 📋 Paso 2: Verificar que las Tablas se Crearon

```sql
-- Conectar a la BD
\c dfkj68lnvi5nki

-- Listar tablas
\dt

-- Debería mostrar:
-- users
-- influencer_profiles
-- subscription_plans
-- transactions
-- campaigns
-- messages
-- alembic_version
```

---

## 📋 Paso 3: Configurar Variables de Entorno en Digital Ocean

### En App Platform

1. Ve a **Apps** → Tu app → **Settings** → **Environment Variables**

2. Agrega/actualiza:

```bash
# Database (automático desde managed DB)
DATABASE_URL=${db-postgres.DATABASE_URL}

# O si ya tienes la cadena de conexión:
DATABASE_URL=postgresql://doadmin:PASSWORD@host-xxx.db.ondigitalocean.com:25060/dfkj68lnvi5nki?sslmode=require

# Security
SECRET_KEY=<genera con: python app/scripts/generate_secret.py>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# Application
ENVIRONMENT=production
DEBUG=false

# Trial
TRIAL_DURATION_HOURS=24

# Stripe (producción)
STRIPE_SECRET_KEY=sk_live_XXXXXX
STRIPE_PUBLISHABLE_KEY=pk_live_XXXXXX
PLATFORM_COMMISSION_RATE=0.15

# Social Media APIs
FACEBOOK_APP_ID=tu_app_id
FACEBOOK_APP_SECRET=tu_app_secret
INSTAGRAM_ACCESS_TOKEN=tu_token_longevo

# Email (opcional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu@email.com
SMTP_PASSWORD=tu_app_password
```

---

## 📋 Paso 4: Actualizar app.yaml (Digital Ocean)

El archivo `.do/app.yaml` ya está configurado. Solo necesitas:

```yaml
# En .do/app.yaml - Sección databases
databases:
  - name: db-postgres
    engine: PG
    version: "16"
    production: true
    cluster_name: dfkj68lnvi5nki  # ← Tu BD existente
```

**IMPORTANTE:** Si ya creaste la BD en Digital Ocean, el nombre del cluster debe coincidir.

---

## 📋 Paso 5: Deploy

### Opción A: Desde GitHub (Recomendado)

```bash
# Commitear cambios
git add .
git commit -m "Configure database dfkj68lnvi5nki for Digital Ocean"
git push origin main

# Digital Ocean auto-detectará el push y re-desplegará
```

### Opción B: CLI de Digital Ocean

```bash
# Instalar doctl
# https://docs.digitalocean.com/reference/doctl/how-to/install/

# Autenticar
doctl auth init

# Crear app desde spec
doctl apps create --spec .do/app.yaml

# O actualizar app existente
doctl apps update <APP_ID> --spec .do/app.yaml
```

---

## 📋 Paso 6: Aplicar Migraciones (Primera Vez)

Después del deploy, las migraciones se ejecutan automáticamente gracias a:

```yaml
# En .do/app.yaml
run_command: |
  alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Si necesitas ejecutarlas manualmente:

1. Ve a **Apps** → Tu app → **api** → **Console**
2. Click **Launch Console**
3. Ejecuta:
   ```bash
   alembic upgrade head
   ```

---

## 📋 Paso 7: Verificar Datos Iniciales

```sql
-- Admin user
SELECT email, role FROM users WHERE role = 'ADMIN';
-- Debe mostrar: admin@appinfluencers.com

-- Planes de suscripción
SELECT name, price_display FROM subscription_plans ORDER BY display_order;
-- Debe mostrar: Básico, Profesional, Empresarial

-- Usuarios de prueba
SELECT email, role, is_approved FROM users WHERE email LIKE '%test.com';
-- Debe mostrar 3 usuarios de prueba
```

---

## 🔐 Credenciales por Defecto

**Admin:**
- Email: `admin@appinfluencers.com`
- Password: `Admin123!`
- ⚠️ **CAMBIAR INMEDIATAMENTE EN PRODUCCIÓN**

**Usuarios de Prueba** (password: `Test1234`):
- `empresa@test.com` (EMPRESA)
- `influencer1@test.com` (INFLUENCER - María González)
- `influencer2@test.com` (INFLUENCER - Carlos Ramírez)

---

## 🔄 Flujo de Datos en Digital Ocean

```
GitHub (push) → Digital Ocean App Platform
    ↓
Build (Docker)
    ↓
Run Migrations (alembic upgrade head)
    ↓
Start API (uvicorn)
    ↓
Start Frontend (npm start)
    ↓
✅ App Running
```

---

## 🗄️ Conexión a la Base de Datos

### Desde tu Local (para debugging)

```bash
# Obtener connection string de Digital Ocean
# Dashboard → Databases → dfkj68lnvi5nki → Connection Details

# Conectar con psql
psql "postgresql://doadmin:PASSWORD@host.db.ondigitalocean.com:25060/dfkj68lnvi5nki?sslmode=require"

# Conectar con Python
DATABASE_URL=postgresql://doadmin:PASSWORD@host.db.ondigitalocean.com:25060/dfkj68lnvi5nki?sslmode=require
```

### Connection Pooler (Recomendado para producción)

Digital Ocean ofrece connection pooling:

```bash
# Usar el connection pool URL en lugar del direct URL
postgresql://doadmin:PASSWORD@host-pool.db.ondigitalocean.com:25060/dfkj68lnvi5nki?sslmode=require
```

---

## 📊 Verificar que Todo Funciona

### 1. Health Check

```bash
curl https://tu-api-url.ondigitalocean.app/health
```

Debe responder:
```json
{"status": "healthy"}
```

### 2. Test de Login

```bash
curl -X POST https://tu-api-url.ondigitalocean.app/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@appinfluencers.com",
    "password": "Admin123!"
  }'
```

Debe devolver un token JWT.

### 3. Ver Planes

```bash
curl https://tu-api-url.ondigitalocean.app/plans
```

Debe listar 3 planes de suscripción.

---

## 🚨 Troubleshooting

### Error: "relation does not exist"

**Causa:** Tablas no creadas

**Solución:**
```bash
# Ejecutar script SQL
psql "tu_connection_string" -f app/scripts/init_complete_db.sql

# O ejecutar migraciones
alembic upgrade head
```

### Error: "password authentication failed"

**Causa:** Credenciales incorrectas

**Solución:**
1. Verifica el password en Digital Ocean Dashboard
2. Asegúrate de usar el connection string completo
3. Incluye `?sslmode=require`

### Error: "SSL connection required"

**Causa:** Falta sslmode en connection string

**Solución:**
```bash
# Agregar ?sslmode=require al final
postgresql://user:pass@host:25060/dfkj68lnvi5nki?sslmode=require
```

### Error: "too many connections"

**Causa:** Pool agotado

**Solución:**
1. Usa connection pooler URL
2. Ajusta `pool_size` en `database.py`
3. Escala tu plan de BD en Digital Ocean

---

## 📈 Optimizaciones Post-Deploy

### 1. Habilitar Backups Automáticos

Digital Ocean → Databases → dfkj68lnvi5nki → Settings → Backups
- Daily backups: ON
- Retention: 7 days (gratis) o más

### 2. Configurar Alertas

Digital Ocean → Databases → dfkj68lnvi5nki → Alerts
- CPU > 80%
- Memory > 90%
- Disk > 85%

### 3. Habilitar Metrics

Dashboard → Enable → Ver métricas de:
- Queries per second
- Connection count
- Latency

---

## 🔒 Security Checklist

- [ ] Cambiar password de admin
- [ ] Generar nuevo SECRET_KEY
- [ ] Usar Stripe production keys
- [ ] Configurar CORS solo para tu dominio
- [ ] Habilitar SSL/TLS (automático en DO)
- [ ] Configurar firewall (solo app puede acceder a BD)
- [ ] Revisar pg_hba.conf (Digital Ocean lo maneja)
- [ ] Rotar passwords regularmente

---

## 💰 Costos Estimados

| Recurso | Plan | Costo/mes |
|---------|------|-----------|
| PostgreSQL Basic | 1GB RAM, 10GB SSD | $15 |
| API Service | Basic XXS | $5 |
| Frontend Service | Basic XXS | $5 |
| **Total** | | **$25** |

---

## 📞 Soporte

- Digital Ocean Docs: https://docs.digitalocean.com/
- Community: https://www.digitalocean.com/community/
- Tickets: Available on paid plans

---

## ✅ Checklist de Deployment

- [ ] Base de datos `dfkj68lnvi5nki` creada en Digital Ocean
- [ ] Script `init_complete_db.sql` ejecutado
- [ ] Tablas verificadas (7 tablas)
- [ ] Datos iniciales verificados (admin, planes, test users)
- [ ] Variables de entorno configuradas en App Platform
- [ ] Código pusheado a GitHub
- [ ] App desplegada en Digital Ocean
- [ ] Health check funcionando
- [ ] Login admin funcionando
- [ ] Password admin cambiado
- [ ] Backups configurados
- [ ] Alertas configuradas

---

🎉 **¡Tu app está lista para producción en Digital Ocean!**
