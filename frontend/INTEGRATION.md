# 🔗 Integración Frontend-Backend

Guía para conectar el frontend Next.js con el backend FastAPI.

---

## 📋 Pre-requisitos

- ✅ Backend corriendo en `http://localhost:8000`
- ✅ Frontend instalado y configurado

---

## 🔧 Configuración del Backend (CORS)

El backend **YA DEBERÍA** tener CORS configurado, pero verifica:

### Archivo: `Influencers/app/main.py`

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Influencers Platform API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend en desarrollo
        "http://127.0.0.1:3000",  # Alternativa
    ],
    allow_credentials=True,  # ⭐ CRÍTICO para cookies httpOnly
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**⚠️ IMPORTANTE**: `allow_credentials=True` es CRÍTICO para que las cookies httpOnly funcionen.

---

## 🍪 Configuración de Cookies (Backend)

El backend debe configurar cookies httpOnly para los tokens JWT.

### Archivo: `Influencers/app/api/auth.py`

Verifica que el endpoint de login configure la cookie:

```python
@router.post("/login")
async def login(
    credentials: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    # ... autenticación ...
    
    # Crear token
    access_token = create_access_token(data={"sub": user.email})
    
    # ⭐ Configurar cookie httpOnly
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,   # ⭐ No accesible desde JavaScript
        secure=True,     # ⭐ Solo HTTPS (en producción)
        samesite="lax",  # ⭐ Protección CSRF
        max_age=3600,    # 1 hora
    )
    
    return {"message": "Login successful", "user": user}
```

---

## 🌐 Configuración del Frontend

### Archivo: `.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

### Archivo: `lib/api.ts` (YA CREADO)

Verifica que tenga `withCredentials: true`:

```typescript
export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, // ⭐ CRÍTICO: Envía cookies en cada request
  headers: {
    'Content-Type': 'application/json',
  },
});
```

---

## 🧪 Probar la Integración

### Paso 1: Levantar Backend

```bash
cd c:\Users\yoiner.castillo\CascadeProjects\Influencers
docker-compose up
```

Verificar: http://localhost:8000/health

### Paso 2: Levantar Frontend

```bash
cd c:\Users\yoiner.castillo\CascadeProjects\InfluencersFront
npm run dev
```

Verificar: http://localhost:3000

### Paso 3: Probar Login (Consola del Navegador)

Abre la consola del navegador (F12) y ejecuta:

```javascript
// Probar login
fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include', // Importante!
  body: JSON.stringify({
    email: 'admin@influencers.com',
    password: 'admin123'
  })
})
.then(res => res.json())
.then(data => console.log('Login:', data))
.catch(err => console.error('Error:', err));

// Verificar que la cookie se configuró
document.cookie; // Debería mostrar la cookie (si no es httpOnly)

// Probar endpoint protegido
fetch('http://localhost:8000/users/me', {
  credentials: 'include' // Envía la cookie
})
.then(res => res.json())
.then(data => console.log('User:', data))
.catch(err => console.error('Error:', err));
```

---

## 🐛 Troubleshooting

### Error: CORS policy blocked

**Síntoma**: 
```
Access to fetch at 'http://localhost:8000/auth/login' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solución**:
1. Verificar que `allow_origins` incluye `http://localhost:3000`
2. Verificar que `allow_credentials=True`
3. Reiniciar el backend

### Error: Cookie not being set

**Síntoma**: Login exitoso pero `/users/me` retorna 401

**Solución**:
1. Verificar que el backend configura la cookie con `httponly=True`
2. Verificar que el frontend usa `withCredentials: true`
3. Verificar que ambos están en el mismo dominio (localhost)
4. En producción, asegurarse de usar HTTPS

### Error: 401 Unauthorized en /users/me

**Síntoma**: Login funciona pero otros endpoints retornan 401

**Solución**:
1. Verificar que el backend lee la cookie en el middleware de auth
2. Verificar que el token no expiró
3. Verificar que `withCredentials: true` en todas las requests

### Error: Cannot read cookie in backend

**Síntoma**: Backend no puede leer la cookie

**Solución**:

Verificar que el backend lee cookies correctamente:

```python
# app/api/dependencies.py
from fastapi import Cookie

async def get_current_user(
    access_token: str = Cookie(None),  # ⭐ Leer cookie
    db: AsyncSession = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Decodificar token...
```

---

## 🔐 Seguridad en Producción

### Backend

```python
# Solo en producción
response.set_cookie(
    key="access_token",
    value=access_token,
    httponly=True,
    secure=True,      # ⭐ Solo HTTPS
    samesite="strict", # ⭐ Más restrictivo
    domain=".tudominio.com",  # ⭐ Dominio específico
    max_age=3600,
)
```

### Frontend

```typescript
// next.config.js
module.exports = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://api.tudominio.com',
  },
};
```

### CORS en Producción

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tudominio.com",
        "https://www.tudominio.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)
```

---

## 📊 Flujo Completo de Autenticación

```
1. Usuario ingresa credenciales en /login
   ↓
2. Frontend: POST /auth/login (email, password)
   ↓
3. Backend: Valida credenciales
   ↓
4. Backend: Crea JWT token
   ↓
5. Backend: Configura cookie httpOnly con el token
   ↓
6. Backend: Retorna { message, user }
   ↓
7. Frontend: Recibe respuesta (cookie se guarda automáticamente)
   ↓
8. Frontend: Actualiza AuthContext con user
   ↓
9. Frontend: Redirige a dashboard según rol
   ↓
10. Requests subsecuentes: Cookie se envía automáticamente
    ↓
11. Backend: Lee cookie, valida token, retorna data
```

---

## 🧪 Testing de Integración

### Test Manual

1. **Login**:
   - Ir a http://localhost:3000/login
   - Ingresar: admin@influencers.com / admin123
   - Verificar redirección a dashboard

2. **Trial Status** (si eres EMPRESA):
   - Ir a http://localhost:3000/empresa/dashboard
   - Verificar que muestra estado del trial

3. **Ver Perfil** (trigger trial):
   - Ir a http://localhost:3000/empresa/explorar
   - Click en un perfil
   - Verificar que se registra la vista en el backend

4. **Logout**:
   - Click en logout
   - Verificar que la cookie se elimina
   - Verificar redirección a /login

### Test con Postman

1. **Login**:
   ```
   POST http://localhost:8000/auth/login
   Body: { "email": "admin@influencers.com", "password": "admin123" }
   ```
   
2. **Verificar Cookie**:
   - En Postman, ir a "Cookies"
   - Debería ver `access_token`

3. **Usar Cookie**:
   ```
   GET http://localhost:8000/users/me
   (La cookie se envía automáticamente)
   ```

---

## 📝 Checklist de Integración

- [ ] Backend corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 3000
- [ ] CORS configurado con `allow_credentials=True`
- [ ] Backend configura cookies httpOnly
- [ ] Frontend usa `withCredentials: true`
- [ ] Login funciona y retorna user
- [ ] Cookie se configura correctamente
- [ ] `/users/me` funciona con la cookie
- [ ] Logout elimina la cookie
- [ ] Trial status se obtiene correctamente

---

## 🎯 Próximos Pasos

1. ✅ Verificar CORS en backend
2. ✅ Verificar configuración de cookies
3. ✅ Probar login desde frontend
4. ✅ Implementar páginas de autenticación
5. ✅ Implementar lógica de trial en UI

---

**¡Integración lista! 🎉**
