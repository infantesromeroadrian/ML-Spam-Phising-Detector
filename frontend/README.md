# 🎨 SPAM & PHISHING Detector - Frontend

**Modern React frontend** with cybersecurity-themed UI for email threat analysis.

## 🏗️ Tech Stack

| Technology | Purpose | Why |
|------------|---------|-----|
| **React 18** | UI framework | Component-based, hooks, concurrent features |
| **TypeScript** | Type safety | Catch errors at compile time |
| **Vite** | Build tool | 10-100x faster than webpack |
| **Tailwind CSS** | Styling | Utility-first, rapid development |
| **Framer Motion** | Animations | Smooth, declarative animations |
| **Chart.js** | Data viz | Gauge charts for threat levels |
| **React Query** | State management | Server state, caching, refetching |
| **Axios** | HTTP client | Promise-based API calls |
| **Lucide React** | Icons | Modern, customizable icons |

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+**
- **npm** or **yarn**

### Installation

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# App will be at http://localhost:5173
```

### Environment Variables

Create `.env` file:

```bash
VITE_API_URL=http://localhost:8000
```

For production:

```bash
VITE_API_URL=https://api.yourdomain.com
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Header.tsx       # Animated header with shield
│   │   ├── EmailForm.tsx    # Email input form
│   │   ├── GaugeChart.tsx   # Semicircle gauge (Chart.js)
│   │   └── ResultsPanel.tsx # Threat analysis display
│   ├── pages/               # Page components
│   ├── services/            # API client (axios)
│   │   └── api.ts
│   ├── hooks/               # Custom React hooks
│   │   └── useClassifyEmail.ts
│   ├── types/               # TypeScript interfaces
│   │   └── index.ts
│   ├── utils/               # Helper functions
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles + Tailwind
├── public/                  # Static assets
├── index.html               # HTML template
├── vite.config.ts           # Vite configuration
├── tailwind.config.js       # Tailwind configuration
├── tsconfig.json            # TypeScript configuration
└── package.json
```

## 🎨 Design System

### Color Palette

```js
colors: {
  'dark-bg': '#0a0e27',        // Main background
  'dark-card': '#141937',      // Card backgrounds
  'neon-cyan': '#00d9ff',      // Primary accent
  'neon-purple': '#a855f7',    // Secondary accent
  'threat-high': '#ef4444',    // Critical/High risk
  'threat-medium': '#f59e0b',  // Medium risk
  'threat-low': '#10b981',     // Low risk / Safe
}
```

### Components

#### Header

Animated shield icon with gradient title.

```tsx
import { Header } from './components/Header';

<Header />
```

#### EmailForm

Form with email text, subject, and sender inputs.

```tsx
import { EmailForm } from './components/EmailForm';

<EmailForm onSubmit={handleSubmit} isLoading={isLoading} />
```

#### GaugeChart

Semicircle gauge for probability visualization.

```tsx
import { GaugeChart } from './components/GaugeChart';

<GaugeChart 
  value={85.5} 
  label="SPAM Probability" 
  color="#ef4444" 
/>
```

#### ResultsPanel

Full threat analysis display with dual gauges.

```tsx
import { ResultsPanel } from './components/ResultsPanel';

<ResultsPanel result={classificationResult} />
```

## 🔌 API Integration

### API Client

Located in `src/services/api.ts`:

```typescript
import { classifyEmail } from './services/api';

const result = await classifyEmail({
  email_text: "Email content",
  subject: "Optional subject",
  sender: "Optional sender"
});
```

### React Query Hook

Located in `src/hooks/useClassifyEmail.ts`:

```typescript
import { useClassifyEmail } from './hooks/useClassifyEmail';

function MyComponent() {
  const { mutate, data, isPending, error } = useClassifyEmail();
  
  const handleSubmit = (emailText: string) => {
    mutate({ email_text: emailText });
  };
  
  return (
    <>
      {isPending && <p>Analyzing...</p>}
      {error && <p>Error: {error.message}</p>}
      {data && <ResultsPanel result={data} />}
    </>
  );
}
```

### API Response Types

```typescript
interface ClassifyResponse {
  verdict: 'HAM' | 'SPAM' | 'PHISHING' | 'SPAM+PHISHING';
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  is_malicious: boolean;
  
  spam_label: string;
  spam_probability: number;
  spam_model_version: string;
  
  phishing_label: string;
  phishing_probability: number;
  phishing_model_version: string;
  
  execution_time_ms: number;
  threat_report?: { /* ... */ };
}
```

See `src/types/index.ts` for complete types.

## 🧪 Development

### Available Scripts

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Type check
npm run type-check  # (add to package.json)
```

