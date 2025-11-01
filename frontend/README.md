# 🚀 Influencers Platform - Frontend

Frontend moderno construido con Next.js 14, TypeScript, React Query y Tailwind CSS.

---

## ✅ Estado del Proyecto

**ESTRUCTURA BASE GENERADA** - Requiere instalación de dependencias y completar archivos faltantes.

### Archivos Generados (Core)

✅ Configuración:
- `package.json` - Dependencias y scripts
- `tsconfig.json` - TypeScript config
- `tailwind.config.ts` - Tailwind CSS config
- `next.config.js` - Next.js config
- `.env.local.example` - Variables de entorno

✅ Lib (Utilidades):
- `lib/api.ts` - Axios instance con httpOnly cookies
- `lib/utils.ts` - Utilidades (cn, formatCurrency, etc.)
- `lib/validators.ts` - Esquemas Zod (MATCH backend Pydantic)

✅ Contexts:
- `contexts/AuthContext.tsx` - Auth state + trial status

✅ Services (React Query):
- `services/profileService.ts` - Queries/mutations de perfiles
- `services/campaignService.ts` - Queries/mutations de campañas

✅ App Router:
- `app/layout.tsx` - Root layout
- `app/providers.tsx` - React Query + Auth providers
- `app/globals.css` - Tailwind styles

---

## 📋 Instalación

```bash
# 1. Navegar al directorio
cd c:\Users\yoiner.castillo\CascadeProjects\InfluencersFront

# 2. Instalar dependencias
npm install

# 3. Crear archivo de entorno
copy .env.local.example .env.local

# 4. Iniciar desarrollo
npm run dev
```

La aplicación estará en: http://localhost:3000

---

## 🏗️ Estructura Completa del Proyecto

```
InfluencersFront/
├── app/
│   ├── (auth)/                    # ⚠️ FALTA CREAR
│   │   ├── login/page.tsx
│   │   └── registro/page.tsx
│   ├── (marketing)/               # ⚠️ FALTA CREAR
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── (plataforma)/              # ⚠️ FALTA CREAR (CRÍTICO)
│   │   ├── layout.tsx             # ← RBAC + Auth protection
│   │   ├── empresa/
│   │   │   ├── dashboard/page.tsx
│   │   │   ├── explorar/page.tsx  # ← TRIAL LOGIC
│   │   │   └── campañas/[id]/page.tsx
│   │   ├── influencer/
│   │   │   ├── dashboard/page.tsx
│   │   │   └── perfil/page.tsx
│   │   └── admin/
│   │       ├── dashboard/page.tsx
│   │       └── aprobaciones/page.tsx
│   ├── layout.tsx                 # ✅ CREADO
│   ├── providers.tsx              # ✅ CREADO
│   └── globals.css                # ✅ CREADO
├── components/
│   ├── ui/                        # ⚠️ FALTA CREAR (Shadcn)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── layout/                    # ⚠️ FALTA CREAR
│   │   ├── Navbar.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   └── features/                  # ⚠️ FALTA CREAR
│       ├── ProfileCard.tsx
│       ├── CampaignForm.tsx
│       ├── TrialPaywall.tsx       # ← CRÍTICO
│       └── NotificationBell.tsx
├── contexts/
│   └── AuthContext.tsx            # ✅ CREADO
├── hooks/
│   └── useAuth.ts                 # ✅ CREADO
├── lib/
│   ├── api.ts                     # ✅ CREADO
│   ├── utils.ts                   # ✅ CREADO
│   └── validators.ts              # ✅ CREADO
├── services/
│   ├── profileService.ts          # ✅ CREADO
│   ├── campaignService.ts         # ✅ CREADO
│   ├── authService.ts             # ⚠️ FALTA CREAR
│   └── notificationService.ts     # ⚠️ FALTA CREAR
└── package.json                   # ✅ CREADO
```

---

## 🔑 Archivos Críticos Faltantes

### 1. Layout de Plataforma con RBAC

**Archivo**: `app/(plataforma)/layout.tsx`

