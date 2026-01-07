# 🎨 Email Classifier - Frontend

**Modern HTML/CSS/JavaScript frontend** para la API de clasificación de emails.

---

## 📦 Estructura

```
frontend/
├── index.html          # Página principal (184 LOC)
├── css/
│   └── styles.css      # Estilos modernos (558 LOC)
└── js/
    └── app.js          # Lógica de aplicación (306 LOC)
```

**Total:** 1,048 LOC

---

## 🚀 Características

### ✨ UI/UX
- ✅ Diseño moderno y responsivo
- ✅ Gradientes y animaciones suaves
- ✅ Indicadores de progreso visuales
- ✅ Badges de riesgo con código de colores
- ✅ Contador de caracteres en tiempo real
- ✅ Smooth scrolling a resultados

### 🎯 Funcionalidad
- ✅ Formulario de clasificación de emails
- ✅ Campos opcionales (subject, sender)
- ✅ Llamadas asíncronas a FastAPI
- ✅ Visualización de resultados dual (spam + phishing)
- ✅ Barras de probabilidad animadas
- ✅ Manejo de errores robusto
- ✅ Health check automático del backend

### 🎨 Diseño
- ✅ CSS moderno con variables CSS
- ✅ Flexbox y Grid layouts
- ✅ Mobile-first responsive
- ✅ Iconos SVG inline
- ✅ Sistema de colores coherente

---

## 🌐 Cómo Usar

### 1. Lanzar el Backend

```bash
# Opción 1: Comando instalado
email-classifier-api

# Opción 2: Con uvicorn
uvicorn ml_engineer_course.infrastructure.api.main:app --reload
```

### 2. Abrir el Frontend

```
http://localhost:8000
```

Verás una página de inicio con 3 opciones:
- **🚀 Launch App** → Abre el frontend
- **📚 API Docs** → Swagger UI
- **📖 Reference** → ReDoc

### 3. Usar la Aplicación

1. Click en **"Launch App"**
2. Escribe o pega el contenido del email
3. (Opcional) Añade subject y sender
4. Click en **"Classify Email"**
5. ¡Ve los resultados!

---

## 📊 Interfaz

### Formulario

```
┌─────────────────────────────────────┐
│  Email Content *                    │
│  ┌────────────────────────────────┐ │
│  │ Paste your email here...       │ │
│  │                                │ │
│  │                                │ │
│  └────────────────────────────────┘ │
│  123 characters                     │
│                                     │
│  Subject (Optional)                 │
│  ┌────────────────────────────────┐ │
│  │ e.g., Urgent Prize             │ │
│  └────────────────────────────────┘ │
│                                     │
│  Sender (Optional)                  │
│  ┌────────────────────────────────┐ │
│  │ e.g., sender@example.com       │ │
│  └────────────────────────────────┘ │
│                                     │
│  [ ✓  Classify Email ]              │
└─────────────────────────────────────┘
```

### Resultados

```
┌─────────────────────────────────────┐
│  Classification Results             │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  🚨  SPAM+PHISHING            │  │
│  └───────────────────────────────┘  │
│  [ CRITICAL ]                       │
│                                     │
│  🗑️ Spam Detection                 │
│  ████████████░░░░░ 95.4%           │
│  Label: SPAM                        │
│  Model: 20240105_143022             │
│                                     │
│  🎣 Phishing Detection              │
│  ██████████████░░░ 88.2%           │
│  Label: PHISHING                    │
│  Model: 20240105_143022             │
│                                     │
│  ⚡ Analysis completed in 45.3ms    │
│                                     │
│  [ Analyze Another Email ]          │
└─────────────────────────────────────┘
```

---

## 🎨 Sistema de Colores

### Verdicts

