"use client";

import { useAuth } from "@/hooks/useAuth";
import { useRouter, usePathname } from "next/navigation";
import { useEffect } from "react";
import Navbar from "@/components/layout/Navbar";
import Sidebar from "@/components/layout/Sidebar";

export default function PlataformaLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    console.log('PlataformaLayout: isLoading=', isLoading, 'isAuthenticated=', isAuthenticated, 'user=', user?.email, 'role=', user?.role, 'pathname=', pathname);
    
    // Si no está autenticado, redirigir al login
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
      return;
    }

    // Protección de rutas por rol
    if (user && !isLoading) {
      const userRole = user.role.toLowerCase();
      
      // Verificar si el usuario está intentando acceder a una ruta de otro rol
      if (pathname.startsWith("/empresa") && user.role !== "EMPRESA") {
        console.log('Acceso denegado: Usuario no es EMPRESA, redirigiendo a', `/${userRole}/dashboard`);
        router.push(`/${userRole}/dashboard`);
        return;
      }
      
      if (pathname.startsWith("/influencer") && user.role !== "INFLUENCER") {
        console.log('Acceso denegado: Usuario no es INFLUENCER, redirigiendo a', `/${userRole}/dashboard`);
        router.push(`/${userRole}/dashboard`);
        return;
      }
      
      if (pathname.startsWith("/admin") && user.role !== "ADMIN") {
        console.log('Acceso denegado: Usuario no es ADMIN, redirigiendo a', `/${userRole}/dashboard`);
        router.push(`/${userRole}/dashboard`);
        return;
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, isAuthenticated, isLoading, pathname]);

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