```typescript
'use client';

import { useAuth } from '@/hooks/useAuth';
import { useRouter, usePathname } from 'next/navigation';
import { useEffect } from 'react';
import Navbar from '@/components/layout/Navbar';
import Sidebar from '@/components/layout/Sidebar';

export default function PlataformaLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
      return;
    }

    if (user) {
      // RBAC: Redirect if accessing wrong role routes
      if (pathname.startsWith('/empresa') && user.role !== 'EMPRESA') {
        router.push(`/${user.role.toLowerCase()}/dashboard`);
      } else if (pathname.startsWith('/influencer') && user.role !== 'INFLUENCER') {
        router.push(`/${user.role.toLowerCase()}/dashboard`);
      } else if (pathname.startsWith('/admin') && user.role !== 'ADMIN') {
        router.push(`/${user.role.toLowerCase()}/dashboard`);
      }
    }
  }, [user, isAuthenticated, isLoading, pathname, router]);

  if (isLoading) {
    return <div>Cargando...</div>;
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Navbar />
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  );
}
```

### 2. Página de Explorar con Lógica de Trial

**Archivo**: `app/(plataforma)/empresa/explorar/page.tsx`

```typescript
'use client';

import { useSearchProfiles } from '@/services/profileService';
import { useAuth } from '@/hooks/useAuth';
import ProfileCard from '@/components/features/ProfileCard';
import TrialPaywall from '@/components/features/TrialPaywall';
import { useState } from 'react';

export default function ExplorarPage() {
  const { data: profiles, isLoading } = useSearchProfiles();
  const { trialStatus } = useAuth();
  const [showPaywall, setShowPaywall] = useState(false);

  const canViewProfile = (profileId: number) => {
    if (!trialStatus) return true; // Has subscription

    // If trial expired
    if (!trialStatus.is_active) {
      return false;
    }

    // If already viewed a profile and this is a different one
    if (trialStatus.has_viewed_free_profile && !trialStatus.can_view_more_profiles) {
      return false;
    }

    return true;
  };

  const handleProfileClick = (profileId: number) => {
    if (!canViewProfile(profileId)) {
      setShowPaywall(true);
      return;
    }

    // Navigate to profile detail
    window.location.href = `/empresa/perfil/${profileId}`;
  };

  if (isLoading) {
    return <div>Cargando perfiles...</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Explorar Influencers</h1>

      {/* Trial Status Banner */}
      {trialStatus?.is_active && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <p className="text-sm text-blue-800">
            🎁 <strong>Trial Activo:</strong> {trialStatus.hours_remaining?.toFixed(1)} horas restantes.
            {trialStatus.has_viewed_free_profile 
              ? ' Ya usaste tu vista gratuita.'
              : ' Puedes ver 1 perfil completo gratis.'}
          </p>
        </div>
      )}

      {/* Profiles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {profiles?.map((profile) => (
          <ProfileCard
            key={profile.id}
            profile={profile}
            isLocked={!canViewProfile(profile.id)}
            onClick={() => handleProfileClick(profile.id)}
          />
        ))}
      </div>

      {/* Paywall Modal */}
      {showPaywall && (
        <TrialPaywall onClose={() => setShowPaywall(false)} />
      )}
    </div>
  );
}
```

### 3. Componente de Paywall

**Archivo**: `components/features/TrialPaywall.tsx`

```typescript
'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/hooks/useAuth';
import { formatCurrency } from '@/lib/utils';

interface TrialPaywallProps {
  onClose: () => void;
}

export default function TrialPaywall({ onClose }: TrialPaywallProps) {
  const { trialStatus } = useAuth();

  const handleSubscribe = () => {
    // Redirect to payment page
    window.location.href = '/empresa/suscripcion';
  };

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="text-2xl">🔒 Suscripción Requerida</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          {trialStatus?.has_viewed_free_profile ? (
            <p className="text-muted-foreground">
              Ya utilizaste tu vista gratuita durante el trial de 24 horas.
            </p>
          ) : (
            <p className="text-muted-foreground">
              Tu trial de 24 horas ha expirado.
            </p>
          )}

          <div className="bg-primary/10 rounded-lg p-6 text-center">
            <p className="text-3xl font-bold text-primary mb-2">
              {formatCurrency(49900)}
              <span className="text-base font-normal text-muted-foreground">/mes</span>
            </p>
            <p className="text-sm text-muted-foreground">
              Acceso ilimitado a todos los perfiles
            </p>
          </div>

          <ul className="space-y-2 text-sm">
            <li className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              Ver perfiles ilimitados
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              Crear campañas ilimitadas
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              Mensajería directa con influencers
            </li>
            <li className="flex items-center gap-2">
              <span className="text-green-500">✓</span>
              Soporte prioritario
            </li>
          </ul>

          <div className="flex gap-3">
            <Button variant="outline" onClick={onClose} className="flex-1">
              Cancelar
            </Button>
            <Button onClick={handleSubscribe} className="flex-1">
              Suscribirse Ahora
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
```

