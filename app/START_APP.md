# 🚀 Guía para Iniciar la Aplicación

## ✅ Prerequisitos

- Docker y Docker Compose instalados
- Node.js 18+ instalado
- Puertos disponibles: 8000 (Backend), 3000 (Frontend), 5432 (PostgreSQL)

---

## 📋 Pasos para Iniciar

### 1. Iniciar Backend (API + Base de Datos)

```bash
# Navegar a la carpeta del backend
cd C:\Users\yoiner.castillo\CascadeProjects\Influencers

# Iniciar servicios con Docker Compose
docker-compose up -d

# Verificar que los servicios estén corriendo
docker-compose ps

# Ver logs (opcional)
docker-compose logs -f api
```

**Resultado esperado**:
```
NAME              STATUS
influencers_api   Up (healthy)
influencers_db    Up (healthy)
```

**Backend disponible en**: http://localhost:8000
**Documentación API**: http://localhost:8000/docs

### 2. Iniciar Frontend (Next.js)

```bash
# Navegar a la carpeta del frontend
cd "C:\Users\yoiner.castillo\Downloads\New folder\InfluencersFront"

# Instalar dependencias (solo la primera vez)
npm install

# Iniciar servidor de desarrollo
npm run dev
```

**Frontend disponible en**: http://localhost:3000

---

## 👥 Usuarios de Prueba

### 1. Admin
- **Email**: `admin@influencers.com`
- **Password**: `admin123`
- **Acceso**: Dashboard de administrador, gestión de usuarios, transacciones

### 2. Empresa
- **Email**: `empresa@test.com`
- **Password**: `empresa123`
- **Acceso**: Explorar influencers, crear campañas, ver transacciones

### 3. Influencer (CON INSIGHTS COMPLETOS)
- **Email**: `gaby@gmail.com`
- **Password**: `gaby123`
- **Acceso**: Perfil con insights de Instagram y TikTok
- **Datos**:
  - Instagram: 85,000 seguidores, 6.52% engagement
  - TikTok: 120,000 seguidores, 9.5% engagement
  - Top posts y videos
  - Métricas detalladas

### 4. Otro Influencer
- **Email**: `influencer@test.com`
- **Password**: `influencer123`
- **Acceso**: Perfil básico de influencer

---

## 🔍 Verificar que Todo Funciona

### Backend
```bash
# Verificar salud del API
curl http://localhost:8000/health

# O abrir en navegador:
# http://localhost:8000/docs
```

### Frontend
```bash
# Abrir en navegador:
# http://localhost:3000
```

### Base de Datos
```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U influencer_user -d influencers_platform

# Ver usuarios
SELECT email, role, is_active FROM users;

# Salir
\q
```

---

## 🛠️ Comandos Útiles

### Backend

```bash
# Ver logs en tiempo real
docker-compose logs -f api

# Reiniciar backend
docker-compose restart api

# Detener todo
docker-compose down

# Detener y eliminar volúmenes (⚠️ BORRA LA BD)
docker-compose down -v

# Ejecutar migraciones
docker-compose exec api alembic upgrade head

# Crear nueva migración
docker-compose exec api alembic revision --autogenerate -m "descripcion"

# Agregar datos de prueba a gaby@gmail.com
docker-compose exec api python scripts/seed_gaby_insights.py
```

### Frontend

```bash
# Instalar dependencias
npm install

# Iniciar desarrollo
npm run dev

# Build para producción
npm run build

# Iniciar producción
npm start

# Limpiar cache
rm -rf .next
npm run dev
```

---

## 🐛 Solución de Problemas

### Backend no inicia

```bash
# Ver logs de error
docker-compose logs api

# Reiniciar servicios
docker-compose restart

# Si persiste, reconstruir
docker-compose down
docker-compose up --build -d
```

### Frontend no inicia

```bash
# Limpiar node_modules
rm -rf node_modules package-lock.json
npm install

# Limpiar cache de Next.js
rm -rf .next
npm run dev
```

### Error de conexión a BD

