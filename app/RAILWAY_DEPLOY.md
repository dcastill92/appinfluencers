# 🚀 Despliegue en Railway - Guía Paso a Paso

## 🎯 ¿Por qué Railway?

✅ **Más fácil**: Despliegue con GitHub en minutos  
✅ **Todo incluido**: Backend + Frontend + Base de datos  
✅ **HTTPS automático**: Certificado SSL gratis  
✅ **Sin configuración**: Detecta tu docker-compose.yml  
✅ **Escalable**: Auto-scaling incluido  

---

## 📋 Pre-requisitos

1. **Cuenta GitHub** con tu código
2. **Cuenta Railway**: https://railway.app
3. **Dominio** (opcional, pero recomendado)
4. **Tarjeta de crédito** (para el plan Pro)

---

## 🚀 Paso 1: Preparar el Repositorio

### A. Unificar Backend y Frontend

Railway funciona mejor con un solo repositorio. Vamos a mover el frontend al backend:

```bash
# En la carpeta del backend
cd C:\Users\yoiner.castillo\CascadeProjects\Influencers

# Mover frontend como subcarpeta
mv "C:\Users\yoiner.castillo\Downloads\New folder\InfluencersFront" ./frontend

# Ahora tu estructura es:
Influencers/
├── app/              # Backend FastAPI
├── frontend/         # Frontend Next.js
├── docker-compose.yml
└── Dockerfile
```

### B. Actualizar docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
      POSTGRES_DB: ${POSTGRES_DB:-influencers}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    environment:
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:-password}@db:5432/${POSTGRES_DB:-influencers}
      SECRET_KEY: ${SECRET_KEY}
      STRIPE_SECRET_KEY: ${STRIPE_SECRET_KEY}
      STRIPE_PUBLISHABLE_KEY: ${STRIPE_PUBLISHABLE_KEY}
      FACEBOOK_APP_ID: ${FACEBOOK_APP_ID}
      FACEBOOK_APP_SECRET: ${FACEBOOK_APP_SECRET}
      TIKTOK_CLIENT_KEY: ${TIKTOK_CLIENT_KEY}
      TIKTOK_CLIENT_SECRET: ${TIKTOK_CLIENT_SECRET}
      ENVIRONMENT: production
      DEBUG: "false"
    ports:
      - "8000:8000"
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: ${RAILWAY_PUBLIC_URL}/api
      NEXT_PUBLIC_FACEBOOK_APP_ID: ${FACEBOOK_APP_ID}
    depends_on:
      - api

volumes:
  postgres_data:
```

### C. Crear Dockerfile para Frontend

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "run", "build", "&&", "npm", "start"]
```

### D. Actualizar Dockerfile Principal

```dockerfile
# Dockerfile (raíz)
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### E. Crear railway.toml

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "docker-compose up"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

[[services]]
name = "api"
source = "."
[services.config]
cpu = "1"
memory = "512"
```

---

## 🚀 Paso 2: Subir a GitHub

```bash
# Agregar todo al Git
git add .
git commit -m "Add frontend and prepare for Railway deployment"

# Subir a GitHub
git push origin main
```

---

## 🚀 Paso 3: Configurar Railway

### 1. Crear Proyecto

1. Ve a https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Conecta tu cuenta GitHub
4. Selecciona tu repositorio "Influencers"

### 2. Configurar Variables de Entorno

En Railway dashboard → Settings → Variables, agrega:

```bash
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu-contraseña-segura
POSTGRES_DB=influencers

# Security
SECRET_KEY=tu-secret-key-muy-largo-y-único-para-producción

# Stripe (producción)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...

# Facebook
FACEBOOK_APP_ID=1531422201378331
FACEBOOK_APP_SECRET=67e9b81b1ae62703dd9f45417ff4d548

# TikTok (opcional)
TIKTOK_CLIENT_KEY=tu-tiktok-key
TIKTOK_CLIENT_SECRET=tu-tiktok-secret
```