| Verdict | Color | Emoji |
|---------|-------|-------|
| HAM | Verde (#10b981) | ✅ |
| SPAM | Naranja (#f59e0b) | 🗑️ |
| PHISHING | Rojo (#ef4444) | 🎣 |
| SPAM+PHISHING | Rojo oscuro (#dc2626) | 🚨 |

### Risk Levels

| Risk | Color | Badge |
|------|-------|-------|
| LOW | Gris | Gray badge |
| MEDIUM | Amarillo | Yellow badge |
| HIGH | Naranja | Orange badge |
| CRITICAL | Rojo | Red badge + pulso |

---

## 🔌 API Integration

### Endpoint Usado

```javascript
POST http://localhost:8000/api/v1/classify
```

### Request Payload

```javascript
{
  "email_text": "WINNER! You won $1000!",
  "subject": "Urgent Prize",      // opcional
  "sender": "scam@fake.com"       // opcional
}
```

### Response

```javascript
{
  "verdict": "SPAM+PHISHING",
  "risk_level": "CRITICAL",
  "is_malicious": true,
  "spam_label": "SPAM",
  "spam_probability": 0.954,
  "spam_model_version": "20240105_143022",
  "phishing_label": "PHISHING",
  "phishing_probability": 0.882,
  "phishing_model_version": "20240105_143022",
  "execution_time_ms": 45.3
}
```

---

## 🛠️ Tecnologías

- **HTML5**: Estructura semántica
- **CSS3**: Variables, Flexbox, Grid, Animations
- **Vanilla JavaScript**: Sin frameworks, puro ES6+
- **Fetch API**: Llamadas HTTP asíncronas
- **SVG**: Iconos escalables inline

---

## 📱 Responsive Design

### Breakpoints

- **Desktop**: > 768px
  - Grid de 2 columnas para detecciones
  - Padding generoso
  
- **Mobile**: ≤ 768px
  - Grid de 1 columna
  - Padding reducido
  - Fuentes adaptativas

---

## ⚡ Características Avanzadas

### Loading States

```javascript
// Spinner animado mientras se clasifica
┌─────────────────┐
│      ⟳         │
│  Analyzing...  │
└─────────────────┘
```

### Error Handling

```javascript
// Manejo robusto de errores
try {
  const response = await fetch(...);
  if (!response.ok) throw new Error(...);
  // ...
} catch (error) {
  showError(error.message);
}
```

### Animaciones

- **fadeInUp**: Entrada de cards
- **scaleIn**: Entrada de badges
- **spin**: Loading spinner
- **pulse**: Badge crítico pulsante
- **progress bars**: Transición suave de width

---

## 🔧 Configuración

### Cambiar URL del Backend

Edita `frontend/js/app.js`:

```javascript
// Línea 7
const API_BASE_URL = 'http://localhost:8000';

// Cambiar a:
const API_BASE_URL = 'https://tu-dominio.com';
```

---

## 🧪 Testing

### Health Check Automático

Al cargar la página, el frontend verifica automáticamente si el backend está disponible:

```javascript
async function checkAPIHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (response.ok) {
      console.log('✅ API is healthy');
    }
  } catch (error) {
    console.error('❌ Cannot connect to API');
  }
}
```

Abre la **consola del navegador** (F12) para ver el estado.

---

## 🚀 Deploy

### Opción 1: Servido por FastAPI (Actual)

El backend sirve el frontend automáticamente en `/static/`.

```bash
email-classifier-api
# Frontend disponible en http://localhost:8000/static/index.html
```

### Opción 2: Servidor Web Separado

Puedes servir el frontend con cualquier servidor web:

```bash
# Nginx
server {
  root /path/to/frontend;
  location / {
    try_files $uri $uri/ /index.html;
  }
}

# Python HTTP Server (desarrollo)
cd frontend
python -m http.server 8080
```

Recuerda actualizar `API_BASE_URL` en `app.js`.

---

## 📈 Métricas

| Métrica | Valor |
|---------|-------|
| **HTML** | 184 LOC |
| **CSS** | 558 LOC |
| **JavaScript** | 306 LOC |
| **Total** | 1,048 LOC |
| **Archivos** | 3 |
| **Dependencias** | 0 (vanilla) |
| **Tamaño** | ~30 KB total |

---

## ✨ Próximas Mejoras (Opcionales)

- [ ] Tema oscuro (toggle)
- [ ] Historial de clasificaciones
- [ ] Copiar resultados al portapapeles
- [ ] Exportar resultados como JSON/PDF
- [ ] Ejemplos pre-cargados (spam, phishing, ham)
- [ ] Gráficos de distribución de probabilidad
- [ ] Comparación de múltiples emails
- [ ] Autenticación de usuarios
- [ ] Guardar favoritos

---

## 🎓 Código Limpio

### Principios Aplicados

1. **Separación de concerns**: HTML (estructura) / CSS (presentación) / JS (lógica)
2. **Nombres descriptivos**: `classifyEmail()`, `displayResults()`, `showError()`
3. **Funciones pequeñas**: Max ~30 líneas
4. **Sin duplicación**: DRY principle
5. **Comentarios útiles**: Secciones y funciones documentadas
6. **Constantes**: `API_BASE_URL` configurable
7. **Error handling**: Try-catch en todas las llamadas async

---

## 🌟 Diseño Visual

### Paleta de Colores

```css
--primary: #3b82f6      /* Azul principal */
--success: #10b981      /* Verde (HAM) */
--warning: #f59e0b      /* Naranja (SPAM) */
--danger: #ef4444       /* Rojo (PHISHING) */
--critical: #dc2626     /* Rojo oscuro (ambos) */
```

### Tipografía

- **Font**: System fonts stack (San Francisco, Segoe UI, Roboto)
- **Sizes**: 0.75rem - 2.5rem
- **Weights**: 300, 500, 600, 700

### Espaciado

- **Sistema 8px**: Base de espaciado
- **Variables**: `--spacing-xs` a `--spacing-2xl`
- **Consistente**: Mismo espaciado en toda la app

---

## 📝 Licencia

Parte del proyecto **Email Classifier** - ML Engineer Course

---

¡Disfruta clasificando emails! 📧✨
