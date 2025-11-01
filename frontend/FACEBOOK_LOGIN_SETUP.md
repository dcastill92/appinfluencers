# Configuración de Facebook Login

## 📋 Pasos para Configurar Facebook Login

### 1. Crear una App de Facebook

1. Ve a [Facebook Developers](https://developers.facebook.com/)
2. Haz clic en "Mis Apps" → "Crear App"
3. Selecciona "Consumidor" como tipo de app
4. Completa el formulario:
   - **Nombre de la app**: Influencers Platform
   - **Email de contacto**: tu email
5. Haz clic en "Crear App"

### 2. Configurar Facebook Login

1. En el dashboard de tu app, busca "Facebook Login"
2. Haz clic en "Configurar"
3. Selecciona "Web" como plataforma
4. Ingresa la URL de tu sitio: `http://localhost:3000`
5. Guarda los cambios

### 3. Configurar Dominios Permitidos

1. Ve a "Configuración" → "Básica"
2. En "Dominios de la App", agrega:
   - `localhost`
3. En "URLs de Redireccionamiento de OAuth Válidas", agrega:
   - `http://localhost:3000/`
   - `http://localhost:3000/login`

### 4. Obtener el App ID

1. En "Configuración" → "Básica"
2. Copia el **ID de la App**
3. Crea un archivo `.env.local` en la raíz del proyecto:

```bash
# Copia el archivo de ejemplo
cp .env.local.example .env.local
```

4. Edita `.env.local` y agrega tu App ID:

```env
NEXT_PUBLIC_FACEBOOK_APP_ID=tu_app_id_aqui
```

### 5. Configurar Permisos

1. Ve a "Productos" → "Facebook Login" → "Configuración"
2. Asegúrate de que estos permisos estén habilitados:
   - `public_profile` (por defecto)
   - `email`

### 6. Modo de Desarrollo vs Producción

**Modo de Desarrollo** (actual):
- Solo tú y los usuarios que agregues como desarrolladores/testers pueden usar el login
- Para agregar testers: "Roles" → "Roles de Prueba" → "Agregar Testers"

**Modo de Producción**:
1. Ve a "Configuración" → "Básica"
2. Cambia el estado de la app a "En Producción"
3. Completa la revisión de la app si Facebook lo requiere

---

## 🔧 Cómo Funciona

### Frontend (Ya Implementado)

1. **Componente FacebookLoginButton**: Carga el SDK de Facebook y maneja el login
2. **Login Page**: Integra el botón de Facebook con el flujo de autenticación

### Backend (Pendiente de Implementar)

Necesitas crear un endpoint en tu backend para manejar el login de Facebook:

```python
# app/api/auth.py

@router.post("/facebook-login")
async def facebook_login(
    facebook_data: FacebookLoginData,
    db: AsyncSession = Depends(get_db)
):
    """
    Autenticar usuario con Facebook.
    
    1. Verificar el token de Facebook con Graph API
    2. Buscar usuario por facebook_id o email
    3. Si no existe, crear nuevo usuario
    4. Retornar JWT token de tu app
    """
    # Verificar token con Facebook Graph API
    fb_response = requests.get(
        f"https://graph.facebook.com/v20.0/me",
        params={
            "access_token": facebook_data.facebook_token,
            "fields": "id,name,email"
        }
    )
    
    if fb_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid Facebook token")
    
    fb_user = fb_response.json()
    
    # Buscar o crear usuario
    user = await user_repo.get_by_facebook_id(fb_user["id"])
    
    if not user:
        # Crear nuevo usuario
        user = await user_repo.create({
            "email": fb_user.get("email"),
            "full_name": fb_user["name"],
            "facebook_id": fb_user["id"],
            "role": "EMPRESA",  # O permitir que el usuario elija
            "is_approved": True,
            "is_active": True
        })
    
    # Crear JWT token
    access_token = create_access_token(user)
    
    return {"access_token": access_token}
```

---

## 🧪 Probar el Login

1. Inicia el servidor de desarrollo:
```bash
npm run dev
```

2. Ve a `http://localhost:3000/login`

3. Haz clic en "Continuar con Facebook"

4. Autoriza la app (primera vez)

5. Verás un alert con tus datos de Facebook

6. En la consola del navegador verás:
   - El access token de Facebook
   - Los datos del usuario

---

## 📊 Datos que Obtienes de Facebook

Con los permisos básicos (`public_profile`, `email`):

```javascript
{
  id: "123456789",           // Facebook User ID
  name: "Juan Pérez",        // Nombre completo
  email: "juan@email.com",   // Email (si el usuario lo compartió)
  picture: {                 // Foto de perfil
    data: {
      url: "https://..."
    }
  }
}
```

---

## 🔐 Seguridad

### Buenas Prácticas:

1. **Nunca expongas tu App Secret**: Solo usa el App ID en el frontend
2. **Verifica el token en el backend**: Siempre valida el token de Facebook en tu servidor
3. **HTTPS en producción**: Facebook requiere HTTPS para apps en producción
4. **Maneja errores**: El usuario puede cancelar el login o denegar permisos

### Flujo Seguro:

```
Frontend                Backend                 Facebook
   |                       |                        |
   |-- Click Login ------->|                        |
   |<-- Redirect FB -------|                        |
   |-- Auth Dialog --------|----------------------->|
   |<-- Token -------------|------------------------|
   |-- Send Token -------->|                        |
   |                       |-- Verify Token ------->|
   |                       |<-- User Data ----------|
   |                       |-- Create/Login User -->|
   |<-- JWT Token ---------|                        |
   |-- Authenticated ----->|                        |
```

---

## 🐛 Troubleshooting

### "App ID no configurado"
- Verifica que `.env.local` existe y tiene el App ID correcto
- Reinicia el servidor de desarrollo

### "URL no permitida"
- Agrega `localhost` en los dominios de la app en Facebook Developers
- Agrega las URLs de redirección correctas

### "Permisos denegados"
- El usuario puede denegar permisos (especialmente email)
- Maneja el caso donde `email` es `undefined`

### "SDK no carga"
- Verifica tu conexión a internet
- Revisa la consola del navegador para errores
- Asegúrate de que el App ID es correcto

---

## 📚 Recursos

- [Facebook Login Documentation](https://developers.facebook.com/docs/facebook-login/web)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Facebook App Dashboard](https://developers.facebook.com/apps/)
