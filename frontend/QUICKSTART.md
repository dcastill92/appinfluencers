# ⚡ Quick Start - Frontend

Guía rápida para levantar el frontend en 5 minutos.

---

## 📋 Pre-requisitos

- ✅ Node.js 18+ instalado
- ✅ Backend corriendo en `http://localhost:8000`

---

## 🚀 Paso 1: Instalar Dependencias (2 minutos)

```bash
# Navegar al directorio
cd c:\Users\yoiner.castillo\CascadeProjects\InfluencersFront

# Instalar dependencias
npm install
```

---

## 🔧 Paso 2: Configurar Variables de Entorno (30 segundos)

```bash
# Windows PowerShell
Copy-Item .env.local.example .env.local

# Linux/Mac
cp .env.local.example .env.local
```

Editar `.env.local` si es necesario:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🎨 Paso 3: Instalar Shadcn UI (1 minuto)

```bash
# Inicializar Shadcn
npx shadcn-ui@latest init

# Responder a las preguntas:
# - TypeScript: Yes
# - Style: Default
# - Base color: Slate
# - CSS variables: Yes
# - Tailwind config: Yes
# - Components: @/components
# - Utils: @/lib/utils
# - React Server Components: Yes

# Instalar componentes básicos
npx shadcn-ui@latest add button card input dialog badge avatar
```

---

## 🏃 Paso 4: Ejecutar en Desarrollo (30 segundos)

```bash
npm run dev
```

Abrir en navegador: **http://localhost:3000**

---

## ✅ Verificar que Funciona

1. **Frontend corre**: http://localhost:3000
2. **Backend corre**: http://localhost:8000
3. **API responde**: http://localhost:8000/health

---

## 🎯 Próximos Pasos

El frontend tiene la estructura base, pero necesitas crear:

1. **Páginas de autenticación** (`app/(auth)/`)
2. **Layout de plataforma con RBAC** (`app/(plataforma)/layout.tsx`)
3. **Página de explorar con trial** (`app/(plataforma)/empresa/explorar/page.tsx`)
4. **Componentes de UI** (`components/`)

Ver `README.md` para ejemplos de código completos.

---

## 🐛 Troubleshooting

### Error: Cannot find module 'next'

```bash
# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
```

### Error: CORS

Asegúrate que el backend tenga CORS configurado para `http://localhost:3000`:

```python
# Backend: app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Puerto 3000 en uso

```bash
# Usar otro puerto
PORT=3001 npm run dev
```

---

**¡Listo para desarrollar! 🎉**
