import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, // CRITICAL: Send httpOnly cookies with every request
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // You can add additional headers here if needed
    // For example, CSRF token from meta tag
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // Handle 401 Unauthorized (token expired)
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      originalRequest.url !== '/auth/refresh' // <-- Corrección para bucle infinito
    ) {
      originalRequest._retry = true;

      try {
        // Attempt to refresh token
        await api.post('/auth/refresh');
        // Retry the original request
        return api(originalRequest);
      } catch (refreshError) { // <-- ERROR DE SINTAXIS CORREGIDO AQUÍ
        // Refresh failed — redirect to login only if we're not already there.
        if (typeof window !== 'undefined') {
          try {
            if (window.location.pathname !== '/login') {
              // Use full navigation to ensure cookies/session cleared client-side too
              window.location.href = '/login';
            } else {
              // Already on /login — avoid forcing another reload which can create a loop
              // Keep the error propagation so callers can handle it.
              // Helpful debug log while developing:
              // eslint-disable-next-line no-console
              console.debug('Auth refresh failed and already on /login — not redirecting to avoid loop.');
            }
          } catch (e) {
            // If accessing window.location fails for any reason, fall back to setting href.
            window.location.href = '/login';
          }
        }
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;