```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps db

# Reiniciar BD
docker-compose restart db

# Ver logs de BD
docker-compose logs db
```

### Login no funciona

1. Verificar que el backend esté corriendo: http://localhost:8000/docs
2. Verificar que el frontend esté corriendo: http://localhost:3000
3. Abrir consola del navegador (F12) y verificar errores
4. Verificar que las cookies estén habilitadas
5. Probar con usuario de prueba: `admin@influencers.com` / `admin123`

### No se ven los insights

```bash
# Agregar datos de prueba
docker-compose exec api python scripts/seed_gaby_insights.py

# Verificar en BD
docker-compose exec db psql -U influencer_user -d influencers_platform
SELECT instagram_insights, tiktok_insights FROM influencer_profiles WHERE user_id = 4;
\q
```

---

## 📊 Estructura de Carpetas

```
Influencers/                    # Backend (FastAPI)
├── app/
│   ├── api/                   # Endpoints
│   ├── models/                # Modelos de BD
│   ├── schemas/               # Schemas Pydantic
│   ├── services/              # Lógica de negocio
│   └── core/                  # Configuración
├── alembic/                   # Migraciones
├── scripts/                   # Scripts útiles
└── docker-compose.yml         # Configuración Docker

InfluencersFront/              # Frontend (Next.js)
├── app/                       # Páginas y rutas
│   ├── (auth)/               # Páginas de autenticación
│   └── (plataforma)/         # Páginas de la plataforma
├── components/                # Componentes reutilizables
├── hooks/                     # Custom hooks
├── lib/                       # Utilidades
└── public/                    # Archivos estáticos
```

---

## 🎯 Flujo de Trabajo Típico

1. **Iniciar servicios**:
   ```bash
   # Terminal 1: Backend
   cd C:\Users\yoiner.castillo\CascadeProjects\Influencers
   docker-compose up -d
   
   # Terminal 2: Frontend
   cd "C:\Users\yoiner.castillo\Downloads\New folder\InfluencersFront"
   npm run dev
   ```

2. **Probar login**:
   - Ir a http://localhost:3000
   - Login con `gaby@gmail.com` / `gaby123`
   - Ver perfil con insights completos

3. **Desarrollar**:
   - Modificar código
   - Los cambios se recargan automáticamente
   - Ver logs en las terminales

4. **Detener servicios**:
   ```bash
   # Frontend: Ctrl+C en la terminal
   
   # Backend:
   docker-compose down
   ```

---

## 📝 Notas Importantes

- ✅ El backend se reinicia automáticamente al cambiar código
- ✅ El frontend tiene hot-reload activado
- ✅ Los datos de la BD persisten entre reinicios
- ✅ Los insights se guardan en la BD (no se llaman APIs en cada carga)
- ⚠️ Para APIs reales de Instagram/TikTok, configurar `.env` con credenciales
- ⚠️ `docker-compose down -v` BORRA todos los datos de la BD

---

## 🔐 Variables de Entorno

### Backend (.env)
```bash
# Ya configurado en docker-compose.yml
DATABASE_URL=postgresql+asyncpg://influencer_user:influencer_pass@db:5432/influencers_platform
SECRET_KEY=your-secret-key-here
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Opcional para APIs reales
FACEBOOK_APP_ID=tu_app_id
FACEBOOK_APP_SECRET=tu_app_secret
TIKTOK_CLIENT_KEY=tu_client_key
TIKTOK_CLIENT_SECRET=tu_client_secret
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_FACEBOOK_APP_ID=tu_facebook_app_id
```

---

## ✅ Checklist de Inicio

- [ ] Docker Desktop está corriendo
- [ ] Backend iniciado: `docker-compose up -d`
- [ ] Backend healthy: `docker-compose ps`
- [ ] Frontend iniciado: `npm run dev`
- [ ] Navegador en: http://localhost:3000
- [ ] Login funciona con usuario de prueba
- [ ] Insights visibles en perfil de gaby@gmail.com

---

¡Listo para desarrollar! 🎉
