# syntax=docker/dockerfile:1.7
# ── build: Vite bakes VITE_API_BASE_URL in at build time, so it's a build arg, not a runtime env ──
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
# --legacy-peer-deps: same TypeScript 6.x / openapi-typescript peer-range mismatch as the
# real-estate project's frontend (see that Dockerfile's comment) — `npm ci` re-validates peers
# strictly where `npm install` did not.
RUN npm ci --ignore-scripts --legacy-peer-deps
COPY . .
ARG VITE_API_BASE_URL=/api/v1
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build

# ── runtime: static files behind nginx, SPA history-mode fallback ──
FROM nginx:1.27-alpine AS runtime
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 3000
HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3000/health >/dev/null || exit 1
CMD ["nginx", "-g", "daemon off;"]
