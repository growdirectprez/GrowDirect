# syntax=docker/dockerfile:1.7

# --- stage 1: tailwind build + alpine bundle ---
FROM node:20-alpine AS assets
WORKDIR /assets
COPY package.json tailwind.config.js postcss.config.js ./
RUN npm install
COPY solex/static/css ./solex/static/css
COPY solex/templates ./solex/templates
RUN npx tailwindcss -i ./solex/static/css/input.css -o ./solex/static/css/output.css --minify \
 && mkdir -p ./solex/static/js/vendor \
 && cp ./node_modules/alpinejs/dist/cdn.min.js ./solex/static/js/vendor/alpine.min.js

# --- stage 2: runtime ---
FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential curl \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .
COPY --from=assets /assets/solex/static/css/output.css ./solex/static/css/output.css
COPY --from=assets /assets/solex/static/js/vendor ./solex/static/js/vendor

EXPOSE 5003
CMD ["gunicorn", "-b", "0.0.0.0:5003", "--reload", "--workers", "2", "wsgi:app"]
