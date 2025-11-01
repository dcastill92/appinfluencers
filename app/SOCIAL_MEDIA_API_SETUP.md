# 🔗 Integración Completa de APIs de Redes Sociales

## ✅ Sistema Implementado

Se ha creado un sistema completo y parametrizable para sincronizar insights de Instagram y TikTok usando sus APIs oficiales.

---

## 📋 Configuración Inicial

### 1. Variables de Entorno (Backend)

Edita el archivo `.env` en el backend:

```bash
# Social Media APIs Configuration
# Facebook/Instagram - Get from: https://developers.facebook.com/apps/
FACEBOOK_APP_ID=tu_facebook_app_id_aqui
FACEBOOK_APP_SECRET=tu_facebook_app_secret_aqui
INSTAGRAM_ACCESS_TOKEN=tu_instagram_token_aqui  # Opcional

# TikTok - Get from: https://developers.tiktok.com/
TIKTOK_CLIENT_KEY=tu_tiktok_client_key_aqui
TIKTOK_CLIENT_SECRET=tu_tiktok_client_secret_aqui
```

### 2. Configurar Facebook/Instagram App

1. **Crear App en Facebook Developers**:
   - Ve a https://developers.facebook.com/apps/
   - Clic en "Crear App"
   - Selecciona "Empresa" o "Consumidor"
   - Completa el formulario

2. **Agregar Producto Instagram Graph API**:
   - En el dashboard de tu app, busca "Instagram Graph API"
   - Haz clic en "Configurar"
   - Completa la configuración

3. **Configurar Permisos**:
   - Ve a "Configuración" → "Básica"
   - Copia el **App ID** y **App Secret**
   - En "Productos" → "Instagram Graph API" → "Configuración"
   - Agrega los permisos:
     - `instagram_basic`
     - `instagram_manage_insights`
     - `pages_read_engagement`

4. **URLs de Redirección**:
   - Agrega: `http://localhost:3000/influencer/perfil`
   - Para producción: `https://tudominio.com/influencer/perfil`

5. **Obtener Token de Acceso** (Opcional):
   - Ve a "Herramientas" → "Explorador de Graph API"
   - Selecciona tu app
   - Solicita permisos: `instagram_basic`, `instagram_manage_insights`
   - Genera token
   - Copia el token a `INSTAGRAM_ACCESS_TOKEN`

### 3. Configurar TikTok App

1. **Crear App en TikTok Developers**:
   - Ve a https://developers.tiktok.com/
   - Inicia sesión con tu cuenta de TikTok
   - Clic en "Manage apps" → "Create app"

2. **Configurar App**:
   - Nombre: "Influencers Platform"
   - Categoría: "Social Media"
   - Descripción: Tu descripción

3. **Agregar Productos**:
   - Habilita "Login Kit"
   - Habilita "User Info"
   - Habilita "Video List"

4. **Configurar Redirect URIs**:
   - Agrega: `http://localhost:3000/influencer/perfil`
   - Para producción: `https://tudominio.com/influencer/perfil`

5. **Obtener Credenciales**:
   - En "Settings" → "Basic information"
   - Copia el **Client Key** y **Client Secret**

---

## 🚀 Cómo Funciona

### Flujo de Datos

**IMPORTANTE**: Los insights se almacenan en la base de datos y siempre se muestran desde ahí.

```
┌─────────────────────────────────────────────────────────┐
│  VISUALIZACIÓN (Siempre desde Base de Datos)           │
├─────────────────────────────────────────────────────────┤
│  1. Usuario abre perfil                                 │
│  2. Frontend carga datos de BD                          │
│  3. Se muestran insights guardados                      │
│  4. Si no hay datos → Mensaje "No disponible"           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  SINCRONIZACIÓN (Solo cuando se solicita)              │
├─────────────────────────────────────────────────────────┤
│  1. Usuario → Clic en "Sincronizar"                     │
│  2. Frontend → Abre ventana OAuth                       │
│  3. Usuario → Autoriza la app                           │
│  4. OAuth → Retorna access token                        │
│  5. Frontend → Envía token al backend                   │
│  6. Backend → Llama a API de Instagram/TikTok           │
│  7. Backend → Procesa y GUARDA en BD                    │
│  8. Frontend → Recarga datos desde BD                   │
│  9. Se muestran insights actualizados                   │
└─────────────────────────────────────────────────────────┘
```

### Quién Puede Sincronizar

- ✅ **Influencer**: Puede sincronizar su propio perfil
- ✅ **Admin**: Puede sincronizar cualquier perfil de influencer
- ❌ **Empresa**: Solo puede ver los insights (no sincronizar)

### Endpoints del Backend

#### 1. Obtener Configuración
```http
GET /social-media/config
```

Respuesta:
```json
{
  "facebook_app_id": "123456789",
  "tiktok_client_key": "abcd1234",
  "instagram_configured": true,
  "tiktok_configured": true
}
```

#### 2. Sincronizar Instagram
```http
POST /social-media/instagram/sync
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "instagram_user_id": "17841400123456789",
  "access_token": "EAABwzLixnjY..."
}
```

Respuesta:
```json
{
  "message": "Instagram insights synced successfully",
  "insights": {
    "followers": 150000,
    "engagement_rate": 4.86,
    ...
  }
}
```

#### 3. Sincronizar TikTok
```http
POST /social-media/tiktok/sync
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "access_token": "act.example..."
}
```

---

## 🎨 Componentes Frontend

