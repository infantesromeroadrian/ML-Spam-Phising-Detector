# 🐳 Docker Deployment Guide

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     SPAM/Phishing Detector                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐          ┌──────────────────┐         │
│  │   Frontend UI    │          │   Backend API    │         │
│  │   (Reflex)       │◄────────►│   (FastAPI)      │         │
│  │   Port: 3000     │          │   Port: 8000     │         │
│  │   Python 3.12    │          │   Python 3.12    │         │
│  └──────────────────┘          └──────────────────┘         │
│         │                              │                     │
│         │                              │                     │
│         │                              ▼                     │
│         │                      ┌──────────────┐             │
│         │                      │ ML Models    │             │
│         │                      │ (Volume)     │             │
│         │                      └──────────────┘             │
│         │                                                    │
│         └────────────────────────────────────────────────── │
│                    spam-detector-network                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔒 Seguridad Implementada

### ✅ Backend Dockerfile
- ✅ **Multi-stage build** (builder + runtime separados)
- ✅ **Usuario NO-ROOT** (appuser, UID 1001)
- ✅ **Modelos ML montados como volumen** (no copiados en imagen)
- ✅ **Variables de entorno validadas**
- ✅ **Health check mejorado** (valida carga de modelos)
- ✅ **Imagen base oficial y actualizada** (python:3.12-slim)
- ✅ **`.dockerignore` completo** (excluye tests, cache, git)

### ✅ Frontend Dockerfile
- ✅ **Multi-stage build** con Reflex export
- ✅ **Usuario NO-ROOT** (appuser, UID 1001)
- ✅ **Sin Node.js en producción** (Reflex usa Python)
- ✅ **Health check configurado**
- ✅ **`.dockerignore` completo**

### ✅ Docker Compose
- ✅ **Health check dependencies** (frontend espera a backend)
- ✅ **CORS correctamente configurado** (puerto 3000)
- ✅ **Volumen read-only** para modelos ML (`:ro`)
- ✅ **Restart policy** (`unless-stopped`)
- ✅ **Red aislada** (`spam-detector-network`)

---

## 🚀 Inicio Rápido

### 1. Construir imágenes

```bash
docker-compose build
```

**Tiempos esperados:**
- Backend: ~2-3 minutos (primera vez), ~30s (con caché)
- Frontend: ~3-5 minutos (primera vez, por Reflex export), ~1min (con caché)

### 2. Levantar servicios

```bash
docker-compose up -d
```

### 3. Verificar estado

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver solo logs del backend
docker-compose logs -f backend

# Ver solo logs del frontend
docker-compose logs -f frontend

# Verificar health checks
docker ps
```

**Salida esperada:**
```
CONTAINER ID   IMAGE              STATUS                   PORTS
abc123...      frontend:latest    Up 1 min (healthy)       0.0.0.0:3000->3000/tcp
def456...      backend:latest     Up 2 min (healthy)       0.0.0.0:8000->8000/tcp
```

### 4. Acceder a la aplicación

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API Reference**: http://localhost:8000/redoc

---

## 📋 Variables de Entorno

### Backend (FastAPI)

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `API_HOST` | Host del servidor | `0.0.0.0` |
| `API_PORT` | Puerto del servidor | `8000` |
| `API_CORS_ORIGINS` | Orígenes permitidos (CORS) | `http://localhost:3000` |

### Frontend (Reflex)

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `API_URL` | URL del backend FastAPI | `http://backend:8000` |
| `ENV` | Entorno (`dev` o `production`) | `production` |

---

## 🔧 Comandos Útiles

### Construcción y Deployment

```bash
# Reconstruir sin caché (útil tras cambios en dependencias)
docker-compose build --no-cache

# Reconstruir solo backend
docker-compose build --no-cache backend

# Reconstruir solo frontend
docker-compose build --no-cache frontend

# Levantar con logs en foreground
docker-compose up
```

### Debugging

```bash
# Entrar al contenedor del backend
docker-compose exec backend bash

# Entrar al contenedor del frontend
docker-compose exec frontend bash

# Ver modelos ML montados
docker-compose exec backend ls -lh /app/models/

# Verificar health check manualmente
docker-compose exec backend curl http://localhost:8000/health

# Ver variables de entorno
docker-compose exec backend env | grep API
docker-compose exec frontend env | grep API
```

### Limpieza

```bash
# Parar contenedores
docker-compose down

# Parar y eliminar volúmenes
docker-compose down -v

# Eliminar imágenes también
docker-compose down --rmi all

# Limpieza completa de Docker
docker system prune -a --volumes
```

---

## 🏗️ Estructura de Archivos

```
.
├── docker-compose.yml          # Orquestación de servicios
├── src/
│   ├── backend/
│   │   ├── Dockerfile          # Multi-stage, NO-ROOT, sin models COPY
│   │   ├── .dockerignore       # Excluye tests, cache, git
│   │   ├── pyproject.toml      # Dependencias con uv
│   │   ├── uv.lock             # Lockfile reproducible
│   │   ├── models/             # Montado como volumen :ro
│   │   └── spam_detector/      # Código de la aplicación
│   │
│   └── frontend/
│       ├── Dockerfile          # Multi-stage Reflex, NO-ROOT
│       ├── .dockerignore       # Excluye .web, node_modules
│       ├── requirements.txt    # reflex, httpx, pydantic
│       ├── rxconfig.py         # Configuración de Reflex
│       └── spam_detector_ui/   # Código de la UI
│           ├── components/     # Componentes reutilizables
│           ├── pages/          # Páginas de la app
│           ├── state/          # Estado de Reflex
│           └── services/       # Cliente HTTP para backend
```