### 3. Configurar Dominio (Opcional)

1. Settings → Custom Domains
2. Agrega tu dominio: `tuapp.com`
3. Railway te dará los registros DNS
4. Configura en tu registrador de dominios

---

## 🚀 Paso 4: Despliegue Automático

Railway detectará tu `docker-compose.yml` y desplegará automáticamente:

- ✅ Base de datos PostgreSQL
- ✅ Backend FastAPI
- ✅ Frontend Next.js
- ✅ Balanceador de carga
- ✅ HTTPS automático

Puedes ver el progreso en el dashboard de Railway.

---

## 🔧 Paso 5: Verificar Despliegue

### 1. Backend API

Visita: `https://tu-app.railway.app/health`

Deberías ver:
```json
{"status":"healthy","environment":"production"}
```

### 2. Frontend

Visita: `https://tu-app.railway.app`

Deberías ver la aplicación funcionando.

### 3. Dominio Personalizado (si configuraste)

Visita: `https://tuapp.com`

---

## 📊 Monitoreo

### Ver Logs

En Railway dashboard → Logs, puedes ver:
- Logs de la API
- Logs del frontend
- Logs de la base de datos

### Métricas

- CPU usage
- Memory usage
- Network traffic
- Request count

---

## 💰 Costos

| Plan | Costo | Límites |
|------|-------|---------|
| Starter | $5/mes | 500h runtime, 100GB bandwidth |
| **Pro (Recomendado)** | **$20/mes** | **Ilimitado, dominios, SSL** |
| Team | $40/mes | Todo + miembros del equipo |

---

## 🔄 Actualizaciones

Cada vez que hagas push a GitHub:

```bash
git add .
git commit -m "Update: new feature"
git push origin main
```

Railway detectará los cambios y desplegará automáticamente.

---

## 🐛 Troubleshooting

### Error: "Service failed to start"

1. **Verifica logs**: Railway dashboard → Logs
2. **Variables de entorno**: Asegúrate que todas estén configuradas
3. **Dockerfile**: Verifica que sea correcto

### Error: "Database connection failed"

1. **Verifica DATABASE_URL**: Debe usar el hostname `db`
2. **Espera a la BD**: Asegúrate que la BD esté healthy antes que la API

### Error: "Frontend not connecting to API"

1. **NEXT_PUBLIC_API_URL**: Debe ser `${RAILWAY_PUBLIC_URL}/api`
2. **CORS**: Verifica que tu dominio esté en `ALLOWED_ORIGINS`

---

## 🎯 Checklist Final

- [ ] Frontend movido al backend
- [ ] docker-compose.yml actualizado
- [ ] Railway.toml creado
- [ ] Código subido a GitHub
- [ ] Proyecto creado en Railway
- [ ] Variables de entorno configuradas
- [ ] Dominio configurado (opcional)
- [ ] HTTPS funcionando
- [ ] Login con Facebook funcionando
- [ ] Pagos con Stripe funcionando

---

## 🚀 ¡Listo para Producción!

Tu aplicación está ahora desplegada en producción con:

✅ **URL personalizada**: `https://tuapp.com`  
✅ **HTTPS automático**: Certificado SSL válido  
✅ **Base de datos**: PostgreSQL gestionada  
✅ **Escalabilidad**: Auto-scaling  
✅ **Logs y monitoreo**: Dashboard completo  
✅ **Despliegue automático**: GitHub integration  

---

## 📞 Próximos Pasos

1. **Configurar monitoreo**: Agregar Sentry para errores
2. **Configurar backups**: Railway hace backups automáticos
3. **Configurar analytics**: Google Analytics, Hotjar
4. **Optimizar rendimiento**: CDN, imágenes optimizadas
5. **Marketing**: SEO, redes sociales, ads

🎉 **¡Tu plataforma de influencers está en producción!**
