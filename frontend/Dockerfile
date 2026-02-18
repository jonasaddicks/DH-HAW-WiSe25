# Builder - 1st stage
FROM node:22.12-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Caddy - 2nd stage
FROM caddy:2.10.2
COPY --from=builder /app/dist /srv