---

## 🐛 Troubleshooting

### ❌ Error: "curl: command not found" en health check

**Causa**: Imagen base no tiene `curl` instalado.

**Solución**: Ya está instalado en los Dockerfiles actuales (línea 19-21 backend, línea 8-10 frontend).

### ❌ Frontend no conecta con backend

**Síntomas**:
```
Error: Connection refused to http://backend:8000
```

**Solución**:
1. Verificar que backend esté `healthy`:
   ```bash
   docker ps
   ```
2. Verificar logs del backend:
   ```bash
   docker-compose logs backend
   ```
3. Verificar CORS en `docker-compose.yml`:
   ```yaml
   API_CORS_ORIGINS=http://localhost:3000,http://frontend:3000
   ```

### ❌ Modelos ML no se cargan

**Síntomas**:
```json
{
  "status": "degraded",
  "models_loaded": false,
  "models": {"spam": false, "phishing": false}
}
```

**Solución**:
1. Verificar que existen los symlinks `*_latest.joblib`:
   ```bash
   ls -lh src/backend/models/*_latest.joblib
   ```
2. Verificar volumen montado:
   ```bash
   docker-compose exec backend ls -lh /app/models/
   ```
3. Si no existen, crearlos:
   ```bash
   cd src/backend/models/
   ln -sf spam_detector_model_20260105_194602.joblib spam_detector_model_latest.joblib
   ln -sf spam_detector_vectorizer_20260105_194602.joblib spam_detector_vectorizer_latest.joblib
   ln -sf spam_detector_metadata_20260105_194602.joblib spam_detector_metadata_latest.joblib
   # Repetir para phishing_detector_*
   ```

### ❌ Permiso denegado al escribir en volumen

**Síntomas**:
```
PermissionError: [Errno 13] Permission denied: '/app/models/new_model.joblib'
```

**Solución**:
El volumen está montado como `:ro` (read-only) intencionalmente. Para entrenar nuevos modelos:
1. Entrenar en el host (fuera de Docker)
2. Guardar en `src/backend/models/`
3. Actualizar symlinks
4. Reiniciar contenedor: `docker-compose restart backend`

---

## 📦 Tamaños de Imagen Esperados

| Imagen | Tamaño sin optimizar | Tamaño optimizado |
|--------|----------------------|-------------------|
| Backend | ~800MB (sin .dockerignore) | **~250MB** (con multi-stage) |
| Frontend | ~1.2GB (sin .dockerignore) | **~350MB** (con multi-stage) |

**Verificar tamaños**:
```bash
docker images | grep spam-detector
```

---

## 🚀 Deployment en Producción

### Render.com (recomendado para este proyecto)

1. **Backend**:
   - Tipo: Web Service
   - Build Command: `docker build -f src/backend/Dockerfile -t backend .`
   - Start Command: Auto-detectado (CMD del Dockerfile)

2. **Frontend**:
   - Tipo: Web Service
   - Build Command: `docker build -f src/frontend/Dockerfile -t frontend .`
   - Start Command: Auto-detectado

3. **Variables de entorno**:
   ```
   # Backend
   API_CORS_ORIGINS=https://tu-frontend.onrender.com
   
   # Frontend
   API_URL=https://tu-backend.onrender.com
   ENV=production
   ```

### Otras plataformas

- **Railway.app**: Similar a Render
- **Fly.io**: Usa `fly.toml` (configurar puertos 3000 y 8000)
- **AWS ECS**: Usar `docker-compose` como base para task definitions
- **Kubernetes**: Convertir con `kompose convert`

---

## ✅ Checklist Pre-Deployment

- [ ] Health checks retornan `healthy`
- [ ] Frontend conecta correctamente con backend
- [ ] Modelos ML se cargan correctamente
- [ ] CORS configurado para dominio de producción
- [ ] Logs no muestran errores críticos
- [ ] Tamaños de imagen son razonables (<400MB cada uno)
- [ ] Contenedores corren como NO-ROOT (verificar con `docker exec backend whoami`)
- [ ] Variables de entorno de producción configuradas
- [ ] Secrets NO están en código ni en imágenes

---

## 📝 Notas Finales

### Arquitectura Limpia
- ✅ Backend sigue **Arquitectura Hexagonal**
- ✅ Frontend usa **Reflex** (Python fullstack, no React)
- ✅ Separación clara de responsabilidades

### Próximos pasos
1. **Agregar Redis** para caché de predicciones
2. **Agregar PostgreSQL** para logs de clasificaciones
3. **Agregar Prometheus + Grafana** para métricas
4. **CI/CD con GitHub Actions**

---

**Creado**: 2026-01-11  
**Autor**: AIR (Adrian Infantes Romero)  
**Versión**: 1.0.0
