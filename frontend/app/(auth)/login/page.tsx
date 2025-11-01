'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import FacebookLoginButton from '@/components/FacebookLoginButton';
import Logo from '@/components/Logo';

export default function LoginPage() {
  const router = useRouter();
  const { login, isLoading } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await login(email, password);
      // La redirección se maneja en AuthContext.login()
    } catch (err: any) {
      // Manejar diferentes tipos de errores
      if (err.response?.status === 403) {
        const detail = err.response?.data?.detail || '';
        if (detail.includes('pending approval')) {
          // Redirigir a página de pendiente
          router.push('/pendiente');
          return;
        } else if (detail.includes('inactive')) {
          setError('❌ Tu cuenta ha sido desactivada. Contacta al soporte para más información.');
        } else {
          setError(detail);
        }
      } else if (err.response?.status === 401) {
        setError('❌ Correo electrónico o contraseña incorrectos.');
      } else {
        setError('❌ Error al iniciar sesión. Por favor intenta de nuevo.');
      }
    }
  };

  const handleFacebookSuccess = async (accessToken: string, userData: any) => {
    try {
      setError(null);
      console.log('Facebook Access Token:', accessToken);
      console.log('Facebook User Data:', userData);

      // TODO: Enviar el token y datos al backend para crear/autenticar usuario
      // Por ahora solo mostramos los datos
      alert(`¡Bienvenido ${userData.name}!\n\nEmail: ${userData.email || 'No disponible'}\nID: ${userData.id}`);
      
      // Aquí deberías hacer una llamada a tu backend para:
      // 1. Verificar si el usuario existe (por facebook_id o email)
      // 2. Si no existe, crear una cuenta nueva
      // 3. Si existe, hacer login
      // 4. Retornar tu propio JWT token
      
      // Ejemplo:
      // const response = await api.post('/auth/facebook-login', {
      //   facebook_token: accessToken,
      //   facebook_id: userData.id,
      //   email: userData.email,
      //   name: userData.name,
      //   picture: userData.picture?.data?.url
      // });
      // await login con el token de tu backend
      
    } catch (err: any) {
      console.error('Error con Facebook login:', err);
      setError('❌ Error al iniciar sesión con Facebook. Por favor intenta de nuevo.');
    }
  };

  const handleFacebookError = (error: any) => {
    console.error('Facebook login error:', error);
    setError('❌ Error al conectar con Facebook.');
  };

  return (
    <div className="min-h-screen grid place-items-center p-4 bg-gradient-to-br from-purple-50 to-pink-50">
      <div className="w-full max-w-sm border rounded-lg p-6 bg-white shadow-lg">
        <div className="flex justify-center mb-4">
          <Logo size={60} />
        </div>
        <h1 className="text-2xl font-bold mb-1 text-center">Iniciar sesión</h1>
        <p className="text-sm text-muted-foreground mb-6 text-center">Accede a tu cuenta para continuar</p>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <form className="space-y-4" onSubmit={onSubmit}>
          <div className="space-y-1">
            <label className="text-sm font-medium" htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full h-10 px-3 rounded-md border bg-transparent"
              placeholder="tu@email.com"
            />
          </div>

          <div className="space-y-1">
            <label className="text-sm font-medium" htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full h-10 px-3 rounded-md border bg-transparent"
              placeholder="••••••••"
            />
          </div>

          <Button type="submit" disabled={isLoading} className="w-full">
            {isLoading ? 'Ingresando…' : 'Ingresar'}
          </Button>
        </form>

        {/* Divider */}
        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">O continúa con</span>
          </div>
        </div>

        {/* Facebook Login */}
        <FacebookLoginButton 
          onSuccess={handleFacebookSuccess}
          onError={handleFacebookError}
        />

        <div className="text-xs text-muted-foreground mt-4 text-center">
          ¿No tienes cuenta? <Link className="underline" href="/registro">Regístrate</Link>
        </div>
      </div>
    </div>
  );
}
