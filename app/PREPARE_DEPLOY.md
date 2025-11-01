# 📋 Preparación Manual para Despliegue en Railway

## 🎯 Objetivo
Unificar backend y frontend en un solo repositorio para Railway

---

## 📁 Paso 1: Mover Frontend al Backend

```bash
# En la carpeta del backend (C:\Users\yoiner.castillo\CascadeProjects\Influencers)
# Copiar el frontend como subcarpeta
xcopy "C:\Users\yoiner.castillo\Downloads\New folder\InfluencersFront" ".\frontend" /E /I /H /Y
```

Ahora tu estructura será:
```
Influencers/
├── app/                    # Backend FastAPI
├── frontend/               # Frontend Next.js (movido)
├── alembic/               # Migraciones
├── scripts/               # Scripts útiles
├── docker-compose.yml     # Configuración Docker
└── Dockerfile            # Imagen del backend
```

---

## 📝 Paso 2: Actualizar docker-compose.yml

Reemplaza el contenido de `docker-compose.yml` con:

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

---

## 🐳 Paso 3: Crear Dockerfile para Frontend

Crea el archivo `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "run", "build", "&&", "npm", "start"]
```

---

## 🚂 Paso 4: Crear railway.toml

Crea el archivo `railway.toml` en la raíz:

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "docker-compose up"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

---

## 📝 Paso 5: Actualizar .gitignore

Reemplaza el contenido de `.gitignore` con:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.ENV/
env.bak/
venv.bak/

# Database
*.db
*.sqlite3

# Docker
.dockerignore

# Railway
railway.toml

# Frontend
frontend/.next/
frontend/out/
frontend/build/
frontend/.env.local
frontend/.env.development.local
frontend/.env.test.local
frontend/.env.production.local
frontend/npm-debug.log*
frontend/yarn-debug.log*
frontend/yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## 🚀 Paso 6: Subir a GitHub

```bash
# Agregar todo
git add .

# Hacer commit
git commit -m "Prepare for Railway deployment - unified backend and frontend"

# Subir
git push origin main
```

---

## 🎯 Paso 7: Desplegar en Railway

### 1. Crear Cuenta
- Ve a https://railway.app
- Regístrate con GitHub

### 2. Nuevo Proyecto
- Click "New Project"
- "Deploy from GitHub repo"
- Selecciona tu repositorio "Influencers"

### 3. Configurar Variables
En Settings → Variables, agrega:

```bash
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu-contraseña-segura-123
POSTGRES_DB=influencers

# Security
SECRET_KEY=tu-secret-key-muy-largo-y-unico-para-produccion-12345

# Stripe (producción)
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...

# Facebook
FACEBOOK_APP_ID=1531422201378331
FACEBOOK_APP_SECRET=67e9b81b1ae62703dd9f45417ff4d548

# TikTok
TIKTOK_CLIENT_KEY=tu-tiktok-key
TIKTOK_CLIENT_SECRET=tu-tiktok-secret
```

### 4. Dominio (Opcional)
- Settings → Custom Domains
- Agrega tu dominio: `tuapp.com`
- Railway te dará los registros DNS

---

## ✅ Verificación

1. **Backend**: `https://tu-app.railway.app/health`
2. **Frontend**: `https://tu-app.railway.app`
3. **API Docs**: `https://tu-app.railway.app/docs`

---

## 💰 Costos

- **Starter**: $5/mes (500h runtime)
- **Pro**: $20/mes (ilimitado, dominios) ⭐
- **Team**: $40/mes (miembros)

---

## 🔄 Actualizaciones Futuras

Cada vez que hagas cambios:

```bash
git add .
git commit -m "Update: new feature"
git push origin main
```

Railway desplegará automáticamente.

---

## 📞 Soporte

- **Logs**: Railway dashboard → Logs
- **Métricas**: Railway dashboard → Metrics
- **Settings**: Railway dashboard → Settings

---

## 🎉 ¡Listo!

Tu aplicación está ahora en producción con:

✅ URL propia  
✅ HTTPS automático  
✅ Base de datos gestionada  
✅ Despliegue automático  
✅ Escalabilidad  

📖 **Guía completa**: `RAILWAY_DEPLOY.md`
