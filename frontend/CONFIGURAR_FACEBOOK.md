# 🔧 Configurar Facebook Login

## ⚠️ IMPORTANTE: Crear archivo .env.local

El archivo `.env.local` NO está en el repositorio por seguridad. Debes crearlo manualmente:

### Paso 1: Crear el archivo

En la raíz del proyecto frontend, crea un archivo llamado `.env.local`:

```
C:\Users\yoiner.castillo\Downloads\New folder\InfluencersFront\.env.local
```

### Paso 2: Agregar el contenido

Copia y pega esto en el archivo `.env.local`:

```bash
# API Backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Facebook App ID (para login con Facebook)
NEXT_PUBLIC_FACEBOOK_APP_ID=1531422201378331
```

### Paso 3: Reiniciar el servidor de desarrollo

Si el frontend ya está corriendo, debes reiniciarlo:

```bash
# Presiona Ctrl+C para detener el servidor

# Inicia nuevamente
npm run dev
```

---

## ✅ Verificar que funciona

1. Abre http://localhost:3000
2. Ve a la página de login
3. Deberías ver el botón "Continuar con Facebook"
4. Al hacer clic, se abrirá la ventana de Facebook para autorizar

---

## 🔍 Troubleshooting

### No veo el botón de Facebook
- Verifica que el archivo `.env.local` exista
- Verifica que tenga el `NEXT_PUBLIC_FACEBOOK_APP_ID`
- Reinicia el servidor de desarrollo

### Error al hacer clic en el botón
- Verifica que el backend esté corriendo: http://localhost:8000/docs
- Verifica que las credenciales estén en `docker-compose.yml`
- Revisa la consola del navegador (F12) para ver errores

### "App ID inválido"
- Verifica que el App ID sea correcto: `1531422201378331`
- Verifica en Facebook Developers que la app esté activa

---

## 📝 Nota sobre .env.local vs .env.example

- `.env.example` - Archivo de ejemplo (SÍ va en Git)
- `.env.local` - Archivo real con credenciales (NO va en Git)

Siempre debes crear `.env.local` basándote en `.env.example`.
