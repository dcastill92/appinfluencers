# frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar package files
COPY package*.json ./
RUN npm ci

# Copiar código y construir
COPY . .
RUN npm run build

# Imagen de producción
FROM node:18-alpine AS runner

WORKDIR /app

# Copiar build y node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

# Exponer puerto
EXPOSE 3000

# Iniciar servidor de producción
CMD ["npm", "start"]