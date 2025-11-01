# 🌱 Auto-Seed de Base de Datos

La aplicación **automáticamente** carga datos de prueba al iniciar si la base de datos está vacía.

No necesitas ejecutar ningún script manualmente. Los datos se crean automáticamente en el primer inicio.

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

## 🚀 Cómo funciona

### Automático ✨

Cuando la aplicación inicia:
1. Verifica si hay usuarios en la base de datos
2. Si está vacía, crea automáticamente:
   - Las tablas necesarias
   - Los usuarios de prueba
   - Campañas de ejemplo
   - Notificaciones
   - Todos los datos relacionados

### Manual (Opcional)

Si necesitas ejecutar el seed manualmente:

```bash
# Desde la carpeta app/
cd app
python seed_data.py
```

**Nota:** Normalmente no necesitas hacer esto, ya que el seed es automático.

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