---

## 🎨 Componentes UI (Shadcn)

Instalar componentes de Shadcn/ui:

```bash
# Inicializar Shadcn
npx shadcn-ui@latest init

# Instalar componentes necesarios
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add avatar
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add table
```

---

## 🔐 Seguridad Implementada

✅ **XSS Prevention**:
- NO uso de `dangerouslySetInnerHTML`
- React escapa automáticamente todo el contenido
- DOMPurify para contenido HTML (si es necesario)

✅ **JWT en httpOnly Cookies**:
- El backend configura cookies `httpOnly` y `Secure`
- El frontend NO almacena tokens en localStorage
- Axios configurado con `withCredentials: true`

✅ **CSRF Protection**:
- Interceptor de Axios listo para agregar token CSRF

✅ **Validación con Zod**:
- Todos los formularios validan con esquemas Zod
- Esquemas coinciden con Pydantic del backend

---

## ⚡ Optimizaciones de Rendimiento

✅ **Server Components por Defecto**:
- Solo usar `'use client'` cuando sea necesario

✅ **React Query Caching**:
- Stale time: 1 minuto
- Refetch on window focus: deshabilitado

✅ **Code Splitting**:
- Next.js hace code splitting automático por ruta

✅ **Image Optimization**:
- Usar `next/image` para todas las imágenes

---

## 📝 Archivos Faltantes por Crear

### Páginas de Autenticación

1. `app/(auth)/login/page.tsx` - Página de login
2. `app/(auth)/registro/page.tsx` - Página de registro

### Páginas de Empresa

3. `app/(plataforma)/empresa/dashboard/page.tsx` - Dashboard empresa
4. `app/(plataforma)/empresa/campañas/page.tsx` - Lista de campañas
5. `app/(plataforma)/empresa/campañas/[id]/page.tsx` - Detalle de campaña

### Páginas de Influencer

6. `app/(plataforma)/influencer/dashboard/page.tsx` - Dashboard influencer
7. `app/(plataforma)/influencer/perfil/page.tsx` - Editar perfil

### Páginas de Admin

8. `app/(plataforma)/admin/dashboard/page.tsx` - Dashboard admin
9. `app/(plataforma)/admin/aprobaciones/page.tsx` - Aprobar usuarios

### Componentes de Layout

10. `components/layout/Navbar.tsx` - Barra de navegación
11. `components/layout/Sidebar.tsx` - Barra lateral
12. `components/layout/Footer.tsx` - Pie de página

### Componentes de Features

13. `components/features/ProfileCard.tsx` - Tarjeta de perfil
14. `components/features/CampaignForm.tsx` - Formulario de campaña
15. `components/features/NotificationBell.tsx` - Campana de notificaciones

### Servicios Faltantes

16. `services/authService.ts` - Servicio de autenticación
17. `services/notificationService.ts` - Servicio de notificaciones

---

## 🚀 Próximos Pasos

1. **Instalar dependencias**: `npm install`
2. **Configurar .env.local**: Copiar `.env.local.example`
3. **Instalar Shadcn**: `npx shadcn-ui@latest init`
4. **Crear archivos faltantes**: Usar los ejemplos de arriba
5. **Ejecutar**: `npm run dev`

---

## 🔗 Conexión con Backend

El frontend se conecta al backend en `http://localhost:8000` (configurable en `.env.local`).

**Asegúrate de**:
1. El backend esté corriendo en el puerto 8000
2. CORS esté configurado para permitir `http://localhost:3000`
3. Las cookies httpOnly estén habilitadas en el backend

---

## 📚 Documentación de Referencia

- [Next.js 14 Docs](https://nextjs.org/docs)
- [React Query Docs](https://tanstack.com/query/latest)
- [Shadcn/ui Docs](https://ui.shadcn.com/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Zod Docs](https://zod.dev/)

---

**Estado**: ✅ Estructura base completa - Requiere completar archivos faltantes
**Versión**: 1.0.0 (MVP)
