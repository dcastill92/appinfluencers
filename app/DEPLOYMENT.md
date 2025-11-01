# 🚀 Guía de Despliegue a Producción - Influencers Platform

## 🎯 Resumen Rápido

**Estado Actual**: ✅ Aplicación funcionando en local (Docker + Next.js)
**Objetivo**: Desplegar en producción con dominio propio
**Recomendación**: Railway (fácil y completo) o Vercel + Supabase (frontend optimizado)

---

## 📋 Opciones de Despliegue

### ⭐ Opción 1: Railway (Recomendado para empezar)
- ✅ **Facilidad**: Despliegue con GitHub en 5 minutos
- ✅ **Todo incluido**: Backend + Frontend + Base de datos
- ✅ **HTTPS automático**: Certificado SSL gratis
- ✅ **Escalable**: Auto-scaling incluido
- 💰 **Costo**: $20-50/mes

### 🌐 Opción 2: Vercel + Supabase (Frontend especializado)
- ✅ **Next.js optimizado**: Edge CDN global
- ✅ **Base de datos potente**: PostgreSQL con Supabase
- ✅ **Separación clara**: Backend y frontend independientes
- 💰 **Costo**: $20-40/mes

### ☁️ Opción 3: AWS EC2 + RDS (Empresarial)
- ✅ **Control total**: Configuración personalizada completa
- ✅ **Infraestructura AWS**: Escalabilidad infinita
- ✅ **Seguridad**: AWS security groups
- 💰 **Costo**: $50-200/mes

---

## 🚀 Opción 1: Railway (Despliegue Rápido)

---

## Opción 1: Despliegue en AWS (ECS + RDS)

### 1. Preparar Base de Datos

```bash
# Crear RDS PostgreSQL instance
aws rds create-db-instance \
    --db-instance-identifier influencers-prod-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password SECURE_PASSWORD \
    --allocated-storage 20
```

### 2. Construir y Subir Imagen Docker

```bash
# Login a ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ECR_URL

# Build imagen
docker build -t influencers-api:latest .

# Tag imagen
docker tag influencers-api:latest YOUR_ECR_URL/influencers-api:latest

# Push imagen
docker push YOUR_ECR_URL/influencers-api:latest
```

### 3. Crear Task Definition (ECS)

```json
{
  "family": "influencers-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "YOUR_ECR_URL/influencers-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:..."
        },
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:..."
        }
      ]
    }
  ]
}
```

### 4. Configurar Load Balancer

```bash
# Crear Application Load Balancer
aws elbv2 create-load-balancer \
    --name influencers-alb \
    --subnets subnet-xxx subnet-yyy \
    --security-groups sg-xxx
```

---

## Opción 2: Despliegue en Google Cloud (Cloud Run + Cloud SQL)

### 1. Configurar Cloud SQL

```bash
# Crear instancia de PostgreSQL
gcloud sql instances create influencers-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1

# Crear base de datos
gcloud sql databases create influencers_platform \
    --instance=influencers-db
```

### 2. Construir y Desplegar en Cloud Run

```bash
# Build y push a Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/influencers-api

# Deploy a Cloud Run
gcloud run deploy influencers-api \
    --image gcr.io/PROJECT_ID/influencers-api \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --add-cloudsql-instances PROJECT_ID:us-central1:influencers-db \
    --set-env-vars DATABASE_URL="postgresql+asyncpg://..." \
    --set-secrets SECRET_KEY=secret-key:latest
```

---

## Opción 3: Despliegue en DigitalOcean (App Platform)

### 1. Crear App

```yaml
# .do/app.yaml
name: influencers-platform
services:
  - name: api
    github:
      repo: your-org/influencers-platform
      branch: main
      deploy_on_push: true
    dockerfile_path: Dockerfile
    http_port: 8000
    instance_count: 2
    instance_size_slug: basic-xxs
    envs:
      - key: ENVIRONMENT
        value: production
      - key: DATABASE_URL
        type: SECRET
      - key: SECRET_KEY
        type: SECRET
databases:
  - name: influencers-db
    engine: PG
    version: "15"
```

### 2. Deploy

```bash
doctl apps create --spec .do/app.yaml
```

---

## Opción 4: Despliegue en Heroku

### 1. Preparar Aplicación