### 1. SyncSocialMedia
Componente para iniciar la sincronización:

```tsx
<SyncSocialMedia onSyncComplete={() => {
  // Callback cuando se completa la sincronización
  fetchProfile();
}} />
```

**Características**:
- Verifica si las APIs están configuradas
- Abre ventana de OAuth
- Maneja el flujo de autenticación
- Llama al backend para sincronizar
- Muestra estado de carga

### 2. InstagramInsights
Muestra insights de Instagram:

```tsx
<InstagramInsights insights={profile.instagram_insights} />
```

### 3. TikTokInsights
Muestra insights de TikTok:

```tsx
<TikTokInsights insights={profile.tiktok_insights} />
```

---

## 📊 Datos Sincronizados

### Instagram
- ✅ Seguidores
- ✅ Siguiendo
- ✅ Número de publicaciones
- ✅ Engagement rate
- ✅ Likes promedio
- ✅ Comentarios promedio
- ✅ Alcance
- ✅ Impresiones
- ✅ Visitas al perfil
- ✅ Clics al sitio web
- ✅ Top 3 posts

### TikTok
- ✅ Seguidores
- ✅ Siguiendo
- ✅ Likes totales
- ✅ Número de videos
- ✅ Vistas promedio
- ✅ Likes promedio
- ✅ Comentarios promedio
- ✅ Compartidos promedio
- ✅ Engagement rate
- ✅ Vistas totales
- ✅ Top 3 videos

---

## 🔐 Seguridad

### Tokens de Acceso
- Los tokens se envían desde el frontend al backend
- El backend valida los tokens con las APIs
- Los tokens NO se guardan en la base de datos
- Solo se guardan los insights procesados

### Permisos
- Solo usuarios INFLUENCER pueden sincronizar
- Solo pueden sincronizar su propio perfil
- Los tokens tienen tiempo de expiración

### Validaciones
- Backend valida que el usuario sea propietario del perfil
- Backend valida que las APIs estén configuradas
- Backend maneja errores de API gracefully

---

## 🧪 Pruebas

### 1. Usuario de Prueba con Datos Completos

Ya existe un usuario de prueba con insights completos:

**Credenciales**:
- 📧 Email: `gaby@gmail.com`
- 🔑 Password: `gaby123`
- 👤 Rol: INFLUENCER

**Datos incluidos**:
- ✅ Perfil completo de influencer
- ✅ Instagram insights (85,000 seguidores, 6.52% engagement)
- ✅ TikTok insights (120,000 seguidores, 9.5% engagement)
- ✅ Top posts y videos
- ✅ Métricas detalladas

Para regenerar o actualizar estos datos:

```bash
docker-compose exec api python scripts/seed_gaby_insights.py
```

### 2. Agregar Datos a Otros Perfiles

Para agregar datos de ejemplo a todos los perfiles:

```bash
docker-compose exec api python scripts/seed_insights.py
```

### 3. Probar Sincronización Real

1. Configura las variables de entorno
2. Reinicia el backend:
   ```bash
   docker-compose restart api
   ```

3. En el frontend:
   - Inicia sesión como influencer
   - Ve a "Mi Perfil"
   - Haz clic en "Sincronizar Instagram" o "Sincronizar TikTok"
   - Autoriza la app
   - Verifica que los insights se actualicen

---

## 🔄 Actualización Automática

### Crear Cron Job (Opcional)

Para actualizar insights automáticamente cada 24 horas:

```python
# app/tasks/sync_insights.py
from app.services.social_media_service import SocialMediaService
from app.models.profile import InfluencerProfile
from sqlalchemy import select

async def sync_all_profiles():
    """Sync insights for all profiles with tokens."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(InfluencerProfile))
        profiles = result.scalars().all()
        
        service = SocialMediaService(db)
        
        for profile in profiles:
            try:
                if profile.instagram_token:
                    await service.sync_instagram_insights(
                        profile.id,
                        profile.instagram_user_id,
                        profile.instagram_token
                    )
                
                if profile.tiktok_token:
                    await service.sync_tiktok_insights(
                        profile.id,
                        profile.tiktok_token
                    )
            except Exception as e:
                print(f"Error syncing profile {profile.id}: {e}")
```

Configurar con Celery o APScheduler.

---

## 🐛 Troubleshooting

### Error: "Instagram API not configured"
- Verifica que `FACEBOOK_APP_ID` esté en `.env`
- Reinicia el backend

### Error: "Invalid access token"
- El token puede haber expirado
- Vuelve a autorizar la app

### Error: "Permission denied"
- Verifica que la app tenga los permisos correctos
- Revisa la configuración en Facebook/TikTok Developers

### No se muestran insights
- Verifica que el perfil tenga `instagram_insights` o `tiktok_insights`
- Revisa la consola del navegador para errores
- Verifica que los componentes estén importados correctamente

---

## 📚 Recursos

- [Instagram Graph API Docs](https://developers.facebook.com/docs/instagram-api)
- [TikTok for Developers](https://developers.tiktok.com/doc)
- [OAuth 2.0 Flow](https://oauth.net/2/)

---

## ✨ Próximas Mejoras

1. **Guardar tokens** (encriptados) para actualización automática
2. **Histórico de insights** para ver tendencias
3. **Gráficas** de evolución temporal
4. **Comparación** entre períodos
5. **Alertas** cuando métricas bajan
6. **YouTube Analytics** integration
7. **Twitter/X** integration
8. **LinkedIn** integration
