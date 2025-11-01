# 🔒 Configurar HTTPS para Facebook Login

## ⚠️ Problema

Facebook **ya no permite** login desde páginas HTTP (como `http://localhost:3000`). 
Solo funciona con HTTPS.

Error: `The method FB.login can no longer be called from http pages`

---

## ✅ Soluciones

### Opción 1: Usar Ngrok (MÁS FÁCIL) ⭐

Ngrok crea un túnel HTTPS hacia tu localhost.

#### Paso 1: Instalar Ngrok

1. Descarga desde: https://ngrok.com/download
2. Descomprime el archivo
3. Opcional: Crea una cuenta gratuita en https://ngrok.com/

#### Paso 2: Iniciar Ngrok

```bash
# En una nueva terminal
ngrok http 3000
```

Verás algo como:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:3000
```

#### Paso 3: Configurar Facebook App

1. Ve a https://developers.facebook.com/apps/1531422201378331/
2. Ve a "Facebook Login" → "Configuración"
3. En "URI de redireccionamiento OAuth válidos", agrega:
   ```
   https://abc123.ngrok.io
   https://abc123.ngrok.io/auth/callback
   ```
4. Guarda

#### Paso 4: Usar la URL de Ngrok

Abre en tu navegador: `https://abc123.ngrok.io`

✅ Ahora el login de Facebook funcionará!

**Nota**: La URL de Ngrok cambia cada vez que lo reinicias (en la versión gratuita).

---

### Opción 2: Certificado SSL Local (MÁS COMPLEJO)

#### Windows con mkcert

1. **Instalar Chocolatey** (si no lo tienes):
   ```powershell
   # En PowerShell como Administrador
   Set-ExecutionPolicy Bypass -Scope Process -Force
   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Instalar mkcert**:
   ```bash
   choco install mkcert
   ```

3. **Crear certificados**:
   ```bash
   # En la carpeta del proyecto
   cd "C:\Users\yoiner.castillo\Downloads\New folder\InfluencersFront"
   
   # Crear CA local
   mkcert -install
   
   # Crear certificado para localhost
   mkcert localhost 127.0.0.1 ::1
   ```

4. **Configurar Next.js**:

   Crea `server.js`:
   ```javascript
   const { createServer } = require('https');
   const { parse } = require('url');
   const next = require('next');
   const fs = require('fs');

   const dev = process.env.NODE_ENV !== 'production';
   const app = next({ dev });
   const handle = app.getRequestHandler();

   const httpsOptions = {
     key: fs.readFileSync('./localhost-key.pem'),
     cert: fs.readFileSync('./localhost.pem'),
   };

   app.prepare().then(() => {
     createServer(httpsOptions, (req, res) => {
       const parsedUrl = parse(req.url, true);
       handle(req, res, parsedUrl);
     }).listen(3000, (err) => {
       if (err) throw err;
       console.log('> Ready on https://localhost:3000');
     });
   });
   ```

5. **Actualizar package.json**:
   ```json
   {
     "scripts": {
       "dev": "node server.js",
       "dev:http": "next dev"
     }
   }
   ```

6. **Configurar Facebook App**:
   - Agregar `https://localhost:3000` en URIs de redirección

---

### Opción 3: Deshabilitar Facebook Login (TEMPORAL)

Si solo quieres probar la app sin Facebook:

1. Comenta el componente FacebookLoginButton en `app/(auth)/login/page.tsx`
2. Usa el login tradicional con email/password

**Usuarios de prueba**:
- `admin@influencers.com` / `admin123`
- `gaby@gmail.com` / `gaby123`
- `empresa@test.com` / `empresa123`

---

## 🎯 Recomendación

**Para desarrollo rápido**: Usa **Ngrok** (Opción 1)
- ✅ Fácil de configurar
- ✅ Funciona inmediatamente
- ✅ No requiere instalar nada complejo
- ⚠️ La URL cambia cada vez (versión gratuita)

**Para desarrollo serio**: Usa **mkcert** (Opción 2)
- ✅ URL siempre es `https://localhost:3000`
- ✅ Certificado confiable
- ⚠️ Requiere más configuración

**Para pruebas rápidas**: Deshabilita Facebook (Opción 3)
- ✅ No requiere HTTPS
- ✅ Login tradicional funciona perfectamente
- ⚠️ No puedes probar Facebook login

---

## 📝 Configuración de Facebook App

Independientemente de la opción que elijas, necesitas configurar las URLs en Facebook:

1. Ve a https://developers.facebook.com/apps/1531422201378331/
2. "Configuración" → "Básica":
   - Dominios de la aplicación: `localhost` o tu dominio de ngrok
3. "Facebook Login" → "Configuración":
   - URIs de redireccionamiento OAuth válidos:
     - Para Ngrok: `https://tu-url.ngrok.io`
     - Para mkcert: `https://localhost:3000`
4. Guarda cambios

---

## ✅ Verificar que Funciona

1. Abre tu URL (HTTPS)
2. Ve a la página de login
3. Haz clic en "Continuar con Facebook"
4. Debería abrir la ventana de Facebook sin errores
5. Autoriza la app
6. Deberías ser redirigido de vuelta

---

¿Necesitas ayuda con alguna opción específica?