### Adding New Components

1. Create file in `src/components/`
2. Use TypeScript with proper types
3. Follow naming convention: `PascalCase.tsx`
4. Export as named export

```tsx
// src/components/MyComponent.tsx
interface MyComponentProps {
  title: string;
  onClick: () => void;
}

export const MyComponent = ({ title, onClick }: MyComponentProps) => {
  return <button onClick={onClick}>{title}</button>;
};
```

### Styling with Tailwind

```tsx
// Use utility classes
<div className="glass-card p-8 neon-border">
  <h1 className="text-3xl font-bold text-neon-cyan">
    Title
  </h1>
</div>

// Custom classes in index.css
.glass-card {
  @apply bg-dark-card/50 backdrop-blur-xl rounded-xl border border-gray-700/50;
}

.neon-border {
  @apply border-neon-cyan/50 shadow-lg shadow-neon-cyan/20;
}
```

### Animations with Framer Motion

```tsx
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Content
</motion.div>
```

## 🏗️ Build & Deploy

### Build for Production

```bash
npm run build
```

Output will be in `dist/` directory.

### Deployment Options

#### Option 1: Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variable
vercel env add VITE_API_URL
```

#### Option 2: Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod

# Set environment variable in Netlify dashboard
```

#### Option 3: Cloudflare Pages

1. Connect GitHub repository
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Add environment variable: `VITE_API_URL`

#### Option 4: Docker

```bash
# Build image
docker build -t spam-detector-frontend .

# Run container
docker run -p 80:80 \
  -e VITE_API_URL=https://api.yourdomain.com \
  spam-detector-frontend
```

#### Option 5: Backend Serves Frontend

```bash
# Build frontend
npm run build

# Copy to backend static directory
cp -r dist ../backend/static

# Backend will serve frontend at /
```

## 🔧 Configuration

### Vite Config

```typescript
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

### Tailwind Config

```javascript
// tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'dark-bg': '#0a0e27',
        'dark-card': '#141937',
        'neon-cyan': '#00d9ff',
        'neon-purple': '#a855f7',
        'threat-high': '#ef4444',
        'threat-medium': '#f59e0b',
        'threat-low': '#10b981',
      },
    },
  },
};
```

## 🐛 Troubleshooting

### Port 5173 already in use

```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9

# Or use different port
vite --port 3000
```

### API calls failing (CORS)

- Check backend CORS configuration
- Verify `VITE_API_URL` is correct
- Check browser console for errors
- Ensure backend is running

```bash
# Check backend health
curl http://localhost:8000/health
```

### Build errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check TypeScript errors
npx tsc --noEmit

# Check for missing dependencies
npm install
```

### Styling not working

```bash
# Rebuild Tailwind
npx tailwindcss -i ./src/index.css -o ./dist/output.css --watch

# Or restart dev server
npm run dev
```

## 📊 Performance

### Optimization Tips

1. **Code Splitting**
```tsx
const LazyComponent = lazy(() => import('./components/Heavy'));
```

2. **Memoization**
```tsx
const MemoizedComponent = memo(MyComponent);
```

3. **React Query Caching**
```tsx
const { data } = useQuery({
  queryKey: ['email', id],
  queryFn: fetchEmail,
  staleTime: 5 * 60 * 1000, // 5 minutes
});
```

4. **Image Optimization**
- Use WebP format
- Lazy load images
- Compress assets

### Bundle Analysis

```bash
# Install analyzer
npm install --save-dev rollup-plugin-visualizer

# Analyze bundle
npm run build -- --mode analyze
```

## 🎯 Features

- ✅ Dark glassmorphism UI
- ✅ Real-time threat analysis
- ✅ Dual gauge visualization (SPAM & PHISHING)
- ✅ Color-coded risk levels
- ✅ Smooth animations
- ✅ Loading states
- ✅ Error handling
- ✅ Responsive design (mobile-friendly)
- ✅ TypeScript type safety
- ✅ Accessible components
- ✅ Fast dev server (Vite HMR)

## 📚 Resources

- **React Docs**: https://react.dev
- **Vite Docs**: https://vitejs.dev
- **Tailwind CSS**: https://tailwindcss.com
- **Framer Motion**: https://www.framer.com/motion
- **React Query**: https://tanstack.com/query
- **Chart.js**: https://www.chartjs.org

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test locally
4. Run linter: `npm run lint`
5. Build: `npm run build`
6. Commit and push
7. Create PR

## 📄 License

MIT License - see LICENSE file

---

**Built with ⚡ for blazing-fast user experience**
