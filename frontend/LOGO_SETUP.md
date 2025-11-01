# 🎨 Configuración del Logo

## 📁 Ubicación del Logo

Guarda tu imagen del logo en:
```
public/logo.png
```

## ✅ Pasos para Configurar

1. **Guarda la imagen**:
   - Nombre del archivo: `logo.png`
   - Ubicación: carpeta `public/` en la raíz del proyecto
   - Formato recomendado: PNG con fondo transparente
   - Tamaño recomendado: 512x512px o mayor

2. **El logo ya está integrado en**:
   - ✅ Página principal (`/`)
   - ✅ Página de login (`/login`)
   - ✅ Página de registro (`/registro`)
   - ✅ Favicon del navegador

## 🎨 Componente Logo

El componente `Logo.tsx` acepta las siguientes props:

```tsx
<Logo 
  size={60}           // Tamaño en píxeles (default: 40)
  className="..."     // Clases CSS adicionales
/>
```

## 📱 Tamaños Usados

- **Página principal**: 120px
- **Login/Registro**: 60-80px
- **Favicon**: Automático

## 🔧 Personalización

Para cambiar el logo en cualquier página, simplemente usa el componente:

```tsx
import Logo from '@/components/Logo';

<Logo size={100} />
```

## 🌈 Colores del Gradiente

El texto "Influencers" usa un gradiente:
- De: `purple-600` (#9333EA)
- A: `pink-600` (#DB2777)

Esto combina con los colores del logo (azul, púrpura, rosa, naranja).