```bash
# Login a Heroku
heroku login

# Crear app
heroku create influencers-api-prod

# Agregar PostgreSQL
heroku addons:create heroku-postgresql:mini
```

### 2. Configurar Variables de Entorno

```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set STRIPE_SECRET_KEY="sk_live_..."
heroku config:set ENVIRONMENT="production"
```

### 3. Deploy

```bash
# Push a Heroku
git push heroku main

# Ejecutar migraciones
heroku run alembic upgrade head

# Inicializar DB
heroku run python scripts/init_db.py
```

---

## Configuración de Nginx (Reverse Proxy)

Si despliegas en un VPS:

```nginx
# /etc/nginx/sites-available/influencers-api

upstream api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.influencers.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.influencers.com;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/api.influencers.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.influencers.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;
    
    location / {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Health check endpoint
    location /health {
        proxy_pass http://api/health;
        access_log off;
    }
}
```

---

## Configuración de Systemd (VPS)

```ini
# /etc/systemd/system/influencers-api.service

[Unit]
Description=Influencers Platform API
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/influencers-api
Environment="PATH=/opt/influencers-api/venv/bin"
ExecStart=/opt/influencers-api/venv/bin/gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile /var/log/influencers/access.log \
    --error-logfile /var/log/influencers/error.log \
    --log-level info
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Activar servicio:
```bash
sudo systemctl enable influencers-api
sudo systemctl start influencers-api
sudo systemctl status influencers-api
```

---

## Monitoreo y Logging

### Sentry (Error Tracking)

```python
# app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://xxx@sentry.io/xxx",
    integrations=[FastApiIntegration()],
    environment=settings.ENVIRONMENT,
    traces_sample_rate=0.1,
)
```

### Prometheus (Métricas)

```python
# requirements.txt
prometheus-fastapi-instrumentator==6.1.0

# app/main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

### CloudWatch Logs (AWS)

```python
# requirements.txt
watchtower==3.0.1

# app/core/logging.py
import watchtower
import logging

logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())
```

---

## Backup y Recuperación

### Backup Automático de PostgreSQL

```bash
# Script de backup
#!/bin/bash
# /opt/scripts/backup_db.sh

BACKUP_DIR="/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/influencers_$TIMESTAMP.sql.gz"

pg_dump -h localhost -U influencer_user influencers_platform | gzip > $BACKUP_FILE

# Mantener solo últimos 7 días
find $BACKUP_DIR -name "influencers_*.sql.gz" -mtime +7 -delete

# Subir a S3 (opcional)
aws s3 cp $BACKUP_FILE s3://influencers-backups/
```

Configurar cron:
```bash
# Ejecutar backup diario a las 2 AM
0 2 * * * /opt/scripts/backup_db.sh
```

---

## Rollback

### Rollback de Código

```bash
# Docker
docker pull YOUR_REGISTRY/influencers-api:previous-tag
docker-compose up -d

# Heroku
heroku releases:rollback v123
```

### Rollback de Migraciones

```bash
# Revertir última migración
alembic downgrade -1

# Revertir a versión específica
alembic downgrade abc123
```

---

## Checklist Post-Despliegue

- [ ] Verificar `/health` endpoint responde 200
- [ ] Verificar `/docs` accesible
- [ ] Probar registro de usuario
- [ ] Probar login y obtención de token
- [ ] Verificar lógica de trial funciona
- [ ] Probar creación de campaña
- [ ] Verificar notificaciones se crean
- [ ] Revisar logs por errores
- [ ] Configurar alertas de monitoreo
- [ ] Documentar URLs de producción
- [ ] Notificar al equipo

---

## URLs de Producción

Actualizar en documentación:

- **API Base URL**: `https://api.influencers.com`
- **Docs**: `https://api.influencers.com/docs`
- **Health Check**: `https://api.influencers.com/health`
- **Admin Panel**: (si aplica)

---

## Soporte y Mantenimiento

### Logs

```bash
# Ver logs en tiempo real
docker-compose logs -f api

# Últimas 100 líneas
docker-compose logs --tail=100 api

# Buscar errores
docker-compose logs api | grep ERROR
```

### Métricas a Monitorear

- Request rate (req/s)
- Response time (p50, p95, p99)
- Error rate (%)
- Database connections
- Memory usage
- CPU usage
- Trial conversion rate
- Active campaigns

---

**¡Despliegue exitoso! 🎉**
