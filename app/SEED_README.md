# 🌱 Seed de Base de Datos

Este script pobla la base de datos con datos de prueba para desarrollo y testing.

## 📦 Datos que se crean

### Usuarios

1. **Admin** 👤
   - Email: `admin@influencers.com`
   - Password: `admin123`
   - Rol: Administrador
   - Permisos: Acceso total

2. **Empresa Premium** 🏢
   - Email: `empresa@test.com`
   - Password: `empresa123`
   - Rol: Empresa
   - Suscripción: Premium activa (15 días restantes)
   - Pago: $99.99 completado

3. **Influencer** ⭐
   - Email: `influencer@test.com`
   - Password: `influencer123`
   - Rol: Influencer
   - Seguidores TikTok: 125,000
   - Seguidores YouTube: 45,000
   - Engagement rate: 4.5%
   - Campañas completadas: 12
   - Rating promedio: 4.8/5

### Campañas

1. **Lanzamiento Producto Tech** ✅
   - Estado: Completada
   - Budget: $1,500
   - Alcance total: 130,000
   - Engagement: 18,560

2. **Colección Moda Verano** 🔄
   - Estado: En progreso
   - Budget: $2,000
   - 1 de 10 entregables completados

3. **Promoción App Fitness** ⏳
   - Estado: Pendiente
   - Budget: $1,200
   - Inicio en 7 días

### Otros Datos

- Plan de suscripción Premium ($99.99/mes)
- Transacción de pago completada
- Perfil de influencer con métricas completas
- Portfolio con 2 campañas anteriores
- 4 notificaciones de ejemplo

## 🚀 Cómo ejecutar el seed

### Opción 1: Localmente

```bash
# Desde la carpeta app/
cd app

# Asegúrate de tener las variables de entorno configuradas
# DATABASE_URL debe apuntar a tu base de datos

# Ejecutar el script
python seed_data.py
```

### Opción 2: En Render (Producción)

**IMPORTANTE:** Solo ejecuta esto si quieres poblar la base de datos de producción con datos de prueba.

1. Conéctate a tu servicio en Render
2. Abre una shell
3. Ejecuta:
```bash
python seed_data.py
```

## ⚠️ Advertencias

- Este script **creará las tablas** si no existen
- Si los usuarios ya existen, el script fallará (esto es intencional para evitar duplicados)
- Los datos son **solo para desarrollo/testing**
- **NO ejecutes esto en producción** si ya tienes datos reales

## 🔄 Resetear la base de datos

Si quieres empezar desde cero:

```bash
# Opción 1: Usar Alembic
alembic downgrade base
alembic upgrade head
python seed_data.py

# Opción 2: Eliminar y recrear la base de datos manualmente
# (depende de tu configuración de PostgreSQL)
```

## 📝 Personalización

Puedes modificar el archivo `seed_data.py` para:
- Cambiar las contraseñas
- Agregar más usuarios
- Crear más campañas
- Modificar las métricas del influencer
- Agregar más notificaciones

## ✅ Verificación

Después de ejecutar el seed, puedes verificar que todo funcionó:

1. Inicia sesión con cualquiera de las credenciales
2. Verifica que el dashboard muestre los datos correctos
3. Prueba las diferentes funcionalidades según el rol

## 🐛 Troubleshooting

**Error: "User already exists"**
- Los usuarios ya fueron creados. Si quieres recrearlos, resetea la base de datos primero.

**Error: "Connection refused"**
- Verifica que la variable `DATABASE_URL` esté correctamente configurada
- Asegúrate de que la base de datos esté corriendo

**Error: "Module not found"**
- Instala las dependencias: `pip install -r requirements.txt`
- Asegúrate de estar en el directorio correcto
