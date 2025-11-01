@echo off
echo ========================================
echo   Iniciando Influencers Platform
echo ========================================
echo.

echo [1/2] Iniciando Backend (Docker)...
docker-compose up -d

echo.
echo [2/2] Esperando que el backend este listo...
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   SERVICIOS INICIADOS
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Documentacion: http://localhost:8000/docs
echo.
echo Para iniciar el Frontend:
echo   cd "C:\Users\yoiner.castillo\Downloads\New folder\InfluencersFront"
echo   npm run dev
echo.
echo Usuarios de prueba:
echo   Admin: admin@influencers.com / admin123
echo   Influencer: gaby@gmail.com / gaby123
echo.
echo ========================================

docker-compose ps

echo.
pause
