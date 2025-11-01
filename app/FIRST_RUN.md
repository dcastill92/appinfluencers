# 🎯 Primera Ejecución - Guía Paso a Paso

Esta guía te llevará desde cero hasta tener la API funcionando y probada en **menos de 10 minutos**.

---

## ✅ Pre-requisitos

Antes de comenzar, verifica que tienes instalado:

```bash
# Verificar Docker
docker --version
# Debe mostrar: Docker version 20.x.x o superior

# Verificar Docker Compose
docker-compose --version
# Debe mostrar: docker-compose version 1.29.x o superior
```

Si no tienes Docker instalado:
- **Windows/Mac**: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: [Docker Engine](https://docs.docker.com/engine/install/)

---

## 🚀 Paso 1: Configuración Inicial (1 minuto)

### 1.1 Navegar al Proyecto

```bash
cd c:\Users\yoiner.castillo\CascadeProjects\Influencers
```

### 1.2 Crear Archivo de Variables de Entorno

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

### 1.3 (Opcional) Editar Variables de Entorno

Para desarrollo local, los valores por defecto funcionan perfectamente.

Para producción, edita `.env` y cambia:
- `SECRET_KEY` - Genera uno seguro
- `STRIPE_SECRET_KEY` - Usa tus keys reales
- Credenciales de email

---

## 🐳 Paso 2: Levantar los Servicios (3 minutos)

### 2.1 Construir y Levantar

```bash
docker-compose up --build
```

**Espera a ver estos mensajes**:
```
✅ influencers_db    | database system is ready to accept connections
✅ influencers_api   | Uvicorn running on http://0.0.0.0:8000
```

> **Nota**: La primera vez tomará 2-3 minutos mientras descarga imágenes y construye.

### 2.2 Verificar que los Servicios Están Corriendo

Abre otra terminal y ejecuta:

```bash
docker-compose ps
```

Deberías ver:
```
Name                    State    Ports
influencers_api         Up       0.0.0.0:8000->8000/tcp
influencers_db          Up       5432/tcp
```

---

## 🗄️ Paso 3: Configurar la Base de Datos (1 minuto)

### 3.1 Ejecutar Migraciones

En una nueva terminal:

```bash
docker-compose exec api alembic upgrade head
```

Deberías ver:
```
INFO  [alembic.runtime.migration] Running upgrade  -> abc123, initial migration
```

### 3.2 Inicializar Datos (Crear Admin)

```bash
docker-compose exec api python scripts/init_db.py
```

Deberías ver:
```
🚀 Initializing database...
✅ Admin user created successfully
   Email: admin@influencers.com
   Password: admin123
   ⚠️  CHANGE PASSWORD IN PRODUCTION!
✅ Database initialization complete!
```

---

## 🎉 Paso 4: Verificar que Todo Funciona (2 minutos)

### 4.1 Verificar Health Check

Abre tu navegador y ve a:
```
http://localhost:8000/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "environment": "development"
}
```

### 4.2 Abrir Documentación Interactiva

```
http://localhost:8000/docs
```

¡Deberías ver la documentación Swagger con todos los endpoints! 🎊

---

## 🧪 Paso 5: Probar la API (3 minutos)

### 5.1 Registrar un Usuario EMPRESA

En la documentación (`/docs`), busca el endpoint `POST /auth/register` y prueba con:

```json
{
  "email": "empresa@test.com",
  "password": "password123",
  "full_name": "Mi Empresa de Prueba",
  "role": "EMPRESA"
}
```

Click en **"Execute"**.

Deberías recibir un **201 Created** con los datos del usuario.

### 5.2 Hacer Login

Busca `POST /auth/login` y prueba con:

```json
{
  "email": "empresa@test.com",
  "password": "password123"
}
```

Deberías recibir:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

**¡Copia el `access_token`!** Lo necesitarás para los siguientes pasos.

### 5.3 Autorizar en Swagger

1. En la parte superior derecha de `/docs`, click en **"Authorize"** 🔒
2. Pega tu token en el campo `Value`
3. Click en **"Authorize"**
4. Click en **"Close"**

¡Ahora puedes probar endpoints protegidos!

### 5.4 Ver Tu Usuario

Busca `GET /users/me` y click en **"Execute"**.

Deberías ver tus datos de usuario.

### 5.5 Ver Estado del Trial

Busca `GET /users/trial-status` y click en **"Execute"**.

Deberías ver:
```json
{
  "has_trial": true,
  "is_active": true,
  "trial_start": "2025-10-27T...",
  "trial_end": "2025-10-28T...",
  "hours_remaining": 23.9,
  "has_viewed_free_profile": false,
  "can_view_more_profiles": true
}
```

¡El trial está funcionando! ⭐

---

## 🎯 Paso 6: Probar la Lógica del Trial (Opcional)

### 6.1 Registrar un Influencer

Usa `POST /auth/register` con:

```json
{
  "email": "influencer@test.com",
  "password": "password123",
  "full_name": "Influencer de Prueba",
  "role": "INFLUENCER"
}
```

### 6.2 Aprobar el Influencer (como Admin)

1. Logout del usuario empresa (click en "Authorize" y "Logout")
2. Login como admin:
   ```json
   {
     "email": "admin@influencers.com",
     "password": "admin123"
   }
   ```
3. Copia el nuevo token y autoriza
4. Busca `PATCH /users/{user_id}/approve`
5. Usa `user_id = 2` (el influencer)
6. Execute

### 6.3 Crear Perfil de Influencer

1. Logout del admin
2. Login como influencer (`influencer@test.com`)
3. Autoriza con el nuevo token
4. Busca `POST /profiles/`
5. Usa este JSON:
   ```json
   {
     "bio": "Influencer de tecnología",
     "instagram_handle": "@techinfluencer",
     "instagram_followers": 50000,
     "suggested_rate_per_post": 500
   }
   ```
6. Execute

### 6.4 Probar el Trial (como Empresa)

1. Logout del influencer
2. Login como empresa (`empresa@test.com`)
3. Autoriza con el token de empresa
4. Busca `GET /profiles/1` (ver el perfil del influencer)
5. Execute

**Primera vez**: ✅ Deberías ver el perfil completo

6. Intenta ver el mismo perfil de nuevo (`GET /profiles/1`)

**Segunda vez (mismo perfil)**: ✅ Deberías ver el perfil (permitido)

7. Si hubiera un segundo influencer, intenta ver `GET /profiles/2`

**Perfil diferente**: ❌ Deberías recibir **403 Forbidden** con mensaje:
```json
{
  "detail": "You have already viewed your free profile during the trial. Please subscribe to view more profiles."
}
```

¡La lógica del trial está funcionando perfectamente! 🎉

---

## 🧪 Paso 7: Ejecutar Pruebas Automatizadas (1 minuto)

```bash
# Ejecutar todas las pruebas
docker-compose exec api pytest -v

# Solo pruebas del trial (las más importantes)
docker-compose exec api pytest tests/unit/test_trial_logic.py -v
```

Deberías ver:
```
tests/unit/test_trial_logic.py::TestTrialLogic::test_trial_is_active_for_new_empresa PASSED
tests/unit/test_trial_logic.py::TestTrialLogic::test_trial_expiration PASSED
tests/unit/test_trial_logic.py::TestTrialLogic::test_first_profile_view_allowed PASSED
tests/unit/test_trial_logic.py::TestTrialLogic::test_second_profile_view_blocked PASSED
...
======================== 22 passed in 2.34s ========================
```

¡Todas las pruebas pasan! ✅

---

## 📊 Resumen de lo que Acabas de Hacer

✅ Levantaste la API con Docker  
✅ Configuraste la base de datos  
✅ Creaste un usuario admin  
✅ Registraste una empresa  
✅ Hiciste login y obtuviste un JWT token  
✅ Verificaste el estado del trial  
✅ Probaste la lógica del trial (opcional)  
✅ Ejecutaste las pruebas automatizadas  

---

## 🎓 Próximos Pasos

### Explorar la API

1. **Crear más usuarios**: Prueba registrar más empresas e influencers
2. **Crear campañas**: Usa `POST /campaigns/` como empresa
3. **Aceptar campañas**: Usa `POST /campaigns/{id}/accept` como influencer
4. **Ver notificaciones**: Usa `GET /notifications/`

### Leer Documentación

1. **README.md** - Documentación técnica completa
2. **QUICKSTART.md** - Guía de inicio rápido
3. **COMMANDS.md** - Cheat sheet de comandos
4. **STRUCTURE.txt** - Estructura del proyecto

### Desarrollo

1. **Modificar código**: Los cambios se reflejan automáticamente (hot reload)
2. **Ver logs**: `docker-compose logs -f api`
3. **Ejecutar tests**: `docker-compose exec api pytest`

---

## 🛑 Detener los Servicios

Cuando termines:

```bash
# Detener servicios (mantiene datos)
docker-compose down

# Detener y eliminar datos (⚠️ borra la base de datos)
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
# Ver logs de la base de datos
docker-compose logs db

# Reiniciar servicios
docker-compose restart
```

### Errores de migraciones

```bash
# Revertir migraciones
docker-compose exec api alembic downgrade base

# Volver a ejecutar
docker-compose exec api alembic upgrade head
```

### Limpiar todo y empezar de nuevo

```bash
# Detener y eliminar todo
docker-compose down -v

# Volver a empezar desde el Paso 2
docker-compose up --build
```

---

## ✅ Checklist de Verificación

- [ ] Docker está instalado y corriendo
- [ ] Archivo `.env` creado
- [ ] `docker-compose up --build` exitoso
- [ ] Migraciones ejecutadas
- [ ] Admin user creado
- [ ] `/health` responde OK
- [ ] `/docs` accesible
- [ ] Registro de usuario funciona
- [ ] Login retorna token
- [ ] Estado del trial visible
- [ ] Pruebas pasan

---

## 🎉 ¡Felicitaciones!

Has completado exitosamente la primera ejecución de la **Influencers Platform API**.

La API está corriendo y lista para:
- ✅ Desarrollo local
- ✅ Integración con frontend
- ✅ Pruebas de usuario
- ✅ Despliegue a producción

---

## 📞 Ayuda Adicional

Si tienes problemas:

1. Revisa los logs: `docker-compose logs -f api`
2. Consulta `COMMANDS.md` para más comandos
3. Lee `README.md` para documentación completa
4. Verifica que Docker tiene suficiente memoria (4GB recomendado)

---

## 🚀 Siguiente Paso

Lee el **README.md** para entender:
- Arquitectura del sistema
- Todos los endpoints disponibles
- Lógica de negocio detallada
- Cómo desplegar a producción

---

**¡Disfruta desarrollando! 🎊**
