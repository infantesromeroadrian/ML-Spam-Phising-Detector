# ⚡ Quick Start - SPAM/Phishing Detector

## 🚀 Inicio en 3 Comandos

```bash
# 1. Construir imágenes Docker
docker-compose build

# 2. Levantar servicios
docker-compose up -d

# 3. Ver logs en tiempo real
docker-compose logs -f
```

**Acceso**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## ✅ Verificación Rápida

```bash
# Ver estado de contenedores (debe decir "healthy")
docker ps

# Verificar health del backend
curl http://localhost:8000/health | jq

# Verificar health del frontend
curl http://localhost:3000/_health

# Ver modelos ML montados
docker-compose exec backend ls -lh /app/models/ | grep latest
```

**Salida esperada del health check**:
```json
{
  "status": "healthy",
  "models_loaded": true,
  "models": {
    "spam": true,
    "phishing": true
  },
  "api_version": "1.0.0"
}
```

---

## 🛑 Detener Todo

```bash
# Parar contenedores
docker-compose down

# Parar y eliminar volúmenes
docker-compose down -v
```

---

## 🐛 Troubleshooting Rápido

### Frontend no conecta con backend

```bash
# 1. Verificar que backend esté healthy
docker ps | grep backend

# 2. Ver logs del backend
docker-compose logs backend | tail -50

# 3. Verificar CORS
docker-compose exec backend env | grep CORS
```

### Modelos ML no se cargan

```bash
# Verificar symlinks en el host
ls -lh src/backend/models/*_latest.joblib

# Verificar dentro del contenedor
docker-compose exec backend ls -lh /app/models/*_latest.joblib
```

### Reconstruir sin caché

```bash
# Reconstruir todo desde cero
docker-compose build --no-cache

# Reconstruir solo backend
docker-compose build --no-cache backend

# Reconstruir solo frontend
docker-compose build --no-cache frontend
```

---

## 📚 Más Información

- **Guía completa**: Ver `DOCKER_GUIDE.md`
- **Cambios realizados**: Ver `REFACTOR_SUMMARY.md`
- **Arquitectura**: Ver `docs/PROJECT_STRUCTURE.md`

---

**Listo para usar en 2 minutos** ⏱️
