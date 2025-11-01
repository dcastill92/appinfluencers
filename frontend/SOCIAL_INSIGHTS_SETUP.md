# 📊 Social Media Insights - Configuración

## ✅ Implementación Completada

Se han integrado insights detallados de Instagram y TikTok en los perfiles de influencers.

---

## 🎨 Componentes Creados

### 1. **InstagramInsights** (`components/InstagramInsights.tsx`)

Muestra métricas detalladas de Instagram:

**Métricas Principales:**
- 👥 Seguidores
- 📊 Engagement Rate
- 📸 Publicaciones
- 📈 Alcance

**Métricas Detalladas:**
- ❤️ Likes promedio
- 💬 Comentarios promedio
- 👁️ Impresiones
- 👤 Visitas al perfil
- 🔗 Clics al sitio web
- 👥 Siguiendo

**Top Posts:**
- Muestra los 3 posts con mejor rendimiento
- Hover para ver likes y comentarios

### 2. **TikTokInsights** (`components/TikTokInsights.tsx`)

Muestra métricas detalladas de TikTok:

**Métricas Principales:**
- 👥 Seguidores
- ❤️ Likes Totales
- 📊 Engagement Rate
- 📹 Videos

**Métricas Detalladas:**
- 👁️ Vistas promedio
- ❤️ Likes promedio
- 💬 Comentarios promedio
- 🔄 Compartidos promedio
- 📹 Vistas totales
- 👤 Visitas al perfil

**Top Videos:**
- Muestra los 3 videos con mejor rendimiento
- Hover para ver vistas, likes, comentarios y shares

---

## 📊 Estructura de Datos

### Instagram Insights (JSON)

```json
{
  "followers": 150000,
  "following": 897,
  "posts_count": 414,
  "engagement_rate": 4.86,
  "avg_likes": 7292,
  "avg_comments": 621,
  "reach": 95801,
  "impressions": 187500,
  "profile_views": 30000,
  "website_clicks": 350,
  "top_posts": [
    {
      "id": "post_1",
      "likes": 14584,
      "comments": 1242,
      "image_url": "https://..."
    }
  ]
}
```

### TikTok Insights (JSON)

```json
{
  "followers": 250000,
  "following": 150,
  "total_likes": 5000000,
  "total_videos": 120,
  "avg_views": 350000,
  "avg_likes": 28000,
  "avg_comments": 1400,
  "avg_shares": 2800,
  "engagement_rate": 8.5,
  "video_views": 42000000,
  "profile_views": 75000,
  "top_videos": [
    {
      "id": "video_1",
      "views": 1750000,
      "likes": 140000,
      "comments": 7000,
      "shares": 14000,
      "thumbnail_url": "https://..."
    }
  ]
}
```

---

## 🔧 Integración con APIs Reales

### Instagram Graph API

Para obtener insights reales de Instagram:

1. **Configurar Facebook App**:
   - Agregar producto "Instagram Graph API"
   - Solicitar permisos: `instagram_basic`, `instagram_manage_insights`

2. **Endpoint para obtener insights**:
```python
@router.post("/profiles/{profile_id}/sync-instagram")
async def sync_instagram_insights(
    profile_id: int,
    access_token: str,
    db: AsyncSession = Depends(get_db)
):
    """Sincronizar insights de Instagram."""
    # Obtener datos del perfil
    ig_user_id = "..."  # ID del usuario de Instagram
    
    # Llamar a Graph API
    insights_response = requests.get(
        f"https://graph.facebook.com/v18.0/{ig_user_id}/insights",
        params={
            "metric": "impressions,reach,profile_views,website_clicks",
            "period": "day",
            "access_token": access_token
        }
    )
    
    # Obtener media
    media_response = requests.get(
        f"https://graph.facebook.com/v18.0/{ig_user_id}/media",
        params={
            "fields": "id,like_count,comments_count,media_url",
            "access_token": access_token
        }
    )
    
    # Actualizar perfil con insights
    profile = await profile_repo.get_by_id(profile_id)
    profile.instagram_insights = {
        "followers": ...,
        "engagement_rate": ...,
        # ... más datos
    }
    await db.commit()
```

### TikTok API

Para obtener insights reales de TikTok:

1. **Registrar app en TikTok Developers**:
   - https://developers.tiktok.com/
   - Solicitar acceso a "Creator Insights"

2. **Endpoint para obtener insights**:
```python
@router.post("/profiles/{profile_id}/sync-tiktok")
async def sync_tiktok_insights(
    profile_id: int,
    access_token: str,
    db: AsyncSession = Depends(get_db)
):
    """Sincronizar insights de TikTok."""
    # Llamar a TikTok API
    response = requests.get(
        "https://open-api.tiktok.com/user/info/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    # Obtener videos
    videos_response = requests.get(
        "https://open-api.tiktok.com/video/list/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    # Actualizar perfil
    profile = await profile_repo.get_by_id(profile_id)
    profile.tiktok_insights = {
        "followers": ...,
        "total_likes": ...,
        # ... más datos
    }
    await db.commit()
```

---

## 🧪 Datos de Prueba

Ya se han generado insights de ejemplo para los perfiles existentes usando el script `seed_insights.py`.

Para regenerar o actualizar:

```bash
docker-compose exec api python scripts/seed_insights.py
```

---

## 📱 Uso en el Frontend

Los insights se muestran automáticamente en:

- **Página de perfil del influencer** (`/empresa/perfil/[id]`)
- Se muestran después de las tarifas sugeridas
- Si no hay datos, muestra un mensaje para conectar la cuenta

---

## 🎨 Personalización

### Cambiar colores de Instagram:
```tsx
// En InstagramInsights.tsx
className="bg-gradient-to-br from-purple-500 via-pink-500 to-orange-500"
```

### Cambiar colores de TikTok:
```tsx
// En TikTokInsights.tsx
className="bg-black" // Logo de TikTok
className="bg-gradient-to-br from-red-500 to-pink-500" // Métricas
```

---

## 📊 Métricas Calculadas

### Engagement Rate (Instagram):
```
(avg_likes + avg_comments) / followers * 100
```

### Engagement Rate (TikTok):
```
(avg_likes + avg_comments + avg_shares) / avg_views * 100
```

---

## 🚀 Próximos Pasos

1. **Integrar APIs reales**: Conectar con Instagram Graph API y TikTok API
2. **Actualización automática**: Crear cron job para sincronizar insights diariamente
3. **Histórico**: Guardar histórico de insights para ver tendencias
4. **Gráficas**: Agregar gráficas de evolución temporal
5. **YouTube**: Agregar insights de YouTube Analytics
6. **Comparación**: Permitir comparar múltiples influencers

---

## 📚 Recursos

- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [TikTok for Developers](https://developers.tiktok.com/)
- [YouTube Analytics API](https://developers.google.com/youtube/analytics)
